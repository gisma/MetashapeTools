#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""MetaShape tools+
    @author Marvin Ludwig Chris Reudenbach
    @copyright Copyright 2016-2022, gisma
    @license GPL 3.0
    @version 0.1.0
    @maintainer Chris Reudenbach
    @email creuden@gmail.com"""

import Metashape
from msFunctions.msSubsetImages import subsetImages
from msFunctions.msError import exportMarker
from msFunctions.msExportTiepointError import *
from msFunctions.msOptimizeSparsecloud import *
from msFunctions.msReproducibility import *
from msFunctions.msDenseCloud import *
from msFunctions.msSparseCloud import *
from msFunctions.msOrtho import *
from msFunctions.msError import *
from os.path import expanduser
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import os
import sys
import re
import glob
import textwrap
import copy

#goal = sys.argv[1] if len(sys.argv) > 1 else 0
#imgPath = sys.argv[2] if len(sys.argv) > 2 else 0
#projName = sys.argv[3] if len(sys.argv) > 3 else 0
#alignQuality = sys.argv[4] if len(sys.argv) > 4 else 0
#orthoRes =  sys.argv[5] if len(sys.argv) > 5 else 0


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
    

def show_message(msg):
    msgBox = QMessageBox()
    #print(msg)
    msgBox.setText(msg)
    msgBox.exec()
    #menuSubsetImages = menuHelper(subsetImages)


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
    link = "https://github.com/gisma/MetashapeTools"
    msg = "Get more information at the Workflow+: <a href='%s'>GitHub Repository</a>" % link
    show_message(msg)
    
    
def Toolchain03():
    orthoRes = Metashape.app.getFloat("Target Resolution of Orthoimage in meter?",value =0.05)
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


Metashape.app.addMenuSeparator("Workflow+/BestPractice")


Metashape.app.addMenuSeparator("Workflow+/Tools+")   
Metashape.app.addMenuItem("Workflow+/Tools+/Reduce Overlap", menufasteCreateSparse)

Metashape.app.addMenuItem("Workflow+/Tools+/Densecloud", menuDensecloud)
Metashape.app.addMenuItem("Workflow+/Tools+/Orthoimage", Toolchain03)

Metashape.app.addMenuSeparator("Workflow+/Utilities")
Metashape.app.addMenuItem("Workflow+/Utilities/Export Marker Error", menuError)
Metashape.app.addMenuItem("Workflow+/Utilities/Export Tiepoint Error", menuTiepoints)
Metashape.app.addMenuItem("Workflow+/Utilities/Reproducibility", menuReproducibility)

Metashape.app.addMenuItem("Workflow+/Help", helpmsg)








