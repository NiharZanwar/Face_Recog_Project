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










