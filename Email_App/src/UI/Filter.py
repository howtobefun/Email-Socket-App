import re
import os
import shutil
from UI_User import *
from email import message_from_file

class Filter:
    def __init__(self):
        user = User()
        self.USER_MAILBOX_PATH = user.pop3_client.USER_MAILBOX_PATH
        self.MAIL_RECEIVED_FOLDER = user.pop3_client.MAIL_RECEIVED_FOLDER

    def __extract_words_and_save(self, input_string):
        words = re.split(',|\.|;|\s|\[|\]', input_string)
        return words

    #trả về loại folder được phân loại, đang tìm cách trả thẳng về folder
    def __get_filter(self,string_mail_subject,string_mail_body):
        words_in_subject=self.__extract_words_and_save(string_mail_subject)
        words_in_body=self.__extract_words_and_save(string_mail_body)

        target_word_list1 = ['educational','education','study', 'learn', 'student','university','degree','learning']
        if any(word.lower() in words_in_subject for word in target_word_list1):
            return 'Study'
        if any(word.lower() in words_in_body for word in target_word_list1):
            return 'Study'
        target_word_list2=['job','money','work','employment','employee','schedule','career','business','hire']
        if any(word.lower() in words_in_subject for word in target_word_list2):
            return 'Work'
        if any(word.lower() in words_in_body for word in target_word_list2):
            return 'Work'
        else: return None

    def __get_mail_body(self, complete_path):
        string_mail_body = ""
        with open(complete_path, "r") as fp:
            mail_message = message_from_file(fp)
            for part in mail_message.walk():
                if part.get_content_type() == "text/plain":
                    string_mail_body = part.get_payload(decode=True).decode()
        return string_mail_body

    def filter_all_mails(self):    
        for msg_folder in os.listdir(self.MAIL_RECEIVED_FOLDER):
            for msg_file in os.listdir(self.MAIL_RECEIVED_FOLDER + msg_folder + '/'):
                complete_path = self.MAIL_RECEIVED_FOLDER + msg_folder + '/' + msg_file
                with open(complete_path, "r") as fp:
                    mail_message = message_from_file(fp)
                    string_mail_subject = mail_message['Subject']
                    string_mail_body = self.__get_mail_body(complete_path)
                    self.__filter_mail(msg_folder,msg_file, string_mail_subject, string_mail_body)

    def __filter_mail(self,msg_folder,msg_file, string_mail_subject, string_mail_body):
        folder_type=self.__get_filter(string_mail_subject, string_mail_body)

        if folder_type is None:
            return

        folder_type = folder_type + '/'
        mail_class_path = self.USER_MAILBOX_PATH + folder_type + '/'
        source_file = self.MAIL_RECEIVED_FOLDER + msg_folder + '/' + msg_file
        destination_file = mail_class_path + msg_folder + '/' + msg_file

        if not os.path.exists(mail_class_path):
            os.mkdir(mail_class_path)
        if not os.path.exists(mail_class_path + msg_folder):
            os.mkdir(mail_class_path + msg_folder)
        
        shutil.copy(source_file, destination_file)