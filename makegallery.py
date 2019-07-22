import os
import os.path
import fnmatch
import json
import sys
import PIL
from PIL import Image
from tkinter import filedialog
from shutil import copyfile
import argparse

def seldir():
    #folder_selected = filedialog.askdirectory(initialdir=os.getcwd(),title='Please select a directory')
    folder_selected = filedialog.askdirectory(title='Please select a directory')
    folder_selected = folder_selected.replace("/","\\")
    return folder_selected

def main():
    # initiate the arg parser
    parser = argparse.ArgumentParser()

    # add long and short argument
    parser.add_argument("--dir", "-d", help="specify directory")

    # read arguments from the command line
    args = parser.parse_args()

    # check for --dir
    if args.dir:
        print("set directory to %s" % args.dir)

    # copy index.html to selected directory
    origdir = os.getcwd()
    origindex = origdir + "\index-template.html"
    if args.dir:
        targetdir = args.dir
    else:
        targetdir = seldir()
    targetfile = targetdir + '\index.html'
    copyfile(origindex, targetfile)
    os.chdir(targetdir)
    
    # Set tn photo width
    mywidth = 400   
	
    # make thumbnail directory if needed
    if not os.path.exists('tn'):
        os.makedirs('tn')

    # find name of current directory
    dirpath = os.getcwd()
    print("current directory is : " + dirpath)
    foldername = os.path.basename(dirpath)
    print("Directory name is : " + foldername)

    # define gallery values for the json file
    gallery = {
        "gallery_title": foldername,
        "gallery_desc": "Description.",
        "gallery_location": "Location",
        "gallery_date": "Date",
        "showdesc": False,
        "showdate": False,
        "showlocation": False,
        }

    # create list of existing photos for the json file
    photos = []
    listOfFiles = os.listdir('.')
    pattern = "*.jpg"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
                img = Image.open(entry)
                print (entry)
                #resize
                wpercent = (mywidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((mywidth,hsize), PIL.Image.ANTIALIAS)
                fl = 'tn/'+entry
                img.save(fl)
                photos.append({"photodesc":entry,"photodisplay":True,"photofn":entry,"photoname":entry})

    # add photo list to gallery dictionary
    gallery["photos"] = photos

    # write the json file
    with open('gallery.json', 'w', encoding='utf-8') as f:
        json.dump(gallery, f, ensure_ascii=False, indent=4)            


if __name__ == "__main__":
    main()