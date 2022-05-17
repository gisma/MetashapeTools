#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MetaShape common tool for sparse cloud building
    and filtering
    @author Marvin Ludwig Chris Reudenbach
    @copyright Copyright 2016-2022, gisma
    @license GPL 3.0
    @version 0.1.0
    @maintainer Chris Reudenbach
    @email creuden@gmail.com"""

import Metashape

def createSparse(chunk, doc = Metashape.app.document, kpl = 40000, tpl = 4000):
    
    # align photos
    chunk.matchPhotos(downscale = 1, reference_preselection = True,
                      keypoint_limit = kpl, tiepoint_limit = tpl, reset_matches = True)
    
    chunk.alignCameras(adaptive_fitting = True, reset_alignment = True)
    chunk.resetRegion()



def fastCreateSparse(chunk, doc = Metashape.app.document, kpl = 10000, tpl = 1000, overl = 8):
    chunk.analyzePhotos(chunk.cameras)
    for camera in chunk.cameras:
        if float(camera.meta["Image/Quality"]) < 0.75:
            camera.enabled = False
            
    chunk.matchPhotos(downscale = 4, reference_preselection = True,
                      keypoint_limit = kpl, tiepoint_limit = tpl, reset_matches = True)
    chunk.alignCameras(adaptive_fitting = True, reset_alignment = True)
    chunk.buildModel(surface_type=Metashape.SurfaceType.HeightField, source_data = Metashape.DataSource.PointCloudData,
                     interpolation = Metashape.Interpolation.EnabledInterpolation, face_count = Metashape.FaceCount.LowFaceCount)
    chunk.smoothModel(10)
    chunk.reduceOverlap(overlap=overl, use_selection=False)    
    chunk.resetRegion()


def filterSparse(chunk, doc = Metashape.app.document):
    
    MF = Metashape.PointCloud.Filter()
    # Reconstruction Accuracy Filter
    for i in range(3-1):
        MF.init(chunk, Metashape.PointCloud.Filter.ReconstructionUncertainty)       
        MF.selectPoints(50)
        chunk.point_cloud.removeSelectedPoints()
        chunk.optimizeCameras(fit_f=True, fit_cxcy=True, fit_aspect=True, fit_skew=True, fit_k1k2k3=True, fit_p1p2=True, fit_k4=True)
        chunk.resetRegion()     
    
    # Reprojection Error Filter
    for i in range(4-1):
        MF.init(chunk, Metashape.PointCloud.Filter.ReprojectionError)       
        MF.selectPoints(1)
        chunk.point_cloud.removeSelectedPoints()
        chunk.optimizeCameras(fit_f=True, fit_cxcy=True, fit_aspect=True, fit_skew=True, fit_k1k2k3=True, fit_p1p2=True, fit_k4=True)
        chunk.resetRegion()
    
    # Projection Accuracy Filter    
    for i in range(2-1):
        MF.init(chunk, Metashape.PointCloud.Filter.ProjectionAccuracy)      
        MF.selectPoints(10)
        chunk.point_cloud.removeSelectedPoints()    
        chunk.optimizeCameras(fit_f=True, fit_cxcy=True, fit_aspect=True, fit_skew=True, fit_k1k2k3=True, fit_p1p2=True, fit_k4=True)
        chunk.resetRegion()
        
    #------------------------------------------------------------------------


def exportSparse(chunk, doc = Metashape.app.document):

    outpath = doc.path[:-4]  # project path without file extension
    crs = Metashape.CoordinateSystem("EPSG::25832")

    # export filtered tiepoints
    chunk.exportPoints(str(outpath + "_" + str(chunk.label) + "_tiepoints.las"), source = Metashape.DataSource.PointCloudData, colors = True, projection = crs)
        
    # save document
    doc.read_only = False
    doc.save()
    

    

