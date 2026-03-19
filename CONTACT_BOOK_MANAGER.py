import json
class ContactBookManager():
    
    def __init__(self):
        self.ContactJson = "CONTACT_BOOK_CONTACTS.json"

    def LoadContactsJSON(self):
        try:
            with open(self.ContactJson,"r")as Contactfile:
                Contacts = json.load(Contactfile)
                return Contacts
        except:
            return []
        
    def SaveNewContactsJSON(self,contacts):
        try:
            with open(self.ContactJson,"w")as Contactfile:
                json.dump(contacts,Contactfile,indent=4)
        except :
            return []
        
    def addContacts(self,id, name, phone, email):
        AddNewContacts = self.LoadContactsJSON()

        AddNewContacts.append({
            "id":id,
            "name": name,
            "phone": phone,
            "email": email
        })
        self.SaveNewContactsJSON(contacts=AddNewContacts)

    def EditCoontactJSON(self,index,id,name,phone,email):
        MyContactsEdit = self.LoadContactsJSON()
        MyContactsEdit[index] = {
            "id":id,
            "name": name,
            "phone": phone,
            "email": email
            }
        
        self.SaveNewContactsJSON(contacts=MyContactsEdit)

    def DeleteContactJSON(self,index):
        MyContactDelete = self.LoadContactsJSON()
        MyContactDelete.pop(index)
        self.SaveNewContactsJSON(contacts=MyContactDelete)

    def ImportAndReadVCF(self, path):

        contacts = []
        name = ""
        phone = ""
        email = ""

        with open(path, "r", encoding="utf-8") as file:
            RawLines = file.readlines()

        for Data in RawLines:
            StripedLine = Data.strip()
            UpperLine = StripedLine.upper()

            if UpperLine.startswith("FN:"):
                name = StripedLine.split(":",1)[1]

            elif UpperLine.startswith("TEL"):
                phone = StripedLine.split(":")[-1].replace(" ", "")

            elif UpperLine.startswith("EMAIL"):
                email = StripedLine.split(":")[-1]

            elif UpperLine.startswith("END:VCARD"):

                if name == "":
                    name = "Unknown"

                if email == "":
                    email = "Email Not Added"

                contacts.append({
                    "name": name,
                    "phone": phone,
                    "email": email
                })

                name = ""
                phone = ""
                email = ""

        return contacts
    
    def ExportContactsToVCF(self,path):
        ExportContacts = self.LoadContactsJSON()

        with open(path,"w",encoding="utf-8") as FileofContacts:
            for ContactData in ExportContacts:
                
                name = ContactData["name"]
                phone = ContactData["phone"]
                email = ContactData["email"]

                FileofContacts.write("BEGIN:VCARD\n")
                FileofContacts.write("VERSION:3.0\n")
                FileofContacts.write(F"FN:{name}\n")
                FileofContacts.write(F"TEL:{phone}\n")

                if email != "Email Not Added":
                    FileofContacts.write(F"EMAIL:{email}\n")

                FileofContacts.write("END:VCARD\n")
