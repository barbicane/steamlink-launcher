"""Steamlink Launcher for Raspbian"""
import os
import xbmc
import xbmcgui
import xbmcaddon

__plugin__ = "steamlink"
__author__ = "toast"
__url__ = "https://github.com/swetoast/steamlink-launcher/"
__git_url__ = "https://github.com/swetoast/steamlink-launcher/"
__credits__ = "toast"
__version__ = "0.0.12"

dialog = xbmcgui.Dialog()
addon = xbmcaddon.Addon(id='plugin.program.steamlink')

def main():
    """Main operations of this plugin."""
    create_files()
    output = os.popen("sh /tmp/steamlink-launcher.sh").read()
    dialog.ok("Starting Steamlink...", output)

def create_files():
    """Creates bash files to be used for this plugin."""
    with open('/tmp/steamlink-launcher.sh', 'w') as outfile:
        outfile.write("""#!/bin/bash
chmod 755 /tmp/steamlink-watchdog.sh
sudo openvt -c 7 -s -f clear
sudo su -c "nohup sudo openvt -c 7 -s -f -l /tmp/steamlink-watchdog.sh >/dev/null 2>&1 &"
""")
        outfile.close()
    with open('/tmp/steamlink-watchdog.sh', 'w') as outfile:
        outfile.write("""#!/bin/bash
        sudo apt update # write a better update check
if [ ! $(dpkg --list | grep gnupg) ]; then 
   kodi-send --action="Notification(Downloading and installing Steamlink depenancies (gnupg)... ,3000)"
   sudo apt install gnupg -y
fi
if [ ! $(dpkg --list | grep curl) ]; then 
    kodi-send --action="Notification(Downloading and installing Steamlink depenancies (curl)... ,3000)" 
    sudo apt install curl -y 
fi
if [ ! $(dpkg --list | grep libgles2) ]; then 
    kodi-send --action="Notification(Downloading and installing Steamlink depenancies (libgles2)... ,3000)" 
    sudo apt install libgles2 -y 
fi
if [ ! $(dpkg --list | grep libegl1) ]; then 
    kodi-send --action="Notification(Downloading and installing Steamlink depenancies (libegl1)... ,3000)" 
    sudo apt install libegl1 -y 
fi
if [ ! $(dpkg --list | grep libgl1-mesa-dri) ]; then 
    kodi-send --action="Notification(Downloading and installing Steamlink depenancies (libgl1-mesa-dri)... ,3000)" 
    sudo apt install libgl1-mesa-dri -y 
fi
if [ "$(which steamlink)" = "" ]; then
    kodi-send --action="Notification(Downloading and installing Steamlink Application... ,3000)" 
    curl -o /tmp/steamlink.deb -#Of http://media.steampowered.com/steamlink/rpi/latest/steamlink.deb
    sudo dpkg -i /tmp/steamlink.deb
    rm -f /tmp/steamlink.deb
fi
if [ -f "/home/media/.wakeup" ] 
   then /usr/bin/wakeonlan "$(cat "/home/media/.wakeup")"
   else sudo apt install wakeonlan -y; /usr/bin/wakeonlan "$(cat "/home/media/.wakeup")" 
fi
systemctl stop mediacenter
#if [ "$(systemctl is-active hyperion.service)" = "active" ]; then systemctl restart hyperion; fi
sudo -u media steamlink
openvt -c 7 -s -f clear
systemctl start mediacenter
""")
        outfile.close()
main()
