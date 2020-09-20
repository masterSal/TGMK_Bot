#!/usr/bin/env python3
#
#
#

import os
import json
import glob
import time
import sys

sys.path.append("src\\")

from ConfigRead import ConfigRead


try:
    import telethon
    from telethon import utils
    from telethon import TelegramClient, events, sync
    from telethon.tl.functions.channels import GetParticipantsRequest
    from telethon.tl.functions.channels import GetFullChannelRequest
    from telethon.tl.types import ChannelParticipantsSearch
except:
    print("[-] telethon not found!")
    print("[*] pip install telethon")
    exit(1)





class UserBot(ConfigRead):

    def __init__(self):
        self.config = None

        super().__init__("config.ini")

        self.SESSION_NAME = "black_session"
        self.api_id = self.getVal("API", "api_id")
        self.api_hash = self.getVal("API", "api_hash")
        self.phone = self.getVal("CREDENTIALS", "phone")
        self.passwd = self.getVal("CREDENTIALS", "passwd")
        self.groups = {}
        self.msg = ""

        self.client = TelegramClient(self.SESSION_NAME, self.api_id, self.api_hash)
    

    def tgStart(self):
        self.client.start()
    

    def getMe(self):
        me = self.client.get_me()
        print("==> ME: " + me.stringify())
    
    def sendMessage(self, to, msg):
        self.client.send_message(to, msg)
    

    def getMsg(self, usr, lim=10):
        for msg in self.client.get_dialog(limit=int(lim)):
            print(utils.get_display_name(msg.sender), msg.message)
    

    def getDialogs(self):
        return self.client.get_dialogs()
    

    @staticmethod
    def jsonConvert(key, value):
        j = {}
        j[key] = value

        return json.dumps(j)


    @staticmethod    
    def groupJsonLoads():
        print("[*] Looking for a latest file...")

        list_ = glob.glob("data\\groups\\*")
        latestFile = max(list_, key=os.path.getctime)

        print("[+] File found: ", latestFile)

        f = open(latestFile, 'r')
        r = f.read()
        f.close()

        return json.loads(r)
    

    def jsonGroupNameWrite(self):
        if glob.glob('data\\groups\\'):
            json_file = "group_name_" + time.asctime().replace(':', '-') + ".json"
            

            # json write
            g_data = self.jsonConvert("groups", self.groups)

            print("[*] Writing file: ", json_file)
            with open("data\\groups\\" + json_file, 'w') as f:
                f.write(g_data)
                f.close()
        else:
            print("[-] Error: 'groups' directory not found.")
            exit(0)
        
    
    def jsonUsersWrite(self, part, name=""):
        if glob.glob("data\\users\\"):
            json_file = "user_name_(" + name + ")_" + time.asctime().replace(':', '-') + ".json"

            # json Write
            g_data = self.jsonConvert("users", part)

            print("[*] Writing file: ", json_file)
            with open("data\\users\\" + json_file, 'w') as f:
                f.write(g_data)
                f.close()
        else:
            print("[-] Erro: 'users' directory not found.")
            exit(1)
    
    
    def filterGroups(self):
        print("[*] Filtering groups...")
        for group in self.getDialogs():
            try:
                if group.entity.megagroup:

                    try:
                        count = self.client.get_participants(group.entity.title).total
                    except telethon.errors.rpcerrorlist.ChatAdminRequiredError:
                        print("[-] Error: Chat Admin is required, Group: ", group.name)
                        continue
                    
                    print("\t\t[+] Group name: ", group.name, " Count: ", count)
                    
                    self.groups[group.name] = {
                                                "id": group.entity.id,
                                                "title": group.entity.title,
                                                "username": group.entity.username,
                                                "count": count
                                                }
                else:
                    pass
            except AttributeError:
                # print("[-] Error: ", group.name)
                pass
            
        print("==> Total Groups: ", len(self.groups))
        self.jsonGroupNameWrite()
    
    
    def getChannelUsers(self):
    
        my_filter = ChannelParticipantsSearch('')
        all_groups = self.groupJsonLoads()

        for grp in all_groups["groups"]:

            usr_name = all_groups["groups"][grp]["username"]
            title = all_groups["groups"][grp]["title"]
            limit = all_groups["groups"][grp]["count"]        
            offset = 0

            all_participants = {}

            if usr_name == None: continue

            print("==========> Group: ", title)
            self.client(GetFullChannelRequest(usr_name))
            
        
            while True:
                part = self.client(GetParticipantsRequest(channel=usr_name, filter=my_filter, offset=offset, limit=limit, hash=0))
                for usr in part.users:
                    if usr.deleted == True: continue
                    
                    all_participants[usr.username] = {
                        "id": usr.id,
                        "first_name": usr.first_name,
                        "last_name": usr.last_name,
                        "username": usr.username,
                        "phone": usr.phone
                    }

                    print("[+] Adding: ", usr.username, "...")
                
                offset += len(part.users)
                if len(part.users) < limit:
                    break
            
            self.jsonUsersWrite(all_participants, title)
            














def main():
    print("=> Starting userBot!")
    ub = UserBot()
    ub.tgStart()

    ub.getChannelUsers()
    ub.filterGroups()


if __name__ == "__main__":
    main()
