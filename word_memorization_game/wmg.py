import os,sys,random
from textblob import TextBlob
# https://github.com/TayfunBasoglu

#---------Edit this field -------------
# file name and path
file_name = 'file.txt'

#ISO Country Codes
translate_to = 'en'
translate_from = 'tr' #-> If it is empty, it detects automatically. (translate_from = " '')

#Box Size
width = 50
height = 2
#--------------------------------------

#file check
if not os.path.exists("file.txt"):
    print("File not found")
    sys.exit()

#translate_from check
if translate_from == ' ' or translate_from == '':
    translate_from = "auto"

#control for width and height
if width %2 != 0:
    width = int(width+1)
height = int(height)

#box
def box(word):
    left_space = int((width-len(word)--1) / 2)
    right_space = width-(left_space+len(word)+2)
    print("-" * width)
    box_height(height)
    print("|"+" " * left_space+ str(word)+" " * right_space +str("|"))
    box_height(height)
    print("-" * width)
    empty_input = input("\n")

def box_height(height):
    for i in range(0,height):
        print("|"+" " * (width - 2)+"|")


# words append to list
words = []
with open(file_name) as word_file:
    for i in word_file:
        if i == "\n":
            pass
        else:
            words.append(i.strip())

#word print and pop
while len(words)>0:
    os.system('clear')
    print("! Press 'enter' to see the answer or the next question.")
    print("! Ctrl + Z for exit","\n"*2)
    print("Question",len(words))
    r_number = random.randint(0,(len(words)-1))
    box(str(words[r_number]).lower())
    word_translate = TextBlob(words[r_number])
    print("Answer ↓")
    try:
        box(str(word_translate.translate(from_lang=translate_from,to=translate_to)).lower())
    except:
        box(str("Word not found"))
    words.pop(r_number)

