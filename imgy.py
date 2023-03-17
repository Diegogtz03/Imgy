import tkinter as tk
from tkinter import filedialog
import os, os.path
import PIL
from PIL import Image
import sys
import cv2
import argparse

# Standard = 1MB
# Change this value according to the standard wanted
WEIGHT_STANDARD = 1000000

# Initial JPEG image quality when compressed (0-100) 
# where 0 is the lowest quality and 100 the same quality
JPG_IMG_QUALITY = 50

# Initial PNG image compression value (0-9) 
# where 0 is the lowest compression and 9 the highest (longer time)
PNG_IMG_QUALITY = 4


# Directory Browser Function
def directory_browse():
  global folder_path
  filename = filedialog.askdirectory()
  folder_path.set(filename)
  compress_imgs(folder_path.get())


def compress_imgs(folder_path):
  imgs = []
  valid_images = [".jpg",".png"]

  for f in os.listdir(folder_path):
    ext = os.path.splitext(f)[1]
    img_weight = os.stat(folder_path).st_size

    # Skip images that are not valid and those already under the 1MB standard
    if ext.lower() not in valid_images or img_weight <= WEIGHT_STANDARD:
      continue

    imgInfo = {
      "path": os.path.join(folder_path,f),
      "ext": ext.lower(),
      "weight": img_weight
    }

    imgs.append(imgInfo)

  for img in imgs:
    img_weight = img["weight"]
    quality = JPG_IMG_QUALITY

    while (img_weight > WEIGHT_STANDARD):
      compress_img(img["path"], img["ext"], quality)
      img_weight = os.stat(img["path"]).st_size

      quality -= 2

      print(img_weight)


    print("DONE!")




def compress_img(path, ext, jpg_quality):
  image = cv2.imread(path)

  os.remove(path)

  if (ext == '.jpg'):
    cv2.imwrite(path, image, [cv2.IMWRITE_JPEG_QUALITY, jpg_quality])
  else:
    cv2.imwrite(path, image, [int(cv2.IMWRITE_PNG_COMPRESSION), PNG_IMG_QUALITY])


window = tk.Tk()
window.configure(background='#383838')
window.geometry("1000x450")
window.attributes("-alpha", 0.95)
window.title("Imgy")
windowWidth = 1000
windowHeight = 450
posR = int(window.winfo_screenwidth()/2 - windowWidth/2)
posL = int(window.winfo_screenheight()/2.3 - windowHeight/2)
window.geometry("+{}+{}".format(posR, posL))


# VARIABLES
folder_path = tk.StringVar()
var = tk.IntVar()

button_file = tk.Button(window, text="Browse", command=directory_browse, width=10, height=5, bg="white")
button_file.pack()

window.mainloop()