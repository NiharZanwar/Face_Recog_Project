from PIL import Image
import face_recognition
import os 


dir_path =os.getcwd()

# Load the jpg file into a numpy array
image = face_recognition.load_image_file("sample.jpg")
im = Image.open('sample.jpg')

# Find all the faces in the image using the default HOG-based model.
# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
# See also: find_faces_in_picture_cnn.py
face_locations = face_recognition.face_locations(image)

print("I found {} face(s) in this photograph.-{}".format(len(face_locations)))
i=1
for face_location in face_locations:

    # Print the location of each face in this image
    top, right, bottom, left = face_location
    coordinate_crop=(left,top,(right-left),(bottom-top))
    crop=im.crop((left,top,right,bottom))
    file_name='detected_faces/'+'face'+str(i)+'.jpg'
    crop.save(file_name)
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
    i=i+1
    # You can access the actual face itself like this:
    #face_image = image[top:bottom, left:right]
    #pil_image = Image.fromarray(face_image)
    #pil_image.show()
    #crop.show()
