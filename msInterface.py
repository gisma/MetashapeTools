#!/usr/bin/env python3
# -*- coding: utf-8 -*- 


import Metashape
from msFunctions.msSubsetImages import subsetImages
from msFunctions.msError import exportMarker
from msFunctions.msExportTiepointError import *
from msFunctions.msOptimizeSparsecloud import *
from msFunctions.msReproducibility import *
from msFunctions.msDenseCloud import *
import textwrap
from msFunctions.msSparseCloud import *
from msFunctions.msOrtho import *
from msFunctions.msError import *
import os
import sys
import re
import glob
from os.path import expanduser

goal = sys.argv[1] if len(sys.argv) > 1 else 0
imgPath = sys.argv[2] if len(sys.argv) > 2 else 0
projName = sys.argv[3] if len(sys.argv) > 3 else 0
alignQuality = sys.argv[4] if len(sys.argv) > 4 else 0
orthoRes =  sys.argv[5] if len(sys.argv) > 5 else 0


# helper for optional all chunk processing:
def menuHelper(fun):
    def menuFunc():
        ac = Metashape.app.getBool("Process all chunks?")
        if ac:
            for chunk in Metashape.app.document.chunks:
                fun(chunk)
        else:
            fun(chunk)
    return menuFunc
    


menuSubsetImages = menuHelper(subsetImages)


def menuError():
    ac = Metashape.app.getBool("Process all chunks?")
    if ac:
        for chunk in Metashape.app.document.chunks:
            exportMarker(chunk)
    else:
        exportMarker(chunk)
    


def menuTiepoints():
    ac = Metashape.app.getBool("Process all chunks?")
    if ac:
        for chunk in Metashape.app.document.chunks:
            ExportTiepointError(chunk)
    else:
        ExportTiepointError(chunk)


def menuDensecloud():
    ac = Metashape.app.getBool("Process all chunks?")
    if ac:
        for chunk in Metashape.app.document.chunks:
            createDenseCloud(chunk)
    else:
        createDenseCloud(chunk)

def menufasteCreateSparse():
    chunk = Metashape.app.document.chunk
    fastCreateSparse(chunk)


def menuOptimizeSparsecloud():
    chunk = Metashape.app.document.chunk
    optimizeSparsecloud(chunk)



def menuReproducibility():
    RE = Metashape.app.getFloat(label = "Optimal Reprojection Error", value = 0)
    k = Metashape.app.getInt(label = "Times", value = 5)
    
    repro(chunk, RE = RE, k = k)

def helpmsg():
    message = "More information at: \                  https://github.com/gisma/MetashapeTools"
    Metashape.app.messageBox(textwrap.fill(message, 40,drop_whitespace=False))
    
def Toolchain03(orthoRes=0.025):
  ac = Metashape.app.getBool("Process all Chunks?")
  if ac:
    for chunk in Metashape.app.document.chunks:
      sparse2ortho(chunk,orthoRes)
      exportOrtho(chunk)
      #exportSeamlines(chunk)
      exportMarker(chunk,orthoRes)
  else:
      chunk = Metashape.app.document.chunk
      sparse2ortho(chunk,orthoRes)
      exportOrtho(chunk)
      #exportSeamlines(chunk)
      exportMarker(chunk)

   
Metashape.app.addMenuItem("MetashapeTools/Reduce Overlap", menufasteCreateSparse)
# Metashape.app.addMenuItem("MetashapeTools/Subset Images", menuSubsetImages)
Metashape.app.addMenuItem("MetashapeTools/Optimize Sparsecloud", menuOptimizeSparsecloud)
Metashape.app.addMenuItem("MetashapeTools/Densecloud", menuDensecloud)
Metashape.app.addMenuItem("MetashapeTools/Orthoimage", Toolchain03)

Metashape.app.addMenuSeparator("MetashapeTools/Utilities")

Metashape.app.addMenuItem("MetashapeTools/Utilities/Export Marker Error", menuError)
Metashape.app.addMenuItem("MetashapeTools/Utilities/Export Tiepoint Error", menuTiepoints)
Metashape.app.addMenuItem("MetashapeTools/Utilities/Reproducibility", menuReproducibility)

Metashape.app.addMenuSeparator("MetashapeTools/Standard Workflows")

Metashape.app.addMenuItem("MetashapeTools/Help", helpmsg)








