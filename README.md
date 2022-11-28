# Lubedude
By Alexander Richter, info@theartoftinkering.com 2022


My CNC Machine has a central lubrication unit, which needs to pump for a couple seconds every two minutes. 
i created this module to make driving it with LinuxCNC easy. 

# +++this is still in early development and doesn't work+++
I publish it in this state to discuss on Forums and chatgroups about it. 

Currently the Software provides: 
- manual input button signal
- Pump Power pin
- lube canister fill sensor


# inner workings
The software reads the Movespeed parameter (XYZvel) of Linuxcnc and if it is greater than 0 (any axis are moving) it will send out a signal to squirt some lube every x minutes. 



# Installation
- move lubedude.py to  /usr/bin and make it executable with chmod +x
- add to your hal file: loadusr lubedude


# License
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

