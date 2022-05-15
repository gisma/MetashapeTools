## Metashape Toolbox

This Toolbox provides default basic workflow scripts and convinience functions to  optimize low budget camera derived orthoimagery for Agisoft Metashape.

Follow the installation guide and you will find a new Menu Item in Metashape main menu.



## The default Workflows

### Load images 

1. Add the images you want to process to the Chunk.
2. Give the chunk a meaningful name.

### Worflow noGCP
If you do NOT have Ground Control Points you can run an optimized wiorkflow of ortho image production by one click.
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
* export of Orthomosaic, Seamlines and Marker error
* export of a report

### Worflow with GCPs

1. Add the images you want to process to the Chunk.
2. Give the chunk a usefull name.
3. Start the script `Toolchain Part 1`

* Calculate a first alignement and mesh with 
  * Key Point Limit: 10000
  * Tie Point Limit: 1000
  * Downsampling: 4
  * Smoothing 10 times
* reduce overlap with a value of 15 
* After the script is finished, import your Ground Control Points (GCP) and align them manually in at least 4 images. Use about 30 % of the GCP as independent Checkpoints by unticking the checkbox in the Reference Pane.
* Now you should optimize the georeferencing of the product with the script `Optimize Sparsecloud`. This will print out a Reprojection Error for which the checkpoint error reach its minimum.
4. Now use `Toolchain Part 2`. This includes the following steps:
* create 2.5D Mesh
* smooth Mesh with factor 35
* create Orthomosaic
	* surface: mesh
	* refine seamlines = True
* export of Orthomosaic, Seamlines and Marker error


## Orthomosaic Reproducibility

1. Add the images you want to process to the Chunk.
2. Import the GCP and align them.
3. Start the script `Reproducibility`


This will compute a set amount of orthomosaics (default is 5), which later can be analysed in R.

