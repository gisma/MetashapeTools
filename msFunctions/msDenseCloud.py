#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MetaShape common tool for dense cloud building
    and filtering
    @author Marvin Ludwig Chris Reudenbach
    @copyright Copyright 2016-2022, gisma
    @license GPL 3.0
    @version 0.1.0
    @maintainer Chris Reudenbach
    @email creuden@gmail.com"""

# import markers

import Metashape




def createDenseCloud(chunk):
    
    # build depth maps with moderate filter
    chunk.buildDepthMaps(downscale = 4, filter_mode = Metashape.FilterMode.ModerateFiltering)
    # build dense cloud
    chunk.buildPointloud(point_colors=True, keep_depth=True, point_confidence = True)
    # export
    outpath = Metashape.app.document.path[:-4]
    chunk.exportPoints(path = str(outpath + "_" + str(chunk.label) + "_densecloud.laz"), sourceData = Metashape.DataSource.PointCloudData, save_colors = True, save_confidence = True)
    

