#!/usr/bin/env python3
from flask import Flask, jsonify
from flask import request

main = Flask(__name__)

#storing the device profiles in a dictionary where the key is the id of the device.
deviceProfile = {}
#storing the location of a device in a dictionary where the key is the id of the device.
currentLocations = {}

#Creates a radio profile with the given id, alias and allowed locations
@main.route('/POST/radios/<int:id>', methods=['POST'])
def postRadioProfile(id):
    locationList = []
    for location in request.json["allowed_locations"]:
        locationList.append(location)
    #saved the alias and the allowed locations of the device.
    profile = {
            "alias": request.json["alias"],
            "allowed_locations": locationList
    }
    #the profile is then stored in a dectionary where the id is the key
    deviceProfile[id] = profile
    return jsonify({'profile': profile}), 201

#ask for a location and if the location is allowed sets it as the radios(ids) location
@main.route('/POST/radios/<int:id>/location', methods=['POST'])
def postRadioLocation(id):
    forbiddenLocation = True
    #check if id is in deviceProfile
    if id in deviceProfile:
        #get the new locaion
        newLocation = request.json["location"]
        if newLocation != "":
            #compares the new location with the allowed location
            for location in deviceProfile[id]["allowed_locations"]:
                if location == newLocation:
                    forbiddenLocation = False
                    #saved the new location and EXIT's
                    currentLocations[id] = newLocation
                    return "200 OK" #jsonify({'new location': newLocation}),
                    break

    #if the new location does not mach any of the allowed location 403 FORBIDDEN is reported back.
    if forbiddenLocation:
        return "403 FORBIDDEN"


#function check if id is in both divice profile and currentLocations for the device.
@main.route('/GET/radios/<int:id>/location', methods=['GET'])
def getRadioLocation(id):
    #check if id is in deviceProfile and if the id has a location
    if id in deviceProfile and id in currentLocations:
        return ("200 OK " + "{\"location\": " + currentLocations[id] + "}")
    else:
        return ("404 NOT FOUND")


if __name__ == '__main__':
    main.run(host='0.0.0.0')#, debug=True)
