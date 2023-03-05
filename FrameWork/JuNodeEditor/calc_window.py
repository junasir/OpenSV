import os

from PySide2.QtWidgets import QGridLayout, QVBoxLayout
from PySide2.QtGui import QIcon, QKeySequence
from PySide2.QtWidgets import QMdiArea, QWidget, QDockWidget, QAction, QMessageBox, QFileDialog

from nodeeditor.utils import loadStylesheets
from nodeeditor.node_editor_window import NodeEditorWindow
from JuNodeEditor.calc_sub_window import CalculatorSubWindow
from JuControl.ju_ui_drag import QDMDragListbox
from nodeeditor.utils import dumpException, pp
from JuRunModule.ju_auto_package import Auto_Pack

# Enabling edge validators
from nodeeditor.node_edge import Edge
from nodeeditor.node_edge_validators import (
    edge_validator_debug,
    edge_cannot_connect_two_outputs_or_two_inputs,
    edge_cannot_connect_input_and_output_of_same_node
)
Edge.registerEdgeValidator(edge_validator_debug)
Edge.registerEdgeValidator(edge_cannot_connect_two_outputs_or_two_inputs)
Edge.registerEdgeValidator(edge_cannot_connect_input_and_output_of_same_node)


# images for the dark skin
# import JuResource.qss.nodeeditor_dark_resources


DEBUG = False


class CalculatorWindow(NodeEditorWindow):

    def initUI(self):
        self.user_logger.info("info")
        self.Auto_Pack = Auto_Pack(log=self.user_logger)

        self.stylesheet_filename = os.getcwd() + "JuResource/qss/nodeeditor.qss"
        loadStylesheets(
            os.getcwd() + "JuResource/qss/nodeeditor-dark.qss",
            self.stylesheet_filename
        )
        self.empty_icon = QIcon(".")

        # if DEBUG:
        print("Registered nodes:")
        # pp(self.Auto_Pack.CALC_NODES)
        self.createNodesDock()
        self.createActions()
        self.createMenus()
        self.readSettings()

        self.setWindowTitle("Calculator NodeEditor Example")
        # self.mdiArea = self.createMdiChild()
        # self.mdiArea.fileNew()
        # self.mdiArea.fileLoad(filename="2.json")
        # self.mdiArea.fileLoad(filename="2.json")
        # self.mdiArea.show()
        # self.mdiArea.s_del.connect(self.onEditDelete)
        # self.mdiArea.s_copy.connect(self.onEditCopy)
        # self.mdiArea.s_paste.connect(self.onEditPaste)
        # self.mdiArea.s_cut.connect(self.onEditCut)
        # self._grid = QGridLayout(self)
        # self._grid.addWidget(self.mdiArea)

    def createActions(self):
        super().createActions()

    # def getCurrentNodeEditorWidget(self):
    #     """ we're returning NodeEditorWidget here... """
    #     return self.mdiArea

    def onFileNew(self):
        try:
            subwnd = self.createMdiChild()
            subwnd.widget().fileNew()
            subwnd.show()
        except Exception as e: dumpException(e)

    def createMenus(self):
        super().createMenus()
        self.updateWindowMenu()

    def updateEditMenu(self):
        try:
            # print("update Edit Menu")
            active = self.getCurrentNodeEditorWidget()
            hasMdiChild = (active is not None)

            self.actPaste.setEnabled(hasMdiChild)

            self.actCut.setEnabled(hasMdiChild)
            self.actCopy.setEnabled(hasMdiChild)
            self.actDelete.setEnabled(hasMdiChild)

            self.actUndo.setEnabled(hasMdiChild)
            self.actRedo.setEnabled(hasMdiChild)
        except Exception as e: dumpException(e)

    def updateWindowMenu(self):
        pass

    def createToolBars(self):
        pass

    def createNodesDock(self):
        self.nodesListWidget = QDMDragListbox(self, auto_pack=self.Auto_Pack)

    def createMdiChild(self, child_widget=None, file=None, flag=1):
        nodeeditor = child_widget if child_widget is not None else CalculatorSubWindow(auto_pack=self.Auto_Pack,
                                                                                       log=self.user_logger)
        subwnd = nodeeditor
        # subwnd.setWindowIcon(self.empty_icon)
        nodeeditor.scene.addItemSelectedListener(self.updateEditMenu)
        nodeeditor.scene.addItemsDeselectedListener(self.updateEditMenu)
        nodeeditor.scene.history.addHistoryModifiedListener(self.updateEditMenu)
        # nodeeditor.addCloseEventListener(self.onSubWndClose)
        mdiArea = subwnd
        # mdiArea.s_del.connect(self.onEditDelete)
        # mdiArea.s_copy.connect(self.onEditCopy)
        # mdiArea.s_paste.connect(self.onEditPaste)
        # mdiArea.s_cut.connect(self.onEditCut)
        # mdiArea.s_save.connect(self.onFileSave)
        _grid = QGridLayout(self)
        _grid.addWidget(mdiArea)
        if flag == 1:
            mdiArea.fileNew()
            mdiArea.fileSave(file)
        else:
            mdiArea.fileLoad(file)
        mdiArea = self.getCurrentNodeEditorWidget(mdiArea=mdiArea)
        return mdiArea

    def getCurrentNodeEditorWidget(self, mdiArea=None):
        """get current :class:`~nodeeditor.node_editor_widget`

        :return: get current :class:`~nodeeditor.node_editor_widget`
        :rtype: :class:`~nodeeditor.node_editor_widget`
        """
        return mdiArea

    def file_load(self, file):
        nodeeditor = CalculatorSubWindow(auto_pack=self.Auto_Pack, log=self.user_logger)
        nodeeditor.fileLoad(file)
        mdiArea = self.createMdiChild(child_widget=nodeeditor, file=file, flag=2)
        # mdiArea = self.getCurrentNodeEditorWidget(mdiArea=mdiArea)
        return mdiArea
