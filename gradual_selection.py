# Author  : Del Bello, R
# Date    : May 2020
# Purpose : Automate the sparse point cloud gradual selection with iterative bundle adjustment(camera optimization) in Agisoft Metashape 1.6 Professional

"""
Remarks: this script was written for the Applied Geomatics Research Group(AGRG) as part of a student project on UAV-based photogrammetry for geomorphic applications. 
The project was a requirement for the completion of the Advanced Diploma in Remote Sensing at the Centre of Geographic Sciences in Nova Scotia.
This work was supported by AGRG who provided the data, the hardware, and advice throughout the project. 
The author would also like to thank Stephen Escarzaga from NPS AKRO Natural Resources group and user "rbnkc" from the Agisoft community in helping writting this script.
"""

import Metashape
import math, sys

doc = Metashape.app.document  # specifies open document
chunk = doc.chunk             # specifies active chunk
T = chunk.transform.matrix
crs = chunk.crs               
pc = chunk.tie_points        # point cloud object for sparse cloud
pc_init = len(pc.points)      # returns the amount of points in cloud (currently)


# *******************************************************************************************************
# ******************************** PARAMETER BLOCK ******************************************************

# STEP 1: Reconstruction Uncertainty as RU

RU_PercentageRemove = 20    # percentage of point removed for each iteration
RU_ThreshMax        = 45    # stop iteration if this percentage of points is removed
RU_Value            = 10    # stop iteration if this RU value is reached (i.e the largest value in all keypoints)

# STEP 2 : Projection Accuracy as PA

PA_PercentageRemove = 20    # threshold percentage of point removed for each iteration
PA_ThreshMax        = 45    # stop iteration loop if this percentage of points is removed (i.e % when starting Step 2)
PA_Value            = 2.   # stop iteration loop if this PA value is reached (largest value)

# STEP 3: Reprojection Error as RE

RE_PercentageRemove = 5     # threshold percentage of point removed for each iteration
RE_MaxIterations    = 10    # max iterations for step 3
RE_Value            = 0.5   # stop iteration if this RE value is reached (largest value)
perc_total_thresh   = 80    # threshold percentage of points to remove from initial point cloud


global_thresh = pc_init*(1- perc_total_thresh / 100)   # convert percentage to actual number of points that must remain

# **********************************************************************************************************************


# Begin Gradual Selection Process :


# **********************************************************************************************************************
# STEP 1 : Reconstruction Uncertainty - RU

RU_init = len(pc.points)  # current count of points
total_removed = 0         # initialize count for points removed
RU_iter_count = 0         # initialize count for interation 
print("*"*100,"\n****Step 1 : Reconstruction Uncertainty \n****Number of starting points:", pc_init,"\n","*"*100)

# RU loop
RU_refined = False
while RU_refined == False:
      
    f = Metashape.TiePoints.Filter()                             # initialise cloud filter based on criteria
    f.init(pc, criterion=Metashape.TiePoints.Filter.ReconstructionUncertainty) 
    values = f.values.copy()
    values.sort()                                                  # sort points for selection
    thresh = values[int(len(values) * (1 - RU_PercentageRemove / 100))]  # define selection based on iteration threshold limit 
    f.selectPoints(thresh)                                         # apply selection of points
    nselected = len([p for p in pc.points if p.selected])          # fetch the amount of points selected in filter
    pc.removeSelectedPoints()                                      # remove points
    RU_iter_count += 1                                             # add 1 to iteration count
    total_removed += nselected                                     # add selected points to count

    print("*****\n***** Iteration---------->", RU_iter_count)
    print("***** Points Removed ----->", nselected)
    print("***** Largest RU Value --->", values[-1],"\n****")

    # camera optimization
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=True, fit_b2=True, fit_k1=True,
                          fit_k2=True, fit_k3=True, fit_k4=False, fit_p1=True, fit_p2=True, fit_p3=False,
                          fit_p4=False, adaptive_fitting=True, tiepoint_covariance=False)

    # logic to break loop
    if total_removed >= RU_init * (RU_ThreshMax / 100):         # if total points removed is greater than the threshold set  (45-50%)
        RU_refined = True                                       # break loop
        print('*'*100,"\n****Reconstruction uncertainty filtering complete.",RU_ThreshMax,"% of initial sparse cloud removed",\
        "\n****Total iterations ------>", RU_iter_count)
            
    elif values[-1] <= RU_Value:                                # values[-1] is largest RU value for all points, since they were sorted previously.
        RU_refined = True                                       # break loop 2
        print('*'*100,"\n****Reconstruction uncertainty filtering complete. Target value of", RU_Value, "reached",\
        "\n****Total iterations ------>", RU_iter_count)

# Report total Camera Error
sums = 0
num = 0
for camera in chunk.cameras:
    if not camera.transform:
        continue
    if not camera.reference.location:
        continue
    estimated_geoc = chunk.transform.matrix.mulp(camera.center)
    error = chunk.crs.unproject(camera.reference.location) - estimated_geoc
    error = error.norm()
    sums += error ** 2
    num += 1
print("****Total Camera Error: ", round(math.sqrt(sums / num), 3))
print('*'*100)
doc.save()

# **********************************************************************************************************************
#  STEP 2: Projection Accuracy - PA

PA_pts_removed = 0                                
PA_init = len(pc.points)                          
print("*"*100,"\n****Step 2 : Projection Accuracy \n****Number of starting points:", PA_init,"\n","*"*100)

## PA loop
PA_iter_count = 0
PA_refined = False
while PA_refined == False:

    f = Metashape.TiePoints.Filter()
    f.init(pc, criterion=Metashape.TiePoints.Filter.ProjectionAccuracy)
    values = f.values.copy()
    values.sort()
    thresh = values[int(len(values) * (1 - PA_PercentageRemove / 100))]
    f.selectPoints(thresh)
    nselected = len([p for p in pc.points if p.selected])
    pc.removeSelectedPoints()

    PA_iter_count += 1
    PA_pts_removed += nselected  
    #print()
    #print("****", nselected, " points removed during projection accuracy filtering iteration *****",PA_iter_count,"*****")
    #print("****", values[-1]," is currently the largest PA value")

    print("*****\n****** Iteration ---------->", PA_iter_count)
    print("***** Points Removed ----->", nselected)
    print("***** Largest PA Value --->", values[-1],"\n****")
    
    # Camera Optimization
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=True, fit_b2=True, fit_k1=True,
                          fit_k2=True, fit_k3=True, fit_k4=False, fit_p1=True, fit_p2=True, fit_p3=False,
                          fit_p4=False, adaptive_fitting=True, tiepoint_covariance=False)

    if PA_pts_removed >= PA_init * (PA_ThreshMax / 100):
        PA_refined = True
        print('*'*100,"\n****Projection Accuracy filtering complete.",PA_ThreshMax,"% of sparse cloud removed")
        print("****Total iterations ------>", PA_iter_count)
        
    elif values[-1] <= PA_Value:
        PA_refined = True
        print('*'*100,"\n****Projection Accuracy filtering complete. Target value of", PA_Value, "reached.")
        print("****Total iterations ------>", PA_iter_count)

# Report Total Camera Error
sums = 0
num = 0
for camera in chunk.cameras:
    if not camera.transform:
        continue
    if not camera.reference.location:
        continue

    estimated_geoc = chunk.transform.matrix.mulp(camera.center)
    error = chunk.crs.unproject(camera.reference.location) - estimated_geoc
    error = error.norm()
    sums += error ** 2
    num += 1
print("****Total Camera Error: ", round(math.sqrt(sums / num), 3))
print('*'*100)
doc.save()

# ****************************************************************************************************************************************************************************
#  Step 3 : Reprojection Error - RE
#  Note : important to verify that cameras have enough projections at the end (in reference pane), if needed modify parameter block to limit iteration or total points removed

print("*"*100,"\n****Step 3 : Reprojection Error \n****Number of starting points:", pc_init,"\n","*"*100)

RE_iter_count = 0
RE_refined = False
while RE_refined == False:

    
    f = Metashape.TiePoints.Filter()
    f.init(pc, criterion=Metashape.TiePoints.Filter.ReprojectionError)
    values = f.values.copy()
    values.sort()
    thresh = values[int(len(values) * (1 - RE_PercentageRemove / 100))]
    f.selectPoints(thresh)
    nselected = len([p for p in pc.points if p.selected])
    pc.removeSelectedPoints()
    RE_iter_count += 1
    print("*****\n***** Iteration---------->", RE_iter_count)
    print("***** Points Removed ---->", nselected)
    print("***** Larges RE Value --->", values[-1],"\n****")

    # Camera optimization
    chunk.optimizeCameras(fit_f=True, fit_cx=True, fit_cy=True, fit_b1=True, fit_b2=True, fit_k1=True,
                          fit_k2=True, fit_k3=True, fit_k4=True, fit_p1=True, fit_p2=True, fit_p3=True,
                          fit_p4=False, adaptive_fitting=True, tiepoint_covariance=True)

    # if current number of points is smaller or equal to (global_thresh) or ~80% of original point cloud loop will break
    if len(pc.points) <= global_thresh:                                     
        RE_refined = True
        print('*'*100,"\n****Total threshrold of ------>", perc_total_thresh,"% of original point cloud removed")
        print("****Total iterations --------->", RE_iter_count,"\n****Max reprojection value --->", values[-1])
    # or if current iteration count reaches the max iteration count
    if RE_iter_count == RE_MaxIterations:
        RE_refrined = True
        print('*'*100,"\n****Maximum iteration reached")
    # or if the largest RE value for all points reaches the target RE value 
    elif values[-1] <= RE_Value:
        RE_refined = True
        print('*'*100,"\n****Reprojection refinement achieved with max value of", RE_Value, "Gradual Selection and Optimization Complete")

# Report Total Camera Error
sums = 0
num = 0
for camera in chunk.cameras:
    if not camera.transform:
        continue
    if not camera.reference.location:
        continue

    estimated_geoc = chunk.transform.matrix.mulp(camera.center)
    error = chunk.crs.unproject(camera.reference.location) - estimated_geoc
    error = error.norm()
    sums += error ** 2
    num += 1
print("****Total Camera Error: ", round(math.sqrt(sums / num), 3))
print('*'*100)
doc.save()
