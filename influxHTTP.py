import requests
import time
#facedata='FaceTxn1,fieldtag=1 duplicate=T,FaceID='+DuplicateID+' '+(str(list1[i].replace('.jpg','')))[5:]
facedata='mymeas,mytag=1 myfield=92 ' + str(time.time()*100000)

r=requests.post("http://localhost:8086/write?db=test&precision=u",data=facedata)

print (r.Response)
