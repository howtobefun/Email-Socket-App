import string
import array
def extract_words_and_save(input_string):
    words = [input_string[start:space_index] for start, space_index in enumerate(input_string.split(' '))]
    words_array = array('str', words)
    return words_array

def fill_mail(string_mail):
    words=extract_words_and_save(string_mail)
    target_word_list = ['study', 'learn', 'student']
    if any(word in words for word in target_word_list):
        return 'School folder'
  