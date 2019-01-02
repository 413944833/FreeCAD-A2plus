#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2019 kbwbe                                              *
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
import os, sys, math, copy
from a2p_viewProviderProxies import *
from  FreeCAD import Base

from a2plib import *
from a2p_solversystem import solveConstraints
import a2p_constraints, a2p_constraintDialog

#==============================================================================
class a2p_PointIdentityConstraintCommand:
    def Activated(self):
        selection = FreeCADGui.Selection.getSelectionEx()
        
        if not a2p_constraints.PointIdentityConstraint.isValidSelection(selection):
            msg = '''
                  To add a point Identity constraint select exactly two vertexes!
                  '''
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(), "Incorrect Usage", msg)
            return
        
        c = a2p_constraints.PointIdentityConstraint(selection)
        cvp = a2p_constraintDialog.a2p_ConstraintValuePanel(
            c.constraintObject,
            'createConstraint'
            )
        FreeCADGui.Selection.clearSelection()

    def IsActive(self):
        return a2p_constraints.PointIdentityConstraint.isValidSelection(
            FreeCADGui.Selection.getSelectionEx()
            )

    def GetResources(self):
        return {
             'Pixmap' : path_a2p + '/icons/a2p_PointIdentity.svg',
             'MenuText': 'Add PointIdentity Constraint',
             'ToolTip': a2p_constraints.PointIdentityConstraint.getToolTip()
             }

FreeCADGui.addCommand('a2p_PointIdentityConstraintCommand', a2p_PointIdentityConstraintCommand())

#==============================================================================
class a2p_PointOnLineConstraintCommand:
    def Activated(self):
        selection = FreeCADGui.Selection.getSelectionEx()
        
        if not a2p_constraints.PointOnLineConstraint.isValidSelection(selection):
            msg = '''
                  for PointOnLine constraint select in this order:
                  1.) a vertex
                  2.) a line (linear edge)  
    
                  Selection made: %s
                  ''' % printSelection(selection)
    
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(), "Incorrect Usage", msg)
            return 
        
        c = a2p_constraints.PointOnLineConstraint(selection)
        cvp = a2p_constraintDialog.a2p_ConstraintValuePanel(
            c.constraintObject,
            'createConstraint'
            )
        FreeCADGui.Selection.clearSelection()
              
    def IsActive(self):
        return a2p_constraints.PointOnLineConstraint.isValidSelection(
            FreeCADGui.Selection.getSelectionEx()
            )

    def GetResources(self): 
        return {
             'Pixmap' : path_a2p + '/icons/a2p_PointOnLineConstraint.svg', 
             'MenuText': 'Add PointOnLine constraint', 
             'ToolTip': a2p_constraints.PointOnLineConstraint.getToolTip()
             } 

FreeCADGui.addCommand('a2p_PointOnLineConstraintCommand', a2p_PointOnLineConstraintCommand())

#==============================================================================
class a2p_PointOnPlaneConstraintCommand:
    def Activated(self):
        selection = FreeCADGui.Selection.getSelectionEx()
        
        if not a2p_constraints.PointOnPlaneConstraint.isValidSelection(selection):
            msg = '''
                  for Point on Plane constraint select in this order:
                  1.) a vertex or a center of a circle
                  2.) a plane
    
                  Selection made: %s
                  ''' % printSelection(selection)
    
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(), "Incorrect Usage", msg)
            return
        
        c = a2p_constraints.PointOnPlaneConstraint(selection)
        cvp = a2p_constraintDialog.a2p_ConstraintValuePanel(
            c.constraintObject,
            'createConstraint'
            )
        FreeCADGui.Selection.clearSelection()

    def IsActive(self):
        return a2p_constraints.PointOnPlaneConstraint.isValidSelection(
            FreeCADGui.Selection.getSelectionEx()
            )

    def GetResources(self):
        return {
             'Pixmap' : path_a2p + '/icons/a2p_PointOnPlaneConstraint.svg',
             'MenuText': 'Add PointOnPlane constraint',
             'ToolTip': a2p_constraints.PointOnPlaneConstraint.getToolTip()
             }

FreeCADGui.addCommand('a2p_PointOnPlaneConstraintCommand', a2p_PointOnPlaneConstraintCommand())
#==============================================================================
class a2p_SphericalSurfaceConstraintCommand:
    def Activated(self):
        selection = FreeCADGui.Selection.getSelectionEx()
        
        if not a2p_constraints.SphericalConstraint.isValidSelection(selection):
            msg = '''
                  To add a spherical surface constraint select two
                  spherical surfaces (or vertexs),
                  each from a different part.
                  Selection made: %s
                  '''  % printSelection(selection)
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(), "Incorrect Usage", msg)
            return
        
        c = a2p_constraints.SphericalConstraint(selection)
        cvp = a2p_constraintDialog.a2p_ConstraintValuePanel(
            c.constraintObject,
            'createConstraint'
            )
        FreeCADGui.Selection.clearSelection()

    def IsActive(self):
        return a2p_constraints.SphericalConstraint.isValidSelection(
            FreeCADGui.Selection.getSelectionEx()
            )

    def GetResources(self):
        return {
            'Pixmap' : path_a2p + '/icons/a2p_SphericalSurfaceConstraint.svg',
            'MenuText': 'Add a spherical constraint',
             'ToolTip': a2p_constraints.SphericalConstraint.getToolTip()
            }

FreeCADGui.addCommand('a2p_SphericalSurfaceConstraintCommand', a2p_SphericalSurfaceConstraintCommand())
#==============================================================================
class a2p_CircularEdgeConnectionCommand:
    def Activated(self):
        selection = FreeCADGui.Selection.getSelectionEx()
        
        if not a2p_constraints.CircularEdgeConstraint.isValidSelection(selection):
            msg = '''
                 Please select two circular edges from different parts. 
                 But election made is:
                 %s
                 '''  % printSelection(selection)
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(), "Incorrect Usage", msg)
            return
        
        c = a2p_constraints.CircularEdgeConstraint(selection)
        cvp = a2p_constraintDialog.a2p_ConstraintValuePanel(
            c.constraintObject,
            'createConstraint'
            )
        FreeCADGui.Selection.clearSelection()

    def IsActive(self):
        return a2p_constraints.CircularEdgeConstraint.isValidSelection(
            FreeCADGui.Selection.getSelectionEx()
            )

    def GetResources(self):
        return {
            'Pixmap' : path_a2p + '/icons/a2p_CircularEdgeConstraint.svg' ,
            'MenuText': 'Add circular edge connection',
             'ToolTip': a2p_constraints.CircularEdgeConstraint.getToolTip()
            }

FreeCADGui.addCommand('a2p_CircularEdgeConnection', a2p_CircularEdgeConnectionCommand())
#==============================================================================
class a2p_AxialConstraintCommand:
    def Activated(self):
        selection = FreeCADGui.Selection.getSelectionEx()
        
        if not a2p_constraints.AxialConstraint.isValidSelection(selection):
            msg = '''
                  To add an axial constraint select two cylindrical surfaces or two
                  straight lines, each from a different part. Selection made:%s
                  '''  % printSelection(selection)
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(), "Incorrect Usage", msg)
            return
        
        c = a2p_constraints.AxialConstraint(selection)
        cvp = a2p_constraintDialog.a2p_ConstraintValuePanel(
            c.constraintObject,
            'createConstraint'
            )
        FreeCADGui.Selection.clearSelection()

    def IsActive(self):
        return a2p_constraints.AxialConstraint.isValidSelection(
            FreeCADGui.Selection.getSelectionEx()
            )

    def GetResources(self):
        return {
             'Pixmap' : path_a2p + '/icons/a2p_AxialConstraint.svg',
             'MenuText': 'Add axial constraint',
             'ToolTip': a2p_constraints.AxialConstraint.getToolTip()
             }

FreeCADGui.addCommand('a2p_AxialConstraintCommand', a2p_AxialConstraintCommand())
#==============================================================================
class a2p_AxisParallelConstraintCommand:
    def Activated(self):
        selection = FreeCADGui.Selection.getSelectionEx()
        
        if not a2p_constraints.AxisParallelConstraint.isValidSelection(selection):
            msg = '''
                  axisParallelConstraint requires a selection of:
                  - cylinderAxis or linearEdge on a part
                  - cylinderAxis or linearEdge on another part
                  Selection made: %s
                  ''' % printSelection(selection)
    
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(), "Incorrect Usage", msg)
            return
        
        c = a2p_constraints.AxisParallelConstraint(selection)
        cvp = a2p_constraintDialog.a2p_ConstraintValuePanel(
            c.constraintObject,
            'createConstraint'
            )
        FreeCADGui.Selection.clearSelection()

    def IsActive(self):
        return a2p_constraints.AxisParallelConstraint.isValidSelection(
            FreeCADGui.Selection.getSelectionEx()
            )

    def GetResources(self):
        return {
             'Pixmap' : ':/icons/a2p_AxisParallelConstraint.svg',
             'MenuText': 'Add axisParallel constraint',
             'ToolTip': a2p_constraints.AxisParallelConstraint.getToolTip()
             }

FreeCADGui.addCommand('a2p_AxisParallelConstraintCommand', a2p_AxisParallelConstraintCommand())
#==============================================================================
class a2p_AxisPlaneParallelCommand:
    def Activated(self):
        selection = FreeCADGui.Selection.getSelectionEx()
        
        if not a2p_constraints.AxisPlaneParallelConstraint.isValidSelection(selection):
            msg = '''
                  AxisPlaneParallel constraint requires a selection of 
                  1) linear edge or axis of cylinder
                  2) a plane face
                  each on different objects. Selection made:
                  %s
                  '''  % printSelection(selection)
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(), "Incorrect Usage", msg)
            return
        
        c = a2p_constraints.AxisPlaneParallelConstraint(selection)
        cvp = a2p_constraintDialog.a2p_ConstraintValuePanel(
            c.constraintObject,
            'createConstraint'
            )
        FreeCADGui.Selection.clearSelection()

    def IsActive(self):
        return a2p_constraints.AxisPlaneParallelConstraint.isValidSelection(
            FreeCADGui.Selection.getSelectionEx()
            )

    def GetResources(self):
        return {
             'Pixmap' : ':/icons/a2p_AxisPlaneParallelConstraint.svg',
             'MenuText': 'axisPlaneParallel constraint',
             'ToolTip': a2p_constraints.AxisPlaneParallelConstraint.getToolTip()
             }

FreeCADGui.addCommand('a2p_AxisPlaneParallelCommand', a2p_AxisPlaneParallelCommand())
#==============================================================================
class a2p_PlanesParallelConstraintCommand:
    def Activated(self):
        selection = FreeCADGui.Selection.getSelectionEx()
        
        if not a2p_constraints.PlanesParallelConstraint.isValidSelection(selection):
            msg = '''
                  PlanesParallel constraint requires a selection of:
                  - exactly 2 planes on different parts
    
                  Selection made: %s
                  ''' % printSelection(selection)
    
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(), "Incorrect Usage", msg)
            return
        
        c = a2p_constraints.PlanesParallelConstraint(selection)
        cvp = a2p_constraintDialog.a2p_ConstraintValuePanel(
            c.constraintObject,
            'createConstraint'
            )
        FreeCADGui.Selection.clearSelection()
        
    def IsActive(self):
        return a2p_constraints.PlanesParallelConstraint.isValidSelection(
            FreeCADGui.Selection.getSelectionEx()
            )

    def GetResources(self):
        return {
             'Pixmap' : path_a2p + '/icons/a2p_PlanesParallelConstraint.svg',
             'MenuText': 'Add planesParallel constraint',
             'ToolTip': a2p_constraints.PlanesParallelConstraint.getToolTip()
             }

FreeCADGui.addCommand('a2p_PlanesParallelConstraintCommand', a2p_PlanesParallelConstraintCommand())
#==============================================================================
class a2p_PlaneCoincidentConstraintCommand:
    def Activated(self):
        selection = FreeCADGui.Selection.getSelectionEx()
        
        if not a2p_constraints.PlaneConstraint.isValidSelection(selection):
            msg = '''
                  Plane constraint requires a selection of:
                  - exactly 2 planes on different parts
    
                  Selection made: %s
                  ''' % printSelection(selection)
    
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(), "Incorrect Usage", msg)
            return
        
        c = a2p_constraints.PlaneConstraint(selection)
        cvp = a2p_constraintDialog.a2p_ConstraintValuePanel(
            c.constraintObject,
            'createConstraint'
            )
        FreeCADGui.Selection.clearSelection()

    def IsActive(self):
        return a2p_constraints.PlaneConstraint.isValidSelection(
            FreeCADGui.Selection.getSelectionEx()
            )

    def GetResources(self):
        return {
             'Pixmap' : path_a2p + '/icons/a2p_PlaneCoincidentConstraint.svg',
             'MenuText': 'Add plane constraint',
             'ToolTip': a2p_constraints.PlaneConstraint.getToolTip()
             }

FreeCADGui.addCommand('a2p_PlaneCoincidentConstraintCommand', a2p_PlaneCoincidentConstraintCommand())
#==============================================================================
class a2p_AngledPlanesConstraintCommand:
    def Activated(self):
        selection = FreeCADGui.Selection.getSelectionEx()
        
        if not a2p_constraints.AngledPlanesConstraint.isValidSelection(selection):
            msg = '''
                  Angle constraint requires a selection of 2 planes
                  each on different objects. Selection made:
                  %s
                  '''  % printSelection(selection)
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(), "Incorrect Usage", msg)
            return
        
        c = a2p_constraints.AngledPlanesConstraint(selection)
        cvp = a2p_constraintDialog.a2p_ConstraintValuePanel(
            c.constraintObject,
            'createConstraint'
            )
        FreeCADGui.Selection.clearSelection()


    def IsActive(self):
        return a2p_constraints.AngledPlanesConstraint.isValidSelection(
            FreeCADGui.Selection.getSelectionEx()
            )

    def GetResources(self):
        return {
             'Pixmap' : path_a2p + '/icons/a2p_AngleConstraint.svg',
             'MenuText': 'angle between planes constraint',
             'ToolTip': a2p_constraints.AngledPlanesConstraint.getToolTip()
             }

FreeCADGui.addCommand('a2p_AngledPlanesConstraintCommand', a2p_AngledPlanesConstraintCommand())

#==============================================================================