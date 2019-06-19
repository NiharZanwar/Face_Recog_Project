import os
from flask import Flask, render_template, request, redirect, url_for
import time
import datetime
import Final_Project
import json


app = Flask(__name__)

render_issue = 000


@app.route('/')
def login():
    return render_template('upload_photo.html')


@app.route('/dashboard', methods=['POST'])
def login_check():

    test_connection = Final_Project.sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    username = request.form['username']
    password = request.form['pass']
    o_code = request.form['org_code']

    check = Final_Project.verify_user(username, password, o_code)
    if check[0] == 205:
        try:
            return render_template('upload_photo.html')
        except:
            return redirect(url_for('error', error_str=sys.exec_info()[1], error_code=render_issue))
    else:
        return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/error/<error_code>/<error_str>')
def error(error_str, error_code):
    return render_template('error_login.html', error=error_str, error_code=error_code)


@app.route('/upload', methods=['POST'])
def upload_file():
    start = time.time()
    UPLOAD_FOLDER = os.path.basename('temp_img_dir')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cameracode = request.form['camcode']
    
    try:
        time_from_request = request.form['time']
    except:
        time_from_request = ''
    
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
    file.filename = imgtxn_id + '_' + time_now + '.jpg'
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)

    time_capture = Final_Project.get_datetime(Final_Project.dir_path + Final_Project.temp_img_dir + file.filename)  ##reduced to relative
    if len(time_capture) == 0:
        time_capture = time_now
    if len(time_from_request) != 0:
        time_capture = time_from_request

    img_path = Final_Project.Organisation + o_code + '/' + bucket_code + '/' + cameracode + '_dump/' + file.filename  ##reduced to relative
    Final_Project.full_img_txn(imgtxn_id, img_path, time_capture, time_now)
    # Final_Project.update_info(Final_Project.s_txn_img_table,Final_Project.s_tximg_id, imgtxn_id, 'path', img_path)
    json1 = Final_Project.input_image(cameracode, time_now, imgtxn_id, bucket_id, oid, camera_id)
    json_2 = json.loads(json1)
    end = time.time()
    time_taken = start - end
    res = json.dumps(json_2, indent=4, sort_keys=True) + str(time_taken)
    return render_template('result.html', value=res)
    # return ('<pre>'+json.dumps(json_2, indent=4, sort_keys=True)+str(time_taken) + '</pre>')
    # return (json.dumps(json_2, indent=4, sort_keys=True)+str(time_taken))


@app.route('/Manual', methods=['POST'])
def upload_fil():
    start = time.time()
    UPLOAD_FOLDER = os.path.basename('temp_img_dir')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cameracode = request.form['camcode']

    try:
        time_from_request = request.form['time']
    except:
        time_from_request = ''

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
    file.filename = imgtxn_id + '_' + time_now + '.jpg'
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)

    time_capture = Final_Project.get_datetime(
        Final_Project.dir_path + Final_Project.temp_img_dir + file.filename)  ##reduced to relative
    if len(time_capture) == 0:
        time_capture = time_now
    if len(time_from_request) != 0:
        time_capture = time_from_request

    img_path = Final_Project.Organisation + o_code + '/' + bucket_code + '/' + cameracode + '_dump/' + file.filename  ##reduced to relative
    Final_Project.full_img_txn(imgtxn_id, img_path, time_capture, time_now)
    # Final_Project.update_info(Final_Project.s_txn_img_table,Final_Project.s_tximg_id, imgtxn_id, 'path', img_path)
    json1 = Final_Project.input_image(cameracode, time_now, imgtxn_id, bucket_id, oid, camera_id)
    json_2 = json.loads(json1)
    end = time.time()
    time_taken = start - end
    res = json.dumps(json_2, indent=4, sort_keys=True) + str(time_taken)
    return res
    # return ('<pre>'+json.dumps(json_2, indent=4, sort_keys=True)+str(time_taken) + '</pre>')
    # return (json.dumps(json_2, indent=4, sort_keys=True)+str(time_taken))


if __name__ == '__main__':
    app.run(host='192.168.1.222', debug=True, port=5000, threaded=True)