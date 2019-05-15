import numpy
import face_recognition
import os
import time
import requests

def getUniqueID():                         # function for generating new ID
    f=open("idGen.txt", "r+")
    contents =f.read()
    NewID=str(int(contents)+1)
    f.seek(0)
    i=len(NewID)
    NewID=NewID.zfill(6)
    f.write(NewID)
    f.close()
    return NewID

#def checkForName

dir_path =os.getcwd()
xarr=[]

while True:
    time.sleep(0.5)
    list1 = os.listdir(dir_path+'/detected_faces')
    if (len(list1)>0):  #check if new faces have been dumped in detected_faces
        number_files = len(list1)
        for i in range(0,number_files):
            current_img = face_recognition.load_image_file(dir_path+'/detected_faces/'+list1[i])
            try:
                current_img_enc = face_recognition.face_encodings(current_img,num_jitters=5)[0]
            except:
                print("indexError for {}".format(list1[i]))
                dest=dir_path+'/ErrorWhileEnc/'+list1[i]
                src=dir_path+'/detected_faces/'+list1[i]
                os.rename(src,dest)
                continue
            p=0
            k=1
            l=""
            list2=os.listdir(dir_path+'/numpy_arrays')
            for j in range(0,len(list2)):

                existing_enc=numpy.load(dir_path+'/numpy_arrays/'+list2[j])#.replace('.jpg','.npy'))
                existing_img_arr=[existing_enc]
                results = face_recognition.compare_faces(existing_img_arr, current_img_enc,tolerance=0.5)
                if results[0]==True:
                    print("duplicate occured for {} with {}".format(list1[i],list2[j]))
                    k=0
                    p=j
                    l=list2[j]
                    break
                else:
                    k=1
            
            if k==1:
                name=''   #person is new maybe with or without name from either flask or put in manually
                if(len((list1[i].replace('.jpg','')).split('_'))>2): # if person is with name then get the name format
                    name=((list1[i].replace('.jpg','')).split('_'))[0]
                    print("found name {}".format(name))
                else:
                    name='null'
                    print("found name {}".format(name))
                UniqueID=getUniqueID()
                facedata='FaceTxn1,fieldtag=1,Name='+name+' duplicate=F,FaceID='+UniqueID.zfill(6)+' '+((list1[i].replace('.jpg','')).split('_'))[-1]
                #print((str(list1[i].replace('.jpg','')))[4:])
                print(facedata)
                r=requests.post("http://localhost:8086/write?db=test&precision=u",data=facedata)
                if(len(name)>0):
                    name=name+'_'
                
                numpy.save(dir_path+'/numpy_arrays/'+name+UniqueID,current_img_enc)
                
                dest=dir_path+'/encoded_faces/'+name+UniqueID+'.jpg'
                src=dir_path+'/detected_faces/'+list1[i]
                os.rename(src,dest)
                print("encoding done for {}".format(list1[i]))
            else:
                duplicate=''
                name=''
                if((len((list1[i].replace('.jpg','')).split('_'))>2))&(((list2[p].replace('.npy','')).split('_'))[0]=='null'): # to change name of numpy arrays because duplicate came with a name and ensure there is no same named person stored before
                    name=((list1[i].replace('.jpg','')).split('_'))[0]
                    existing_file=list2[p]
                    new_file=name+'_'+((existing_file.replace('.npy','')).split('_'))[-1]
                    dest=dir_path+'/numpy_arrays/'+new_file + '.npy'
                    src=dir_path+'/numpy_arrays/'+list2[p]
                    os.rename(src,dest) # replace array with no name with array with name
                
                if(len((l.replace('.npy','')).split('_'))>1):  # to extract name and ID of duplicate to put in influx
                    DuplicateID=((l.replace('.npy','')).split('_'))[-1]
                    name=((l.replace('.npy','')).split('_'))[0]
                else:
                    DuplicateID=((l.replace('.npy','')).split('_'))[0]
                    name='null'
                facedata='FaceTxn1,fieldtag=1,Name='+name+' duplicate=T,FaceID='+DuplicateID+' '+((list1[i].replace('.jpg','')).split('_'))[-1]
                #facedata="FaceTxn"+",Location=A1,SubLocation=B2, FaceID="+DuplicateID+"Duplicate=F"+" "+str(list1[i].replace('.jpg',''))
                r=requests.post("http://localhost:8086/write?db=test&precision=u",data=facedata)
                dest=dir_path+'/duplicate_faces/'+list1[i]
                src=dir_path+'/detected_faces/'+list1[i]
                os.rename(src,dest)
            print("------------")








