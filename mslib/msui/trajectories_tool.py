# -*- coding: utf-8 -*-
"""

    mslib.msui.trajectories_tool
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Tool application that manages trajectories.

    This file is part of mss.

    :copyright: Copyright 2008-2014 Deutsches Zentrum fuer Luft- und Raumfahrt e.V.
    :copyright: Copyright 2011-2014 Marc Rautenhaus (mr)
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

from builtins import str
import logging
import os

from mslib.msui.mss_qt import QtCore, QtWidgets, QtGui, get_open_filename, get_existing_directory
from mslib.msui.mss_qt import ui_trajectories_window as ui
from mslib.msui import trajectory_item_tree as titree
from mslib.msui.viewwindows import MSSViewWindow
from mslib.msui.icons import icons
from mslib.msui import MissionSupportSystemDefaultConfig as mss_default
from mslib.utils import config_loader


class MSSTrajectoriesToolWindow(MSSViewWindow, ui.Ui_TrajectoriesWindow):
    """Implements a trajectory tool.
    """

    name = "Trajectories Tool"
    moduleCloses = QtCore.pyqtSignal(name="moduleCloses")

    def __init__(self, parent=None, listviews=None, listtools=None, viewsChanged=None):
        """
        """
        super(MSSTrajectoriesToolWindow, self).__init__(parent)
        self.setupUi(self)
        self.last_save_directory = config_loader(dataset="data_dir", default=mss_default.data_dir)
        self.setWindowIcon(QtGui.QIcon(icons('64x64')))

        self.actionOpenFlightTrack.setEnabled(titree.HAVE_NAPPY)
        self.viewsChanged = viewsChanged

        # traj_item_tree stores all data corresponding to the map, i.e. flight
        # tracks, trajectories, etc. The design follows Qt's model/view
        # architecture: the data structure is derived from QAbstractItemModel,
        # thus it provides all methods necessary so that the data can be
        # displayed in a QTreeView widget, but it also makes the data accessible
        # for the rest of the program (especially the map).
        self.traj_item_tree = titree.LagrantoMapItemsTreeModel()

        # Connect the implementation for QtAbstractItemModel
        # (self.mapItemsTree) with the tree view. All changes in the data
        # structure will automatically be displayed in the GUI.
        self.tvVisibleElements.setModel(self.traj_item_tree)

        # List that stores the views the trajectory item tree is connected to.
        self.connected_views = []

        # Pointer to the QListWidget that accomodates the views that are
        # open in the MSUI.
        self.listviews = listviews
        self.listtools = listtools

        # Connect Qt SIGNALs:
        # ===================

        # Menu.
        self.actionOpenTrajectories.triggered.connect(self.loadTrajectories)
        self.actionOpenFlightTrack.triggered.connect(self.loadFlightTrack)

        # Item selection.
        self.btSelectMapElements.clicked.connect(self.selectMapElements)

        # Item style.
        self.btColour.clicked.connect(self.setCurrentItemColour)
        self.btLineStyle.clicked.connect(self.setCurrentItemLineStyle)
        self.btLineWidth.clicked.connect(self.setCurrentItemLineWidth)
        self.btTimeMarker.clicked.connect(self.setCurrentItemTimeMarker)

        # View control.
        self.btPlotInView.clicked.connect(self.plotCurrentItemInView)
        self.btRemoveFromView.clicked.connect(self.removeCurrentItemFromView)
        if self.viewsChanged is not None:
            self.viewsChanged.connect(self.updateViews)
        self.updateViews()

    def closeEvent(self, event):
        """Ask user if he/she wants to close the window.

        Overloads MSSViewWindow.closeEvent() and emits the signal
        'moduleCloses()'.
        """
        if super(MSSTrajectoriesToolWindow, self).closeEvent(event):
            self.moduleCloses.emit()

    def loadFlightTrack(self):
        """Slot for the 'Open Flight Track..' menu entry. Opens a file dialog
           and reads the selected NASA Ames file using nappy.
        """
        # Ask for a file to open, convert the return file name from type
        filename = get_open_filename(
            self, "Open NASA Ames File", "", "NASA Ames files (*.nas)",
            pickertag="filepicker_trajectories")
        # ToDo nappy needs filelike object first
        # _dirname, _name = os.path.split(filename)
        # _fs = open_fs(_dirname)
        if filename is not None:
            # until nappy knows filelike objects
            # nas_file = _fs.open(_name, "wb")
            nas_file = os.path.expanduser(filename)

            logging.debug(u"Loading flight track data from '%s'", nas_file)

            # Add the flight track to the data tree.
            try:
                new_item_index = self.traj_item_tree.addFlightTrack(nas_file)

                # Scroll the tree view so that the new item is visible and resize
                # the first column to be wide enough for the text.
                self.tvVisibleElements.scrollTo(new_item_index)
                self.tvVisibleElements.resizeColumnToContents(0)
            except RuntimeError:
                QtWidgets.QMessageBox.critical(
                    self, self.tr("Trajectory Tool"), self.tr(u"ERROR:\nCould not read file\n{}".format(nas_file)))

    def loadTrajectories(self):
        """Slot for the 'Open Trajectories..' menu entry. Opens a QFileDialog
           and reads the selected trajectory file using lagrantooutputreader.
        """
        # Ask for a directory to open.
        traj_dir = get_existing_directory(
            self, "Open Lagranto Output Directory", self.last_save_directory)
        if traj_dir is not None:
            logging.debug(u"Loading trajectory data from '%s'", traj_dir)

            # Test if selected directory contains subdirectories (as is
            # the case with ensemble runs). If yes,
            # load all those subdirectories. Otherwise load the selected
            # directory.
            # ToDo we have to solve this differently, it is not a good idea to have such a traversal
            traj_dir_items = os.listdir(traj_dir)
            subdirs = [sdir for sdir in traj_dir_items
                       if os.path.isdir(os.path.join(traj_dir, sdir))]
            if len(subdirs) > 0:
                for sdir in subdirs:
                    # Add the trajectories to the data tree.
                    new_item_index = self.traj_item_tree \
                        .addTrajectoryDirectory(os.path.join(traj_dir,
                                                             sdir))
            else:
                # Add the trajectories to the data tree.
                new_item_index = self.traj_item_tree.addTrajectoryDirectory(traj_dir)

            # Scroll the tree view so that the new item is visible and resize the
            # first column to be wide enough for the text.
            self.tvVisibleElements.scrollTo(new_item_index)
            self.tvVisibleElements.resizeColumnToContents(0)

    def selectedMapElements(self):
        """Return a list with QModelIndex objects referencing the elements
           selected in tvVisisbleElements.

        Background: For tvVisibleElements.selectedIndexes(), one element is
        a value at a row/column position. That means that, if one row is
        selected, as many indexes are returned as there are columns. However,
        in this application all values in a row belong to the same element.
        The indexes returned by selectedIndexes() for a single row all
        reference the same element, and we need only one reference per row.
        Unfortunately, the ordering of the indexes in the list returned by
        selectedIndexes() is a bit of a mess -- the elements are ordered
        'rows first' for rows selected at once by the user, and 'columns first'
        for rows selected subsequently. For example, if three rows are selected
        at once as a block (click and move down), the list will be ordered
        [r1,c1; r2,c1; .. rN,c1; r1,c2, r2,c2, ...], if the three rows are
        selected one after the other while pressing the ctrl-key, the list
        will be ordered [r1,c1; r1,c2; .. r1,cM; r2,c1, r2,c2, ...].

        The algorithm implemented in this method returns a list of the items
        represented by the rows, with only looking once at each row.
        """
        # Algorithm description: The easiest solution would be to look at each
        # element in the list returned by selectedIndexes(), however, we
        # don't need to look at each element in this list:
        #
        # Get the selected elements from the tree view (one element at each
        # row/column).
        indexes = self.tvVisibleElements.selectedIndexes()
        # Include the item referenced by the first index in the return
        # list, just make sure not to include this item again.
        returnIndexes = indexes[:1]
        # i is the current index in the list, o is an offset.
        i = 0
        o = 1
        while i < len(indexes):
            # If the item referenced by the index at i+o is another than
            # the item referenced by the index at i, include the new item
            # in the return list and look at the next index (ie. increase
            # the offset).
            if indexes[i + o].internalPointer() != indexes[i].internalPointer():
                returnIndexes.append(indexes[i + o])
                o += 1
            # If it is the same, we can use our knowledge about how the
            # elements in indexes[] are ordered: If o rows have been selected
            # in a block, we have encountered o subsequently different items.
            # We will also encounter the same elements columnCount times.
            # Thus, we can skip the next o*columnCount elements in indexes[].
            # The item referenced by the element following then will be
            # a new element, hence we can include it in returnIndexes[] and
            # continue the loop with comparing the new elements to the
            # ones following it (reset o to 1).
            else:
                i += o * self.traj_item_tree.columnCount(None)
                if i < len(indexes):
                    returnIndexes.append(indexes[i])
                o = 1
        return returnIndexes

    def selectMapElements(self):
        """Interpret the selection query entered by the user in the
           leSelectionQuery field and the select all items in the tree
           view that match the query.
        """
        # Check if the selection query should be applied to all available
        # map elements (index of cbSelectElements is 0), or only to the
        # children of the currently selected element (index is 1). In the
        # latter case also check that only one item is currently selected.
        if self.cbSelectElements.currentIndex() == 0:
            # LagrantoMapItemsTreeModel.selectionFromQuery() interprets
            # a root index of None as a selection from all available elements.
            rootIndex = None
        else:
            selectedIndexes = self.selectedMapElements()
            if len(selectedIndexes) != 1:
                QtWidgets.QMessageBox.warning(self, self.tr("select map elements"),
                                              self.tr("Please select a single element for this operation."))
                return
            else:
                rootIndex = selectedIndexes[0]

        # LagrantoMapItemsTreeModel.selectionFromQuery() returns a
        # QtGui.QItemSelection() instance containing the indexes of all
        # elements that match the query.
        #
        # FROM THE PYQT DOCUMENTATION:
        # A QItemSelection is basically a list of selection ranges, see
        # QItemSelectionRange. QItemSelection saves memory, and avoids
        # unnecessary work, by working with selection ranges rather than
        # recording the model item index for each item in the selection.
        # Generally, an instance of this class will contain a list of
        # non-overlapping selection ranges.
        itemSelection = self.traj_item_tree.selectionFromQuery(
            self.leSelectionQuery.text(),
            index=rootIndex)

        # Items can be selected in the tree view by using the select()
        # method of the tree view's selection model. select() takes either
        # a single index or an item selection:
        #     QItemSelectionModel.select (self, QModelIndex index,
        #                                 SelectionFlags command)
        #     QItemSelectionModel.select (self, QItemSelection selection,
        #                                 SelectionFlags command)
        # (see http://www.riverbankcomputing.co.uk/static/Docs/PyQt4/html/
        #   qitemselectionmodel.html#SelectionFlag-enum)
        selectionModel = self.tvVisibleElements.selectionModel()
        if itemSelection.isEmpty():
            # If no item matches the query we can't select anything.
            QtWidgets.QMessageBox.warning(self, self.tr("select map elements"),
                                          self.tr("No matching items have been found."))
        else:
            selectionModel.select(itemSelection,
                                  QtWidgets.QItemSelectionModel.ClearAndSelect |
                                  QtWidgets.QItemSelectionModel.Rows)

    def setCurrentItemColour(self):
        """Informs traj_item_tree to change the colour of the selected elements
           to the one specified by cbColour.
        """
        colour = self.cbColour.currentText()
        if colour == 'None':
            colour = "blue"
        indices = self.selectedMapElements()
        if len(indices) == 1:
            logging.debug(u"Changing colour of element %s",
                          indices[0].internalPointer().getName())
        else:
            logging.debug("Changing colour of selected elements")
        try:
            self.traj_item_tree.changeItemGxProperty_list(indices, 'general',
                                                          'colour', colour)
        except Exception as ex:
            QtWidgets.QMessageBox.warning(self, self.tr('item colour'), self.tr(str(ex)))

    def setCurrentItemLineStyle(self):
        """Informs traj_item_tree to change the line style of the selected
           elements to the one specified by cbLineStyle.
        """
        lineStyle = self.cbLineStyle.currentText()
        if lineStyle == 'None':
            lineStyle = "-"
        indices = self.selectedMapElements()
        if len(indices) == 1:
            logging.debug(u"Changing line style of element %s",
                          indices[0].internalPointer().getName())
        else:
            logging.debug("Changing line style of selected elements")
        try:
            self.traj_item_tree.changeItemGxProperty_list(indices, "general",
                                                          "linestyle", lineStyle)
        except Exception as ex:
            QtWidgets.QMessageBox.warning(self, self.tr('item line style'), self.tr(u"{} {}".format(type(ex), ex)))

    def setCurrentItemLineWidth(self):
        """Informs traj_item_tree to change the line width of the selected
           elements to the one specified by sbLineThickness.
        """
        lineWidth = self.sbLineWidth.value()
        indices = self.selectedMapElements()
        if len(indices) == 1:
            logging.debug(u"Changing line thickness of element %s",
                          indices[0].internalPointer().getName())
        else:
            logging.debug("Changing line thickness of selected elements")
        try:
            self.traj_item_tree.changeItemGxProperty_list(indices, "general",
                                                          "linewidth", lineWidth)
        except Exception as ex:
            QtWidgets.QMessageBox.warning(self, self.tr('item line width'), self.tr(u"{} {}".format(type(ex), ex)))

    def setCurrentItemTimeMarker(self):
        """Set the given time markers for the selected item and all its
           children (the latter for ensembles).

        The method traverses the traj_item_tree starting at the selected item.
        If markers are set for entire ensemble, user feedback is required.
        """
        first_index = None
        last_index = None
        interval = self.teTimeMarker.dateTime().toPyDateTime()
        indexStack = self.selectedMapElements()
        while len(indexStack) > 0:
            index = indexStack.pop()
            item = index.internalPointer()
            #
            # If the current item is a LagrantoOutputItem (i.e. parent for
            # a number of trajectory items) ask the user if he wants to
            # set/change the time marker for all children.
            if isinstance(item, titree.LagrantoOutputItem):
                ret = QtWidgets.QMessageBox.warning(self, self.tr("Time Marker"),
                                                    self.tr("Do you want to set the interval " +
                                                            interval.strftime("%H:%M") +
                                                            "\nfor all children of " + item.getName()),
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                    QtWidgets.QMessageBox.No)
                if ret == QtWidgets.QMessageBox.No:
                    #
                    # If the answer is no, continue with the next item on
                    # the stack.
                    continue
            #
            # If the current item has LagrantoMapItem children, push them onto
            # the stack.
            indexStack.extend([self.traj_item_tree.createIndex(child.row(), 0, child)
                               for child in item.childItems
                               if isinstance(child, titree.LagrantoMapItem)])
            #
            # Now set the time marker for the current item.
            try:
                logging.debug(u"Setting time marker for element %s",
                              item.getName())
                setInterval = self.traj_item_tree.setTimeMarker(index, interval,
                                                                emit_change=False)
                if not setInterval:
                    QtWidgets.QMessageBox.warning(self, self.tr("Time marker"),
                                                  self.tr("Time markers have been deleted."))
                elif setInterval != interval:
                    QtWidgets.QMessageBox.warning(self, self.tr("Time marker"),
                                                  self.tr("Warning: The minimum time interval for the"
                                                          "selected variable is " +
                                                          setInterval.strftime("%H:%M") +
                                                          ".\nThe interval has been set to this value."))
                if not first_index:
                    first_index = index
                last_index = index
            except Exception as ex:
                QtWidgets.QMessageBox.warning(self, self.tr("Time marker"), self.tr(u"{} {}".format(type(ex), ex)))

        self.traj_item_tree.emitChange(first_index, last_index, mode="MARKER_CHANGE")

    def plotCurrentItemInView(self):
        """
        """
        view_name = self.cbPlotInView.currentText()
        selection = self.selectedMapElements()
        if view_name != "None" and len(selection) > 0:
            view_item = (self.listviews.findItems(view_name, QtCore.Qt.MatchContains) +
                         self.listtools.findItems(view_name, QtCore.Qt.MatchContains))[0]
            logging.debug(u"Plotting selected elements in view <%s>", view_name)
            # Connect the trajectory tree to the view.
            view_window = view_item.window
            view = view_window.getView()
            self.traj_item_tree.setItemVisibleInView_list(
                selection, view_item.window, True)
            if view_window not in self.connected_views:
                logging.debug(u"Connecting to view window <%s>",
                              view_window.identifier)
                self.connected_views.append(view_window)
                view.set_trajectory_model(self.traj_item_tree)

    def removeCurrentItemFromView(self):
        """
        """
        view_name = self.cbRemoveFromView.currentText()
        if view_name != "None":
            view_item = (self.listviews.findItems(view_name, QtCore.Qt.MatchContains) +
                         self.listtools.findItems(view_name, QtCore.Qt.MatchContains))[0]
            logging.debug(u"Removing selected elements from view <%s>", view_name)
            self.traj_item_tree.setItemVisibleInView_list(
                self.selectedMapElements(), view_item.window, False)

    def updateViews(self):
        """Update the list of views in the comboboxes cbPlotInView and
           cbRemoveFromView.

           Connected as slot to 'viewsChanged()' of the QListWidget that
           accomodates the views.
        """
        # Remember the currently selected views in the comboboxes.
        item_plot = self.cbPlotInView.currentText()
        item_remove = self.cbRemoveFromView.currentText()

        old_views = [self.cbPlotInView.itemText(i) for i in range(self.cbPlotInView.count())]
        # Clear the boxes, add the "None" view.
        self.cbPlotInView.clear()
        self.cbRemoveFromView.clear()
        self.cbPlotInView.addItem("None")
        self.cbRemoveFromView.addItem("None")
        # Add all available views.
        for i in (self.listviews.findItems("(", QtCore.Qt.MatchContains) +
                  self.listtools.findItems("(", QtCore.Qt.MatchContains)):
            i_view = i.window.getView()
            if hasattr(i_view, "setTrajectoryModel"):
                self.cbPlotInView.addItem(i.text())
                self.cbRemoveFromView.addItem(i.text())
        # Restore the old selection (set "None" if the selected view was
        # closed).
        index = self.cbPlotInView.findText(item_plot)
        self.cbPlotInView.setCurrentIndex(index if index >= 0 else 0)
        index = self.cbRemoveFromView.findText(item_remove)
        self.cbRemoveFromView.setCurrentIndex(index if index >= 0 else 0)

        new_views = [self.cbPlotInView.itemText(i) for i in range(self.cbPlotInView.count())]
        missing_views = [str(_x) for _x in old_views if _x not in new_views]
        stack = [_x for _x in self.traj_item_tree.getRootItem().childItems]
        while len(stack) > 0:
            # Downwards traversal of the tree to determine all visible items
            # below the items that are on the stack.
            item = stack.pop()
            if hasattr(item, "views"):
                item.views = [_x for _x in item.views if _x not in missing_views]
            if hasattr(item, "childItems"):
                stack.extend(item.childItems)
        self.connected_views = [_x for _x in self.connected_views if _x not in missing_views]

    def getItemTree(self):
        """
        """
        return self.traj_item_tree
