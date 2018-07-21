##import xml.etree.ElementTree as ET
##charTree = ET.parse('DATA\\characters.xml')
##charRoot = charTree.getroot()
##
##for child in charRoot:
##    print(charRoot[0][0].text)


##import sys
##sys.path.insert(0, 'CLASSES')
##
##import tkinter as tk
##
##main = tk.Tk()
##
##import UI_HUB
##
##ui = UI_HUB.UI(main)
##
##import charClass
##
##Scavenger = charClass.playerCharacter("Scavenger", "R1")
##Scavenger.whatsMine()

import sys
import random
import tkinter as tk
import UI_HUB
import xml.etree.ElementTree as ET
#from SPINE import *
sys.path.insert(0, 'CLASSES')
main = tk.Tk()
ui = UI_HUB.UI(main)
import charClass, placeClass, doorClass, invFurnClass

location = "miningPlatform01"
rooms = []
roomTree = ET.parse('DATA\\rooms.xml')
roomRoot = roomTree.getroot()
for child in roomRoot:
    if child.attrib["name"] == location:
        for subchild in child:
            rooms.append(placeClass.Place(subchild.attrib["name"], int(subchild[0].text), [elem.text for elem in subchild[1]], [elem.text for elem in subchild[2]], [elem.text for elem in subchild[3]],
                                          subchild[4].text, subchild[5].text))
            
#currentDoors = []
doorTree = ET.parse('DATA\\doors.xml')
doorRoot = doorTree.getroot()
checkVal = False #cuz if it creates an invalid door, I don't want to stuff to mess up, so if it's invalid it gets deleted

for child in doorRoot:
    if child.attrib["name"] == location:
        for subchild in child:
            temp = doorClass.Door(subchild.attrib["name"], subchild[0].text, subchild[1].text, int(subchild[2].text),
                                  [eval(subchild[3][0].text),subchild[3][1].text,subchild[3][2].text], [eval(subchild[4][0].text), subchild[4][1].text],
                                  eval(subchild[5].text), eval(subchild[6].text), subchild[7].text, eval(subchild[8].text))
            temp.hidden = False
            #print(temp.blocked)
            
            for room in rooms:
                if room.name in subchild.attrib["name"]:
                    if room.name == subchild[0].text:
                        temp.room1 = room
                    elif room.name == subchild[1].text:
                        temp.room2 = room
                        
                    room.doors.append(temp)
                    checkVal = True
                    
            if checkVal == False:
                print("deleting door")
                del temp



furnTree = ET.parse('DATA\\roomFurnishings.xml')
furnRoot = furnTree.getroot()
vitalFurns = {}
furnishingList = []
for room in rooms:
    for furn in room.furnishings:
        if furn is not None:
            vitalFurns[furn] = room

for child in furnRoot:
    if child.attrib["name"] in vitalFurns:
        vitalFurns[child.attrib["name"]].furnishings.append(invFurnClass.roomFurnishing(child[0].text, child[1].text, child[2].text,
                                                                                        [eval(child[3][0].text), [elem.text for elem in child[3][1]]], [elem.text for elem in child[4]],
                                                                                        [eval(child[5][0].text), eval(child[5][1].text)], [eval(child[6][0].text),
                                                                                        [elem.text for elem in child[6][1]]],
                                                                                        [eval(child[7][0].text), child[7][1].text],
                                                                                        [eval(child[8][0].text), child[8][1].text, eval(child[8][2].text)]))
        vitalFurns[child.attrib["name"]].furnishings.remove(child.attrib["name"])
                                                         #note: currently does not access 'hidden'. I could change that later.    

for room in rooms:
    print(room.furnishings)
    if not room.furnishings == []:
        for furnishing in room.furnishings:
            furnishingList.append(furnishing)
print(furnishingList)
        

invTree = ET.parse('DATA\\inventoryObjects.xml')
invRoot = invTree.getroot()
vitalInv = {}
for room in rooms:
    if len(room.objects) > 0:
        for obj in room.objects:
            vitalInv[obj] = room

for child in invRoot:
    if child.attrib["name"] in vitalInv:
        vitalInv[child.attrib["name"]].objects.append(invFurnClass.inventoryObject(child.attrib["name"], child[0].text, child[1].text, [eval(child[2][0].text), child[2][1].text],
                                                                                   [eval(child[3][0].text), child[3][1].text], eval(child[4].text),
                                                                                   [eval(child[5][0].text), [elem.text for elem in child[5][1]]], eval(child[6].text),
                                                                                   [eval(child[7][0].text), child[7][1].text], [child[8][0].text, child[8][1].text]))
        vitalInv[child.attrib["name"]].objects.remove(child.attrib["name"])
            
for room in rooms:
    print("objects")
    print(room.objects)
##vitalInv = {}
##for furn in furnishingList:
##    if furn.containedObjects < 0:
##        for obj in furn.containedObjects:
##            vitalInv[obj] = furn


playerCharacter = charClass.playerCharacter("Scavenger", rooms[0])
playerCharacter.whatsMine()

