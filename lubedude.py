#!/usr/bin/python3.9
import time, hal

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
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


c = hal.component("lubedude") #name that we will cal pins from in hal
#Pin Setup

#Inputs 

# i have a Button with an LED for manual lube action
c.newpin("LubeBtn", hal.HAL_BIT, hal.HAL_IN)
c.newpin("LubeBtnLED", hal.HAL_BIT, hal.HAL_IN)
# also there is a sensor which senses if the lube container is empty
c.newpin("LubeFill", hal.HAL_BIT, hal.HAL_IN)

#execute code if this is true:
c.newpin("moveSpeed", hal.HAL_FLOAT, hal.HAL_IN)

#Outputs 
# Lube Pump is controlled with a Realis
c.newpin("LubePump", hal.HAL_BIT, hal.HAL_IN)

#Logic

timeon = 10 #seconds turning the pump on

automodetimer = 180 #seconds have to pass to turn Pump on again if in automode

blinkLED = 1 # blink LED if Tank is empty turn 0 if you want steady light.

# Global Variables
constanttime = 2 
autolubemode = 0
lubeemtpy = 0
timeonT = time.time()
automodetimerT = time.time()
Debug = 1

c.ready()

def Lubeaction(newtime):
    while 1 != (newtime + timeon < time.time()):
					print("lubing")


def autotimer(event):
    return event + automodetimer < time.time()	


while True:

	while c.LubeBtn == 1: #if button is pressed
		c.LubeBtnLED = 1 #turn LED on
		if Lubeaction(timeon):
			c.LubePump = 1 #turn Pump on
		if Debug == 1: print ("turning LubePump on")


		event = time.time()