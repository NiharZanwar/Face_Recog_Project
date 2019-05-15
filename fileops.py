import os


f=open("idGen.txt", "r+")
contents =f.read()
NewID=str(int(contents)+1)
f.seek(0)
i=len(NewID)
NewID=NewID.zfill(6)
f.write(str(int(NewID)))
f.close()
print( NewID )

#for i in range(0,3):
	
