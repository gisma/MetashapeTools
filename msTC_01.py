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
def menuOptimizeSparsecloud():
    chunk = Metashape.app.document.chunk
    optimizeSparsecloud(chunk)


def helpGCP():
    link = "https://agisoft.freshdesk.com/support/solutions/articles/31000153696-aerial-data-processing-with-gcps-orthomosaic-dem-generation"
    msg = "Get more information for the GCP Integration at: <a href='%s'>Metashape Arial data Processing with GCPs</a>" % link
    show_message(msg)    

Metashape.app.addMenuItem("Ortho+/BestPractice/ForestOrtho/Step-2 Add and Place GCP ...", helpGCP)




Metashape.app.addMenuItem("Ortho+/BestPractice/ForestOrtho/Step-3 Optimize Sparsecloud", menuOptimizeSparsecloud)
