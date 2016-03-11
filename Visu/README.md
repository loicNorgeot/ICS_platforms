# Visu

The provided files are meant as backups in case of a need to re-install the system:
* xorg.conf : in /etc/X11/, X11 configuration file
* nv-control-warpblend.c : in ~/Téléchargements/nvidia-settings.../samples. Has to be recompiled with make, which will output a binary in ./binaries/linux, used for blending.
* default-manager: in /etc/X11/, used with lightdm

#Troubleshooting

Connect with "MetaCity"

Demos are located in /usr/local/share/demos
Common data in /usr/local/share/data
Common scripts in /usr/local/bin
Additionnal softwares in /opt/

(maybe) helpful commands:
    ln -s /opt/myapp/myappbinary /usr/local/bin/myappbinary
    sudo service lightdm restart
    sudo startx
    sudo rm ~/.Xauthority
