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

import FreeCAD, FreeCADGui
from a2plib import *
import Part
import os, numpy
from random import random, choice
from FreeCAD import  Base
import time
from a2p_toponamer import TopoNamer
import a2plib
from PySide import QtGui


class Proxy_muxAssemblyObj:
    def execute(self, shape):
        pass

def createTopoInfo(obj): #the new way with topoNames !!!
    tn = TopoNamer(obj)
    topoInfo = tn.executeNaming()
    return topoInfo

def muxObjectsWithKeys(doc, withColor=False):
    '''
    combines all the imported shape object in doc into one shape
    and creates an entry in stringlist called muxinfo with a description of an edge or face.
    these descriptions are used later to retrieve the edges or faces...
    '''
    
    faces = []
    faceColors = []
    muxInfo = [] # Liste der keys...
    
    objects = doc.Objects
        
    visibleObjects = [ obj for obj in doc.Objects
                       if hasattr(obj,'ViewObject') and obj.ViewObject.isVisible()
                       and hasattr(obj,'Shape') and len(obj.Shape.Faces) > 0 and 'Body' not in obj.Name]
    
    if len(visibleObjects) > 1:
        suppressInvisibleObjects = True
    else:
        suppressInvisibleObjects = False

    for obj in objects:
        if 'importPart' in obj.Content:
            
            if suppressInvisibleObjects:
                if not obj.ViewObject.isVisible():
                    continue
            
            t1 = time.time()
            extendNames = False 
            if hasattr(obj, 'muxInfo') and len(obj.muxInfo) > 0: # Subelement-Strings existieren schon...
                extendNames = True
                #
                edgeNames = []
                faceNames = []
                
                for item in obj.muxInfo:
                    if item[:4] == 'EDGE':
                        edgeNames.append(item)
                    if item[:4] == 'FACE':
                        faceNames.append(item)
                        
            for i, edge in enumerate(obj.Shape.Edges):
                if extendNames:
                    newName = "".join((edgeNames[i],'#',obj.Name))
                    muxInfo.append(newName)
                else:
                    newName = "".join(('EDGE#',str(i),'#',obj.Name))
                    muxInfo.append(newName)
                    
            # Save Computing time, store this before the for..enumerate loop later...
            colorFlag = ( len(obj.ViewObject.DiffuseColor) < len(obj.Shape.Faces) )
            shapeCol = obj.ViewObject.ShapeColor
            diffuseCol = obj.ViewObject.DiffuseColor
            
            # now start the loop with use of the stored values..(much faster)
            for i, face in enumerate(obj.Shape.Faces):
                faces.append(face)
                
                if withColor:
                    if colorFlag:
                        faceColors.append(shapeCol)
                    else:
                        faceColors.append(diffuseCol[i])

                if extendNames:
                    newName = "".join((faceNames[i],'#',obj.Name))
                    muxInfo.append(newName)
                else:
                    newName = "".join(('FACE#',str(i),'#',obj.Name))
                    muxInfo.append(newName)

    shell = Part.makeShell(faces)
    if withColor:    
        return muxInfo, shell, faceColors
    else:
        return muxInfo, shell



def muxObjects(doc, mode=0):
    'combines all the imported shape object in doc into one shape'
    faces = []
    if mode == 1:
        objects = doc.getSelection()
    else:
        objects = doc.Objects

    for obj in objects:
        if 'importPart' in obj.Content:
            faces = faces + obj.Shape.Faces
    shell = Part.makeShell(faces)
    return shell



class SimpleAssemblyShape:
    def __init__(self, obj):
        obj.addProperty("App::PropertyString", "type").type = 'SimpleAssemblyShape'
        obj.addProperty("App::PropertyFloat", "timeOfGenerating").timeOfGenerating = time.time()
        obj.Proxy = self
        
    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        pass


class ViewProviderSimpleAssemblyShape:
    def __init__(self,obj):
        obj.Proxy = self

    def onDelete(self, viewObject, subelements):
        #return False # Dont delete PartInformation !
        return True
        
    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
    
    def getIcon(self):
        return a2plib.path_a2p + '/icons/simpleAssemblyShape.svg'
    
    def attach(self, obj):
        self.object_Name = obj.Object.Name
        self.Object = obj.Object
        
    def getDisplayModes(self,obj):
        "Return a list of display modes."
        modes=[]
        modes.append("Shaded")
        modes.append("Wireframe")
        modes.append("Flat Lines")
        return modes
    
    def getDefaultDisplayMode(self):
        "Return the name of the default display mode. It must be defined in getDisplayModes."
        return "Flat Lines"
    
    def setDisplayMode(self,mode):
        return mode
        

def createOrUpdateSimpleAssemblyShape(doc):
    visibleImportObjects = [ obj for obj in doc.Objects
                           if 'importPart' in obj.Content
                           and hasattr(obj,'ViewObject') 
                           and obj.ViewObject.isVisible()
                           and hasattr(obj,'Shape') 
                           and len(obj.Shape.Faces) > 0 
                           ]
    
    if len(visibleImportObjects) == 0:
        QtGui.QMessageBox.critical(  QtGui.QApplication.activeWindow(), 
                                     "Cannot create SimpleAssemblyShape", 
                                     "No visible ImportParts found" 
                                   )
        return
        
    sas = doc.getObject('SimpleAssemblyShape')    
    if sas == None:
        sas = doc.addObject("Part::FeaturePython","SimpleAssemblyShape")
        SimpleAssemblyShape(sas)
        #sas.ViewObject.Proxy = 0
        ViewProviderSimpleAssemblyShape(sas.ViewObject)
    faces = []

    for obj in visibleImportObjects:
        faces = faces + obj.Shape.Faces
    shell = Part.makeShell(faces)
    sas.Shape = shell
    sas.ViewObject.Visibility = False


class a2p_SimpleAssemblyShapeCommand():

    def GetResources(self):
        import a2plib
        return {'Pixmap'  : a2plib.path_a2p +'/icons/a2p_simpleAssemblyShape.svg', 
                'MenuText': "create or refresh simple Shape of complete Assembly",
                'ToolTip': "create or refresh simple Shape of complete Assembly"
                }

    def Activated(self):
        if FreeCAD.ActiveDocument == None: return
        doc = FreeCAD.ActiveDocument
        createOrUpdateSimpleAssemblyShape(doc)
        doc.recompute()

    def IsActive(self):
        return True
    
FreeCADGui.addCommand('a2p_SimpleAssemblyShapeCommand',a2p_SimpleAssemblyShapeCommand()) 




















































