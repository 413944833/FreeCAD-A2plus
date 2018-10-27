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

import FreeCAD, FreeCADGui
import a2plib

import zipfile
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
    
import os

#------------------------------------------------------------------------------
# Small helper funcs
#------------------------------------------------------------------------------
def printElement(elem):
    print(
        "tag: {}, attributes: {}".format(
            elem.tag,
            elem.attrib
            )
        )
    

#------------------------------------------------------------------------------
class A2p_xmldoc_Property(object):
    '''
    BaseClass for xml-Properties
    '''
    def __init__(self,name,_type):
        self.name = name
        self.type = _type
        print(self)
        
    def __str__(self):
        return "PropertyName: {}, Type: {}".format(self.name,self.type)
    

#------------------------------------------------------------------------------
class A2p_xmldoc_Object(object):
    '''
    class prototype to store FC objects found in document.xml
    '''
    def __init__(self,name,_type):
        self.name = name
        self.type = _type
        self.propertyList = []
        print(self)
        
    def __str__(self):
        return "ObjName: {}, Type: {}".format(self.name,self.type)
    
    def loadPropertyList(self,tree):
        for elem in tree.iterfind('ObjectData/Object'):
            if elem.attrib['name'] == self.name:
                for e in elem.findall('Properties/Property'):
                    p = A2p_xmldoc_Property(
                        e.attrib['name'],
                        e.attrib['type']
                        )
                    self.propertyList.append(p)
                    
    
    def loadObjectData(self,tree):
        raise NotImplementedError(
            "xml-ojbect class {} doesn't allow loadObjectData, use inherited classes instead!".format(
                self.__class__.__name__)
            )
        
#------------------------------------------------------------------------------
class A2p_xmldoc_SpreadSheet(A2p_xmldoc_Object):
    def loadObjectData(self,tree):
        '''
        Extract Spreadsheed data from fcstd xml document
        '''
        self.loadPropertyList(tree)

#------------------------------------------------------------------------------
class FCdocumentReader(object):
    '''
    class for extracting the XML-Documentdata from a fcstd-file given by
    filepath. Some data can be extracted without opening the whole document
    within FreeCAD
    '''
    def __init__(self):
        self.realPath = ''
        self.tree = None
        self.root = None
        self.objects = []
        
    def clear(self):
        self.realPath = ''
        self.tree = None
        self.root = None
        self.objects = []
        
    def openDocument(self,fileName, assemblyPath):
        self.clear()
        # Handler abs/rel pathes and projectFiles
        fn = a2plib.findSourceFileInProject(fileName, assemblyPath)
        if fn == None or fn == "":
            print(u"Could not open xml from: {} !".format(
                    fileName
                    )
                  )
            return False
        #
        # decompress the file
        self.realPath = fn
        f = zipfile.ZipFile(fn, 'r')
        xml = f.read('Document.xml')
        f.close()
        #
        # load the ElementTree
        self.tree = ET.ElementTree(ET.fromstring(xml))
        self.root = self.tree.getroot()
        #
        self.loadObjects()
        return True
    
    def loadObjects(self):
        self.objects = []
        for elem in self.tree.iterfind('Objects/Object'):
        #for elem in self.root.findall('Objects/Object'):
            if elem.attrib['type'].startswith('Spreadsheet'): 
                ob = A2p_xmldoc_SpreadSheet(
                        elem.attrib['name'],
                        elem.attrib['type']
                        )
                self.objects.append(ob)
                ob.loadObjectData(self.tree)
            else:
                pass # unhandled object types
#------------------------------------------------------------------------------

        
        
if __name__ == "__main__":
    doc = FreeCAD.activeDocument() 
    fname = doc.FileName
    dr = FCdocumentReader()
    assemblyPath = os.path.split(fname)[0]
    dr.openDocument(fname, assemblyPath)       

























