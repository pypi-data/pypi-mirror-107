import os
import string 
import re

from docx import Document


def get_list_of_files(path):
    '''
    A function to fetch list of names (with extension, without full path) of all files from a folder

    Parameters:
        path : A string containing the path of the directory

        Returns a python list
    '''
    # returns a  of all files 
    # in folder path
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files


def get_list_of_folders(path):
    '''
    returns a list of names (with extension, without full path) of all files in folder path
    Parameters:
        path : A string containing the path of the directory

        Returns a python list
    '''
    files = []
    for name in os.listdir(path):
        if os.path.isdir(os.path.join(path, name)):
            files.append(name)
    return files

def remove_numbers_and_punctuautions(text):
    '''
    A function to remove the numbers and punctuations from a string using regular expressions

    Parameters:
        text: A python string

        Returns a python string
    '''
    text = str(text).lower()
    text = re.sub(r'\d+', '', text) # remove numbers
    text = text.translate(str.maketrans('', '', string.punctuation)).strip()
    return text

def text_extractor(path):
    '''
    function to extract texts from a MS Word file.

    Parameters:
        path: A python string containing the address of a .docx file

        Returns a string 
    '''
    document = Document(path)
    text = ""
    for p in document.paragraphs:
        text =  text + p.text + " "
        text = text.replace('(', '').replace(')', '').replace('"', '').replace("'", "").replace(",", "")
    return text

def clean_text(text):
    """
    Applies some pre-processing on the given text.
    Steps :
    - Removing HTML tags
    - Removing special characters
    - Lowering text
    """
    try:
        text = str(text)        
        # remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # remove the characters [\], ['] and ["]
        text = re.sub(r"\\", "", text)      
        text = re.sub(r"\"", "", text)    
        text = re.sub('[^A-Za-z0-9]+', ' ', text)
        text = re.sub(" \d+", " ", text)
        # convert text to lowercase
        text = text.strip().lower()
        return text
    except Exception as e:
        print(str(e))