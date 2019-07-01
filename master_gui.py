from flask import Flask, render_template, request, redirect, url_for
import datetime
from functions import extract_info, add_new_bucket, add_new_camera, add_new_org, sql_connection, del_bucket, \
    del_camera, del_org, del_user, create_new_user, initialization
import sys
from details import forms, org_form, camera_form, user_form, bucket_form

app = Flask(__name__)

render_issue = 000
delete_issue = 1000


@app.route('/')
def home():
    try:
        return render_template('master_home.html', forms=forms)
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/New_Registration/<path:form_str>/<form_rdt>')
def new_create(form_str, form_rdt):
    forms_list = form_str.split(',')
    try:
        return render_template('registration.html', formreq=forms_list, form_redirect=form_rdt)
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/Delete/<option>')
def delete_x(option):
    try:
        return render_template('delete_x.html', name=option)
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/User_Created', methods=['POST'])
def user_new():
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    username = request.form[user_form[0]]
    password = request.form[user_form[1]]
    email = request.form[user_form[2]]
    orgcode = request.form[user_form[3]]
    display_name = request.form[user_form[4]]
    created_date_time = str(datetime.datetime.now())
    check = extract_info('organisation', 'orgcode', orgcode)
    if check[0] == 228:
        oid = check[1][0]['oid']
        nextcheck = create_new_user(username, password, email, created_date_time, oid, display_name)
        if nextcheck[0] == 212:
            try:
                return render_template('code_gen.html', name='User Name', value=username)
            except:
                return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
        else:
            return redirect(url_for('error', error_str=nextcheck[1], error_code=nextcheck[0]))
    return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/Organisation_Created', methods=['POST'])
def org_new():
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))
    initialization()
    name = request.form[org_form[0]]
    email = request.form[org_form[1]]
    logo = request.form[org_form[2]]
    orgkey = request.form[org_form[3]]
    created_date_time = str(datetime.datetime.now())
    check = add_new_org(name, logo, email, created_date_time, orgkey)
    if check[0] == 203:
        orgcode = check[1]
        try:
            return render_template('code_gen.html', name='Organisation Code', value=orgcode)
        except:
            return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
    return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/Bucket_Created', methods=['POST'])
def bucket_new():
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    name = request.form[bucket_form[0]]
    orgcode = request.form[bucket_form[1]]
    created_date_time = str(datetime.datetime.now())
    check = add_new_bucket(name, created_date_time, orgcode)
    if check[0] == 204:
        bucket_code = check[1]
        try:
            return render_template('code_gen.html', name='Bucket Code', value=bucket_code)
        except:
            return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
    return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/Camera_Created', methods=['POST'])
def camera_new():
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    name = request.form[camera_form[0]]
    ctype = request.form[camera_form[1]]
    bucket_code = request.form[camera_form[2]]
    created_date_time = str(datetime.datetime.now())

    check = extract_info('orgbucket', 'bucketcode', bucket_code)
    if check[0] == 228:
        check1 = add_new_camera(name, bucket_code, ctype, created_date_time)
        if check1[0] == 202:
            camera_code = check1[1]
            try:
                return render_template('code_gen.html', name='Camera Code', value=camera_code)
            except:
                return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))
        else:
            return redirect(url_for('error', error_str=check1[1], error_code=check1[0]))
    return redirect(url_for('error', error_str=check[1], error_code=check[0]))


@app.route('/Camera_Deleted', methods=['POST'])
def camera_delete():
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


@app.route('/Bucket_Deleted', methods=['POST'])
def bucket_delete():
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


@app.route('/User_Deleted', methods=['POST'])
def user_delete():
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


@app.route('/Organisation_Deleted', methods=['POST'])
def organisation_delete():
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


@app.route('/error/<error_code>/<error_str>')
def error(error_code, error_str):
    return render_template('error.html', error=error_str, error_code=error_code)


if __name__ == '__main__':
    app.run(host='192.168.1.214', debug=True, port=5071, threaded=True)
