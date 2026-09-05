import sqlite3


class ContactBookManager:
    def __init__(self, db_path="books/Default.db"):
        self.db_path = db_path
        self._EnsureSchema()

    def _Connect(self):
        return sqlite3.connect(self.db_path)

    def _EnsureSchema(self):
        conn = self._Connect()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                device_ip TEXT DEFAULT ''
            )
        """)
        conn.commit()
        conn.close()

    def SetDatabase(self, db_path):
        self.db_path = db_path
        self._EnsureSchema()

    def LoadContactsJSON(self):
        conn = self._Connect()
        rows = conn.execute("SELECT id, name, phone, email, device_ip FROM contacts ORDER BY id").fetchall()
        conn.close()
        return [
            {"id": row[0], "name": row[1], "phone": row[2], "email": row[3], "device_ip": row[4] or ""}
            for row in rows
        ]

    def addContacts(self, id, name, phone, email, device_ip=""):
        conn = self._Connect()
        conn.execute(
            "INSERT INTO contacts (name, phone, email, device_ip) VALUES (?, ?, ?, ?)",
            (name, phone, email, device_ip)
        )
        conn.commit()
        conn.close()

    def EditCoontactJSON(self, index, id, name, phone, email, device_ip=""):
        contacts = self.LoadContactsJSON()
        target_id = contacts[index]["id"] if 0 <= index < len(contacts) else id

        conn = self._Connect()
        conn.execute(
            "UPDATE contacts SET name=?, phone=?, email=?, device_ip=? WHERE id=?",
            (name, phone, email, device_ip, target_id)
        )
        conn.commit()
        conn.close()

    def DeleteContactJSON(self, index):
        contacts = self.LoadContactsJSON()

        if not (0 <= index < len(contacts)):
            return

        target_id = contacts[index]["id"]

        conn = self._Connect()
        conn.execute("DELETE FROM contacts WHERE id=?", (target_id,))
        conn.commit()
        conn.close()

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
                name = StripedLine.split(":", 1)[1]

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

    def ExportContactsToVCF(self, path):
        ExportContacts = self.LoadContactsJSON()

        with open(path, "w", encoding="utf-8") as FileofContacts:
            for ContactData in ExportContacts:

                name = ContactData["name"]
                phone = ContactData["phone"]
                email = ContactData["email"]

                FileofContacts.write("BEGIN:VCARD\n")
                FileofContacts.write("VERSION:3.0\n")
                FileofContacts.write(f"FN:{name}\n")
                FileofContacts.write(f"TEL:{phone}\n")

                if email != "Email Not Added":
                    FileofContacts.write(f"EMAIL:{email}\n")

                FileofContacts.write("END:VCARD\n")
