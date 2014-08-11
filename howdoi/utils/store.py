'''
Handles Writing of Answers to File
'''

from os import getcwd, path
import string

filename = 'howdoi.txt'
phrase = 'How Do I '


def write(title, answer, directory=None):
    ''' Writes to a File.
    Returns True if successful. Else false. '''
    if not directory:
        directory = getcwd()
    path_to_file = path.join(directory, filename)
    with open(path_to_file, 'a+') as answer_file:
        title = phrase + title.replace('?', '')
        content = '\n'.join(['', title, '-' * len(title), answer])
        content = filter(lambda c: c in string.printable, content)
        answer_file.write(content)
        return True
    return False
