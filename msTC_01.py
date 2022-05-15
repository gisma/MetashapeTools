#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 10:00:09 2019

@author: marvin

update: chris 2022-05-16

"""

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


Metashape.app.addMenuItem("MetashapeTools/Standard Workflows/Toolchain Ortho-1 (preGCP)", Toolchain01)
