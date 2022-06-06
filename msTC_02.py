#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MetaShape common chain for second part of GCP
    based creation of orthoimages
    @author Marvin Ludwig Chris Reudenbach
    @copyright Copyright 2016-2022, gisma
    @license GPL 3.0
    @version 0.1.0
    @maintainer Chris Reudenbach
    @email creuden@gmail.com"""

import Metashape
from msFunctions.msSparseCloud import *
from msFunctions.msOrtho import *
from msFunctions.msError import *


def Toolchain02():
  orthoRes = Metashape.app.getFloat("Target Resolution of Orthoimage in meter?",value =0.03)  
  ac = Metashape.app.getBool("Process all Chunks?")
  if ac:
    for chunk in Metashape.app.document.chunks:
      
      sparse2ortho(chunk,orthoRes)
      exportOrtho(chunk)
      #exportSeamlines(chunk)
      exportMarker(chunk)
  else:
      chunk = Metashape.app.document.chunk
      
      sparse2ortho(chunk,orthoRes)
      exportOrtho(chunk)
      #exportSeamlines(chunk)
      exportMarker(chunk)


Metashape.app.addMenuItem("Ortho+/BestPractice/Step-4 Orthoimage-post-GCP", Toolchain02)
