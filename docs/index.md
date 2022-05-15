## Metashape Toolbox

This Toolbox provides default basic workflow scripts and convinience functions to  optimize low budget camera derived orthoimagery for Agisoft Metashape.

Follow the installation guide and you will find a new Menu Item in Metashape main menu.



## The default Workflows

The default workflows are primarily intended for processing large image sets from low budget drone surveys. The problem that arises here is the huge amount of images with numerous starts and landings and a fixed continuous camera system (time lapse 2 sec). This way, 10k images are quickly collected, 80% of which are oversampled or of low image quality. The workflows identify poor image quality and reduce the number of images by an inverse camera position calculation based on the preliminary surface model. This dramatically reduces the number of images, eliminates unusable taxiways and takeoff and landing sequences, and activates optimized cameras. In this way, the quality and reproducibility can be improved in a reproducible manner. At the same time, processing time is reduced by one to two orders of magnitude. 

### Load images 
All functions are based on image data so first do **always** the following:

1. Add the images you want to process to the Chunk.
2. Give the chunk a meaningful name.
3. Save the project using a meaningful name


### Worflow with GCPs

#### Worflow Orthoimage with GCP step 1 (apply GCP)
* Start the script `Ortho-1 (preGCP)`.
  * Calculate a first alignment and mesh using the following parameters: 
  * Key Point Limit: 10000
  * Tie Point Limit: 1000
  * Downsampling: 4
  * Smoothing 10 times
  * reduce overlap with a value of 8 
  * Calculate a **second** alignment and mesh using the following parameters: 
  * Key Point Limit: 40000
  * Tie Point Limit: 4000
  * Downsampling: 1



#### Worflow Orthoimage with GCP step 2 (apply GCP)

After the script is finished, import your Ground Control Points (GCP) and align them manually in at least 4 images. Use about 30 % of the GCP as independent Checkpoints by unticking the checkbox in the Reference Pane.


#### Worflow Orthoimage with GCP step 3 (create Orthoimage)

* Use `Toolchain Ortho-2 (postGCP)`. This includes the following steps:
  * optimize sparse cloud
  * create 2.5D Mesh
  * smooth Mesh with factor 35
  * create Orthomosaic
	  * surface: mesh
	  * refine seamlines = True
  * export Orthomosaic, Seamlines and Marker error
  * export report

### Worflow Orthoimage without GCP
If you do NOT have Ground Control Points you can run an optimized workflow of orthoimages production by one click.
1. Load images as above (you may load several distinct chunks for e.g. different time slots)
2. Start the script `Toolchain noGCP`


This will do the following steps:.
* Check image Quality and drop images with  a quality less than 0.78
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

