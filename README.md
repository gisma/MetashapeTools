# MetashapeTools
Scripts, Utilities and default otimized workflows for Agisoft Metashape



# Installation

## Linux

Copy the content of this repo to `~/.local/share/Agisoft/Metashape Pro/scripts/`

```bash

cd ~/.local/share/Agisoft/Metashape Pro/scripts
git clone https://github.com/gisma/MetashapeTools.git .

```

## Windows

Copy the content of this repo to `User/AppData/Local/AgiSoft/PhotoScan Pro/scripts`


# Metashape Toolbox

This Toolbox provides default basic workflow scripts and convinience functions to  optimize low budget camera derived orthoimagery for Agisoft Metashape.

Follow the installation guide and you will find a new Menu Item in Metashape main menu.



## The default Workflows

The default workflows are primarily intended for processing large image sets from low budget drone surveys. The problem that arises here is the huge amount of images with numerous starts and landings and a fixed continuous camera system (time lapse 2 sec). This way, 10k images are quickly collected, 80% of which are oversampled or of low image quality. The workflows identify poor image quality and reduce the number of images by an inverse camera position calculation based on the preliminary surface model. This dramatically reduces the number of images, eliminates unusable taxiways and takeoff and landing sequences, and activates optimized cameras. In this way, the quality and reproducibility can be improved in a reproducible manner. At the same time, processing time is reduced by one to two orders of magnitude. 

### Preliminary Task - Load images 
All functions are based on image data so first do **always** the following:

1. Add the images you want to process to the Chunk.
2. Give the chunk a meaningful name.
3. Save the project using a meaningful name


### Orthoimage Workflow integrating Ground Control Points (GCPs)

It is obligatory that you run consecutively  all three steps.

#### Step 1 - preprocessing
* Start the script `Ortho-1 (preGCP)`
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


#### Step 2 - link GCP to images

After the script is finished you may need to manually remove the few remaining start and landing area pictures. Otherwise you will find at the launching place some artefacts. To do so just right-click on the position in the model and choose filter by point. Mark and remove all pictures with the launching pad and repeated launching and landing images.

Then import your Ground Control Points (GCP) and align them manually in at least 4 images. Use about 30 % of the GCP as independent Checkpoints by unticking the checkbox in the Reference Pane.


#### Step 3 - optimize point cloud and create Orthoimage

* Use `Toolchain Ortho-2 (postGCP)`. This includes the following steps:
  * optimize sparse cloud using the point cloud statistics
  * create 2.5D Mesh
  * smooth Mesh with factor 35 (empirical value for forests)
  * create Orthomosaic
	  * surface: mesh
	  * refine seamlines = True
  * export Orthomosaic, Seamlines and Marker error
  * export report

Finally you have a result that automatically tries to optimize the number of necessary cameras, minimize reprojection errors in the tie point cloud (sparse cloud), re-arrange the cameras and thus produce an reproducible orthoimage on the (statistically) best possible spatial resolution. 

### Worflow Orthoimage without GCP
If you do NOT have Ground Control Points you can run corresponding to the upper workflow, an one click production of optimized orthoimages. This maybe very useful if you have several repeated flights over an area and if you want to get an overview. Just put the image data of each flight in a seperate chunk and start the script `Toolchain noGCP` with the option to process all chunks.

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


### Orthomosaic from Sparse Cloud
If you do not want to optimize the camera positions and the sparse cloud you should choose `Toolchain Toolchain Ortho from Sparse`. This includes the following steps:

* create 2.5D Mesh
* smooth Mesh with factor 35
* create Orthomosaic
	* surface: mesh
	* refine seamlines = True
* export of Orthomosaic, Seamlines and Marker error
* export of report

It is recommended run beforehand the `Optimize Sparsecloud` script. This will print out a Reprojection Error for which the checkpoint error reach its minimum.

## Special Tasks

### Orthomosaic Reproducibility

1. Add the images you want to process to the Chunk.
2. Import the GCP and align them.
3. Start the script `Reproducibility`


This will compute a set amount of orthomosaics (default is 5), which later can be analysed in R.





