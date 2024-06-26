#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 10:00:09 2019

@author: marvin


"""

import Metashape
import csv
from os import path

######





def createSparse(chunk, kpl, tpl, ds):
    # align photos
    chunk.matchPhotos(downscale = ds, reference_preselection = True,
                      keypoint_limit = kpl, tiepoint_limit = tpl, reset_matches = True)
    
    chunk.alignCameras(adaptive_fitting = True, reset_alignment = True)
    chunk.resetRegion()



def sparseFilter(chunk, RE, RU, PA):
    MF = Metashape.TiePoints.Filter()
    # Reconstruction Accuracy Filter
    MF.init(chunk, Metashape.TiePoints.Filter.ReconstructionUncertainty)
    MF.selectPoints(RU)
    chunk.tie_points.removeSelectedPoints()
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy = True, fit_b1=True, fit_b2 = True, fit_k1 = True, fit_k2 = True, fit_k3 = True, fit_k4=True, fit_p1 = True, fit_p2 =True)
    chunk.resetRegion()     
    
    # Reprojection Error Filter
    MF.init(chunk, Metashape.TiePoints.Filter.ReprojectionError)
    MF.selectPoints(RE)
    chunk.tie_points.removeSelectedPoints()
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy = True, fit_b1=True, fit_b2 = True, fit_k1 = True, fit_k2 = True, fit_k3 = True, fit_k4=True, fit_p1 = True, fit_p2 =True)
    chunk.resetRegion()
    
    # Projection Accuracy Filter    
    MF.init(chunk, Metashape.TiePoints.Filter.ProjectionAccuracy)
    MF.selectPoints(PA)
    chunk.tie_points.removeSelectedPoints()
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy = True, fit_b1=True, fit_b2 = True, fit_k1 = True, fit_k2 = True, fit_k3 = True, fit_k4=True, fit_p1 = True, fit_p2 =True)
    chunk.resetRegion()
    
    
def createMesh(chunk):
	chunk.buildModel(surface_type=Metashape.SurfaceType.HeightField, source_data = Metashape.DataSource.TiePointsData,
					interpolation = Metashape.Interpolation.EnabledInterpolation, face_count = Metashape.FaceCount.HighFaceCount)
	chunk.smoothModel(35)	




def repro(chunk, k, RE,RU,PA):
	current_doc = Metashape.app.document.path
	outpath = str(path.dirname(current_doc) +  "/repro-test/" )
	for j in range(k):
		createSparse(chunk, kpl = 40000, tpl = 40000, ds = 0)
		sparseFilter(chunk, RE,RU,PA)
		createMesh(chunk)
		chunk.buildOrthomosaic(surface_data=Metashape.ModelData, resolution = 0.05, refine_seamlines = True)
		chunk.exportRaster(str(outpath + str(j+1) + "_ortho.tif"),
					raster_transform = Metashape.RasterTransformNone,save_alpha=False,
					white_background=True, resolution = 0.05, source_data = Metashape.DataSource.OrthomosaicData)
