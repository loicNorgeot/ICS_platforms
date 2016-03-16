# Visualisation platform
Ressources for the visualisation platform (backup and infos)

## Files
* /usr/local/launchers/ : ressources for desktop shortcuts
* /usr/local/icons/ : icons for desktop shortcuts
* /usr/share/lightdm/50-*.conf: lightdm configuration files (guest and user sessions)
* /etc/X11/default-display-manager: used to force lightdm
* /usr/share/xsessions/gnome-fallback.desktop: parameters for gnome
* /usr/lib/lightdm/guest-session-auto.sh : launch script for guests
* /usr/local/bin/guest_config: startup script for guest session
* /usr/local/bin/login_config: startup script for user session
* /etc/lightdm/lightdm.conf : lightdm parameters
* /opt/nvidia-settings/samples/nv-control-warpblend.c : compiled with make, binary in ./binaries/linux, used for blending.
* profile: /etc/profile. contains startup session script (blending, copying launchers, adjusting gamma, maybe mounting later)
* ~/nvidia-settings-rc : useless
* /etc/X11/xorg.conf : X11 parameter file


## System

### OS
Ubuntu 14.04 L.T.S 64 bits

### Hardware
* Workstation DELL Precision 7910
* RAM: 128 go
* Processor: 2 x Intel® Xeon(R) CPU E5-2630 v3 @ 2.40GHz (32 total cores)
* GPU: 2 x Quadro K5200/PCIe/SSE2

### Installed softwares
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

Connect with "MetaCity"
Startup script: copy launchers, warp/blend, set gamma and themes
At startup, if some pixels are missing:
    gnome-tweak-tool > GTK+ theme switch

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
