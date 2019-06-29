from flask import Flask, render_template, request, redirect, url_for
import datetime
from Final_Project import extract_info, add_new_bucket, add_new_camera, add_new_org, sql_connection, del_bucket, \
    del_camera, del_org, del_user, create_new_user, initialization
import sys


app = Flask(__name__)

render_issue = 000
delete_issue = 1000


@app.route('/')
def hello_world():
    try:
        return render_template('index backup.html')
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/org')
def org_create():
    try:
        return render_template('org_reg.html')
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/orgdes')
def org_delete():
    try:
        return render_template('org_del.html')
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/user')
def user_create():
    try:
        return render_template('user_reg.html')
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/userdes')
def user_delete():
    try:
        return render_template('user_del.html')
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/bucket')
def bucket_create():
    try:
        return render_template('bucket_reg.html')
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/bucketdes')
def bucket_delete():
    try:
        return render_template('bucket_del.html')
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/camera')
def camera_create():
    try:
        return render_template('camera_reg.html')
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/camerades')
def camera_delete():
    try:
        return render_template('camera_del.html')
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/user_success', methods=['POST'])
def user_new():
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    display_name = request.form['display_name']
    orgcode = request.form['orgcode']
    created_date_time = str(datetime.datetime.now())
    check = extract_info('organisation', 'orgcode', orgcode)
    if check[0] == 228:
        oid = check[1][0]['oid']
        nextcheck = create_new_user(username, password, email, created_date_time, oid, display_name)
        if nextcheck[0] == 212:
            try:
                return render_template('user_code.html', value=username)
            except:
                return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
        else:
            return redirect(url_for('error', error_str=nextcheck[1], error_code=nextcheck[0]))
    return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/org_success', methods=['POST'])
def org_new():
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))
    initialization()
    name = request.form['name']
    email = request.form['email']
    logo = request.form['logo']
    orgkey = request.form['orgkey']
    created_date_time = str(datetime.datetime.now())
    check = add_new_org(name, logo, email, created_date_time, orgkey)
    if check[0] == 203:
        orgcode = check[1]
        try:
            return render_template('org_code.html', value=orgcode)
        except:
            return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
    return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/bucket_success', methods=['POST'])
def bucket_new():
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    name = request.form['name']
    orgcode = request.form['org_code']
    created_date_time = str(datetime.datetime.now())
    check = add_new_bucket(name, created_date_time, orgcode)
    if check[0] == 204:
        bucket_code = check[1]
        try:
            return render_template('bucket_code.html', value=bucket_code)
        except:
            return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
    return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/camera_success', methods=['POST'])
def camera_new():
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    name = request.form['name']
    ctype = request.form['type']
    bucket_code = request.form['bucket_code']
    created_date_time = str(datetime.datetime.now())

    check = extract_info('orgbucket', 'bucketcode', bucket_code)
    if check[0] == 228:
        check1 = add_new_camera(name, bucket_code, ctype, created_date_time)
        if check1[0] == 202:
            camera_code = check1[1]
            try:
                return render_template('camera_code.html', value=camera_code)
            except:
                return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
        else:
            return redirect(url_for('error', error_str=check1[1], error_code=check1[0]))
    return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/error/<error_code>/<error_str>')
def error(error_code, error_str):
    return render_template('error.html', error=error_str, error_code=error_code)


@app.route('/camera_deletes', methods=['POST'])
def camera_():
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    camera_code = request.form['code']
    check = extract_info('orgCamera', 'cameracode', camera_code)
    if check[0] == 228:
        camera_id = check[1][0]['cameraid']
        try:
            del_camera(camera_id)
            try:
                return render_template('delete.html')
            except:
                return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
        except:
            return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=delete_issue))
    return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/bucket_deletes', methods=['POST'])
def bucket_():
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    bucket_code = request.form['code']
    check = extract_info('orgbucket', 'bucketcode', bucket_code)
    if check[0] == 228:
        bucket_id = check[1][0]['bucketid']
        try:
            del_bucket(bucket_id)
            try:
                return render_template('delete.html')
            except:
                return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
        except:
            return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=delete_issue))
    return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/user_deletes', methods=['POST'])
def user_():
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    user_id = request.form['uid']
    try:
        del_user(user_id)
        try:
            return render_template('delete.html')
        except:
            return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=delete_issue))


@app.route('/org_deletes', methods=['POST'])
def org_():
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    org_code = request.form['code']
    check = extract_info('organisation', 'orgcode', org_code)
    if check[0] == 228:
        org_id = check[1][0]['oid']
        try:
            del_org(org_id)
            try:
                return render_template('delete.html')
            except:
                return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
        except:
            return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=delete_issue))
    return redirect(url_for('error', error_str=check[1], error_code=check[0]))


if __name__ == '__main__':
    app.run(host='192.168.1.206', debug=True, port=5071, threaded=True)
