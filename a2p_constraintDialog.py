#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2018 kbwbe                                              *
#*                                                                         *
#*   Portions of code based on hamish's assembly 2                         *
#*                                                                         *
#*   This program is free software; you can redistribute it and/or modify  *
#*   it under the terms of the GNU Lesser General Public License (LGPL)    *
#*   as published by the Free Software Foundation; either version 2 of     *
#*   the License, or (at your option) any later version.                   *
#*   for detail see the LICENCE text file.                                 *
#*                                                                         *
#*   This program is distributed in the hope that it will be useful,       *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
#*   GNU Library General Public License for more details.                  *
#*                                                                         *
#*   You should have received a copy of the GNU Library General Public     *
#*   License along with this program; if not, write to the Free Software   *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
#*   USA                                                                   *
#*                                                                         *
#***************************************************************************

import FreeCAD, FreeCADGui, Part
from PySide import QtGui, QtCore
import os, sys
from a2p_viewProviderProxies import *
from  FreeCAD import Base

from a2p_solversystem import solveConstraints


#==============================================================================
class a2p_ConstraintPanel(QtGui.QWidget):
    def __init__(self):
        super(a2p_ConstraintPanel,self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Create constraints')
        self.setMinimumHeight(200)
        
        mainLayout = QtGui.QVBoxLayout() # a VBoxLayout for the whole form
        #-------------------------------------
        self.panel1 = QtGui.QWidget(self)
        self.panel1.setMinimumHeight(40)
        panel1_Layout = QtGui.QHBoxLayout()
        #-------------------------------------
        self.pointIdentityButton = QtGui.QPushButton(self.panel1)
        self.pointIdentityButton.setFixedSize(32,32)
        self.pointIdentityButton.setIcon(QtGui.QIcon(':/icons/a2p_PointIdentity.svg'))
        self.pointIdentityButton.setToolTip("pointIdentity")
        self.pointIdentityButton.setText("")
        #-------------------------------------
        self.pointOnLineButton = QtGui.QPushButton(self.panel1)
        self.pointOnLineButton.setFixedSize(32,32)
        self.pointOnLineButton.setIcon(QtGui.QIcon(':/icons/a2p_PointOnLineConstraint.svg'))
        self.pointOnLineButton.setToolTip("pointOnLine")
        self.pointOnLineButton.setText("")
        #-------------------------------------
        panel1_Layout.addWidget(self.pointIdentityButton)
        panel1_Layout.addWidget(self.pointOnLineButton)
        panel1_Layout.addStretch(1)
        self.panel1.setLayout(panel1_Layout)
        #-------------------------------------
        
        
        #-------------------------------------
        self.finalPanel = QtGui.QWidget(self)
        self.finalPanel.setMinimumHeight(40)
        finalPanel_Layout = QtGui.QHBoxLayout()
        #-------------------------------------
        self.solveButton = QtGui.QPushButton(self.finalPanel)
        self.solveButton.setFixedSize(32,32)
        self.solveButton.setIcon(QtGui.QIcon(':/icons/a2p_solver.svg'))
        self.solveButton.setToolTip("solve Constraints")
        self.solveButton.setText("")
        #-------------------------------------
        finalPanel_Layout.addStretch(1)
        finalPanel_Layout.addWidget(self.solveButton)
        self.finalPanel.setLayout(finalPanel_Layout)
        #-------------------------------------
        
        #-------------------------------------
        mainLayout.addWidget(self.panel1)
        mainLayout.addStretch(1)
        mainLayout.addWidget(self.finalPanel)
        self.setLayout(mainLayout)       
        #-------------------------------------
        
        self.selectionTimer = QtCore.QTimer()
        QtCore.QObject.connect(self.selectionTimer, QtCore.SIGNAL("timeout()"), self.parseSelections)
        self.selectionTimer.start(200)
        
        QtCore.QObject.connect(self.solveButton, QtCore.SIGNAL("clicked()"), self.solve)
        
    def parseSelections(self):
        print ("parseSelections")
        
        self.selectionTimer.start(200)

        
    def solve(self):
        doc = FreeCAD.activeDocument()
        if doc != None:
            solveConstraints(doc)
        
    
#==============================================================================
class a2p_ConstraintTaskDialog:
    '''
    Form for definition of constraints
    ''' 
    def __init__(self):
        self.form = a2p_ConstraintPanel()
        
    def accept(self):
        return True

    def reject(self):
        return True

    def getStandardButtons(self):
        retVal = (
            #0x02000000 + # Apply
            0x00400000 + # Cancel
            0x00200000 + # Close
            0x00000400   # Ok
            )
        return retVal
#==============================================================================
toolTipText = \
'''
Open a dialog to
define constraints
'''

class a2p_ConstraintDialogCommand:
    def Activated(self):
        
        d = a2p_ConstraintTaskDialog()
        FreeCADGui.Control.showDialog(d)

    def GetResources(self):
        return {
             #'Pixmap' : ':/icons/a2p_PointIdentity.svg',
             'MenuText': 'Define constraints',
             'ToolTip': toolTipText
             }

FreeCADGui.addCommand('a2p_ConstraintDialogCommand', a2p_ConstraintDialogCommand())
#==============================================================================
















