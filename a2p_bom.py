#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2018 kbwbe                                              *
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

import FreeCADGui,FreeCAD
from PySide import QtGui, QtCore
import Spreadsheet
import os

import a2plib
from a2p_fcdocumentreader import FCdocumentReader
from a2p_partlistglobals import PARTLIST_COLUMN_NAMES


#------------------------------------------------------------------------------
def createPartList(
        importPath,
        parentAssemblyDir,
        partListEntries,
        recursive=False
        ):
    '''
    Extract quantities and descriptions of assembled parts from
    document.xml
    Is able to analyse subassemblies by recursion
    '''
    fileNameInProject = a2plib.findSourceFileInProject(
        importPath,
        parentAssemblyDir
        )
    workingDir,basicFileName = os.path.split(fileNameInProject)
    docReader1 = FCdocumentReader()
    docReader1.openDocument(fileNameInProject)
    for ob in docReader1.getA2pObjects():
        print(u'{}, Subassembly? = {}'.format(ob,ob.isSubassembly()))
        if ob.isSubassembly() and recursive:
            partListEntries = createPartList(
                                        ob.getA2pSource(),
                                        workingDir,
                                        partListEntries,
                                        recursive
                                        )
        if not ob.isSubassembly() or not recursive:
            # Try to get spreadsheetdata _PARTINFO_ from linked source
            linkedSource = ob.getA2pSource()
            linkedSource = a2plib.findSourceFileInProject(
                            linkedSource,
                            workingDir
                            ) 
            docReader2 = FCdocumentReader()
            docReader2.openDocument(linkedSource)
            print (linkedSource)
            # Initialize a default parts information...
            partInformation = []
            for i in range(0,len(PARTLIST_COLUMN_NAMES)):
                partInformation.append("*")
            # if there is a proper spreadsheat, then read it...
            for ob in docReader2.getSpreadsheetObjects():
                if ob.name == '_PARTINFO_':
                    cells = ob.getCells()
                    for addr in cells.keys():
                        if addr[:1] == 'B': #column B contains the information
                            idx = int(addr[1:])-1
                            if idx < len(PARTLIST_COLUMN_NAMES): # don't read further!
                                partInformation[idx] = cells[addr]
            # put information to dict and count usage of sourcefiles..
            entry = partListEntries.get(linkedSource,None)
            if entry == None:
                partListEntries[linkedSource] = [
                    1,
                    partInformation
                    ]
            else:
                partListEntries.get(linkedSource)[0]+=1 #count sourcefile usage
                
    return partListEntries
                




#------------------------------------------------------------------------------
class a2p_CreatePartlist():

    def Activated(self):
        doc = FreeCAD.activeDocument()
        if doc == None:
            QtGui.QMessageBox.information(  QtGui.QApplication.activeWindow(),
                                        "No active document found!",
                                        "You have to open an fcstd file first."
                                    )
            return
        completeFilePath = doc.FileName
        p,f = os.path.split(completeFilePath)
        
        partListEntries = createPartList(
            doc.FileName,
            p,
            {},
            recursive=True
            )
        
        for k in partListEntries.keys():
            print partListEntries[k]
        

    def GetResources(self):
        return {
            'Pixmap'  :     a2plib.pathOfModule()+'/icons/a2p_partsList.svg',
            'MenuText':     'create a spreadsheet with a partlist of this file',
            'ToolTip':      'create a spreadsheet with a partlist of this file'
            }
        
FreeCADGui.addCommand('a2p_CreatePartlist', a2p_CreatePartlist())
#------------------------------------------------------------------------------

















