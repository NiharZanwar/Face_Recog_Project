# Face_Recog_Project
## Application made using the face_recognition library

Here I have made a simple application on python which make use of the face_recognition library given below
https://github.com/ageitgey/face_recognition

Dependencies - python libraries
1) `face_recognition` (including it's dependencies)
2) `flask`
3) `requests`
4) `time`
5) `os`
6) `numpy`
7) `PIL`

**USE CASE**
1) Application where you want to cut out the faces from a group picture and store them accordingly
2) Application where you want to detect faces, Recognize them and detect whether there have been faces that were encountered before and store data of all such transactions in a database.

I have used [InfluxDB](https://docs.influxdata.com/influxdb/v1.7) for the database software beacuse of its time-series property

## FLOW OF PROGRAM

Flask server receives a `.jpg` from the webpage `index.html` by a POST request which is processed and a timestamp is created using the `time` library. Filename of the file that was received is replaced with a 16-digit timestamp and this file is dumped into the `imageDump` directory.

`xyz.jpg` becomes `1456278646465678.jpg` lets call this 16-digit filename as `timestamp.jpg`

If name of a person is known a file by name `name.jpg` can be put into the directory `ManualImageDump` from where it is modified to `name_timestamp.jpg` and dumped into `imageDump`

`imageDump` now has two types of filenames `timestamp.jpg` and `name_timestamp.jpg` out of which it is assumed that the latter one only has one face in it.

Files from `imageDump` are scanned from for faces and if found they are dumped into `detected_faces` with file name `name_f###_timestamp.jpg` or `f###_timestamp.jpg` in different cases of whether name was there previously.

Here is where the recognition part starts. Face images are picked up from `detected_faces` and encoded into a numpy array then compared to previously encoded numpy arrays stored in `numpy_arrays`. If no match is found then new entry is made into `numpy_arrays` by filename `name_UniqueID.npy` or `null_UniqueID.npy` and a transaction is put into `InfluxDB` database








