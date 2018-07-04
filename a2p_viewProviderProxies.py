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
from PySide import QtGui, QtCore
from pivy import coin
import traceback

def group_constraints_under_parts():
    return True

def allow_deletetion_when_activice_doc_ne_object_doc():
    return False

class ImportedPartViewProviderProxy:   
    
    def claimChildren(self):
        if hasattr(self,'Object'):
            return self.Object.InList
        else:
            return []
    
    def onDelete(self, viewObject, subelements): # subelements is a tuple of strings
        if FreeCAD.activeDocument() != viewObject.Object.Document:
            return False # only delete objects in the active Document anytime !!
        
        obj = viewObject.Object
        doc = obj.Document
        
        deleteList = []
        for c in doc.Objects:
            if 'ConstraintInfo' in c.Content: # a related Constraint
                if obj.Name in [ c.Object1, c.Object2 ]:
                    deleteList.append(c)
            if 'ConstraintNfo' in c.Content: # a related mirror-Constraint
                if obj.Name in [ c.Object1, c.Object2 ]:
                    deleteList.append(c)
                    
        if len(deleteList) > 0:
            for c in deleteList:
                doc.removeObject(c.Name)
                
        return True # If False is returned the object won't be deleted

    def __getstate__(self):
        return None

    def __setstate__(self, state):
        return None
    
    def attach(self, vobj):
        self.object_Name = vobj.Object.Name
        self.Object = vobj.Object

    def setupContextMenu(self, ViewObject, popup_menu):
        pass

class PopUpMenuItem:
    def __init__( self, proxy, menu, label, Freecad_cmd ):
        self.Object = proxy.Object
        self.Freecad_cmd =  Freecad_cmd
        action = menu.addAction(label)
        action.triggered.connect( self.execute )
        proxy.pop_up_menu_items.append( self )
    def execute( self ):
        try:
            FreeCADGui.runCommand( self.Freecad_cmd )
        except:
            FreeCAD.Console.PrintError( traceback.format_exc() )


class ConstraintViewProviderProxy:
    def __init__( 
            self, 
            constraintObj, 
            iconPath, 
            createMirror=True, 
            origLabel = '', 
            mirrorLabel = '', 
            extraLabel = '' 
            ):
        self.iconPath = iconPath
        self.constraintObj_name = constraintObj.Name
        constraintObj.purgeTouched()
        if createMirror:
            self.mirror_name = create_constraint_mirror(
                constraintObj, 
                iconPath, 
                origLabel, 
                mirrorLabel, 
                extraLabel 
                )
        
    def getIcon(self):
        return self.iconPath
        
    def attach(self, vobj): #attach to what document?
        vobj.addDisplayMode( coin.SoGroup(),"Standard" )

    def getDisplayModes(self,obj):
        return ["Standard"]

    def getDefaultDisplayMode(self):
        return "Standard"

    def onDelete(self, viewObject, subelements): # subelements is a tuple of strings
        if FreeCAD.activeDocument() != viewObject.Object.Document:
            return False

        obj = viewObject.Object
        doc = obj.Document
        if isinstance( obj.Proxy, ConstraintMirrorObjectProxy ):
            try:
                doc.removeObject(  obj.Proxy.constraintObj_name ) # also delete the original constraint which obj mirrors
            except:
                pass # bloede Fehlermeldung weg, wenn Original fehlt! (Klaus)
        elif hasattr( obj.Proxy, 'mirror_name'): # the original constraint, #isinstance( obj.Proxy,  ConstraintObjectProxy ) not done since ConstraintObjectProxy not defined in namespace 
            doc.removeObject( obj.Proxy.mirror_name ) # also delete mirror
        return True


class ConstraintMirrorViewProviderProxy( ConstraintViewProviderProxy ):
    def __init__( self, constraintObj, iconPath ):
        self.iconPath = iconPath
        self.constraintObj_name = constraintObj.Name
    def attach(self, vobj):
        vobj.addDisplayMode( coin.SoGroup(),"Standard" )


def create_constraint_mirror( constraintObj, iconPath, origLabel= '', mirrorLabel='', extraLabel = '' ):
    #FreeCAD.Console.PrintMessage("creating constraint mirror\n")
    cName = constraintObj.Name + '_mirror'
    cMirror =  constraintObj.Document.addObject("App::FeaturePython", cName)
    if origLabel == '':
        cMirror.Label = constraintObj.Label + '_'
    else:
        cMirror.Label = constraintObj.Label + '__' + mirrorLabel
        constraintObj.Label = constraintObj.Label + '__' + origLabel
        if extraLabel != '':
            cMirror.Label += '__' + extraLabel
            constraintObj.Label += '__' + extraLabel
            
    for pName in constraintObj.PropertiesList:
        if pName == "ParentTreeObject": continue #causes problems with fc0.16
        if constraintObj.getGroupOfProperty( pName ) == 'ConstraintInfo':
            #if constraintObj.getTypeIdOfProperty( pName ) == 'App::PropertyEnumeration':
            #    continue #App::Enumeration::contains(const char*) const: Assertion `_EnumArray' failed.
            cMirror.addProperty(
                constraintObj.getTypeIdOfProperty( pName ),
                pName,
                "ConstraintNfo" #instead of ConstraintInfo, as to not confuse the assembly2sovler
                )
            if pName == 'directionConstraint':
                v =  constraintObj.directionConstraint
                if v != "none": #then updating a document with mirrors
                    cMirror.directionConstraint =  ["aligned","opposed"]
                    cMirror.directionConstraint = v
                else:
                    cMirror.directionConstraint =  ["none","aligned","opposed"]
            else:
                setattr( cMirror, pName, getattr( constraintObj, pName) )
            if constraintObj.getEditorMode(pName) == ['ReadOnly']:
                cMirror.setEditorMode( pName, 1 )
                
    cMirror.addProperty("App::PropertyLink","ParentTreeObject","ConstraintNfo") # this was not copied because fc0.16
    parent = FreeCAD.ActiveDocument.getObject(constraintObj.Object2)
    cMirror.ParentTreeObject = parent
    cMirror.setEditorMode('ParentTreeObject',1)
    parent.Label = parent.Label # this is needed to trigger an update
                
    ConstraintMirrorObjectProxy( cMirror, constraintObj )
    cMirror.ViewObject.Proxy = ConstraintMirrorViewProviderProxy( constraintObj, iconPath )
    return cMirror.Name
 
class ConstraintObjectProxy:
    def execute(self, obj):
        self.callSolveConstraints()
            
    def onChanged(self, obj, prop):
        if hasattr(self, 'mirror_name'):
            cMirror = obj.Document.getObject( self.mirror_name )
            if cMirror == None: return #catch issues during deleting...
            if cMirror.Proxy == None:
                return #this occurs during document loading ...
            if obj.getGroupOfProperty( prop ) == 'ConstraintInfo':
                cMirror.Proxy.disable_onChanged = True
                setattr( cMirror, prop, getattr( obj, prop) )
                cMirror.Proxy.disable_onChanged = False

    def reduceDirectionChoices( self, obj, value):
        if hasattr(self, 'mirror_name'):
            cMirror = obj.Document.getObject( self.mirror_name )
            cMirror.directionConstraint = ["aligned","opposed"] #value should be updated in onChanged call due to assignment in 2 lines
        obj.directionConstraint = ["aligned","opposed"]
        obj.directionConstraint = value
        
    def callSolveConstraints(self):
        from solversystem import autoSolveConstraints
        autoSolveConstraints( FreeCAD.activeDocument(), cache = None )
 
 
class ConstraintMirrorObjectProxy:
    def __init__(self, obj, constraintObj ):
        self.constraintObj_name = constraintObj.Name
        constraintObj.Proxy.mirror_name = obj.Name
        self.disable_onChanged = False
        obj.Proxy = self
        
    def execute(self, obj):
        return #no work required in onChanged causes touched in original constraint ...

    def onChanged(self, obj, prop):
        '''
        is triggered by Python code!
        And on document loading...
        '''
        #FreeCAD.Console.PrintMessage("%s.%s property changed\n" % (obj.Name, prop))
        if getattr( self, 'disable_onChanged', True):
            return 
        if obj.getGroupOfProperty( prop ) == 'ConstraintNfo':
            if hasattr( self, 'constraintObj_name' ):
                constraintObj = obj.Document.getObject( self.constraintObj_name )
                try:
                    if getattr(constraintObj, prop) != getattr( obj, prop):
                        setattr( constraintObj, prop, getattr( obj, prop) )
                except AttributeError, msg:
                    pass #loading issues...









































