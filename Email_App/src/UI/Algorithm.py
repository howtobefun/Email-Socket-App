import string
import array
import os
def extract_words_and_save(input_string):
    words = [input_string[start:space_index] for start, space_index in enumerate(input_string.split(' '))]
    words_array = array('str', words)
    return words_array

#trả về loại folder được phân loại, đang tìm cách trả thẳng về folder
def fill_mail(string_mail_subject,string_mail_body):
    words_1=extract_words_and_save(string_mail_subject)
    words_2=extract_words_and_save(string_mail_body)
    target_word_list1 = ['educational','education','study', 'learn', 'student','university','degree','learning']
    if any(word in words_1.lower() for word in target_word_list1):
        return 'Study'
    if any(word in words_2.lower() for word in target_word_list1):
        return 'Study'
    target_word_list2=['job','money','work','employment','employee','schedule','career','business','hire']
    if any(word in words_1.lower() for word in target_word_list2):
        return 'Work'
    if any(word in words_2.lower() for word in target_word_list2):
        return 'Work'

def fill_folder(username, msgID, string_mail_subject, string_mail_body):
    USERS_MAILBOX = "User_Mailbox/"
    USER_MAILBOX_PATH = USERS_MAILBOX + username + "/"
    typefolder=fill_mail(string_mail_subject, string_mail_body)

    if not os.path.exists(USER_MAILBOX_PATH + username):
            os.mkdir(USER_MAILBOX_PATH + username)
            if not os.path.exists(USER_MAILBOX_PATH + username + "/" + msgID + typefolder):
                os.mkdir(USER_MAILBOX_PATH + username + "/" + msgID + typefolder)
#tìm cách chuyển data vào