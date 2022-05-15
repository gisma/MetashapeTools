#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""
Created on 2022-05-16

@author: chris 

"""

import Metashape
from msFunctions.msSparseCloud import *
from msFunctions.msExportTiepointError import *


def Toolchain09():
  ac = Metashape.app.getBool("Process all Chunks?")
  if ac:
      for chunk in Metashape.app.document.chunks:
          createSparse(chunk)
          optimizeSparsecloud(chunk)
          sparse2ortho(chunk)
          exportOrtho(chunk)
          exportSeamlines(chunk)
          exportMarker(chunk)
  else:
      chunk = Metashape.app.document.chunk
      createSparse(chunk)
      optimizeSparsecloud(chunk)
      sparse2ortho(chunk)
      exportOrtho(chunk)
      exportSeamlines(chunk)
      exportMarker(chunk)

Metashape.app.addMenuItem("MetashapeTools/Standard Workflows/Toolchain Ortho-noGCP", Toolchain09)
