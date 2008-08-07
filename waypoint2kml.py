#!/usr/bin/env python
###########################################################################
#                 Converts gpspoint waypoints in to KML
#                         ---------------------
#    Copyright 2006,2007,2008 (C)  Giuseppe "denever" Martino
#    email                : denever@users.berlios.de
###########################################################################
###########################################################################
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 2 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program; if not, write to the Free Software            #
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,             #
#  MA 02110-1301 USA                                                      #
#                                                                         #
###########################################################################

import sys
import re
from elementtree.ElementTree import ElementTree, Element, SubElement, dump, parse

if len(sys.argv) < 3:
   print sys.argv[0] + " inputfile outputfile"
   sys.exit(1)

data = open(sys.argv[1],'r')
kml_root = Element("kml")
kml_root.set("xmlns","http://earth.google.com/kml/2.0")

kml_doc = SubElement(kml_root,"Document")
kml_docname = SubElement(kml_doc,"name")

kml_docname.text = raw_input("Inserire il nome da dare al documento KML: ")

for txtline in data.readlines():
   openlist = re.search('type="waypointlist"', txtline)
   waypoint = re.search('.*name="(?P<name>[^"]+)"\s+altitude="(?P<alt>[^"]+)"\s+latitude="(?P<lat>[^"]+)"\s+longitude="(?P<lon>[^"]+)"', txtline)

   if openlist:
      kml_folder = SubElement(kml_doc,"Folder")
      kml_foldername = SubElement(kml_folder,"name")
      kml_foldername.text = raw_input("Inserire il nome dell'insieme di punti rilevati: ")

   if waypoint:
      kml_placemark = SubElement(kml_folder,"Placemark")
      kml_placemark_desc = SubElement(kml_placemark, "description")
      kml_placemark_desc.text = raw_input("Inserire descrizione per il punto di nome '"+waypoint.group('name')+"': ")
      kml_placemark_name = SubElement(kml_placemark,"name")
      kml_placemark_name.text = waypoint.group('name')
      kml_placemark_point = SubElement(kml_placemark,"Point")
      kml_placemark_extr = SubElement(kml_placemark_point,"extrude")
      kml_placemark_alt = SubElement(kml_placemark_point,"altitudeMode")
      kml_placemark_alt.text = "relativeToGround"
      kml_placemark_coord = SubElement(kml_placemark_point, "coordinates")
      kml_placemark_coord.text = waypoint.group('lon') + "," + waypoint.group('lat') + "," + waypoint.group('alt')

ElementTree(kml_root).write(sys.argv[2])
