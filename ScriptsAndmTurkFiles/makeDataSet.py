import csv
import os
import numpy as np

directory = "./"
dsDir = "../UMBC-RGB-DATASET"

fileDescriptionMaps = {}
for filename in os.listdir(directory):
   if filename.endswith(".csv"):
     fName = os.path.join(directory, filename)
     with open(fName) as csvfile:
        readFile = csv.DictReader(csvfile)
        for row in readFile:
           for no in range(16):
              kName = "Input.image" + str(no + 1) + "_url"
              if no == 0:
                kName = "Input.image_url"
              res = "Answer.tag" + str(int(float(no)/float(4)) + 1)
              tag = row[res]
              if len(tag) > 0 and tag != "{}":
                 tfName = row[kName]
#                 print tfName,tag
                 fileDescriptionMaps.setdefault(tfName, []).append(tag)
os.system("rm -rf " + dsDir)
for file in np.sort(fileDescriptionMaps.keys()):
   desc = fileDescriptionMaps[file]
   arF = file.split("/")
   newFName = os.path.join(dsDir,arF[-3],arF[-2])
   os.system("mkdir -p " + newFName)
   ss = [1 for ff in os.listdir(newFName) if ff.endswith(".png")]
   nFFName = arF[-2] + "_" + str(len(ss) + 1) + ".png"
   pngFName = os.path.join(newFName,nFFName)
   os.system("curl -o " + pngFName + " " + file)
   descFile = os.path.join(newFName,"mTurkDescription_"+ arF[-2] + ".txt")
   for ds in desc:
      lg = nFFName + " " + ds + "\n"
      f = open(descFile,"a+")
      f.write(lg)
      f.close()

for filename in os.listdir(dsDir):
  for fName in os.listdir(os.path.join(dsDir,filename)):
    newLoc = os.path.join(dsDir,filename,fName)
    cmd = "tar -czvf " + newLoc + ".tgz " + newLoc
    os.system(cmd)
  newLoc = os.path.join(dsDir,filename)
  cmd = "tar -czvf " + newLoc + ".tgz " + newLoc
  os.system(cmd)
