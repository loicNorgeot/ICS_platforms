# Visualisation platform

## Repository
The provided files are meant as backups in case of a need to re-install the system:
* xorg.conf : in /etc/X11/, X11 configuration file
* nv-control-warpblend.c : in ~/Téléchargements/nvidia-settings.../samples. Has to be recompiled with make, which will output a binary in ./binaries/linux, used for blending.
* default-manager: in /etc/X11/, used with lightdm

## Installed softwares
* paraview 4.4.0
* visit 2.10
* blender 2.76
* unity 3D 5.1.0
* UnrealEngine 4.7
* processing 2.2.1
* processing 3.0.1
* unitymol
* iqmol
* jmol

## Troubleshooting

Connect with "MetaCity"

Files location:
* Demos in                 /usr/local/share/demos
* Common data in           /usr/local/share/data
* Common scripts in        /usr/local/bin
* Common launchers in      /usr/local/launchers
* Additionnal softwares in /opt/

(maybe) helpful commands:

    ln -s /opt/myapp/myappbinary /usr/local/bin/myappbinary
    sudo service lightdm restart
    sudo startx
    sudo rm ~/.Xauthority
