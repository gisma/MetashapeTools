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
def sparse2ortho(chunk, orthoRes):
    doc = Metashape.app.document
    # create mesh
    chunk.resetRegion()
    #crs=Metashape.OrthoProjection("EPSG::4326")
    chunk.buildModel(surface_type=Metashape.SurfaceType.HeightField, source_data = Metashape.DataSource.TiePointsData,
                     interpolation = Metashape.Interpolation.EnabledInterpolation, face_count = Metashape.FaceCount.HighFaceCount)
    chunk.smoothModel(35)   
    
    # build ortho
    chunk.resetRegion()
    #chunk.buildOrthomosaic(surface_data=Metashape.ModelData, refine_seamlines = True,resolution=orthoRes,projection=4326)
    chunk.buildOrthomosaic(surface_data =Metashape.ModelData, fill_holes = True, ghosting_filter = False, cull_faces = False, refine_seamlines = True, resolution = orthoRes)

#def dense2ortho(chunk, doc = Metashape.app.document, orthoRes = 0.05):
    


def exportOrtho(chunk):
	current_doc = Metashape.app.document.path
	outpatho = str(path.dirname(current_doc) +  "/ortho/" )
	outpathr = str(path.dirname(current_doc) +  "/report/" )
	print("****Outpath: ", outpatho)
	print("****cunk label: ", chunk.label)
    # outpath = Metashape.app.document.path[:-4]  # project path without file extension
    # export ortho
	chunk.resetRegion()
	chunk.exportRaster(str(outpatho + str(chunk.label) + "_orthomosaic.tif"),
                            raster_transform = Metashape.RasterTransformNone,
                            save_kml=False, save_world=False, save_alpha=False,
                white_background=True,
                source_data=Metashape.DataSource.OrthomosaicData)
    # save document
	Metashape.app.document.save()
	
    # create report
	chunk.exportReport(outpathr  + chunk.label + "_report.pdf") 


