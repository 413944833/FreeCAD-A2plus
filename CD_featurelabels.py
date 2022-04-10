#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2020 Dan Miel                                           *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the          *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307   *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************
# This is to be used with A2plus Assembly WorkBench
#

import FreeCADGui
import FreeCAD
from PySide.QtGui import *
from PySide import QtGui, QtCore
import CD_ConstraintDiagnostics

class formMain(QtGui.QMainWindow):

    def __init__(self, name):
        self.name = name
        super(formMain, self).__init__()
        self.setWindowTitle('Create Labels')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setGeometry(300, 200, 200, 200)
        self.setStyleSheet("font: 11pt arial MS")

        self.btnLabels = [['Add Face Labels', 'Add labels to all of the faces on a selected part'],
                          ['Add Edge Labels', 'Add labels to all of the edges on a selected part'],
                          ['Add Vertex Labels', 'Add labels to all of the vertices on a selected part'],
                          ['Delete Labels', 'Delete all labels'],
                          ['Close', '']
                          ]

        self.btns=[]
        BtnNum = 0
        for row in range(0, len(self.btnLabels)) :
            btny = 20 +(28*row)
            self.btn = QtGui.QPushButton( str(self.btnLabels[row][0]), self)
            self.btn.move(5, btny)
            self.btn.setFixedWidth(190)
            self.btn.setFixedHeight(25)
            self.btn.setToolTip(self.btnLabels[row][1])
            self.btn.released.connect(self.button_pushed) # pressed
            self.btns.append(self.btn)
            BtnNum = BtnNum + 1


    def button_pushed(self):
        index = self.btns.index(self.sender())
        btext = self.btns[index].text()
        if btext == 'Add Face Labels':
            labels.addlabels('Face')
        if btext == 'Add Edge Labels':
            labels.addlabels('Edge')
        if btext == 'Add Vertex Labels':
            labels.addlabels('Vertex')

        if btext == 'Delete Labels':
            labels.deletelabels()
        if btext == 'Attach to':
            labels.attachto()
        if btext == 'Close':
            self.Closeme()

        if btext == 'Selected Labels':
            labels.selectedlabels()


    def hideMe(self):
        QtGui.Selection.clearSelection()
        self.close()


    def showme(self):
        self.show()

    def Closeme(self):
        self.close()

    def closeEvent(self, event):
        form1.Closeme()
        self.close()

form1 = formMain('form1')

class classLabels():
    def __init__(self):
        self.labelGroup = None

    def checkselection(self):
        """Checks to see if labels already exist."""
        doc = FreeCAD.activeDocument()
        self.labelGroup = doc.getObject("partLabels")
        if self.labelGroup is None:
            self.labelGroup = doc.addObject("App::DocumentObjectGroup", "partLabels")
        if len(FreeCADGui.Selection.getSelection()) == 0:
            CD_ConstraintDiagnostics.mApp('One part must be selected.\nPlease select One part and try again')
            return(False)
        return(True)


    def addlabels(self, feat):
        sel = self.checkselection()
        if not sel:
            return
        sel = FreeCADGui.Selection.getSelection()  # Select an object
        if feat == 'Face':
            features = sel[0].Shape.Faces
        if feat == 'Edge':
            features = sel[0].Shape.Edges
        if feat == 'Vertex':
            features = sel[0].Shape.Vertexes

        for num in range(0, len(features)):
            ent = features[num]
            if feat == 'Vertex':
                loc = ent.Point
            else:
                loc = ent.CenterOfMass
            partLabel = self.makelabel(ent, feat+str(num+1), loc)
            self.labelGroup.addObject(partLabel)


    def makelabel(self, ent, name, loc):
        partLabel = FreeCAD.ActiveDocument.addObject("App::AnnotationLabel", "partLabel")
        partLabel.LabelText = name
        partLabel.BasePosition.x = loc[0]
        partLabel.BasePosition.y = loc[1]
        partLabel.BasePosition.z = loc[2]
        partLabel.ViewObject.BackgroundColor = (1.0, 1.0, 0.0)
        partLabel.ViewObject.TextColor = (0.0, 0.0, 0.0)
        return(partLabel)



    def deletelabels(self):
        for obj in FreeCAD.ActiveDocument.Objects:
            if "partLabel" in obj.Label:
                FreeCAD.ActiveDocument.removeObject(obj.Name)


    def attachto(self, sel=None, featname=''):

        sel = self.checkselection()
        if not sel:
            return
        if featname == '':
            featname = form1.txtboxaddlabel.text()
        if sel is None:
            sel = FreeCADGui.Selection.getSelection()[0]
        FreeCADGui.Selection.clearSelection()
        FreeCADGui.Selection.addSelection(sel, featname)
        s = FreeCADGui.Selection.getSelectionEx()[0]
        ent = s.SubObjects[0]
        self.makelabel(ent, name, loc)





    def getEntLoc(self, ent, featname):
        if 'V' in featname:
            loc = ent.Point
        else:
            loc = ent.CenterOfMass
        partLabel = self.makelabel(ent, featname, loc)
        self.labelGroup.addObject(partLabel)
        self.makelabel(ent, featname, loc)


    def labelForTable(self, ent, featname):
        """Create a label to find a part."""
        sel = self.checkselection()
        self.getEntLoc(ent, featname)



    def selectedlabels(self):
        sel = self.checkselection()
        if not sel:
            return
        sels = FreeCADGui.Selection.getSelectionEx()  # Select an object
        for sel in sels:
            featname = sel.SubElementNames[0]
            ent = sel.SubObjects[0]
            self.getentloc(ent, featname)

labels = classLabels()
