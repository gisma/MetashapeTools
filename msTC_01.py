#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import Metashape
from msFunctions.msSparseCloud import *
from msFunctions.msExportTiepointError import *


def Toolchain01():
    
    ac = Metashape.app.getBool("Process all Chunks?")
    
    if ac:
        for chunk in Metashape.app.document.chunks:
            fastCreateSparse(chunk)
            createSparse(chunk)
    else:
        chunk = Metashape.app.document.chunk
        fastCreateSparse(chunk)
        createSparse(chunk)


Metashape.app.addMenuItem("MetashapeTools/Standard Workflows/Toolchain Part 1", Toolchain01)
