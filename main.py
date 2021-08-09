# global variables
import random
from IPython.display import display
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from IPython.display import display

url="https://i.imgur.com/RWgekjY.png"

response = requests.get(url)
img = Image.open(BytesIO(response.content)).convert("L")
# display(img)

def crop_image(img, box=(0,0,800,800)): #box is a tuple defining the edges of the region to crop: (left, top, right, bottom)
  img_array = np.array(img)
  img_array_cropped = img_array[box[1]:box[3], box[0]:box[2]]
  img_cropped = Image.fromarray(img_array_cropped, "L") #L means grayscale
  return img_cropped

img_1 = crop_image(img, box=(0,0,270,270))
img_2 = crop_image(img, box=(270,0,540,270))
img_3 = crop_image(img, box=(520,0,800,270))
img_4 = crop_image(img, box=(0,270,270,540))
img_5 = crop_image(img, box=(270,270,540,540))
img_6 = crop_image(img, box=(520,270,800,530))
img_7 = crop_image(img, box=(270,540,540,800))

from google_drive_downloader import GoogleDriveDownloader as gdd
gdd.download_file_from_google_drive(file_id='1jgc7I9NUF7qD0ArcWge3koQ_VxnDiQEs',
                                    dest_path='./Wordlist.xlsx',
                                    unzip=True, showsize=True)

import pandas as pd
df = pd.read_excel("Wordlist.xlsx")

game = Hangman()

#main game class
class Hangman():
  def __init__(self, chosenList="classic", tries=6): #initialization
    classic_list = df["classic"].dropna().to_list()
    countries_list = df["countires"].dropna().to_list()
    animals_list = df["animals"].dropna().to_list()
    python_list = df["python"].dropna().to_list()
    colour_list = df["colour"].dropna().to_list()

    chosenList = chosenList.lower()
    word_list = classic_list
    if chosenList == 'classic':
      word_list = classic_list
    elif chosenList == 'python':
      word_list = python_list
    elif chosenList =='colours':
      word_list = colour_list
    elif chosenList =='animals':
      word_list = animals_list
    elif chosenList == 'countries':
      word_list = countries_list
    else:
      print("Unspecified game mode! Using the default classic word list")
    self.word_list = word_list
    self.tries = 6

  def run(self): #this is a method for the Hangman game class
    tries = self.tries
    word = random.choice(self.word_list)
    # print("answer:", word)
    word_completion = len(word) * '_ '
    guessed=[]

    print('WELCOME TO HANGMAN!')
    print('\n')
    print(word_completion)
    print('you have 6 tries')
    print('\n')

    display(img_1)
    while tries > 0:
      display_text = ""
      guess="" #initial value for guess 
      while len(guess)!=1 or len(guess)==0: 
        guess=input('please guess a letter: ').upper()
        if len(guess)!=1:
          print('Input should be one letter. Please try again')
      guessed.append(guess)
      if guess in word:
        print(guess,'is correct')
      if guess not in word:
        tries-=1
        print('you have',tries,'tries left')
        if tries == 5:
          display(img_2)
        elif tries == 4:
          display(img_3)
        elif tries == 3:
          display(img_4)
        elif tries == 2:
          display(img_5)
        elif tries == 1:
          display(img_6)

      for char in word:
        if char in guessed:
          display_text += char+" "
        else:
          display_text += "_ "
      print(display_text)
      if '_' not in display_text:
        print('yay you win!')
        break
      if tries == 0:
        print('haha you lose')
        print('the word was', word)
        display(img_7)

game = Hangman(chosenList="python", tries=6) 
game.run()
