import requests

def main():
    with open("names.txt") as file:
        for line in file:
            charID = getCharID(line)
            if charID is not "DNE":
                corpID = getCorporationID(str(charID['character'][0]))
                corpNameAndAllianceID = getCorporationNameAndAllianceID(corpID)
                corpName = corpNameAndAllianceID[0]
                allianceID = corpNameAndAllianceID[1]
                allianceName = getAllianceName(allianceID)
                print(line.replace('\n', "") + ": " + corpName + ": " + allianceName)

def getAllianceName(allianceID):
    allianceJsonData = requests.get(buildUrl("alliances", allianceID)).json()
    return allianceJsonData['name'] # Returns the allianceName

def getCorporationID(charID):
    corporationJsonData = requests.get(buildUrl("characters", charID)).json()
    return corporationJsonData['corporation_id'] # Returns the CorporationID

def getCorporationNameAndAllianceID(corpID):
    corpNameAndAllianceID = []
    corporationJsonData = requests.get(buildUrl("corporations", corpID)).json()
    corpNameAndAllianceID.append(corporationJsonData['name'])
    if 'alliance_id' in corporationJsonData:    # If there is an allianceID
        corpNameAndAllianceID.append(corporationJsonData['alliance_id'])
    else:   # Else set the allianceID to '434243723' which is zCCP's alliance ID
        corpNameAndAllianceID.append('434243723')
    return corpNameAndAllianceID

def getCharID(name):
    url = buildCharacterSearchUrl(name.replace(" ", "%20"))
    charData = requests.get(url).json() # Returns the Char ID from the search
    if 'character' in charData: # If the charecter exists
        return charData
    else:   # Else return DNE (Does not exist)
        return 'DNE'

def buildCharacterSearchUrl(name):
    return "https://esi.tech.ccp.is/latest/search/?categories=character&datasource=tranquility&language=en-us&search=" + name + "&strict=true"

def buildUrl(type, id):
    return "https://esi.tech.ccp.is/latest/" + type + "/" + str(id) + "/?datasource=tranquility"    # Type is the api endpoint to hit

main()