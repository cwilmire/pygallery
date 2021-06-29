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

def main():
    # initiate the arg parser
    parser = argparse.ArgumentParser()

    # add long and short argument
    parser.add_argument("--dir", "-d", help="specify directory")
    parser.add_argument("--queue", "-q", help="specify queue.txt file")

    # read arguments from the command line
    args = parser.parse_args()

    # directory list
    dirlist = []

    # check for args and assign directory list
    if args.dir:
        # arg has dir
        dirlist.append(args.dir.replace("\\","/"))   # For Windows, back slashes to forward slashes
    elif args.queue:
        # read file, fill list
        f = open(args.queue, "r")
        for x in f:
            x=x.rstrip()
            x=x.replace("\\","/")   # For Windows, back slashes to forward slashes
            dirlist.append(x)
    else:
        # use filedialog.askdirectory for dir
        folder_selected = filedialog.askdirectory(title='Please select a directory')
        folder_selected = folder_selected.replace("\\","/")
        dirlist.append(folder_selected)

    # Set tn photo width
    mywidth = 400   

    # original directory where app is launched
    origdir = os.getcwd()
    origindex = origdir.replace('\\','/') + "/index-template.html"

    # Loop through the directories in dirlist
    for i in dirlist: 
        # copy index.html to selected directory
        targetdir=i
        targetfile = targetdir.replace('\\','/') + '/index.html'
        copyfile(origindex, targetfile)
        os.chdir(targetdir)
    	
        # make thumbnail directory if needed
        if not os.path.exists('tn'):
            os.makedirs('tn')

        # find name of current directory
        dirpath = os.getcwd()
        print("current directory is : " + dirpath)
        foldername = os.path.basename(dirpath)
        print("directory name is : " + foldername)

        # define gallery values for the json file
        gallery = {
            "gallery_title": foldername,
            "gallery_desc": "Description.",
            "gallery_location": "Location",
            "gallery_date": "Date",
            "showdesc": False,
            "showdate": False,
            "showlocation": False }

        # create list of existing photos for the json file
        photos = []
        listOfFiles = os.listdir('.')
        pattern = "*.jpg"
        for entry in listOfFiles:
            if fnmatch.fnmatch(entry, pattern):
                img = Image.open(entry)
                print (entry)
                # resize images to tn directory
                wpercent = (mywidth/float(img.size[0]))
                hsize = int((float(img.size[1])*float(wpercent)))
                img = img.resize((mywidth,hsize), PIL.Image.ANTIALIAS)
                fl = 'tn/'+entry
                try:
                    exif = img.info['exif']
                    img.save(fl, exif=exif)
                except:
                    img.save(fl)

                photos.append({"photodesc":entry,"photodisplay":True,"photofn":entry,"photoname":entry})

        # add photo list to gallery dictionary
        gallery["photos"] = photos

        # write the json file
        with open('gallery.json', 'w', encoding='utf-8') as f:
            json.dump(gallery, f, ensure_ascii=False, indent=4)            



if __name__ == "__main__":
    main()