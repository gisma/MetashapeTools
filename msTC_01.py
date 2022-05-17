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
    overl = 8
    if ac:

        for chunk in Metashape.app.document.chunks:
            fastCreateSparse(chunk,overl = overl)
            createSparse(chunk)
    else:

        chunk = Metashape.app.document.chunk
        fastCreateSparse(chunk,overl = overl)
        createSparse(chunk)


Metashape.app.addMenuItem("Workflow+/BestPractice/Orthoimage-pre-GCP", Toolchain01)
