#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MetaShape common chain for first part of GCP
    based creation of orthoimages
    @author Marvin Ludwig Chris Reudenbach
    @copyright Copyright 2016-2022, gisma
    @license GPL 3.0
    @version 0.1.0
    @maintainer Chris Reudenbach
    @email creuden@gmail.com"""

import Metashape
from msFunctions.msSparseCloud import *
from msFunctions.msExportTiepointError import *

def Toolchain01():
    
    ac = Metashape.app.getBool("Process all Chunks?")
    fcsc = Metashape.app.getBool("Process Reduce overlap?")
    if ac:

        for chunk in Metashape.app.document.chunks:
            if fcsc:
                overl = Metashape.app.getFloat("Overlap Number?",value = 8.0)  
                fastCreateSparse(chunk,overl = overl)
        createSparse(chunk)
    else:
        chunk = Metashape.app.document.chunk
        if fcsc:
            overl = Metashape.app.getFloat("Overlap Number?",value = 8.0)
            fastCreateSparse(chunk,overl = overl)
#            fastCreateSparse(chunk,overl = overl)
        createSparse(chunk)


Metashape.app.addMenuItem("Ortho+/BestPractice/ForestOrtho/Step-1 Orthoimage-pre-GCP", Toolchain01)
