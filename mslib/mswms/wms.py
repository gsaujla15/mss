# -*- coding: utf-8 -*-
"""

    mslib.mswms.wms
    ~~~~~~~~~~~~~~~

    WSGI module for MSS WMS server that provides access to ECMWF forecast data.

    The module implements a Web Map Service 1.1.1 interface to provide forecast data
    from numerical weather predictions to the Mission Support User Interface.
    Supported operations are GetCapabilities and GetMap for (WMS 1.1.1 compliant)
    maps and (non-compliant) vertical sections.

    1) Configure the WMS server by modifying the settings in mss_wms_settings.py
    (address, products that shall be offered, ..).

    2) If you want to define new visualisation styles, the files to put them
    are mpl_hsec_styles.py and mpl_vsec_styles for maps and vertical sections,
    respectively.

    For more information on WMS, see http://www.opengeospatial.org/standards/wms

    This file is part of mss.

    :copyright: Copyright 2008-2014 Deutsches Zentrum fuer Luft- und Raumfahrt e.V.
    :copyright: Copyright 2011-2014 Marc Rautenhaus (mr), Omar Qunsul (oq)
    :copyright: Copyright 2016-2017 Reimar Bauer
    :copyright: Copyright 2016-2019 by the mss team, see AUTHORS.
    :license: APACHE-2.0, see LICENSE for details.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from future import standard_library
standard_library.install_aliases()

import os
import logging
from datetime import datetime
import traceback
import urllib.parse
from chameleon import PageTemplateLoader


from flask import Flask, request, make_response
from flask_httpauth import HTTPBasicAuth
from mslib.mswms.utils import conditional_decorator

# Flask basic auth's documentation
# https://flask-basicauth.readthedocs.io/en/latest/#flask.ext.basicauth.BasicAuth.check_credentials

app = Flask(__name__)
auth = HTTPBasicAuth()

realm = 'Mission Support Web Map Service'
app.config['realm'] = realm

try:
    import mss_wms_settings
except ImportError as ex:
    logging.warning(u"Couldn't import mss_wms_settings (ImportError:'%s'), creating dummy config.", ex)

    class mss_wms_settings(object):
        base_dir = os.path.abspath(os.path.dirname(__file__))
        xml_template_location = os.path.join(base_dir, "xml_templates")
        service_name = "OGC:WMS"
        service_title = "Mission Support System Web Map Service"
        service_abstract = ""
        service_contact_person = ""
        service_contact_organisation = ""
        service_address_type = ""
        service_address = ""
        service_city = ""
        service_state_or_province = ""
        service_post_code = ""
        service_country = ""
        service_fees = ""
        service_access_constraints = "This service is intended for research purposes only."
        register_horizontal_layers = []
        register_vertical_layers = []
        data = {}
        enable_basic_http_authentication = False
        __file__ = None

try:
    import mss_wms_auth
except ImportError as ex:
    logging.warning(u"Couldn't import mss_wms_auth (ImportError:'{%s), creating dummy config.", ex)

    class mss_wms_auth(object):
        allowed_users = [("mswms", "add_md5_digest_of_PASSWORD_here"),
                         ("add_new_user_here", "add_md5_digest_of_PASSWORD_here")]
        __file__ = None


if mss_wms_settings.__dict__.get('enable_basic_http_authentication', False):
    logging.debug("Enabling basic HTTP authentication. Username and "
                  "password required to access the service.")
    import hashlib

    def authfunc(username, password):
        for u, p in mss_wms_auth.allowed_users:
            if (u == username) and (p == hashlib.md5(password.encode('utf-8')).hexdigest()):
                return True
        return False

    @auth.verify_password
    def verify_pw(username, password):
        if request.authorization:
            auth = request.authorization
            username = auth.username
            password = auth.password
        return authfunc(username, password)


from mslib.mswms import mss_plot_driver
from mslib.utils import CaseInsensitiveMultiDict, get_projection_params

# Logging the Standard Output, which will be added to the Apache Log Files
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(funcName)19s || %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

# Chameleon XMl template
base_dir = os.path.abspath(os.path.dirname(__file__))
xml_template_location = os.path.join(base_dir, "xml_templates")
templates = PageTemplateLoader(mss_wms_settings.__dict__.get("xml_template_location", xml_template_location))


class WMSServer(object):

    def __init__(self):
        """
        init method for wms server
        """
        data_access_dict = mss_wms_settings.data

        for key in data_access_dict:
            data_access_dict[key].setup()

        self.hsec_drivers = {}
        for key in data_access_dict:
            self.hsec_drivers[key] = mss_plot_driver.HorizontalSectionDriver(
                data_access_dict[key])

        self.vsec_drivers = {}
        for key in data_access_dict:
            self.vsec_drivers[key] = mss_plot_driver.VerticalSectionDriver(
                data_access_dict[key])

        self.hsec_layer_registry = {}
        for layer, datasets in mss_wms_settings.register_horizontal_layers:
            self.register_hsec_layer(datasets, layer)

        self.vsec_layer_registry = {}
        for layer, datasets in mss_wms_settings.register_vertical_layers:
            self.register_vsec_layer(datasets, layer)

    def register_hsec_layer(self, datasets, layer_class):
        """Register horizontal section layer in internal dict of layers.

        Arguments:
        datasets -- list of strings describing the datasets with which the
                    layer shall be registered.
        layer_class -- class of which the layer instances shall be created.
        """
        # Loop over all provided dataset names. Create an instance of the
        # provided layer class for all datasets and register the layer
        # instances with the datasets.
        for dataset in datasets:
            try:
                layer = layer_class(self.hsec_drivers[dataset])
            except KeyError:
                continue
            logging.debug(u"registering horizontal section layer '%s' with dataset '%s'", layer.name, dataset)
            # Check if the current dataset has already been registered. If
            # not, check whether a suitable driver is available.
            if dataset not in self.hsec_layer_registry:
                if dataset in self.hsec_drivers:
                    self.hsec_layer_registry[dataset] = {}
                else:
                    raise ValueError(u"dataset '%s' not available", dataset)
            self.hsec_layer_registry[dataset][layer.name] = layer

    def register_vsec_layer(self, datasets, layer_class):
        """Register vertical section layer in internal dict of layers.

        See register_hsec_layer() for further information.
        """
        # Loop over all provided dataset names. Create an instance of the
        # provided layer class for all datasets and register the layer
        # instances with the datasets.
        for dataset in datasets:
            try:
                layer = layer_class(self.vsec_drivers[dataset])
            except KeyError:
                continue
            logging.debug(u"registering vertical section layer '%s' with dataset '%s'", layer.name, dataset)
            # Check if the current dataset has already been registered. If
            # not, check whether a suitable driver is available.
            if dataset not in self.vsec_layer_registry:
                if dataset in self.vsec_drivers:
                    self.vsec_layer_registry[dataset] = {}
                else:
                    raise ValueError(u"dataset '%s' not available", dataset)
            self.vsec_layer_registry[dataset][layer.name] = layer

    def create_service_exception(self, code=None, text=""):
        """Create a service exception XML from the XML template defined above.

        Arguments:
        code -- WMS 1.1.1 exception code, see p.51 of the WMS 1.1.1 standard.
                This parameter is optional.
        text -- arbitrary error message

        Returns an XML as string.
        """
        logging.error(u"creating service exception code='%s' text='%s'.", code, text)
        template = templates['service_exception.pt']
        return template(code=code, text=text).encode("utf-8"), "text/xml"

    def get_capabilities(self, server_url=None):
        # ToDo find a more elegant method to do the same
        # Preferable we don't want a seperate data_access module to be configured
        data_access_dict = mss_wms_settings.data

        for key in data_access_dict:
            data_access_dict[key].setup()

        template = templates['get_capabilities.pt']
        logging.debug(u"server-url '%s'", server_url)

        # Horizontal Layers
        hsec_layers = []
        for dataset in self.hsec_layer_registry:
            for layer in self.hsec_layer_registry[dataset].values():
                if layer.uses_time_dimensions() and len(layer.get_init_times()) == 0:
                    logging.error(u"layer %s/%s has no init times!", layer, dataset)
                    continue
                if layer.uses_time_dimensions() and len(layer.get_all_valid_times()) == 0:
                    logging.error(u"layer %s/%s has no valid times!", layer, dataset)
                    continue
                hsec_layers.append((dataset, layer))

        # Vertical Layers
        vsec_layers = []
        for dataset in self.vsec_layer_registry:
            for layer in self.vsec_layer_registry[dataset].values():
                if layer.uses_time_dimensions() and len(layer.get_init_times()) == 0:
                    logging.error(u"layer %s/%s has no init times!", layer, dataset)
                    continue
                if layer.uses_time_dimensions() and len(layer.get_all_valid_times()) == 0:
                    logging.error(u"layer %s/%s has no valid times!", layer, dataset)
                    continue
                vsec_layers.append((dataset, layer))

        settings = mss_wms_settings.__dict__
        return_data = template(hsec_layers=hsec_layers, vsec_layers=vsec_layers, server_url=server_url,
                               service_name=settings.get("service_name", "OGC:WMS"),
                               service_title=settings.get("service_title", "Mission Support System Web Map Service"),
                               service_abstract=settings.get("service_abstract", ""),
                               service_contact_person=settings.get("service_contact_person", ""),
                               service_contact_organisation=settings.get("service_contact_organisation", ""),
                               service_contact_position=settings.get("service_contact_position", ""),
                               service_email=settings.get("service_email", ""),
                               service_address_type=settings.get("service_address_type", ""),
                               service_address=settings.get("service_address", ""),
                               service_city=settings.get("service_city", ""),
                               service_state_or_province=settings.get("service_state_or_province", ""),
                               service_post_code=settings.get("service_post_code", ""),
                               service_country=settings.get("service_country", ""),
                               service_fees=settings.get("service_fees", ""),
                               service_access_constraints=settings.get(
                                   "service_access_constraints",
                                   "This service is intended for research purposes only."))
        return return_data.encode("utf-8"), "text/xml"

    def produce_plot(self, query, mode):
        """
        Handler for a GetMap and GetVSec requests. Produces a plot with
        the parameters specified in the URL.

        # TODO: Handle multiple layers. (mr, 2010-06-09)
        # TODO: Cache the produced images: Check whether an image with the given
        #      parameters has already been produced. (mr, 2010-08-18)
        """
        logging.debug("GetMap/GetVSec request. Interpreting parameters..")

        # 1) Make query parameters Case Insenstitive
        # =========================================
        query = CaseInsensitiveMultiDict(query)
        # 2) Evaluate query parameters:
        # =============================

        # Image size.
        figsize = float(query.get('WIDTH', 900)), float(query.get('HEIGHT', 600))
        logging.debug(u"  requested image size = %sx%s", figsize[0], figsize[1])

        # Requested layers.
        layers = [layer for layer in query.get('LAYERS', '').strip().split(',') if layer]
        layer = layers[0] if len(layers) > 0 else ''
        if layer.find(".") > 0:
            dataset, layer = layer.split(".")
        else:
            dataset = None
        logging.debug(u"  requested dataset = '%s', layer = '%s'", dataset, layer)

        # Requested style(s).
        styles = [style for style in query.get('STYLES', 'default').strip().split(',') if style]
        style = styles[0] if len(styles) > 0 else None
        logging.debug(u"  requested style = '%s'", style)

        # Forecast initialisation time.
        init_time = query.get('DIM_INIT_TIME')
        if init_time is not None:
            try:
                init_time = datetime.strptime(init_time, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                return self.create_service_exception(
                    code="InvalidDimensionValue",
                    text="DIM_INIT_TIME has wrong format (needs to be 2005-08-29T13:00:00Z)")
        logging.debug(u"  requested initialisation time = '%s'", init_time)

        # Forecast valid time.
        valid_time = query.get('TIME')
        if valid_time is not None:
            try:
                valid_time = datetime.strptime(valid_time, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                return self.create_service_exception(
                    code="InvalidDimensionValue",
                    text="TIME has wrong format (needs to be 2005-08-29T13:00:00Z)")
        logging.debug(u"  requested (valid) time = '%s'", valid_time)

        # Coordinate reference system.
        crs = query.get('SRS', 'EPSG:4326').lower()
        # Allow to request vertical sections via GetMap, if the specified CRS is of type "VERT:??".
        msg = None
        if crs.startswith('vert:logp'):
            mode = "getvsec"
        else:
            try:
                get_projection_params(crs)
            except ValueError:
                return self.create_service_exception(
                    code="InvalidSRS", text=u"The requested CRS '{}' is not supported.".format(crs))
        logging.debug(u"  requested coordinate reference system = '%s'", crs)

        # Create a frameless figure (WMS) or one with title and legend
        # (MSS specific)? Default is WMS mode (frameless).
        noframe = query.get('FRAME', 'off').lower() == 'off'

        # Transparency.
        transparent = query.get('TRANSPARENT', 'false').lower() == 'true'
        if transparent:
            logging.debug("  requested transparent image")

        # Return format (image/png, text/xml, etc.).
        return_format = query.get('FORMAT', 'image/png').lower()
        logging.debug(u"  requested return format = '%s'", return_format)
        if return_format not in ["image/png", "text/xml"]:
            return self.create_service_exception(
                code="InvalidFORMAT",
                text=u"unsupported FORMAT: '{}'".format(return_format))

        # 3) Check GetMap/GetVSec-specific parameters and produce
        #    the image with the corresponding section driver.
        # =======================================================
        if mode == "getmap":
            # Check requested layer.
            if (dataset not in self.hsec_layer_registry) or (layer not in self.hsec_layer_registry[dataset]):
                return self.create_service_exception(
                    code="LayerNotDefined",
                    text=u"Invalid LAYER '{}.{}' requested".format(dataset, layer))

            # Check if the layer requires time information and if they are given.
            if self.hsec_layer_registry[dataset][layer].uses_time_dimensions():
                if init_time is None:
                    return self.create_service_exception(
                        code="MissingDimensionValue",
                        text="INIT_TIME not specified (use the DIM_INIT_TIME keyword)")
                if valid_time is None:
                    return self.create_service_exception(code="MissingDimensionValue", text="TIME not specified")

            # Check if the requested coordinate system is supported.
            if not self.hsec_layer_registry[dataset][layer].support_epsg_code(crs):
                return self.create_service_exception(
                    code="InvalidSRS",
                    text=u"The requested CRS '{}' is not supported.".format(crs))

            # Bounding box.
            try:
                bbox = [float(v) for v in query.get('BBOX', '-180,-90,180,90').split(',')]
            except ValueError:
                return self.create_service_exception(text=u"Invalid BBOX: {}".format(query.get("BBOX")))

            # Vertical level, if applicable.
            level = query.get('ELEVATION')
            level = float(level) if level is not None else None
            layer_datatypes = self.hsec_layer_registry[dataset][layer].required_datatypes()
            if any(_x in layer_datatypes for _x in ["pl", "al", "ml", "tl", "pv"]) and level is None:
                # Use the default value.
                level = -1
            elif ("sfc" in layer_datatypes) and \
                    all(_x not in layer_datatypes for _x in ["pl", "al", "ml", "tl", "pv"]) and \
                    level is not None:
                return self.create_service_exception(
                    text=u"ELEVATION argument not applicable for layer '{}'. Please omit this argument.".format(layer))

            plot_driver = self.hsec_drivers[dataset]
            try:
                plot_driver.set_plot_parameters(self.hsec_layer_registry[dataset][layer], bbox=bbox, level=level,
                                                crs=crs, init_time=init_time, valid_time=valid_time, style=style,
                                                figsize=figsize, noframe=noframe, transparent=transparent,
                                                return_format=return_format)
                image = plot_driver.plot()
            except (IOError, ValueError) as ex:
                logging.error(u"ERROR: %s %s", type(ex), ex)
                logging.debug(u"%s", traceback.format_exc())
                msg = u"The data corresponding to your request is not available. Please check the " \
                      u"times and/or levels you have specified.\n\n" \
                      u"Error message: '{}'".format(ex)
                return self.create_service_exception(text=msg)

        elif mode == "getvsec":
            # Vertical secton path.
            path = query.get("PATH")
            if path is None:
                return self.create_service_exception(text="PATH not specified")
            try:
                path = [float(v) for v in path.split(',')]
                path = [[lat, lon] for lat, lon in zip(path[0::2], path[1::2])]
            except ValueError:
                return self.create_service_exception(text=u"Invalid PATH: {}".format(path))
            logging.debug(u"VSEC PATH: %s", path)

            # Check requested layers.
            if (dataset not in self.vsec_layer_registry) or (layer not in self.vsec_layer_registry[dataset]):
                return self.create_service_exception(
                    code="LayerNotDefined",
                    text=u"Invalid LAYER '{}.{}' requested".format(dataset, layer))

            # Check if the layer requires time information and if they are given.
            if self.vsec_layer_registry[dataset][layer].uses_time_dimensions():
                if init_time is None:
                    return self.create_service_exception(
                        code="MissingDimensionValue",
                        text="INIT_TIME not specified (use the DIM_INIT_TIME keyword)")
                if valid_time is None:
                    return self.create_service_exception(code="MissingDimensionValue", text="TIME not specified")

            # Bounding box (num interp. points, p_bot, num labels, p_top).
            try:
                bbox = [float(v) for v in query.get("BBOX", "101,1050,10,180").split(",")]
            except ValueError:
                return self.create_service_exception(text=u"Invalid BBOX: {}".format(query.get("BBOX")))

            plot_driver = self.vsec_drivers[dataset]
            try:
                plot_driver.set_plot_parameters(plot_object=self.vsec_layer_registry[dataset][layer],
                                                vsec_path=path,
                                                vsec_numpoints=bbox[0],
                                                vsec_path_connection="greatcircle",
                                                vsec_numlabels=bbox[2],
                                                init_time=init_time,
                                                valid_time=valid_time,
                                                style=style,
                                                bbox=bbox,
                                                figsize=figsize,
                                                noframe=noframe,
                                                transparent=transparent,
                                                return_format=return_format)
                image = plot_driver.plot()
            except (IOError, ValueError) as ex:
                logging.error(u"ERROR: %s %s", type(ex), ex)
                msg = u"The data corresponding to your request is not available. Please check the " \
                      u"times and/or path you have specified.\n\n" \
                      u"Error message: {}".format(ex)
                return self.create_service_exception(text=msg)

        # 4) Return the produced image.
        # =============================
        return image, return_format


server = WMSServer()


@app.route('/')
@conditional_decorator(auth.login_required, mss_wms_settings.__dict__.get('enable_basic_http_authentication', False))
def application():
    try:
        # Request info
        query = request.args

        # Processing
        request_type = query.get('request')
        if request_type is None:  # request_type may *actually* be set to None
            request_type = ''
        request_type = request_type.lower()

        url = request.url
        server_url = urllib.parse.urljoin(url, urllib.parse.urlparse(url).path)

        if request_type == "getcapabilities":
            return_data, return_format = server.get_capabilities(server_url)
        elif request_type in ['getmap', 'getvsec']:
            return_data, return_format = server.produce_plot(query, request_type)
        else:
            raise RuntimeError(u"Request type '{}' is not valid.".format(request))

        res = make_response(return_data, 200)
        response_headers = [('Content-type', return_format), ('Content-Length', str(len(return_data)))]
        for response_header in response_headers:
            res.headers[response_header[0]] = response_header[1]

        return res

    except Exception as ex:
        error_message = u"{}: {}\n".format(type(ex), ex)
        error_message = error_message.encode("utf-8")

        response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(error_message)))]
        res = make_response(error_message, 404)
        for response_header in response_headers:
            res.headers[response_header[0]] = response_header[1]

        return res
