Welcome to the image composition engine!

With this tool you are able to apply filters to different images and combine them with
a variety of blend features.  Start by importing your image layers into the images folder.  
In the config.yml file, choose the filters you would like to apply and set the parameters 
for each filter.  Then choose the blend type and parameters if desired to combine image
layers in different ways.  The program will automatically read the config file and apply
the desired combination of features to create an output image.  This image will automatically
be saved into the output folder. 

To use the additional filters (from the other team) simply disactivate the original filters
and activate the other team's filters in the filter.py file. Then in main.py, activate the 
alternative .json path and disactivate the original.  Once the Thomas_config file is modified
for the images, filters, and parameters you want, simply run the engine.py file and your 
new image will be saved to the output folder.

