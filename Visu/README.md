# Visualisation platform
Ressources for the visualisation platform (backup and infos)

## System

#### OS
Ubuntu 14.04 L.T.S 64 bits

#### Hardware
* Workstation DELL Precision 7910
* RAM: 128 go
* Processor: 2 x Intel® Xeon(R) CPU E5-2630 v3 @ 2.40GHz (32 total cores)
* GPU: 2 x Quadro K5200/PCIe/SSE2

#### Installed softwares
* paraview 4.4.0
* visit 2.10.1
* blender 2.76
* unity 3D 5.1.0
* UnrealEngine 4.7
* Python anaconda3
* Code::Blocks 13.12
* Eclipse 3.8
* processing 2.2.1
* processing 3.0.1
* unitymol
* iqmol
* jmol

## Troubleshooting

#### In case of trouble
* Startup script: copy launchers, warp/blend, set gamma and themes
* At startup, if some pixels are missing:
    gnome-tweak-tool > GTK+ theme switch or right click change desktop

#### Files location:
* Demos in                 /usr/local/demos
* Common scripts in        /usr/local/bin
* Common launchers in      /usr/local/launchers
* Common icons in          /usr/local/launchers
* Additionnal softwares in /opt/

#### Helpful commands:

    ln -s /opt/myapp/myappbinary /usr/local/bin/myappbinary
    sudo service lightdm restart
    sudo startx
    sudo rm ~/.Xauthority

## Files
* /usr/local/launchers/ : ressources for desktop shortcuts
* /usr/local/icons/ : icons for desktop shortcuts
* /usr/share/lightdm/50-*.conf: lightdm configuration files (guest and user sessions)
* /etc/X11/default-display-manager: used to force lightdm
* /etc/environment : modify path for all users (anaconda)
* /usr/share/xsessions/gnome-fallback.desktop: parameters for gnome
* /usr/lib/lightdm/guest-session-auto.sh : launch script for guests
* /usr/local/bin/guest_config: startup script for guest session
* /usr/local/bin/login_config: startup script for user session
* /etc/lightdm/lightdm.conf : lightdm parameters
* /opt/nvidia-settings/samples/nv-control-warpblend.c : compiled with make, binary in ./binaries/linux, used for blending.
* ~/nvidia-settings-rc : useless
* /etc/profile startup session script (blending, copying launchers, adjusting gamma, maybe mounting later)
* /etc/X11/xorg.conf : X11 parameter file
