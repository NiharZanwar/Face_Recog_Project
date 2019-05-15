import face_recognition
import numpy
import math
import time

start = time.time()

def eucleadian_dist(array1,array2):
    total=0
    for i in (0,127):
        sub = array1[i]-array2[i]
        mul=sub*sub
        total=total+mul
    return (math.sqrt(total))

# Load the jpg files into numpy arrays
#biden_image = face_recognition.load_image_file("biden.jpg")
obama_image = face_recognition.load_image_file("obama.jpg")
obama_image2 = face_recognition.load_image_file("obama2.jpg")
#unknown_image = face_recognition.load_image_file("obama2.jpg")


# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
try:
    #biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
    
    obama_face_encoding2 = face_recognition.face_encodings(obama_image2)[0]
    
    #unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
except IndexError:
    print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
    quit()

print (type(obama_face_encoding))
list1=obama_face_encoding.tolist()
print (type(list1))


print (obama_face_encoding2[0])

#dist = numpy.linalg.norm(vector(obama_face_encoding)-vector(obama_face_encoding2))
#print (dist)

print (eucleadian_dist(obama_face_encoding,obama_face_encoding2))


known_faces = [
    obama_face_encoding
]
end = time.time()
print(end - start)
# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces(known_faces, obama_face_encoding2)
end = time.time()
print(end - start)
if results[0]==True:
    print("hi")

print("Is the unknown face a picture of Biden? {}".format(type(results[0])))
#print("Is the unknown face a picture of Obama? {}".format(results[1]))
#print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
