#Install

In order to use this add-on, only MMG and Blender are required.

Medit is however an optionnal tool which is recommended as it can greatly increase the process of interactively vizualizing the created meshes.

Please note that the use of MMG plugin is impossible without the prior installation of the Import/Export Plugin.



## MMG install (mandatory)

In order to install MMG (mandatory), navigate to [MMG tools github page](https://github.com/MmgTools/mmg).

The installation process is explained on the main page of the repository, and detailled usage instructions can be found on the project's [Wiki](https://github.com/MmgTools/mmg/wiki)



## Medit install (optionnal)

Medit can be directly downloaded on [Pascal Frey's website](http://www.ann.jussieu.fr/frey/software.html), which also contains a collection of .mesh files.

The [corresponding documentation](http://www.ann.jussieu.fr/frey/logiciels/Docmedit.dir/index.html) is also available in french.


## Blender configuration

After installing Blender from the Download section of [Blender official website](https://www.blender.org), one also needs to configure two addons in order to access the combined features of MMG, Medit and Blender. 

One allows for the import and export of .sol and .mesh file, while the other interfaces Blender weight paint mode with MMG and Medit.

Here is the procedure to follow in order to configure Blender and install the addons:

#### Navigate to File > User Preferences
![](https://cloud.githubusercontent.com/assets/11873158/11323668/fd50c95c-9118-11e5-8096-4d7c50d4c2eb.png "")

#### In the tab "Add-ons", select "Install from File..."
![](https://cloud.githubusercontent.com/assets/11873158/11323675/fd8806c4-9118-11e5-9374-ca5f59cd145c.png "")

#### Select the script "mesh_io.py" and click on "Install from File"
![](https://cloud.githubusercontent.com/assets/11873158/11323670/fd78a06c-9118-11e5-9838-0d1f97ae416a.png "")

#### Check the checkbox corresponding to the newly installed Add-on
![](https://cloud.githubusercontent.com/assets/11873158/11323671/fd7dd5b4-9118-11e5-89e8-d14cf287ce58.png "")

#### Repeat the process for the script "mmg.py". You may then save the configuration by clicking on "Save User's Settings"

#### Import a 3D Model from File > Import
![](https://cloud.githubusercontent.com/assets/11873158/11323673/fd86a644-9118-11e5-967d-ced388b0a494.png "")

#### Select your mesh, and change to "Weight Paint" mode in the 3D View
![](https://cloud.githubusercontent.com/assets/11873158/11323674/fd8771dc-9118-11e5-860d-9dbe128b5964.png "")

#### Use the painting tools to define zones on your model
![](https://cloud.githubusercontent.com/assets/11873158/11323669/fd69aaf8-9118-11e5-9969-86b77cf27dfc.png "")

#### Under the painting tools, set MMG and export parameters, define an output file to store the remeshed model, and click on "Launch MMG"
![](https://cloud.githubusercontent.com/assets/11873158/11323672/fd83b31c-9118-11e5-91c2-9ebacd9ba007.png "")

#### TADAAAAA! Your model has been remeshed according to the settings you fixed.
![](https://cloud.githubusercontent.com/assets/11873158/11323676/fd917056-9118-11e5-8a07-48944e059f26.png "")


For a more detailled description of the add-ons usage, please visit the [Usage Information](USAGE.md) associated wih this project.



