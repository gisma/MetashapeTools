# MetashapeTools

Scripts, utilities and optimized workflows for Agisoft Metashape with respect to reproducible orthoimage and dense cloud generation. 

# Installation
If you are using Metashape 2.x you may sownload the current version. If you rely on Metashape 1.x please use the [V1.x release](https://github.com/gisma/MetashapeTools/releases/tag/v1.x)

## Linux

Copy the content of this repo to `~/.local/share/Agisoft/Metashape Pro/scripts/`

```bash

cd ~/.local/share/Agisoft/Metashape Pro/scripts
git clone https://github.com/gisma/MetashapeTools.git .

```

## Windows
Metashape 1.x:
Copy the content of this repo to `User/AppData/Local/AgiSoft/PhotoScan Pro/scripts`
Metashape 2.x:
Copy the content of this repo to `User/AppData/Local/AgiSoft/Metashape Pro/scripts`

# `Ortho+`

The `Ortho+` menu provides basic workflow scripts and a bunch of convenience functions to optimize (low budget) camera derived ortho imagery and point cloud generation for Agisoft Metashape.

Follow the installation guide and you will find the new `Ortho+` Menu item at the Metashape main menu bar.

## First things first - Load images 
All functions are based on image data so first do **always** the following:

1. Add the images you want to process to the chunk.
2. Give the chunk a meaningful name.
3. Save the project using a meaningful name

Note: You will be always ask if you want to perfrm the task for a singel chunk or all chunks. Choose wisely.

## `BestPractice ForestOrtho`

The `BestPractice` menu provides robust and well tested workflows that are primarily intended for processing large image data sets from (low budget) drone surveys designed for **forest areas**. The problem that arises here is the huge amount of images with numerous starts and landings and a fixed continuous camera system (e.g. GoPro Hero 7, time lapse 2 sec). This way, 10k images are quickly collected, 80% of which are over sampled or of poor image quality and so on. The workflows identify low image quality and reduce the number of images by an inverse camera position calculation based on the preliminary surface model. This *dramatically* reduces the number of images, due to elimination of unusable taxiway and takeoff/landing image sequences. In addition the remaining cameras are activated and optimized. In this way, the quality and reproducibility can be significantly improved. At the same time, processing time is reduced by one to two orders of magnitude. 

## Orthoimage Workflow integrating Ground Control Points (GCPs)

It is obligatory that you run consecutively  all three steps.

### `Step-1 Orthoimage-pre-GCP`
* Start the script `Orthoimage-pre-GCP`
  * checks image Quality and drop images with  a quality less than 0.78
  * calculate a first alignment and mesh using the following parameters: 
  * key point limit: 10000
  * tie point limit: 1000
  * downsampling: 4
  * smoothing 10 times
  * reduce overlap with a value of 8 
  * calculate a **second** alignment and mesh using the following parameters: 
  * key point limit: 40000
  * tie point limit: 4000
  * downsampling: 1


### Step- 2 Link GCP to images ... 

After the script is finished you *may* need to manually remove the few remaining start and landing area pictures. Otherwise you will find at the launching place some artefacts. To do so just right-click on the position in the model and choose filter by point. Mark and remove all pictures with the launching pad and repeated launching and landing images.

The procedure is well documented. Dor instant watch this [YouTube](https://youtu.be/G09r5PXqhBc) or follow this [tutorial](https://agisoft.freshdesk.com/support/solutions/articles/31000153696-aerial-data-processing-with-gcps-orthomosaic-dem-generation). Import your Ground Control Points (GCP) and align them manually in at least 4 images. Use about 30 % of the GCP as independent checkpoints by unticking the check box in the reference pane. Save your project.

### `Step-3 Optimize Sparsecloud`
Performs an gradual filtering ofthe sparse cloud to retrieve a better reprojection error. The tie pointcloud will be much more reliable for all later tasks. Note it works only with GCP markers i.e. step 2.


### `Step-4 Orthoimage-post-GCP`

* Use `Orthoimage-post-GCP`. This includes the following steps:
  * optimize sparse cloud using the point cloud statistics
  * create 2.5D Mesh
  * smooth Mesh with factor 35 (empirical value for forests)
  * create Orthomosaic
	  * surface: mesh
	  * refine seamlines = True
  * export Orthomosaic, Seamlines and Marker error
  * export report

Finally you have a result that automatically tries to optimize the number of necessary cameras, minimize re projection errors in the tie point cloud (sparse cloud), re-arrange the cameras and thus produce an reproducible orthoimage on the (statistically) best possible spatial resolution. 



## `Tools+`

### `Orthoimage-no-GCP`
If you do *NOT* have Ground Control Points or not intending to squeeze the absolute position of the final product, you can run corresponding to the upper workflow, an one click production of optimized orthoimages. This maybe very useful if you have several repeated flights over an area and if you want to get an overview. Just put the image data of each flight in a seperate chunk and start the script `Toolchain noGCP` with the option to process all chunks.

This will do the following steps:.
* Check image Quality and drop images with  a quality less than 0.75
* Calculate a first alignement and mesh with 
  * Key Point Limit: 10000
  * Tie Point Limit: 1000
  * Downsampling: 4
  * Smoothing 10 times
* reduce overlap with a value of 15 
* on the remaining cameras calculate second alignment and 2.5D mesh with: 
  * Key Point Limit: 40000
  * Tie Point Limit: 4000
  * Downsampling: 1
* smooth Mesh with factor 35
* create Orthomosaic
	* surface: mesh
	* refine seamlines = True
* export Orthomosaic, Seamlines and Marker error
* export a report

### Iterative Sparse Cloud filtering

Provides slightly adapted script of [Del Bell](https://github.com/skycontrast/Agisoft) 
 for iterative gradual filtering of the sparse point cloud. It is a very convenient tool for improvining the sparse point cloud in a reproducible way. It may be subset the step 3 of the ForestOrtho if no GCPs are available. The filtering is performed in three steps with the following arguments:

#### STEP 1: Reconstruction Uncertainty as RU

	def_RU_PercentageRemove = 20    # percentage of point removed for each iteration
	def_RU_ThreshMax        = 45    # stop iteration if this percentage of points is removed
	def_RU_Value            = 10    # stop iteration if this RU value is reached (i.e the largest value in all keypoints)

#### STEP 2 : Projection Accuracy as PA

	def_PA_PercentageRemove = 20    # threshold percentage of point removed for each iteration
	def_PA_ThreshMax        = 45    # stop iteration loop if this percentage of points is removed (i.e % when starting Step 2)
	def_PA_Value            = 2.   # stop iteration loop if this PA value is reached (largest value)

#### STEP 3: Reprojection Error as RE

	def_RE_PercentageRemove = 5     # threshold percentage of point removed for each iteration
	def_RE_MaxIterations    = 10    # max iterations for step 3
	def_RE_Value            = 0.5   # stop iteration if this RE value is reached (largest value)
	def_perc_total_thresh   = 80    # threshold percentage of points to remove from initial point cloud

### `Reduce Overlap`
Creates a low quality first alignment and sparse pointcloud  and a smoothed (factor 10) mesh. Calculates then an inverse optimization of the needed images with the factor 8.


### `Densecloud`
Calculates a dense point cloud

### `Orthoimage`
If you do not want to optimize the camera positions and the sparse cloud you should choose `Orthoimage`. This includes the following steps:

* create 2.5D Mesh
* smooth Mesh with factor 35
* create Orthomosaic
	* surface: mesh
	* refine seamlines = True
* export of Orthomosaic, Seamlines and Marker error
* export of report

It is recommended run beforehand the `Optimize Sparsecloud` script. This will print out a Reprojection Error for which the checkpoint error reach its minimum.

## `Utilities`

### `Export Marker Error`
Export the Marker Error to a csv file.

### `Export Tiepoint Error`
Export the Tie Point Errors from the sparse pointcloud to a csv file. This means   Reconstruction Uncertainty, Reprojection Error,Projection Accuracy, Image Count.

### `Orthomosaic Reproducibility`

2. Import the GCP and align them.
3. Start the script `Reproducibility`
This will compute a set amount of orthomosaics (default is 5), which later can be analysed in R.




