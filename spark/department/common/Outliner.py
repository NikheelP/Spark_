from PySide2 import QtCore, QtGui, QtWidgets

from maya import cmds
from maya import mel
import maya.cmds as cmds
import maya.app.general.resourceBrowser as resourceBrowser
from shiboken2 import wrapInstance
import shiboken2
from PySide2 import QtWidgets


from maya import OpenMayaUI as omui


# import time
_OUTLINERS_ = {}

def getOutlinerCustomOutput(outlinerName):
    outliner = _OUTLINERS_[outlinerName]
    output = outliner.customOutput_get()
    return output

class outlinerWidget(QtWidgets.QWidget):
    selectionFilter_global = []

    def __init__(self, parent=None, outlinerName=None, **kwargs):
        super(outlinerWidget, self).__init__(parent=parent, **kwargs)
        self.setObjectName(outlinerName + '_wrapperWidget')
        self.outlinerName = outlinerName
        self.rootLayout = QtWidgets.QVBoxLayout(self)
        self.rootLayout.setObjectName(outlinerName + '_outlinerLayout')
        self.rootLayout.setContentsMargins(0, 0, 0, 0)
        self.rootLayout.setSpacing(0)
        self.rootLayout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        self.setLayout(self.rootLayout)

        self.buildUI()


    def buildUI(self):
        if cmds.outlinerEditor(self.outlinerName, ex=True):
            cmds.deleteUI(self.outlinerName)

        rootLayoutMaya = self.getMayaFullDagPath(self.rootLayout)
        print('root: ', rootLayoutMaya)
        self.outliner = cmds.outlinerEditor(self.outlinerName, panel=None, parent=rootLayoutMaya)
        cmds.outlinerEditor(self.outliner,
                            edit=True,
                            mainListConnection='worldList',
                            selectionConnection='modelList',
                            showReferenceNodes=True,
                            setFilter='defaultSetFilter',
                            showShapes=False,
                            showDagOnly=False,
                            showSetMembers=True,
                            showReferenceMembers=True,
                            )

        self.outlinerWidget = self.getWorkspaceQtPointer(self.outliner)
        self.outlinerWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.rootLayout.addWidget(self.outlinerWidget)

        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setMouseTracking(True)

        self.hotkey_revealSelected = QtWidgets.QShortcut(QtGui.QKeySequence("F"), self)
        self.hotkey_revealSelected.setEnabled(False)
        #self.hotkey_revealSelected.activated.connect(self.revealSelected)


    def getMayaFullDagPath(self, QObject):
        try:
            ptr = long(shiboken2.getCppPointer(QObject)[0])
        except:
            ptr = omui.MQtUtil.fullName(long(QtWidgets.shiboken.unwrapinstance(QObject)))
        mayaFullDagPath = omui.MQtUtil.fullName(ptr)
        return mayaFullDagPath

    def getWorkspaceQtPointer(self, workspaceName):
        qtCtrl = omui.MQtUtil_findControl(workspaceName)
        ptr = wrapInstance(long(qtCtrl), QtWidgets.QWidget)
        return ptr


def iniUI():
    # app = QtWidgets.QApplication([])
    outlinerGUI = outlinerWidget(outlinerName='dummyoutliner')
    outlinerGUI.setWindowTitle('CustomOutlinerA')
    outlinerGUI.setWindowFlags(outlinerGUI.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
    outlinerGUI.resize(600, 350)
    outlinerGUI.show()
