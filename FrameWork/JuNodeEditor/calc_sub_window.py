from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import QDataStream, QIODevice, Qt, QPoint
from PySide2.QtWidgets import QAction, QGraphicsProxyWidget, QMenu
from nodeeditor.node_editor_widget import NodeEditorWidget
from nodeeditor.node_edge import EDGE_TYPE_DIRECT, EDGE_TYPE_BEZIER, EDGE_TYPE_SQUARE
from nodeeditor.node_graphics_view import MODE_EDGE_DRAG
from nodeeditor.utils import dumpException
from queue import Queue
from JuRunModule.ju_run_module import run_module

DEBUG = True
DEBUG_CONTEXT = True


class CalculatorSubWindow(NodeEditorWidget):
    def __init__(self, auto_pack=None, log=None):
        super().__init__()
        self.user_logger = log
        self.set_log(log=self.user_logger)
        self.initUI()
        self.auto_pack = auto_pack
        # self.setAttribute(Qt.WA_DeleteOnClose)
        self.deal_ = Queue()
        self.run_module = run_module(queue=self.deal_, device=self.auto_pack.device, log=self.user_logger)
        # self.setTitle()

        self.initNewNodeActions()

        # self.scene.addHasBeenModifiedListener(self.setTitle)
        self.scene.history.addHistoryRestoredListener(self.onHistoryRestored)
        self.scene.addDragEnterListener(self.onDragEnter)
        self.scene.addDropListener(self.onDrop)
        self.scene.setNodeClassSelector(self.getNodeClassFromData)
        self._close_event_listeners = []
        self.view.double_click.connect(self.double_click_ui_show)

    def double_click_ui_show(self, pos):
        item = self.scene.getItemAt(pos)
        if type(item) == QGraphicsProxyWidget:
            item = item.widget()
        selected = None
        if hasattr(item, 'node'):
            selected = item.node
        if hasattr(item, 'socket'):
            selected = item.socket.node
        if selected:
            selected.grNode.double_click_ui_show()

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_C:
            self.s_copy.emit()
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_V:
            self.s_paste.emit()
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_X:
            self.s_cut.emit()
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
            self.s_save.emit()
        elif event.key() == Qt.Key_Delete:
            self.s_del.emit()

    def getNodeClassFromData(self, data):
        if 'op_code' not in data: return None
        return self.auto_pack.get_class_from_opcode(data['op_code'])

    def doEvalOutputs(self):
        # eval all output nodes
        for node in self.scene.nodes:
            if node.__class__.__name__ == "CalcNode_Output":
                node.eval()

    def onHistoryRestored(self):
        self.doEvalOutputs()

    def fileLoad(self, filename):
        if super().fileLoad(filename):
            self.doEvalOutputs()
            return True
        return False

    def save(self, file=None):
        if file is not None:
            self.fileSave(file)
        else:
            self.fileSave()

    def initNewNodeActions(self):
        CALC_NODES = self.auto_pack.CALC_NODES
        self.node_actions = {}
        keys = list(CALC_NODES.keys())
        keys.sort()
        for key in keys:

            node = CALC_NODES[key]
            self.node_actions[node.op_code] = QAction(QIcon(node.icon), node.op_title)
            self.node_actions[node.op_code].setData(node.op_code)

    def initNodesContextMenu(self):
        CALC_NODES = self.auto_pack.CALC_NODES
        context_menu = QMenu(self)
        keys = list(CALC_NODES.keys())
        keys.sort()
        for key in keys: context_menu.addAction(self.node_actions[key])
        return context_menu

    def setTitle(self):
        self.setWindowTitle(self.getUserFriendlyFilename())

    def addCloseEventListener(self, callback):
        self._close_event_listeners.append(callback)

    def closeEvent(self, event):
        for callback in self._close_event_listeners: callback(self, event)

    def onDragEnter(self, event):
        if event.mimeData().hasFormat(self.auto_pack.LISTBOX_MIMETYPE):
            event.acceptProposedAction()
        else:
            # print(" ... denied drag enter event")
            event.setAccepted(False)

    def onDrop(self, event):
        if event.mimeData().hasFormat(self.auto_pack.LISTBOX_MIMETYPE):
            eventData = event.mimeData().data(self.auto_pack.LISTBOX_MIMETYPE)
            dataStream = QDataStream(eventData, QIODevice.ReadOnly)
            pixmap = QPixmap()
            dataStream >> pixmap
            op_code = dataStream.readQString()
            text = dataStream.readQString()

            mouse_position = event.pos()
            scene_position = self.scene.grScene.views()[0].mapToScene(mouse_position)

            if DEBUG: print("GOT DROP: [%s] '%s'" % (op_code, text), "mouse:", mouse_position, "scene:", scene_position)

            try:
                node = self.auto_pack.get_class_from_opcode(op_code)(self.scene)
                node.setPos(scene_position.x(), scene_position.y())
                self.scene.history.storeHistory("Created node %s" % node.__class__.__name__)
            except Exception as e: dumpException(e)


            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            # print(" ... drop ignored, not requested format '%s'" % LISTBOX_MIMETYPE)
            event.ignore()

    def contextMenuEvent(self, event):
        try:
            item = self.scene.getItemAt(event.pos())
            if DEBUG_CONTEXT: print(item)

            if type(item) == QGraphicsProxyWidget:
                item = item.widget()

            if hasattr(item, 'node') or hasattr(item, 'socket'):
                self.handleNodeContextMenu(event)
            elif hasattr(item, 'edge'):
                self.handleEdgeContextMenu(event)
            #elif item is None:
            else:
                self.handleNewNodeContextMenu(event)

            return super().contextMenuEvent(event)
        except Exception as e: dumpException(e)

    def handleNodeContextMenu(self, event):
        if DEBUG_CONTEXT: print("CONTEXT: NODE")
        # self.mapToGlobal(QPoint(1013, 657))
        context_menu = QMenu(self)
        node_run = context_menu.addAction("Run")
        # markDirtyDescendantsAct = context_menu.addAction("Mark Descendant Dirty")
        # markInvalidAct = context_menu.addAction("Mark Invalid")
        # unmarkInvalidAct = context_menu.addAction("Unmark Invalid")
        # evalAct = context_menu.addAction("Eval")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if type(item) == QGraphicsProxyWidget:
            item = item.widget()

        if hasattr(item, 'node'):
            selected = item.node
        if hasattr(item, 'socket'):
            selected = item.socket.node

        # if DEBUG_CONTEXT: print("got item:", selected)
        if selected and action == node_run:
            deal_dic = {"_class": selected, "default_parm": selected.grNode.default_parm}
            self.deal_.put(deal_dic)

    def handleEdgeContextMenu(self, event):
        if DEBUG_CONTEXT: print("CONTEXT: EDGE")
        context_menu = QMenu(self)
        bezierAct = context_menu.addAction("Bezier Edge")
        directAct = context_menu.addAction("Direct Edge")
        squareAct = context_menu.addAction("Square Edge")
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        selected = None
        item = self.scene.getItemAt(event.pos())
        if hasattr(item, 'edge'):
            selected = item.edge

        if selected and action == bezierAct: selected.edge_type = EDGE_TYPE_BEZIER
        if selected and action == directAct: selected.edge_type = EDGE_TYPE_DIRECT
        if selected and action == squareAct: selected.edge_type = EDGE_TYPE_SQUARE

    # helper functions
    def determine_target_socket_of_node(self, was_dragged_flag, new_calc_node):
        target_socket = None
        if was_dragged_flag:
            if len(new_calc_node.inputs) > 0: target_socket = new_calc_node.inputs[0]
        else:
            if len(new_calc_node.outputs) > 0: target_socket = new_calc_node.outputs[0]
        return target_socket

    def finish_new_node_state(self, new_calc_node):
        self.scene.doDeselectItems()
        new_calc_node.grNode.doSelect(True)
        new_calc_node.grNode.onSelected()


    def handleNewNodeContextMenu(self, event):

        if DEBUG_CONTEXT: print("CONTEXT: EMPTY SPACE")
        context_menu = self.initNodesContextMenu()
        action = context_menu.exec_(self.mapToGlobal(event.pos()))

        if action is not None:
            new_calc_node = self.auto_pack.get_class_from_opcode(action.data())(self.scene)
            scene_pos = self.scene.getView().mapToScene(event.pos())
            new_calc_node.setPos(scene_pos.x(), scene_pos.y())
            if DEBUG_CONTEXT: print("Selected node:", new_calc_node)

            if self.scene.getView().mode == MODE_EDGE_DRAG:
                # if we were dragging an edge...
                target_socket = self.determine_target_socket_of_node(self.scene.getView().dragging.drag_start_socket.is_output, new_calc_node)
                if target_socket is not None:
                    self.scene.getView().dragging.edgeDragEnd(target_socket.grSocket)
                    self.finish_new_node_state(new_calc_node)

            else:
                self.scene.history.storeHistory("Created %s" % new_calc_node.__class__.__name__)
