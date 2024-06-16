#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MetaShape common chain for 
    creation of orthoimages without GCP
    @author Marvin Ludwig Chris Reudenbach
    @copyright Copyright 2016-2022, gisma
    @license GPL 3.0
    @version 0.1.0
    @maintainer Chris Reudenbach
    @email creuden@gmail.com"""

import Metashape
from msFunctions.msSparseCloud import *
from msFunctions.msOrtho import *
from msFunctions.msExportTiepointError import *
from msFunctions.msError import *
from msFunctions.gradual_selection import *
from msFunctions.msOptimizeSparsecloud import *
from os import path


def toolchain09():
  orthoRes = Metashape.app.getFloat("Target Resolution of Orthoimage in meter?",value =0.05)     
  ac = Metashape.app.getBool("Process all Chunks?")
  spcfilter = Metashape.app.getBool("Use iterative tie point filtering?")
  if ac:
      for chunk in Metashape.app.document.chunks:
          createSparse(chunk)
          if spcfilter:
            gradualselection(chunk)
          sparse2ortho(chunk,orthoRes)
          exportOrtho(chunk)
          #exportSeamlines(chunk)
          exportMarker(chunk)
  else:
      chunk = Metashape.app.document.chunk
      createSparse(chunk)
      if spcfilter:
        gradualselection(chunk)
      sparse2ortho(chunk,orthoRes)
      exportOrtho(chunk)
      #exportSeamlines(chunk)
      exportMarker(chunk)

Metashape.app.addMenuSeparator("Ortho+/BestPractice/------------------------------------------")
Metashape.app.addMenuItem("Ortho+/BestPractice/All-in-one Orthoimage-no-GCP", toolchain09)

