#!/usr/bin/env python3
import json
deviceProfile = {}
currentLocations = {}

#Creates a radio profile with the given id, alias and allowed locations
def postRadioProfile(id, Payload):
    #data = input("Enter Payload(json)")
    extractedData = json.loads(Payload)
    #print(extractedData)
    if extractedData["alias"] != "" and extractedData["allowed_locations"] != "":
        #save data and EXIT's
        deviceProfile[id] = extractedData

#ask for a location and if the location is allowed sets it as the radios(ids) location
def postRadioLocation(id, Payload):
    #ask for json data
    #data = input("Enter Payload(json)")
    extractedData = json.loads(Payload)
    #extract the new location from json
    newLocation = extractedData["location"]
    if newLocation != "":
        forbiddenLocation = True
        #compares the new location with the allowed location
        for location in deviceProfile[id]["allowed_locations"]:
            if location == newLocation:
                forbiddenLocation = False
                #saved the new location and EXIT's
                currentLocations[id] = newLocation
                print("200 OK")
                break

        #if the new location does not mach any of the allowed location 403 FORBIDDEN is reported back.
        if forbiddenLocation:
            print("403 FORBIDDEN")

        #save data and EXIT
        #deviceProfile[id] = extractedData


def getRadioLocation(id):
    print("200 OK " + "{\"location\": " + currentLocations[id] + "}")




def enter_Command(command, payload):

    global isDone
    #data = input("Please enter command ")
    #splits the input data by "/"
    array = command.split("/")

    print(command)
    print(payload)
    #check if it was a POST command that was entered
    if array[0]+"/"+array[1] == "POST/radios":
        #if the length of the array and the last value in the array is location
        if array[-1] == "location":
            if array[2] in deviceProfile:
                postRadioLocation(array[2], payload)
        elif array[-1].isnumeric():
            #print("1")
            postRadioProfile(array[2], payload)
    elif array[0]+"/"+array[1] == "GET/radios":
        if array[2] in deviceProfile and array[2] in currentLocations:
            #print("3")
            getRadioLocation(array[2])
        else:
            print("404 NOT FOUND")

scenario1 = True
#scenario1 = False
scenario2 = True
#scenario2 = False
#Scenario 1:
if scenario1:
    print("Scenario 1:")
    enter_Command("POST/radios/100", "{ \"alias\": \"Radio100\", \"allowed_locations\": [\"CPH-1\", \"CPH-2\"] }")
    enter_Command("POST/radios/101", "{ \"alias\": \"Radio101\", \"allowed_locations\": [\"CPH-1\", \"CPH-2\", \"CPH-3\"] }")

    #print(deviceProfile)


    enter_Command("POST/radios/100/location", "{ \"location\": \"CPH-1\" }")
    enter_Command("POST/radios/101/location", "{ \"location\": \"CPH-3\" }")
    enter_Command("POST/radios/100/location", "{ \"location\": \"CPH-3\" }")

    #print(currentLocations)

    enter_Command("GET/radios/101/location", "")
    enter_Command("GET/radios/100/location", "")

print("")
print("")
print("")
#Scenario 2:
if scenario2:
    print("Scenario 2:")
    enter_Command("POST/radios/102", "{ \"alias\": \"Radio102\", \"allowed_locations\": [\"CPH-1\", \"CPH-3\"] }")
    enter_Command("GET/radios/102/location", "")
