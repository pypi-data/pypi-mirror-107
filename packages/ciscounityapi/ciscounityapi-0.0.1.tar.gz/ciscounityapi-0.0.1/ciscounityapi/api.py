import requests
import json


class api(object):
    def __init__(self, cucIP, username, password):
        self.cucIP = cucIP
        self.username = username
        self.password = password

    def get(self, query):
        r = requests.get("https://" + self.cucIP+query, headers = {'Accept': 'application/json'}, auth=(self.username, self.password), verify=False)
        if r.status_code == 200:
            return r.json()

    def post(self, query, data):
        r = requests.post("https://" + self.cucIP+query, data = data, headers = {'Accept': 'application/json','Content-Type': 'application/xml'}, auth=(self.username, self.password), verify=False)
        return r

    def put(self, query, data):
        r = requests.put("https://" + self.cucIP+query, data = data, headers = {'Accept': 'application/json','Content-Type': 'application/xml'}, auth=(self.username, self.password), verify=False)
        return r

    def delete(self, query):
        r = requests.delete("https://" + self.cucIP+query, headers = {'Accept': 'application/json'}, auth=(self.username, self.password), verify=False)
        return r

    # callable Functions 
    def getUserWithMbx(self, userID):
        return self.get(query = "/vmrest/users?query=(alias is "+userID+")")
    
    def getUserLDAP(self, userID):
        return self.get(query = "/vmrest/import/users/ldap?query=(alias is "+userID+")")
        
    def postUserImportLDAP(self, templateName, userID, cucIimportuserPkid, phoneNumber):
        data = "<ImportUser>\r\n <alias>"+userID+"</alias>\r\n <pkid>"+cucIimportuserPkid+"</pkid>\r\n <dtmfAccessId>"+phoneNumber+"</dtmfAccessId>\r\n</ImportUser>"
        return self.post(query = "/vmrest/import/users/ldap?templateAlias="+templateName, data=data)

    def getUserExtensions(self, cucUserObjectID):
        return self.get(query = "/vmrest/users/"+cucUserObjectID+"/alternateextensions")

    def getUserMbxAttr(self, cucUserObjectID):
        return self.get(query = "/vmrest/users/"+cucUserObjectID+"/mailboxattributes")

    def getUserWithMbxAttr(self, cucUserCallHandlerObjectId):
        return self.get(query = "/vmrest/users/"+cucUserCallHandlerObjectId)
    
    def getUserGreetings(self, cucUserCallHandlerObjectId):
        return self.get(query = "/vmrest/handlers/callhandlers/"+cucUserCallHandlerObjectId+"/greetings")

    def putUserCity(self, cucUserCallHandlerObjectId, location):
        data ="<User>\r\n<City>"+location+"</City>\r\n</User>\r\n"
        return self.put(query="/vmrest/users/"+cucUserCallHandlerObjectId, data=data)

    def getUserDependency(self, cucUserObjectID):
        return self.get(query="/vmrest/subscriberdependencies/"+cucUserObjectID)
    
    def deleteUserWithMbx(self, cucUserObjectID):
        return self.delete(query="/vmrest/users/"+cucUserObjectID)
    
    def createLocalEndUser(self, userID, phoneNumber, mail, location):
        data="<User>\r\n  <Alias>"+userID+"</Alias>\r\n  <DtmfAccessId>"+phoneNumber+"</DtmfAccessId>\r\n  <EmailAddress>"+mail+"</EmailAddress>\r\n</User>\r\n"
        return self.post(query="/vmrest/users?templateAlias="+location+"-IIQ", data=data)

    def localEndUserToLDAP(self, cucUserObjectID):
        data="<User>\r\n  <LdapType>3</LdapType>\r\n</User>\r\n"
        return self.post(query="##/vmrest/users?"+cucUserObjectID, data=data)
