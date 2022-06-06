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


Metashape.app.addMenuSeparator("Ortho+/BestPractice/Step-2 Add and Place GCP ...")
Metashape.app.addMenuItem("Ortho+/BestPractice/Step-3 Optimize Sparsecloud", menuOptimizeSparsecloud)
