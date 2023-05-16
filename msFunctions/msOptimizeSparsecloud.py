#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 10:00:09 2019

@author: marvin


"""

import Metashape
import csv
import statistics




# *******************************************************************************************************
# ******************************** PARAMETER BLOCK ******************************************************

RU            = 10    # stop iteration if this RU value is reached (i.e the largest value in all keypoints)
PA            = 2.   # stop iteration loop if this PA value is reached (largest value)
RE            = 1   # stop iteration if this RE value is reached (largest value)


def pointcloudMetrics(chunk, outpath):
    # export original sparse cloud metrics
    MF = Metashape.TiePoints.Filter()
    MF.init(chunk, Metashape.TiePoints.Filter.ReconstructionUncertainty)
    RU = MF.values
    MF.init(chunk, Metashape.TiePoints.Filter.ReprojectionError)
    RE = MF.values
  
    MF.init(chunk, Metashape.TiePoints.Filter.ProjectionAccuracy)
    PA = MF.values
  
     
    res = {"RU": [min(RU), max(RU), statistics.mean(RU)], "RE": [min(RE), max(RE), statistics.mean(RE)], "PA": [min(PA), max(PA), statistics.mean(PA)]}
     
    # save results
    with open(outpath, 'w') as f:
        print(res, file=f)







def optimizeSparsecloud(chunk):
    
    current_doc = Metashape.app.document.path
    outpath = str(path.dirname(current_doc) +  "/tlas/" )  
    
    # optimize camera
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy = True, fit_b1=True, fit_b2 = True, fit_k1 = True, fit_k2 = True, fit_k3 = True, fit_k4=True, fit_p1 = True, fit_p2 =True, adaptive_fitting=True)
    
    # export original marker errors
    chunk.exportReference(path = str(outpath + str(chunk.label) + "_original_marker_error.txt"),
    format = Metashape.ReferenceFormatCSV, items = Metashape.ReferenceItemsMarkers, columns = "noxyzXYZuvwUVW", delimiter = ",")

    pointcloudMetrics(chunk, outpath = str(outpath +  str(chunk.label) +  "_initial_pointcloud_errors.txt"))
    
    # # # Initial Filter
    
    MF = Metashape.TiePoints.Filter()
    MF.init(chunk, Metashape.TiePoints.Filter.ReconstructionUncertainty)
    MF.selectPoints(RU)
    chunk.tie_points.removeSelectedPoints()
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy = True, fit_b1=True, fit_b2 = True, fit_k1 = True, fit_k2 = True, fit_k3 = True, fit_k4=True, fit_p1 = True, fit_p2 =True, adaptive_fitting=True)
    MF.init(chunk, Metashape.TiePoints.Filter.ReprojectionError)       
    MF.selectPoints(RE)
    chunk.tie_points.removeSelectedPoints()
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy = True, fit_b1=True, fit_b2 = True, fit_k1 = True, fit_k2 = True, fit_k3 = True, fit_k4=True, fit_p1 = True, fit_p2 =True, adaptive_fitting=True)
    MF.init(chunk, Metashape.TiePoints.Filter.ProjectionAccuracy)      
    MF.selectPoints(PA)
    chunk.tie_points.removeSelectedPoints()    
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy = True, fit_b1=True, fit_b2 = True, fit_k1 = True, fit_k2 = True, fit_k3 = True, fit_k4=True, fit_p1 = True, fit_p2 =True, adaptive_fitting=True)
    chunk.resetRegion()
    
    # create temporary processing chunk
    
    chunk_backup = Metashape.app.document.chunk
    
    chunk.copy()
    chunk = Metashape.app.document.chunk
    chunk.label = "process"
    
    
    # # # calculation of checkpoint error
    cp_error = []
    for marker in chunk.markers:
        if marker.reference.enabled == False and marker.enabled == True:
            est = chunk.crs.project(chunk.transform.matrix.mulp(marker.position))  # Gets estimated marker coordinate
            ref = marker.reference.location

            if est and ref:
                cp_error.append((est - ref).norm())  # The .norm() method gives the total error. Removing it gives X/Y/Z error
    
    
    cp0 = statistics.mean(cp_error)
    
    # iterative RE filter
    
    MF.init(chunk, Metashape.TiePoints.Filter.ReprojectionError)
    RE = MF.values
    RE = max(RE)
    cp1 = 100
    
    while cp0 < cp1:
         cp1 = cp0
         RE = RE - 0.1
         MF.init(chunk, Metashape.TiePoints.Filter.ReprojectionError)      
         MF.selectPoints(RE)
         chunk.tie_points.removeSelectedPoints()
         chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy = True, fit_b1=True, fit_b2 = True, fit_k1 = True, fit_k2 = True, fit_k3 = True, fit_k4=True, fit_p1 = True, fit_p2 =True, adaptive_fitting=True)
         
         cp_error = []
         for marker in chunk.markers:
             if marker.reference.enabled == False and marker.enabled == True:
                 est = chunk.crs.project(chunk.transform.matrix.mulp(marker.position))  # Gets estimated marker coordinate
                 ref = marker.reference.location
                 if est and ref:
                     cp_error.append((est - ref).norm())  # The .norm() method gives the total error. Removing it gives X/Y/Z error
         cp0 = statistics.mean(cp_error)
    
    # switch back to main chunk
    Metashape.app.document.remove(chunk)
    Metashape.app.document.chunk = chunk_backup
    
    print(chunk.label)
    
    # use second to last RE threshold
    MF.init(chunk, Metashape.TiePoints.Filter.ReprojectionError)
    MF.selectPoints(RE + 0.1)
    chunk.tie_points.removeSelectedPoints()
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy = True, fit_b1=True, fit_b2 = True, fit_k1 = True, fit_k2 = True, fit_k3 = True, fit_k4=True, fit_p1 = True, fit_p2 =True, adaptive_fitting=True)
    
    # export updated marker errors
    chunk.exportReference(path = str(outpath + str(chunk.label) + "_optimized_marker_error.txt"),
    format = Metashape.ReferenceFormatCSV, items = Metashape.ReferenceItemsMarkers, columns = "noxyzXYZuvwUVW", delimiter = ",")

    pointcloudMetrics(chunk, outpath = str(outpath + str(chunk.label) +"_optimized_pointcloud_errors.txt"))
    
    
    

