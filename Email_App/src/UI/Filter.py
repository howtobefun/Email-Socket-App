import re
import os
import shutil
import json
from UI_User import *
from email import message_from_file

class Filter:
    def __init__(self):
        user = User()
        self.USER_MAILBOX_PATH = user.pop3_client.USER_MAILBOX_PATH
        self.INBOX_FOLDER = user.pop3_client.INBOX_FOLDER
        if not os.path.exists(self.INBOX_FOLDER):
            os.mkdir(self.INBOX_FOLDER)
        self.config_data = self.load_config()
        self.school_word_list = self.config_data['school_word_list']
        self.work_word_list = self.config_data['work_word_list']
        self.spam_word_list = self.config_data['spam_word_list']

    def load_config(self):
        config_file_path = 'src/config/filter_config.json'
        with open(config_file_path, 'r') as fp:
            config_data = json.load(fp)

        return config_data

    def __extract_words_and_save(self, input_string):
        words = re.split(',|\.|;|\s|\[|\]', input_string)
        return words

    def __get_filter(self,string_mail_subject,string_mail_body):
        words_in_subject=self.__extract_words_and_save(string_mail_subject)
        words_in_body=self.__extract_words_and_save(string_mail_body)
        
        category_word_lists = {
            'School': self.school_word_list,
            'Work': self.work_word_list,
            'Spam': self.spam_word_list
        }

        for category, word_list in category_word_lists.items():
            if any(word.lower() in words_in_subject for word in word_list):
                return category
            if any(word.lower() in words_in_body for word in word_list):
                return category
        
        return "Others"

    def __get_mail_body(self, complete_path):
        string_mail_body = ""
        with open(complete_path, "r") as fp:
            mail_message = message_from_file(fp)
            for part in mail_message.walk():
                if part.get_content_type() == "text/plain":
                    string_mail_body = part.get_payload(decode=True).decode()
        return string_mail_body

    def filter_all_mails(self): 
        try:
            msg_folders = os.listdir(self.INBOX_FOLDER)
        except FileNotFoundError:
            return
        for msg_folder in msg_folders:
            for msg_file in os.listdir(self.INBOX_FOLDER + msg_folder + '/'):
                complete_path = self.INBOX_FOLDER + msg_folder + '/' + msg_file
                with open(complete_path, "r") as fp:
                    mail_message = message_from_file(fp)
                string_mail_subject = mail_message['Subject']
                string_mail_body = self.__get_mail_body(complete_path)
                self.__filter_mail(msg_folder,msg_file, string_mail_subject, string_mail_body)

    def __filter_mail(self,msg_folder,msg_file, string_mail_subject, string_mail_body):
        folder_type=self.__get_filter(string_mail_subject, string_mail_body)

        folder_type = folder_type + '/'
        mail_class_path = self.USER_MAILBOX_PATH + folder_type + '/'
        source_file = self.INBOX_FOLDER + msg_folder + '/' + msg_file
        destination_file = mail_class_path + msg_folder + '/' + msg_file

        if not os.path.exists(mail_class_path):
            os.mkdir(mail_class_path)
        if not os.path.exists(mail_class_path + msg_folder):
            os.mkdir(mail_class_path + msg_folder)
        
        shutil.copy(source_file, destination_file)


if __name__ == "__main__":
    pass