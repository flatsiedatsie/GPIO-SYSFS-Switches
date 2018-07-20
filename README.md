# GPIO-SYSFS-Switches
A plugin for Domoticz, the open source home automation platform.

It automatically creates switches for GPIO pins that you select. Use it to toggle devices via the GPIO pins.

More details can be found on the Domoticz wiki:
https://www.domoticz.com/wiki/Plugins/GPIO-SYSFS-Switches

#How it works
If you enter a list of GPIO pins, the plugin will automatically create switches for those pins. It does this by exporting those pins via the SYSFS system, and then toggling them. It does all this via sudo shell commands.

#Installing
Download the plugin from Github, and place it into a folder under your plugins directory. DOWNLOAD PAGE

Or enter these commands in the terminal:

 cd domoticz/plugins
 git clone https://github.com/flatsiedatsie/GPIO-SYSFS-Switches.git sysfs-switches
 cd sysfs-switches
 chmod +x plugin.py

#Known problems
In this first version of the plugin using 1 pin is totally safe, as is adding pins.

However, if you have a list of pins and decide to switch the pin numbers around in that list, or to remove a pin form it, then you may have a problem. The switches in Domoticz will then be swapped as well.

The same goes for removing a switch in Domoticz. If you do, then the order changes and switches may start pointing to other PGIO pins than you expected.

#Limitations
The pins are not set before the plugin is loaded. So when you reboot your raspberry pi, it will change the state of the pins.

Also, when you restart Domoticz, the pins are temporarily released and recreated. This effectively means the switch is turned off for a second or two.
