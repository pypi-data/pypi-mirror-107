import requests
import json
import yaml
import base64

class simulation:

    def __init__(self,token,simPath,numImages):
        self.token = token
        self.name = "works"
        self.numImages = numImages
        self.progress = ""
        self.simID = 0
        self.userID = 0
        self.dataID = 0
        self.simPath = simPath
        self.simEncodedstr = "simEncodedstr"
        self.datasetURL = "datasetURL"
        self.simulations = ""
        self.numSimulations = 0
        self.isComplete = False
        self.dataSetItems = ""
        self.numRendered = 0
        self.progress = "you have rendered "+ str(self.numRendered) + "(images including image annotations) out of a total of " + str(self.numImages)

    def createSimulation(self):
        url = "https://lexsetapi.azurewebsites.net/api/Simulations/NewSimulation"

        #encode the config in Base64
        with open(self.simPath) as fast:
            simString = json.dumps(yaml.load(fast))
            simEncoded = base64.b64encode(simString.encode("utf-8"))
            self.simEncodedstr = str(simEncoded, "utf-8")

        payload = json.dumps({
          "id": 0,
          "userid": 1,
          "simulationconfig": self.simEncodedstr,
          "randomseed": 1,
          "renderjobid": 0,
          "imagecount": self.numImages
        })
        headers = {
          'Authorization': 'Bearer ' + self.token,
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        parseResponse = json.loads(response.text)

        #update simulation IDs
        self.simID = parseResponse["id"]
        self.dataID = parseResponse["datasetid"]
        self.userID = parseResponse["userid"]

    def startSimulation(self):
        url = "https://lexsetapi.azurewebsites.net/api/Simulations/StartSimulation?id=" + str(self.simID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

    def getStatus(self):
        url = "https://lexsetapi.azurewebsites.net/api/simulations/getsimulationstatus?id=" + str(self.simID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        #update if sim is complete or not complete
        parseResponse = json.loads(response.text)
        self.isComplete = parseResponse["isComplete"]

    def getDatasetItems(self):
        url = "https://lexsetapi.azurewebsites.net/api/datasetitems/getdatasetitems?dataset_id=" + str(self.dataID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        #return the dataSetItems and check the status/progress
        parseResponse = json.loads(response.text)
        self.dataSetItems = json.loads(response.text)
        self.numRendered = len(self.dataSetItems)
        self.progress = "you have rendered "+ str(self.numRendered) + " out of " + str(self.numImages)

    def stopSimulation(self):
        url = "https://lexsetapi.azurewebsites.net/api/simulations/stopsimulation?id=" + str(self.simID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)

    def downloadData(self):
        url = "https://lexsetapi.azurewebsites.net/api/datasets/getdatasetarchives?dataset_id=" + str(self.dataID)

        payload={}
        headers = {
        'Authorization': 'Bearer ' + self.token
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        parseResponse = json.loads(response.text)
        print("Response:")
        print(response.text)
        self.datasetURL = parseResponse[0]["url"]

def getSimulations(userID,token):
    url = "https://lexsetapi.azurewebsites.net/api/simulations/GetActiveSimulations/?userid=" + str(userID)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + str(token)
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    #print(response.text)
    parseResponse = json.loads(response.text)
    #print("Response:")
    #print(response.text)
    simulations = parseResponse
    return(simulations)

def addPlacementRules(userID,fileName,filePath):
    url = "http://coreapi.lexset.ai/api/UserDataManagement/uploaduserfile"

    payload = {'userid': userID}

    headers = {}

    files=[('files',(fileName,open(str(filePath)+str(fileName),'rb'),'application/json'))]

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)

def listPlacementRules(userID):
    url = "http://coreapi.lexset.ai/api/UserDataManagement/getplacementfiles?userid=" + str(userID)

    payload = {}

    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    print("uploadedFiles")
    print(response.text)

def stopSimulation(simID):
    url = "https://lexsetapi.azurewebsites.net/api/simulations/stopsimulation?id=" + str(simID)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + self.token
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)

def startSimulation(simID):
    url = "https://lexsetapi.azurewebsites.net/api/Simulations/StartSimulation?id=" + str(simID)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + self.token
    }

    response = requests.request("POST", url, headers=headers, data=payload)

def downloadData(dataID,toke):
    url = "https://lexsetapi.azurewebsites.net/api/datasets/getdatasetarchives?dataset_id=" + str(dataID)

    payload={}
    headers = {
    'Authorization': 'Bearer ' + token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    parseResponse = json.loads(response.text)
    datasetURL = parseResponse[0]["url"]
    return(datasetURL)
