#!/usr/bin/python3.9
import time#, hal
#	LubeDude for LinuxCNC
#	By Alexander Richter, info@theartoftinkering.com 2022
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
# Button with an LED for manual lube action
c.newpin("manualLube", hal.HAL_BIT, hal.HAL_IN)
c.newpin("SignalLED", hal.HAL_BIT, hal.HAL_IN)
# also there is a sensor which senses if the lube container is empty
c.newpin("LubeFill", hal.HAL_BIT, hal.HAL_IN)

#Outputs 
# Lube Pump is controlled with a Realis
c.newpin("LubePump", hal.HAL_BIT, hal.HAL_IN)

#execute code if this is true:
movevel = hal.get_val("XYZvel.out")
#Logic

c.ready()

pumpon = 5 #seconds turning the pump on
pumpdelay = 2 #wait at least 2 secs between pump cycles
pumpcycle = 15 #seconds have to pass to turn Pump on again if in automode


# Global Variables

isready = 1
movetime = 0

Debug = 0

if Debug:
	manualPump = 1
	movevel = 1
counter = time.time()


def seconds(counter):
    return counter + 1 < time.time()

while True:

	if movevel > 0:
		
		if seconds(counter):
			movetime += 1
			counter = time.time()
			print (movetime)

	if movetime == 0 and isready:
		c.LubePump = 1
		print ("lubeon")
		isready = 0
	
	if movetime == pumpon:
		print ("lubeoff")
		c.LubePump = 0

		
	if movetime == pumpon + pumpdelay and isready == 0:
		isready = 1
		print ("ready")

	if movetime > pumpcycle:
		movetime = 0
		isready = 1

	if c.manualLube and isready:
		movetime = 0

	if c.manualLube:
		if (movetime % 2) == 0:
			c.SignalLED = 1
		else:
			c.SignalLED = 0

	if c.LubeFill == 1 and not c.manualLube:
		c.SignalLED = 1