import os
from PIL import Image
import face_recognition
import time

crop_margin=50

dir_path =os.getcwd()

while True:
    list1 = os.listdir(dir_path+'/imageDump') # file path where image from camera gets dumped
    
    if (len(list1)>0):     #if there are some file in the folder
        number_files = len(list1)
        for i in range(0,number_files):
            print("---------------------------------------------")
            image = face_recognition.load_image_file(dir_path+'/imageDump/'+list1[i])
            im = Image.open(dir_path+'/imageDump/'+list1[i])
            face_locations = face_recognition.face_locations(image,number_of_times_to_upsample=1)
            print("I found {} face(s) in this photograph.-{}".format(len(face_locations),list1[i]))
            j=1
            for face_location in face_locations:
                name=''
                timeStamp=''
                if(len((list1[i].replace('.jpg','')).split('_'))>1):
                    name=((list1[i].replace('.jpg','')).split('_'))[0] + '_'
                    timeStamp=((list1[i].replace('.jpg','')).split('_'))[1]
                if(len(list1[i].split('_'))==1):
                    timeStamp=list1[i].replace('.jpg','')
                
                top, right, bottom, left = face_location
                crop=im.crop((left-crop_margin,top-crop_margin,right+crop_margin,bottom+crop_margin))
                k=len(str(j))
                file_name='detected_faces/'+name+'f'+str(j).zfill(3)+'_'+str(int(timeStamp)+j) + '.jpg' #format for a detected face is f###_timestamp(16 digit).jpg
                crop.save(file_name)  #save the detected faces to detected_faces Dir
                #print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
                print ("cropped face - {}".format(j))
                j+=1
            dest=dir_path+'/scannedDump/'+list1[i]
            src=dir_path+'/imageDump/'+list1[i]
            os.rename(src,dest)  #put those images that have been scanned to scannedDump Dir
    
    
    list2 = os.listdir(dir_path+'/ManualImageDump')
    if(len(list2)>0):
        number_files=len(list2)
        for i in range(0,number_files):
            name=''
            
            if (((list2[i].split('.'))[0]).isalpha()):
                name=((list2[i].split('.')))[0] + '_'    
            dest=dir_path+'/imageDump/'+name+(str((int((time.time()))*1000000)+i))+'.jpg'
            src=dir_path+'/ManualImageDump/'+list2[i]
            os.rename(src,dest)
            
    time.sleep(3)
