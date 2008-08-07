#!/usr/bin/env python
###########################################################################
#                 Converts gpspoint trackpoints in to KML
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

kml_folder = SubElement(kml_doc,"Folder")
kml_foldername = SubElement(kml_folder,"name")
kml_foldername.text = raw_input("Inserire il nome dell'insieme di punti rilevati: ")
coordinates = str()
for txtline in data.readlines():
   trackopen = re.search('type="track" name="(?P<name>[^"]+)"', txtline)
   trackpoint = re.search('type="trackpoint"\s+altitude="(?P<alt>[^"]+)"\s+latitude="(?P<lat>[^"]+)"\s+longitude="(?P<lon>[^"]+)"', txtline)
   trackend = re.search('type="trackend"', txtline)
   
   if trackopen:
      kml_placemark = SubElement(kml_folder,"Placemark")
      kml_placemark_desc = SubElement(kml_placemark, "description")
      kml_placemark_desc.text = raw_input("Inserire descrizione per il percorso di nome '"+trackopen.group('name')+"': ")
      kml_placemark_name = SubElement(kml_placemark,"name")
      kml_placemark_name.text = trackopen.group('name')
      kml_placemark_vis = SubElement(kml_placemark,"visibility")
      kml_placemark_vis.text = "1"
      kml_placemark_open = SubElement(kml_placemark,"open")
      kml_placemark_open.text = "0"
      kml_placemark_style = SubElement(kml_placemark,"Style")
      kml_placemark_linestyle = SubElement(kml_placemark_style, "LineStyle")
      kml_placemark_linecolor = SubElement(kml_placemark_linestyle, "color")
      kml_placemark_linecolor.text = "ff00ffff"
      kml_placemark_polystyle = SubElement(kml_placemark_style, "PolyStyle")
      kml_placemark_polycolor = SubElement(kml_placemark_polystyle, "color")
      kml_placemark_polycolor.text = "7f00ff00"
      kml_placemark_linestring = SubElement(kml_placemark, "LineString")
      kml_placemark_lineextrude = SubElement(kml_placemark_linestring, "extrude")
      kml_placemark_lineextrude.text = "1"
      kml_placemark_linetesselate = SubElement(kml_placemark_linestring, "tesselate")
      kml_placemark_linetesselate.text = "1"
      kml_placemark_linealtmod = SubElement(kml_placemark_linestring, "altitudeMode")
      kml_placemark_linealtmod.text = "relativeToGround"
      kml_placemark_linecoord = SubElement(kml_placemark_linestring, "coordinates")

   if trackpoint:
      lon = trackpoint.group('lon')
      lat = trackpoint.group('lat')
      alt = trackpoint.group('alt')
      coordinates = coordinates + lon + "," + lat + "," + alt + "\n"

   if trackend:
      kml_placemark_linecoord.text = coordinates
      coordinates = str()

ElementTree(kml_root).write(sys.argv[2])
