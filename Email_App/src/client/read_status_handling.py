import json
import os

class ReadStatusHandling:
    def __init__(self, email: str):
        self.email = email
        self.USERS_MAILBOX = "User_Mailbox/"
        self.USER_MAILBOX_PATH = self.USERS_MAILBOX + self.email + "/"
        self.read_status_file_path = self.USER_MAILBOX_PATH + "read_status.json"

        self.data = {}

        if not os.path.exists(self.read_status_file_path):
            self.__create_read_status_file()
        else:
            with open(self.read_status_file_path, 'r') as fp:
                self.data = json.load(fp)
            if (self.data == {}):
                self.data = self.__generate_data()

    def get_read_status(self):
        return self.data

    def __generate_data(self):
        data = {}
        try: 
            dirs = os.listdir(self.USER_MAILBOX_PATH)
        except:
            return data
        
        for dir in dirs:
            if os.path.isfile(self.USER_MAILBOX_PATH + dir) | (dir == 'Attachments'):  
                continue
            msg_folders = os.listdir(self.USER_MAILBOX_PATH + dir)
            for msg_folder in msg_folders:
                msg_files = os.listdir(self.USER_MAILBOX_PATH + dir + "/" + msg_folder)
                for msg_file in msg_files:
                    if data.get(msg_file) == None:
                        data[msg_file] = False

        return data
    
    def write_read_status(self, data: dict):
        with open(self.read_status_file_path, 'w') as fp:
            json.dump(data, fp)

    def __create_read_status_file(self):
        self.data = self.__generate_data()
        with open(self.read_status_file_path, 'w') as fp:
            json.dump(self.data, fp)

if __name__ == "__main__":
    pass