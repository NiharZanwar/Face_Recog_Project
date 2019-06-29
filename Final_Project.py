import pymysql.cursors
from os import rename, mkdir, path, getcwd, listdir
import face_recognition
import numpy
from PIL import Image
import json
from PIL.ExifTags import TAGS
from shutil import copy2
import sys
from details import errordict, hostname, username, password, database, charset

s_org_table = 'organisation'
s_buc_table = 'orgbucket'
s_cam_table = 'orgCamera'
s_usr_table = 'orgUser'
s_face_table = 'faceinfo'
s_person_table = 'personinfo'
s_txn_img_table = 'tx_img_id'
s_txn_face_table = 'tx_face_id'
s_txn_obj_table = 'tx_obj_id'
s_mrkdel = 'markdelete'
s_time = 'createddatetime'
s_timesvisited = 'TimesVisited'

s_org_id = 'oid'
s_org_name = 'orgname'
s_org_code = 'orgcode'

s_buc_id = 'bucketid'
s_buc_name = 'bucketname'
s_buc_code = 'bucketcode'

s_cam_id = 'cameraid'
s_cam_code = 'cameracode'

s_usr_name = 'username'
s_usr_pass = 'userpassword'

s_tximg_id = 'tx_img_id'
s_face_count = 'faceno'

s_txface_id = 'tx_face_id'
s_txface_path = 'path'
s_txobj_id = 'obj_id'
s_txobj_path = 'path'

s_face_id = 'FaceID'
s_person_id = 'PersonID'
s_pics_stored = 'pics_stored'
temp_img_dir = '/temp_img_dir/'
error_enc_dir = '/error_faces/'
unique_dir = '/unique_faces/'
numpy_arrays = '/numpy_arrays/'
Organisation = '/Organisations/'
ManualImageDump = '/ManualImageDump/'
crop_margin = 50

dir_path = getcwd()


def sql_connection():
    """
    Function to connect to MySQL Database
    :return: It returns two values, 1) Error/success codes 2) connection pointer
    """
    try:
        connection = pymysql.connect(host=hostname,
                                     user=username,
                                     password=password,
                                     db=database,
                                     charset=charset,
                                     cursorclass=pymysql.cursors.DictCursor)
        return 230, connection
    except:
        return 130, sys.exc_info()[1]


def initialization():
    """
    To create the necessary folders 'Organisations', 'temp_img_dict' and 'ManualImageDump' in the current directory
    :return: Nothing. Just creates directory
    """
    if not path.exists(dir_path + temp_img_dir):
        mkdir(dir_path + temp_img_dir)

    if not path.exists(dir_path + Organisation):
        mkdir(dir_path + Organisation)

    if not path.exists(dir_path + ManualImageDump):
        mkdir(dir_path + ManualImageDump)


def extract_info(table, id_name, i_d):
    """
    To extract information from the database
    :param table: Table from where the information needs to be extracted
    :param id_name: Name of the column whose value is known and is used as a filter
    :param i_d: Value of the above column known to us
    :return: It returns two elements. First is error/success code
        Secondly, All the rows from the table having 'id_name' = 'i_d' as a list containing specific rows as dictionary.
    """

    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM {} WHERE {} = '{}'".format(table, id_name, i_d))
            rows = cursor.fetchall()
            return 228, rows
        except:
            return 128, sys.exc_info()[1]


def add_new_camera(cameraname, bucketcode, cameratype, createddatetime):
    """
    To add a new camera to the database and create the folders accordingly
    :param cameraname: Name of the camera entered
    :param bucketcode: Bucket Code under which the camera is to be created
    :param cameratype: Type of camera entered
    :param createddatetime: Date and Time of creation of the camera
    :return: It returns two elements. First is the error/success code and second is the camera code
     Also it creates two folders - 'camera code + _faces' and 'camera code + _dump'
    """

    buc_rows = extract_info(s_buc_table, s_buc_code, bucketcode)[1]
    buc_id = buc_rows[0][s_buc_id]
    org_id = buc_rows[0][s_org_id]
    buc_markdel = buc_rows[0][s_mrkdel]
    orgcode = extract_info(s_org_table, s_org_id, org_id)[1][0]['orgcode']

    if buc_markdel == 1:
        return 102, errordict[102]

    connection = sql_connection()[1]
    try:
        with connection.cursor() as cursor:
            cursor.callproc('create_camera', [cameraname, buc_id, cameratype, org_id, createddatetime])
            cam_id = cursor.fetchall()[0]['id']
    except:
        return 121, sys.exc_info()[1]

    try:
        camera_code = 'CAM' + str(cam_id).zfill(9)  # BUCKET code format
        update_info(s_cam_table, s_cam_id, cam_id, s_cam_code, camera_code)
    except:
        return 122, sys.exc_info()[1]

    try:
        camera_faces_path = dir_path + Organisation + orgcode + '/' + bucketcode + '/' + camera_code + '_faces'
        mkdir(camera_faces_path)
        camera_dump_path = dir_path + Organisation + orgcode + '/' + bucketcode + '/' + camera_code + '_dump'
        mkdir(camera_dump_path)

    except:
        return 123, sys.exc_info()[1]

    return 202, camera_code


def add_new_org(org_name, org_logo, org_email, created_date_time, org_key):
    """
    To add a new organisation to the database and create the folders accordingly
    :param org_name: Name of the organisation entered
    :param org_logo: Logo of the organisation entered
    :param org_email: Email of the organisation entered
    :param created_date_time: Date and Time of creation of the organisation
    :param org_key: Key of the organisation
    :return: It returns two elements. First is the error/success code and second is the organisation code
     Also it creates a folder - org code
    """

    ad = [org_name, org_logo, org_email, created_date_time, org_key]
    connection = sql_connection()[1]
    try:
        with connection.cursor() as cursor:

            cursor.callproc('create_organisation', ad)
            org_id = cursor.fetchall()[0]['id']
    except:
        return 118, sys.exc_info()[1]

    try:
        org_code = 'ORG' + str(org_id).zfill(5)  # BUCKET code format
        update_info(s_org_table, s_org_id, org_id, s_org_code, org_code)
    except:
        return 119, sys.exc_info()[1]

    try:
        org_path = dir_path + Organisation + org_code
        mkdir(org_path)
    except:
        return 120, sys.exc_info()[1]

    return 203, org_code


def add_new_bucket(bucket_name, created_date_time, buc_org_code):
    """
     To add a new bucket to the database and create the folders accordingly
    :param bucket_name: Name of the bucket entered
    :param created_date_time: Date and Time of creation of the bucket
    :param buc_org_code: Organisation Code under which the bucket is to be created
    :return: It returns two elements. First is the error/success code and second is the bucket code
     Also it creates folders - bucket code, 'numpy_arrays', 'error_faces', 'unique_faces'
    """

    org_rows = extract_info(s_org_table, s_org_code, buc_org_code)[1]
    org_id = org_rows[0][s_org_id]
    org_markdel = org_rows[0][s_mrkdel]

    if org_markdel == 1:
        return 105, errordict[105]

    connection = sql_connection()[1]
    try:
        with connection.cursor() as cursor:

            cursor.callproc('create_bucket', [bucket_name, created_date_time, org_id])
            buc_id = cursor.fetchall()[0]['id']
    except:
        return 115, sys.exc_info()[1]

    try:
        bucket_code = 'BUC' + str(buc_id).zfill(9)  # BUCKET code format
        update_info(s_buc_table, s_buc_id, buc_id, s_buc_code, bucket_code)
    except:
        return 116, sys.exc_info()[1]

    try:
        bucket_path = dir_path + Organisation + buc_org_code + '/' + bucket_code
        mkdir(bucket_path)
        numpy_arrays_path = bucket_path + numpy_arrays
        mkdir(numpy_arrays_path)
        unique_faces_path = bucket_path + unique_dir
        mkdir(unique_faces_path)
        error_faces_path = bucket_path + error_enc_dir
        mkdir(error_faces_path)
    except:
        return 117, sys.exc_info()[1]

    return 204, bucket_code


def add_new_faceid(personid, facepath, img_id, org_id, bucket_id):
    """
    To add a new face in faceinfo table and assign a faceid to it
    :param personid: Person ID of the face detected
    :param facepath: Path of the face
    :param img_id: Image ID of the image from which the face was detected
    :param org_id: Organisation ID of the camera which detected the face
    :param bucket_id: Bucket ID of the camera which detected the face
    :return: FaceID
    """

    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        cursor.callproc('new_face', [personid, facepath, img_id, org_id, bucket_id])
        face_id = cursor.fetchall()[0]['id']
    return face_id


def del_org(org_id):
    """
    To disable an organisation
    :param org_id: ID of the organisation to be disabled
    :return: Nothing
    """
    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        cursor.execute("UPDATE `organisation` SET `markdelete` = '1' WHERE `oid` = %s", org_id)
        cursor.execute("UPDATE `orgbucket` SET `markdelete` = '1' WHERE `oid` = %s", org_id)
        cursor.execute("UPDATE `orgCamera` SET `markdelete` = '1' WHERE `oid` = %s", org_id)
        connection.commit()


def renew_org(org_id):
    """
    To enable an organisation
    :param org_id: ID of the organisation to be enabled
    :return: Nothing
    """

    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        cursor.execute("UPDATE `organisation` SET `markdelete` = '0' WHERE `oid` = %s", org_id)
        cursor.execute("UPDATE `orgbucket` SET `markdelete` = '0' WHERE `oid` = %s", org_id)
        cursor.execute("UPDATE `orgCamera` SET `markdelete` = '0' WHERE `oid` = %s", org_id)
        connection.commit()


def del_bucket(bucket_id):
    """
    To disable a bucket
    :param bucket_id: ID of the bucket to be disabled
    :return: Nothing
    """
    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        cursor.execute("UPDATE `orgbucket` SET `markdelete` = '1' WHERE `bucketid` = %s", bucket_id)
        cursor.execute("UPDATE `orgCamera` SET `markdelete` = '1' WHERE `bucketid` = %s", bucket_id)
        connection.commit()


def renew_bucket(bucket_id):
    """
    To enable a bucket
    :param bucket_id: ID of the bucket to be enabled
    :return: Nothing
    """
    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        cursor.execute("UPDATE `orgbucket` SET `markdelete` = '0' WHERE `bucketid` = %s", bucket_id)
        cursor.execute("UPDATE `orgCamera` SET `markdelete` = '0' WHERE `bucketid` = %s", bucket_id)
        connection.commit()


def del_camera(camera_id):
    """
    To disable a camera
    :param camera_id: ID of the camera to be disabled
    :return: Nothing
    """
    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        cursor.execute("UPDATE `orgCamera` SET `markdelete` = '1' WHERE `cameraid` = %s", camera_id)
        connection.commit()


def renew_camera(camera_id):
    """
    To enable a camera
    :param camera_id: ID of the camera to be enabled
    :return: Nothing
    """

    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        cursor.execute("UPDATE `orgCamera` SET `markdelete` = '0' WHERE `cameraid` = %s", camera_id)
        connection.commit()


def del_user(user_id):
    """
    To disable an user
    :param user_id: ID of the user to be disabled
    :return: Nothing
    """

    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        cursor.execute("UPDATE `orgUser` SET `markdelete` = '1' WHERE `userid` = %s", user_id)
        connection.commit()


def renew_user(user_id):
    """
    To enable an user
    :param user_id: ID of the user to be enabled
    :return: Nothing
    """
    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        cursor.execute("UPDATE `orgUser` SET `markdelete` = '0' WHERE `userid` = %s", user_id)
        connection.commit()


def create_new_user(user_name, pass_word, email, createddatetime, oid, displayname):
    """
    To create a new user and add the corresponding details to the database
    :param user_name: Username entered
    :param pass_word: Password entered
    :param email: Email entered
    :param createddatetime: Date and Time of creation of the user
    :param oid: Organisation ID under which the user is registered
    :param displayname: Display name entered
    :return: It returns two elements. First is the error/success code. Second is error/success string
    """

    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        sql = "INSERT INTO `orgUser` (`username`, `userpassword`,`useremail`,`createddatetime`,`oid`,`displayname`) " \
              "VALUES (%s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(sql, (user_name, pass_word, email, createddatetime, oid, displayname))
            connection.commit()
            return 212, errordict[212]
        except:
            return 131, sys.exc_info()[1]


def verify_user(user_name, pass_word, o_code):
    """
    To verify the user credentials
    :param user_name: Username entered
    :param pass_word: Password entered
    :param o_code: Organisation Code entered
    :return: It returns two elements. First is the error/success code. Second is error/success string
    """

    oid = int(o_code.replace('ORG', ''))
    info_org = extract_info(s_org_table, s_org_code, o_code)[1]

    if len(info_org) == 0:
        return 107, errordict[107]

    if info_org[0][s_mrkdel] == 1:
        return 108, errordict[108]

    info_user = extract_info(s_usr_table, s_usr_name, user_name)[1]

    if len(info_user) == 0:
        return 109, errordict[109]

    if info_user[0][s_mrkdel] == 1:
        return 110, errordict[110]

    if info_user[0][s_org_id] != oid:
        return 111, errordict[111]

    if pass_word != info_user[0][s_usr_pass]:
        return 112, errordict[112]

    return 205, errordict[205]


def input_image(camera_code, time, txn_img_id, bucket_id, oid, camera_id):
    """
    To input the image captured by the camera
    :param camera_code: Camera Code
    :param time: Time it was received
    :param txn_img_id: Transaction ID of the image
    :param bucket_id: Bucket ID of the camera
    :param oid: Organisation ID of the camera
    :param camera_id: Camera ID
    :return: JSON output of details
    """

    info_org = extract_info(s_org_table, s_org_id, oid)[1]
    info_bucket = extract_info(s_buc_table, s_buc_id, bucket_id)[1]

    bucket_name = info_bucket[0][s_buc_name]
    org_name = info_org[0][s_org_name]

    bucket_code = 'BUC' + str(bucket_id).zfill(9)
    o_code = 'ORG' + str(oid).zfill(5)

    bucket_path = dir_path + Organisation + o_code + '/' + bucket_code
    bucket_path_rel = Organisation + o_code + '/' + bucket_code

    image = face_recognition.load_image_file(dir_path + temp_img_dir + txn_img_id + '_' +
                                             time.replace(' ', '_') + '.jpg')
    im = Image.open(dir_path + temp_img_dir + txn_img_id + '_' + time.replace(' ', '_') + '.jpg')
    face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=1)
    print("detected {} face(s) in this photograph.-{}".format(len(face_locations), txn_img_id + '_' +
                                                              time.replace(' ', '_') + '.jpg'))

    dump_path = bucket_path + '/' + camera_code + '_dump/' + txn_img_id + '_' + time.replace(' ', '_') + '.jpg'
    dump_path_rel = bucket_path_rel + '/' + camera_code + '_dump/' + txn_img_id + '_' + time.replace(' ', '_') + '.jpg'

    update_info(s_txn_img_table, s_tximg_id, txn_img_id, s_face_count, len(face_locations))

    json_initial_dict = {
        "No of faces found": len(face_locations),
        "No of faces encoded": 0,
        "Dump Path": "",
        "Face Data": []
    }

    json_initial = json.dumps(json_initial_dict)

    j = 1

    for face_location in face_locations:

        top, right, bottom, left = face_location
        crop = im.crop((left - crop_margin, top - crop_margin, right + crop_margin, bottom + crop_margin))
        txn_obj_id = str(add_new_obj_txn(txn_img_id, oid, bucket_id,
                                         camera_id, time, top, left, right, bottom, '1')[1]).zfill(10)
        crop_name = txn_obj_id + '_' + txn_img_id + '_' + str(j).zfill(3) + '_' + time.replace(' ', '_')
        crop_face_path = dir_path + temp_img_dir + crop_name + '.jpg'
        crop.save(crop_face_path)

        print("cropped face - {} for image {}".format(j, camera_code + time + '.jpg'))
        # j += 1 put this at the end of this loop
        current_img = face_recognition.load_image_file(crop_face_path)

        try:
            current_img_enc = face_recognition.face_encodings(current_img, num_jitters=3)[0]
        except:
            print("indexError for {}".format(crop_face_path))
            destination = bucket_path + error_enc_dir + crop_name + '.jpg'
            source = crop_face_path
            rename(source, destination)
            continue

        p = 0
        k = 1

        numpy_dir_path = bucket_path + numpy_arrays
        numpy_dir_list = listdir(numpy_dir_path)

        for i in range(0, len(numpy_dir_list)):  # to create a new numpy array if not existing previously

            existing_enc = numpy.load(numpy_dir_path + numpy_dir_list[i])  # .replace('.jpg','.npy'))
            existing_img_arr = [existing_enc]
            results = face_recognition.compare_faces(existing_img_arr, current_img_enc, tolerance=0.5)
            if results[0]:  # if results[0] gives output as True
                print("duplicate occurred for {} with {}".format(crop_name, numpy_dir_list[i]))
                k = 0
                p = i
                break
            else:
                k = 1

        # face_dst = bucket_path + '/' + camera_code + '_faces/' + crop_name + '.jpg'

        txn_face_id = str(add_new_face_txn(txn_img_id, txn_obj_id, oid, bucket_id, camera_id, time)[1]).zfill(10)
        face_dst = bucket_path + '/' + camera_code + '_faces/' + txn_face_id + '_' + crop_name + '.jpg'
        face_dst_rel = bucket_path_rel + '/' + camera_code + '_faces/' + txn_face_id + '_' + crop_name + '.jpg'
        source = crop_face_path
        update_info(s_txn_face_table, s_txface_id, txn_face_id, s_txface_path, face_dst_rel)

        stored = 'Yes'

        if k == 1:  # new face encounter

            duplicate = 0
            times_visited = 1
            person_id = add_person(face_dst_rel, oid)
            face_id = str(add_new_faceid(person_id, face_dst_rel, txn_img_id, oid, bucket_id)).zfill(8)
            unique_id = face_id + '_1'
            numpy.save(numpy_dir_path + unique_id, current_img_enc)
            destination = bucket_path + unique_dir + unique_id + '.jpg'

            rename(source, destination)
            copy2(destination, face_dst)

            print("encoding done for {}".format(crop_face_path))

        else:  # encounter duplicate face

            duplicate = 1
            duplicate_id = numpy_dir_list[p].replace('.npy', '')
            complete_id = duplicate_id.split('_')
            face_id = complete_id[0]
            info_rows = extract_info(s_face_table, s_face_id, face_id)[1][0]
            total_pics = info_rows[s_pics_stored]
            person_id = info_rows[s_person_id]

            if total_pics == 3:
                print("Pic 3 exists, so not stored.")
                stored = 'No'
                rename(source, face_dst)
            else:
                if total_pics == 2:
                    total_pics = 3
                else:
                    total_pics = 2

                update_info(s_person_table, s_person_id, person_id, 'face_path_' + str(total_pics), face_dst_rel)
                update_info(s_face_table, s_person_id, person_id, s_pics_stored, total_pics)

                numpy.save(numpy_dir_path + face_id + '_' + str(total_pics), current_img_enc)

                destination = bucket_path + unique_dir + face_id + '_' + str(total_pics) + '.jpg'
                rename(source, destination)
                copy2(destination, face_dst)

            times_visited = info_rows[s_timesvisited] + 1
            update_info(s_face_table, s_face_id, face_id, s_timesvisited, times_visited)

        update_face_txn(txn_face_id, face_id, duplicate, times_visited, person_id)

        update_info(s_txn_obj_table, s_txobj_id, txn_obj_id, s_txobj_path, face_dst_rel)

        json_initial = to_json(json_initial, 'null', face_id, time, txn_img_id, top, bottom, left, right,
                               person_id, org_name, o_code, face_dst_rel, str(times_visited), bucket_name, bucket_code,
                               camera_code, str(duplicate), dump_path_rel, stored, txn_obj_id, txn_face_id)

        j += 1

    source = dir_path + temp_img_dir + txn_img_id + '_' + time.replace(' ', '_') + '.jpg'
    destination = dump_path
    rename(source, destination)
    return json_initial


def to_json(json_input, name, face_id, timestamp, txn_img_id, top, bottom, left, right, person_id, org_name, org_code,
            file_path, times_visited, bucket_name, bucket_code, camera, is_duplicate, dump_path, stored, txn_obj_id,
            txn_face_id):

    json_input_dict = json.loads(json_input)
    list_old = json_input_dict['Face Data']
    i = len(list_old)

    list_new = [
        {
            "Face No": (i+1),
            "Name": name,
            "Face ID": face_id,
            "timestamp": timestamp,
            "txn_img_id": txn_img_id,
            "top": top,
            "bottom": bottom,
            "left": left,
            "right": right,
            "Person ID": person_id,
            "Organisation": org_name,
            "organization Code": org_code,
            "File Path": file_path,
            "Times Visited": times_visited,
            "Bucket Name": bucket_name,
            "Bucket Code": bucket_code,
            "Camera": camera,
            "Is Duplicate": is_duplicate,
            "Stored": stored,
            "txn_obj_id": txn_obj_id,
            "txn_face_id": txn_face_id

         }
    ]

    json_input_dict['Face Data'] = list_new + list_old
    json_input_dict['Dump Path'] = dump_path
    json_input_dict['No of faces encoded'] += 1
    json_append = json.dumps(json_input_dict, indent=5, sort_keys=False)

    return json_append


def update_info(table, id_name, i_d, column, data):
    """
    To update the details of a row
    :param table: Name of the table to be updated
    :param id_name: Name of the column whose value is known to us and used as a filter
    :param i_d: Value of the above column known to us
    :param column: Name of the column to be updated
    :param data: Value of the column to be updated
    :return: Nothing
    """

    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        sql = "update {} set `{}`='{}' where `{}`={};".format(table, column, data, id_name, i_d)
        cursor.execute(sql)
        connection.commit()


def get_datetime(fn):
    """
    To get the date and time when the image was captured/created from the meta data of the image
    :param fn: Filename of the image
    :return: DateTime or error string
    """
    ret = {}
    final = ''
    i = Image.open(fn)
    info = i._getexif()
    try:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        try:
            temp = ret['DateTime'].split(' ')
            final = temp[0].replace(':', '-') + ' ' + temp[1]
        except:
            try:
                temp = ret['DateTimeOrignal'].split(' ')
                final = temp[0].replace(':', '-') + ' ' + temp[1]
            except:
                final = sys.exc_info()[1]

        return final
    except:
        return final


def add_new_obj_txn(txn_img_id, oid, bucket_id, camera_id, time_capture, obj_top, obj_left, obj_right,
                    obj_down, is_face):
    """
    To add a new object transaction in the database
    :param txn_img_id: Transaction ID of the image
    :param oid: Organisation ID of the camera
    :param bucket_id: Bucket ID of the camera
    :param camera_id: Camera ID
    :param time_capture: Date and time of image capture
    :param obj_top: Coordinates of top of the object
    :param obj_left: Coordinates of left of the object
    :param obj_right: Coordinates of right of the object
    :param obj_down: Coordinates of down of the object
    :param is_face: Whether the object is a face or not
    :return: It returns two values, 1) Error/success codes 2) Object ID
    """

    connection = sql_connection()[1]
    try:
        with connection.cursor() as cursor:
            cursor.callproc('new_object', [txn_img_id, oid, bucket_id, camera_id, time_capture, obj_top, obj_left,
                                           obj_right, obj_down, is_face])
            obj_id = cursor.fetchall()[0]['id']
        return 216, obj_id
    except:
        return 126, sys.exc_info()[1]


def add_person(face_path, org_id):
    """
    To add a new a person detected
    :param face_path: Face path
    :param org_id: Organisation ID of the camera
    :return: Person ID
    """
    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        cursor.callproc('new_person', [face_path, org_id])
        person_id = cursor.fetchall()[0]['id']
    return person_id


def add_new_face_txn(txn_img_id, txn_obj_id, oid, bucket_id, camera_id, time_capture):
    """
    To add a new/duplicate face detected in face transaction table
    :param txn_img_id: Transaction ID of the image it was part of
    :param txn_obj_id: Transaction ID of the object
    :param oid: Organisation ID of the camera
    :param bucket_id: Bucket ID of the camera
    :param camera_id: Camera ID
    :param time_capture: Date and time of capture of face by camera
    :return: It returns two values, 1) Error/success codes 2) Face Transaction ID
    """

    connection = sql_connection()[1]
    try:
        with connection.cursor() as cursor:
            cursor.callproc('new_txn_face', [txn_img_id, txn_obj_id, oid, bucket_id, camera_id, time_capture])
            txn_face_id = cursor.fetchall()[0]['id']
        return 217, txn_face_id
    except:
        return 127, sys.exc_info()[1]


def update_face_txn(txn_face_id, faceid, isduplicate, timesvisited, personid):
    """
    To update the details of a face in tx_face_id table
    :param txn_face_id: Transaction Face ID of the face whose values need to be updated
    :param faceid: Value of Face ID to be updated
    :param isduplicate: Value of isduplicate to be updated
    :param timesvisited: Value of Times Visited to be updated
    :param personid: Value of Person ID to be updated
    :return: It returns two values, 1) Error/success codes 2) Error/Success string
    """

    connection = sql_connection()[1]
    try:
        with connection.cursor() as cursor:
            sql = " UPDATE tx_face_id SET `faceid` = %s, `isduplicate` = %s,`timesvisited` = %s," \
                  " `personid` = %s WHERE `tx_face_id` = %s"
            cursor.execute(sql, (faceid, isduplicate, timesvisited, personid, txn_face_id))
            connection.commit()
        return 219, errordict[219]
    except:
        return 129, sys.exc_info()[1]


def initial_transaction(bucket_id, oid, camera_id):
    """
    To add an image transaction and update details later
    :param bucket_id: Bucket ID of the camera
    :param oid: Organisation ID of the camera
    :param camera_id: Camera ID
    :return: It returns two values, 1) Error/success codes 2) Image ID
    """
    connection = sql_connection()[1]
    try:
        with connection.cursor() as cursor:
            cursor.callproc('new_txn_image', [bucket_id, oid, camera_id])
            img_id = cursor.fetchall()[0]['id']
        return 215, img_id
    except:
        return 125, sys.exc_info()[1]


def full_img_txn(tx_img_id, img_path, time_capture, time_receive):
    """
    To update the details of an image
    :param tx_img_id: Image transaction ID
    :param img_path: Path of the image
    :param time_capture: Date and time when image was captured/created
    :param time_receive: Date and time when image was received by the system
    :return: It returns two values, 1) Error/success codes 2) Error/Success string
    """
    connection = sql_connection()[1]
    try:
        with connection.cursor() as cursor:
            sql = " UPDATE tx_img_id SET `timecapture` = %s, `timereceive`= %s,`path` = %s WHERE `tx_img_id` = %s)"
            cursor.execute(sql, (time_capture, time_receive, img_path, tx_img_id))
            connection.commit()
        return 214, errordict[214]

    except:
        return 124, sys.exc_info()[1]

