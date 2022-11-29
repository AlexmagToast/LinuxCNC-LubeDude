#!/usr/bin/python3.9
import time, hal
#	LubeDude for LinuxCNC
#	By Alexander Richter, info@theartoftinkering.com 2022
#	Please consider supporting me on Patreon.com/theartoftinkering
#
#	This Program provides support for Central Lubrication Units.
#	Currently supported is a Pump which is run 10 sec to build pressure and then shut off. 
# 	 The Software reads from LinuxCNC if any Axis are moving. After a time of configurable Seconds of movement 
#	the Pump is turned on again. It doesn't run if the machine is not moving.
#
#	There is a pin for Manual Lube pumping, which will also trigger a lube cycle and, if triggered while the machine moves
#	resets the timer, so the Pump won't run until the specified time has passed after. 
#
#
#	Also a Fill sensor is supported, but it only triggers the Signal LED constantly at the moment. 
#
#
#
#	This program is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; either version 2 of the License, or
#	(at your option) any later version.
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#	See the GNU General Public License for more details.
#	You should have received a copy of the GNU General Public License
#	along with this program; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  US


c = hal.component("lubedude") #name that we will cal pins from in hal
#Pin Setup

#Inputs 
c.newpin("manualLube", hal.HAL_BIT, hal.HAL_IN)
c.newpin("SignalLED", hal.HAL_BIT, hal.HAL_OUT)
c.newpin("LubeFill", hal.HAL_BIT, hal.HAL_IN)
#Outputs
c.newpin("LubePump", hal.HAL_BIT, hal.HAL_OUT)


c.ready()


pumpon = 10 #seconds turning the pump on
pumpdelay = 2 #wait at least 2 secs between pump cycles
pumpcycle = 120 #seconds have to pass to turn Pump on again if axis are moving


# Global Variables

isready = 1
movetime = 0

counter = time.time()


def seconds(counter):
    return counter + 1 < time.time()

while True:
	movevel = hal.get_value("XYZvel")
	if movevel != 0 or not isready:
		if movetime == 0 and isready:
			c.LubePump = 1
			isready = 0
			
		if seconds(counter):
			movetime += 1
			counter = time.time()
			print (movetime)

	if movetime == pumpon:
		c.LubePump = 0

		
	if movetime == pumpon + pumpdelay and isready == 0:
		isready = 1

	if movetime > pumpcycle:
		movetime = 0
		isready = 1

	if c.manualLube == 1 and isready:
		if isready: movetime = 0
		c.LubePump = 1
		
		isready = 0


	if c.LubeFill == 1 or c.LubePump == 1:
		c.SignalLED = 1
	else:
		c.SignalLED = 0
