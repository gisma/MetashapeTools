#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MetaShalpe functions for
    orthoimages
    @author Marvin Ludwig Chris Reudenbach
    @copyright Copyright 2016-2022, gisma
    @license GPL 3.0
    @version 0.1.0
    @maintainer Chris Reudenbach
    @email creuden@gmail.com"""

import Metashape
from os import path

# control: do with all chunks or just the active one
def sparse2ortho(chunk, orthoRes, doc = Metashape.app.document):
    
    # create mesh
    chunk.resetRegion()
    crs=Metashape.OrthoProjection("EPSG::25832")
    chunk.buildModel(surface_type=Metashape.SurfaceType.HeightField, source_data = Metashape.DataSource.TiePoints,
                     interpolation = Metashape.Interpolation.EnabledInterpolation, face_count = Metashape.FaceCount.HighFaceCount)
    chunk.smoothModel(35)   
    
    # build ortho
    chunk.resetRegion()
    chunk.buildOrthomosaic(surface_data=Metashape.ModelData, refine_seamlines = True,resolution=orthoRes,projection=crs)
    

#def dense2ortho(chunk, doc = Metashape.app.document, orthoRes = 0.05):
    


def exportOrtho(chunk, doc = Metashape.app.document):
	
    outpath = path.dirname(doc.path)
    # outpath = Metashape.app.document.path[:-4]  # project path without file extension

     # export ortho
    chunk.resetRegion()
    chunk.exportRaster(str(outpath) + "_" + str(chunk.label) + "_orthomosaic.tif",
                            raster_transform = Metashape.RasterTransformNone,
                            save_kml=False, save_world=False, save_alpha=False,
                white_background=True,
                source_data=Metashape.DataSource.OrthomosaicData)
    # save document
    Metashape.app.document.save()
    # create report
    chunk.exportReport(outpath + "_" + chunk.label + "_report.pdf") 


