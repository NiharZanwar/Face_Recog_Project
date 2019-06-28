import os
from flask import Flask, render_template, request, redirect, url_for
import time
import datetime
import Final_Project
import json
import sys


app = Flask(__name__)

render_issue = 000
delete_issue = 1000


@app.route('/')
def hello_world():
    try:
        return render_template('index backup.html')
    except:
        return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))


@app.route('/org')
def org_create():
    try:
        return render_template('org_reg.html')
    except:
        return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))


@app.route('/orgdes')
def org_delete():
    try:
        return render_template('org_del.html')
    except:
        return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))


@app.route('/user')
def user_create():
    try:
        return render_template('user_reg.html')
    except:
        return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))


@app.route('/userdes')
def user_delete():
    try:
        return render_template('user_del.html')
    except:
        return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))


@app.route('/bucket')
def bucket_create():
    try:
        return render_template('bucket_reg.html')
    except:
        return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))


@app.route('/bucketdes')
def bucket_delete():
    try:
        return render_template('bucket_del.html')
    except:
        return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))


@app.route('/camera')
def camera_create():
    try:
        return render_template('camera_reg.html')
    except:
        return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))


@app.route('/camerades')
def camera_delete():
    try:
        return render_template('camera_del.html')
    except:
        return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))


@app.route('/user_success', methods=['POST'])
def user_new():
    test_connection = Final_Project.sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    display_name = request.form['display_name']
    orgcode = request.form['orgcode']
    created_date_time = str(datetime.datetime.now())
    check = Final_Project.extract_info('organisation', 'orgcode', orgcode)
    if check[0] == 228:
        oid = check[1][0]['oid']
        nextcheck = Final_Project.create_new_user(username, password, email, created_date_time, oid, display_name)
        if nextcheck[0] == 212:
            try:
                return render_template('user_code.html', value=username)
            except:
                return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))
        else:
            return redirect(url_for('error', error_str=nextcheck[1], error_code=nextcheck[0]))
    else:
        return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/org_success', methods=['POST'])
def org_new():
    test_connection = Final_Project.sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    name = request.form['name']
    email = request.form['email']
    logo = request.form['logo']
    orgkey = request.form['orgkey']
    created_date_time = str(datetime.datetime.now())
    check = Final_Project.add_new_org(name, logo, email, created_date_time, orgkey)
    if check[0] == 203:
        orgcode = check[1]
        try:
            return render_template('org_code.html', value=orgcode)
        except:
            return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))
    else:
        return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/bucket_success', methods=['POST'])
def bucket_new():
    test_connection = Final_Project.sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    name = request.form['name']
    orgcode = request.form['org_code']
    created_date_time = str(datetime.datetime.now())
    check = Final_Project.add_new_bucket(name, created_date_time, orgcode)
    if check[0] == 204:
        bucket_code = check[1]
        try:
            return render_template('bucket_code.html', value=bucket_code)
        except:
            return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))
    else:
        return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/camera_success', methods=['POST'])
def camera_new():
    test_connection = Final_Project.sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    name = request.form['name']
    ctype = request.form['type']
    bucket_code = request.form['bucket_code']
    created_date_time = str(datetime.datetime.now())

    check = Final_Project.extract_info('orgbucket', 'bucketcode', bucket_code)
    if check[0] == 228:
        org_id = check[1][0]['oid']
        check2 = Final_Project.extract_info('organisation', 'oid', org_id)
        if check2[0] == 228:
            org_code = check2[1][0]['orgcode']
            check3 = Final_Project.add_new_camera(name, bucket_code, ctype, org_code, created_date_time)
            if check3[0] == 202:
                camera_code = check3[1]
                try:
                    return render_template('camera_code.html', value=camera_code)
                except:
                    return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))
            else:
                return redirect(url_for('error', error_str=check3[1], error_code=check3[0]))
        else:
            return redirect(url_for('error', error_str=check2[1], error_code=check2[0]))
    else:
        return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/error/<error_code>/<error_str>')
def error(error_code, error_str):
    return render_template('error.html', error=error_str, error_code=error_code)


@app.route('/camera_deletes', methods=['POST'])
def camera_():
    test_connection = Final_Project.sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    camera_code = request.form['code']
    check = Final_Project.extract_info('orgCamera', 'cameracode', camera_code)
    if check[0] == 228:
        camera_id = check[1][0]['cameraid']
        try:
            Final_Project.del_camera(camera_id)
            try:
                return render_template('delete.html')
            except:
                return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))
        except:
            return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=delete_issue))
    else:
        return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/bucket_deletes', methods=['POST'])
def bucket_():
    test_connection = Final_Project.sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    bucket_code = request.form['code']
    check = Final_Project.extract_info('orgbucket', 'bucketcode', bucket_code)
    if check[0] == 228:
        bucket_id = check[1][0]['bucketid']
        try:
            Final_Project.del_bucket(bucket_id)
            try:
                return render_template('delete.html')
            except:
                return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))
        except:
            return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=delete_issue))
    else:
        return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/user_deletes', methods=['POST'])
def user_():
    test_connection = Final_Project.sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    user_id = request.form['uid']
    try:
        Final_Project.del_user(user_id)
        try:
            return render_template('delete.html')
        except:
            return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=delete_issue))


@app.route('/org_deletes', methods=['POST'])
def org_():
    test_connection = Final_Project.sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    org_code = request.form['code']
    check = Final_Project.extract_info('organisation', 'orgcode', org_code)
    if check[0] == 228:
        org_id = check[1][0]['oid']
        try:
            Final_Project.del_org(org_id)
            try:
                return render_template('delete.html')
            except:
                return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))
        except:
            return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=delete_issue))
    else:
        return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/upload', methods=['POST'])
def upload_file():
    start = time.time()
    UPLOAD_FOLDER = os.path.basename('temp_img_dir')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    time_now = str(datetime.datetime.now())
    cameracode = request.form['camcode']
    # cameracode = 'CAM000000031'
    camera_id = cameracode[3:]

    info = Final_Project.extract_info(Final_Project.s_cam_table, Final_Project.s_cam_id, camera_id)[1]

    if info[0] == 128:
        return redirect(url_for('error', error_str=info[1], error_code=info[0]))

    if len(info) == 0:
        return redirect(url_for('error', error_str=Final_Project.errordict[113], error_code=113))

    if str(info[0][Final_Project.s_mrkdel]) == '1':
        return redirect(url_for('error', error_str=Final_Project.errordict[114], error_code=114))

    bucket_id = info[0][Final_Project.s_buc_id]
    oid = info[0][Final_Project.s_org_id]
    bucket_code = 'BUC' + str(bucket_id).zfill(9)
    o_code = 'ORG' + str(oid).zfill(5)

    file = request.files['image']
    imgtxn_id = str((Final_Project.initial_transaction(bucket_id, oid, camera_id))[1]).zfill(10)
    file.filename = imgtxn_id + '_' + time_now.replace(' ', '_') + '.jpg'
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)

    time_capture = Final_Project.get_datetime(Final_Project.dir_path + Final_Project.temp_img_dir + file.filename)
    if len(time_capture) == 0:
        time_capture = time_now

    img_path = Final_Project.Organisation + o_code + '/' + bucket_code + '/' + cameracode + '_dump/' + file.filename
    Final_Project.full_img_txn(imgtxn_id, img_path, time_capture, time_now)

    json1 = Final_Project.input_image(cameracode, time_now, imgtxn_id, bucket_id, oid, camera_id)
    json_2 = json.loads(json1)
    end = time.time()
    time_taken = start - end
    res = json.dumps(json_2, indent=4, sort_keys=True) + str(time_taken)
    return render_template('result.html', value=res)


if __name__ == '__main__':
    app.run(host='192.168.1.206', debug=True, port=5004, threaded=True)
