 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  13 2020

@author: marvin
"""

import Metashape


def exportMarker(chunk, doc = Metashape.app.document):
	current_doc = Metashape.app.document.path
	outpathr = str(path.dirname(current_doc) +  "/report/" )
	
    chunk.exportReference(path = str(outpath  + str(chunk.label) + "_marker_error.txt"),
	 format = Metashape.ReferenceFormatCSV, items = Metashape.ReferenceItemsMarkers, columns = "noxyzXYZuvwUVW", delimiter = ",")
	
	

