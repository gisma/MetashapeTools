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
from msFunctions.msOrtho import *
from msFunctions.msError import *


def Toolchain02():
  ac = Metashape.app.getBool("Process all Chunks?")
  if ac:
    for chunk in Metashape.app.document.chunks:
      minioptimSparsecloud(chunk)
      sparse2ortho(chunk)
      exportOrtho(chunk)
      exportSeamlines(chunk)
      exportMarker(chunk)
  else:
      chunk = Metashape.app.document.chunk
      minioptimSparsecloud(chunk)
      sparse2ortho(chunk)
      exportOrtho(chunk)
      exportSeamlines(chunk)
      exportMarker(chunk)


Metashape.app.addMenuItem("MetashapeTools/Standard Workflows/Toolchain Ortho-2 (postGCP)", Toolchain02)
