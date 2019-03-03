#***************************************************************************
#*                                                                         *
#*   Copyright (c) 2019 kbwbe                                              *
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



class LCS_Group(object):
    def __init__(self, selfobj):
        selfobj.addExtension('App::GeoFeatureGroupExtensionPython', self)     
        
class VP_LCS_Group(object):
    def __init__(self,vobj):
        vobj.addExtension('Gui::ViewProviderGeoFeatureGroupExtensionPython', self)
        vobj.Proxy = self

    def attach(self, vobj):
        self.ViewObject = vobj
        self.Object = vobj.Object

    def __getstate__(self):
        return None

    def __setstate__(self,state):
        return None


def getListOfLCS(targetDoc,sourceDoc):
    lcsOut = []
    for sourceOb in sourceDoc.Objects:
        if (
                sourceOb.Name.startswith("Local_CS") or
                sourceOb.Name.startswith("App__Placement") or
                sourceOb.Name.startswith("a2pLCS") or
                sourceOb.Name.startswith("PartDesign__CoordinateSystem")
                ):
            newLCS = targetDoc.addObject("PartDesign::CoordinateSystem","a2pLCS")
            pl = sourceOb.getGlobalPlacement()
            newLCS.Placement = pl
            lcsOut.append(newLCS)
    return lcsOut
