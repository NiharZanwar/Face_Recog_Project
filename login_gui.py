import os
from flask import Flask, render_template, request, redirect, url_for
import datetime
from functions import sql_connection, extract_info, verify_user, errordict, get_datetime, input_image, full_img_txn
import functions
import json
import sys
import time

app = Flask(__name__)

render_issue = 000


@app.route('/')
def home():
    """
    To display the login page
    :return: Displays login page
    """
    return render_template('login_home.html')


@app.route('/dashboard', methods=['POST'])
def login_check():
    """
    Verifies the credentials entered by the user to login and logs in if they are correct
    :return:
    """

    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    username = request.form['username']
    password = request.form['pass']
    o_code = request.form['org_code']

    check = verify_user(username, password, o_code)
    if check[0] == 205:
        try:
            return redirect(url_for('login_done', username=username))
        except:
            return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
    else:
        return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/dashboard/<username>')
def login_done(username):
    """
    This function displays the homepage of a user
    :param username:
    :return:
    """
    return render_template('dashboard.html', username=username)


@app.route('/error/<error_code>/<error_str>')
def error(error_str, error_code):
    """
    This function displays any error that occurs during the program and doesn't let the system to crash
    :param error_str: Code of the error manually assigned or assigned by system
    :param error_code: Error string manually defined or by system.
    :return: Displays error code and error string
    """

    return render_template('error.html', error=error_str, error_code=error_code)


@app.route('/upload/<username>', methods=['POST'])
def upload_file(username):
    """
    This function takes an image as input and detects the faces in it. Also it updates the database accordingly.
    :param username: User Name of the user who is uploading the image
    :return: Displays necessary data as JSON object containing all the necessary details of the faces detected
    """
    start = time.time()
    upload_folder = os.path.basename('temp_img_dir')
    app.config['UPLOAD_FOLDER'] = upload_folder

    time_now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cameracode = request.form['camcode']
    camera_id = cameracode[3:]

    info = extract_info(functions.s_cam_table, functions.s_cam_id, camera_id)[1]

    if info[0] == 128:
        return redirect(url_for('error', error_str=info[1], error_code=info[0]))

    if len(info) == 0:
        return redirect(url_for('error', error_str=errordict[113], error_code=113))

    if str(info[0][functions.s_mrkdel]) == '1':
        return redirect(url_for('error', error_str=errordict[114], error_code=114))

    bucket_id = info[0][functions.s_buc_id]
    oid = info[0][functions.s_org_id]
    bucket_code = 'BUC' + str(bucket_id).zfill(9)
    o_code = 'ORG' + str(oid).zfill(5)

    file = request.files['image']
    imgtxn_id = str((functions.initial_transaction(bucket_id, oid, camera_id))[1]).zfill(10)
    file.filename = (imgtxn_id + '_' + time_now + '.jpg').replace(' ', '_')
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)

    time_capture = get_datetime(functions.dir_path + functions.temp_img_dir + file.filename)
    if len(time_capture) == 0:
        time_capture = time_now

    img_path = '/Organisations' + o_code + '/' + bucket_code + '/' + cameracode + '_dump/' + file.filename
    full_img_txn(imgtxn_id, img_path, time_capture, time_now)

    json1 = input_image(cameracode, time_now, imgtxn_id, bucket_id, oid, camera_id, time_capture)
    json_2 = json.loads(json1)
    end = time.time()
    time_taken = start - end
    res = json.dumps(json_2, indent=4, sort_keys=True) + str(time_taken)
    return render_template('result.html', value=res, username=username)


@app.route('/Manual', methods=['POST'])
def upload_fil():
    """
    This function is to manually upload images from a specified folder
    :return: JSON object containing all the necessary details of the faces detected
    """
    start = time.time()
    upload_folder = os.path.basename('temp_img_dir')
    app.config['UPLOAD_FOLDER'] = upload_folder

    time_now = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    cameracode = request.form['camcode']
    camera_id = cameracode[3:]

    info = extract_info(functions.s_cam_table, functions.s_cam_id, camera_id)[1]

    if info[0] == 128:
        return redirect(url_for('error', error_str=info[1], error_code=info[0]))

    if len(info) == 0:
        return redirect(url_for('error', error_str=errordict[113], error_code=113))

    if str(info[0][functions.s_mrkdel]) == '1':
        return redirect(url_for('error', error_str=errordict[114], error_code=114))

    bucket_id = info[0][functions.s_buc_id]
    oid = info[0][functions.s_org_id]
    bucket_code = 'BUC' + str(bucket_id).zfill(9)
    o_code = 'ORG' + str(oid).zfill(5)

    file = request.files['image']
    imgtxn_id = str((functions.initial_transaction(bucket_id, oid, camera_id))[1]).zfill(10)
    file.filename = (imgtxn_id + '_' + time_now + '.jpg').replace(' ', '_')
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)

    time_capture = get_datetime(functions.dir_path + functions.temp_img_dir + file.filename)
    if len(time_capture) == 0:
        time_capture = time_now

    img_path = '/Organisations/' + o_code + '/' + bucket_code + '/' + cameracode + '_dump/' + file.filename
    full_img_txn(imgtxn_id, img_path, time_capture, time_now)

    json1 = input_image(cameracode, time_now, imgtxn_id, bucket_id, oid, camera_id, time_capture)
    json_2 = json.loads(json1)
    end = time.time()
    time_taken = start - end
    res = json.dumps(json_2, indent=4, sort_keys=True) + str(time_taken)
    return res


if __name__ == '__main__':
    app.run(host='192.168.1.214', debug=True, port=5006, threaded=True)
