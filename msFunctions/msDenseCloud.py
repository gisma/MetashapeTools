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
    chunk.buildPointCloud(point_colors=True, keep_depth=True, point_confidence = True)
    # export
    current_doc = Metashape.app.document.path
    outpath = str(path.dirname(current_doc) +  "/laz/" )
    chunk.exportPointCloud(path = str(outpath + str(chunk.label) + "_densecloud.laz"), source_data = Metashape.DataSource.PointCloudData, save_colors = True, save_confidence = True)
    

