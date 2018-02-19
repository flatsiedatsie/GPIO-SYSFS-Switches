# Set a SYSFS pin from the interface
#
# Author: BlauweBuis
#
"""
<plugin key="SYSFS-Switches" name="SYSFS-Switches" author="blauwebuis" version="0.1.0" wikilink="http://www.domoticz.com/wiki/plugins" externallink="https://html5zombo.com/">
	<description>
		Set the SYSFS OUTPUT pins. Make sure you set the GPIO numbers, and not the physical pin numbers.
		Restart Domoticz for it to take effect. This plugin assumes your SYSFS GPIO hardware plugin is set to "automatic". Pins are unexported when Domoticz closes.
	</description>
	<params>
		<param field="Mode1" label="GPIO output pin numbers (comma separated)" width="100px" required="false" default=""/>
	</params>
</plugin>
"""
from subprocess import call
import os
import Domoticz

class BasePlugin:

	def __init__(self):
		pass
	
	def onStart(self):
		Domoticz.Log("onStart called. Will now export SYSFS GPIO output pins.")
		Domoticz.Log("Output pin switches made so far (max 255): " + str(len(Devices)))	

		self.outpins = parseCSV(Parameters["Mode1"])	
		#if(len(Devices) < len(self.outpins)):
		
		if len(self.outpins) > 0:
			#for pin in self.outpins:
			for idx, pin in enumerate(self.outpins):
				Domoticz.Log("_____" + str(idx))
				pinCommand = "sudo echo " + str(pin) + " > /sys/class/gpio/export"
				directionCommand = "sudo echo out > /sys/class/gpio/gpio" + str(pin) + "/direction"
				
				if idx + 1 not in Devices:
					Domoticz.Log("Creating a new SYSFS output switch for pin " + str(pin))
					switchName = "Out pin " + str(pin)
					Domoticz.Device(Name=switchName, Unit=1, TypeName="Switch", Image=9, Used=1).Create()
				
					
				Domoticz.Log(str(pinCommand))			
				try:
					call (pinCommand, shell=True)
					Domoticz.Log(str(directionCommand))		
					try:
						call (pinCommand, shell=True)
						call (directionCommand, shell=True)
						try:
							Domoticz.Log("nValue = " + str(Devices[idx + 1].nValue))
							valueCommand = "sudo echo " + str(Devices[idx + 1].nValue) + " > /sys/class/gpio/gpio" + str(pin) + "/value"
							Domoticz.Log(str(valueCommand))
							try:
								call (valueCommand, shell=True)
							except:
								Domoticz.Error("Unable to flip the SYSFS GPIO pin " + str(pin) + " via a shell call")
						except:
							Domoticz.Error("Cannot find switch in Domoticz, will delete in the devices list. Pin: " + str(pin))
							#Devices[idx].Delete()
					except:
						Domoticz.Error("Sorry, unable to set direction of SYSFS GPIO pin " + str(pin) + " via a shell call")
				except:
					Domoticz.Error("Sorry, unable to export SYSFS GPIO pin " + str(pin) + " via a shell call")
					
		else:
			Domoticz.Error("No SYSFS GPIO pins to enable...")			
			

	def onCommand(self, Unit, Command, Level, Hue):
		Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))		
		
		#first, let's flip the switch.
		if str(Command) == "On":
			Devices[Unit].Update(nValue=1,sValue="On")
			valueCommand = "sudo echo 1 > /sys/class/gpio/gpio" + str(self.outpins[Unit - 1]) + "/value"
		if str(Command) == "Off":
			Devices[Unit].Update(nValue=0,sValue="Off")
			valueCommand = "sudo echo 0 > /sys/class/gpio/gpio" + str(self.outpins[Unit - 1]) + "/value"
		
		Domoticz.Log(str(valueCommand))
		try:
			call (valueCommand, shell=True)
		except:
			Domoticz.Error("Unable to flip the SYSFS GPIO pin " + str(pin) + " via a shell call")
	

	def onStop(self):
		Domoticz.Log("onStop called. Starting the unexport of pins.")
		if len(self.pins) > 0:
			for pin in self.pins:
				pinCommand = "sudo echo " + pin + " > /sys/class/gpio/unexport"
				Domoticz.Log(str(pinCommand))
				try:
					call (pinCommand, shell=True)
				except:
					Domoticz.Error("Unable to unexport SYSFS GPIO pin " + str(pin) + " via a shell call")	


	
		
global _plugin
_plugin = BasePlugin()

def onStart():
	global _plugin
	_plugin.onStart()

def onStop():
	global _plugin
	_plugin.onStop()
	
def onCommand(Unit, Command, Level, Hue):
	global _plugin
	_plugin.onCommand(Unit, Command, Level, Hue)	
	
# Generic helper functions
def DumpConfigToLog():
	for x in Parameters:
		if Parameters[x] != "":
			Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
	Domoticz.Debug("Device count: " + str(len(Devices)))
	for x in Devices:
		Domoticz.Debug("Device:		   " + str(x) + " - " + str(Devices[x]))
		Domoticz.Debug("Device ID:	   '" + str(Devices[x].ID) + "'")
		Domoticz.Debug("Device Name:	 '" + Devices[x].Name + "'")
		Domoticz.Debug("Device nValue:	" + str(Devices[x].nValue))
		Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
		Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
	return

def parseCSV(strCSV):
	listvals = []
	for value in strCSV.split(","):
		try:
			val = int(value)
		except:
			pass
		else:
			listvals.append(val)
	return listvals
