import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Nihar@123',
                             db='FaceData',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

#CREATE  TABLE IF NOT EXISTS `Profiles` (
  #`FaceID` INT,
  #`Name` VARCHAR(150) ,
  #`Gender` VARCHAR(6) ,
  #`Age` VARCHAR(3) ,
  #`Contact_Number` VARCHAR(75) ,
  #`Email` VARCHAR(255) ,
  #`Type`  VARCHAR(2),
  #`Organzation` VARCHAR(50),
 # PRIMARY KEY (`FaceID`) )
#ENGINE = InnoDB;

#with connection.cursor() as cursor:
        # Create a new record
   # sql = "INSERT INTO `Profiles` (`Name`, `FaceID`) VALUES (%s, %s)"
    #cursor.execute(sql, ('nihar', 111111))
   # connection.commit()

#with connection.cursor() as cursor:
        # Read a single record
       # sql = "SELECT `FaceID` FROM `Profiles` WHERE `Name`=%s"
      #  cursor.execute(sql, ('nihar'))
      #  result = cursor.fetchone()
       # print(type(result))

def AddNewProfile(FaceID,Name,Gender,Age,ContactNo,Email,Type,Organization):
    
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `Profiles` (`Name`, `FaceID`,`Gender`,`Age`,`Contact_Number`,`Email`,`Type`,`Organzation`) VALUES (%s, %s,%s, %s,%s, %s,% s, %s)"
        cursor.execute(sql, (Name,FaceID,Gender,Age,ContactNo,Email,Type,Organization))
        connection.commit()
    
AddNewProfile(111222,'nihar','male',18,8888811111,'zan@g.com','em','smarti')

