from flask import Flask, render_template, request, redirect, url_for
import datetime
from functions import extract_info, add_new_bucket, add_new_camera, add_new_org, sql_connection, del_bucket, \
    del_camera, del_org, del_user, create_new_user, initialization
import functions
import sys
from details import forms, org_form, camera_form, user_form, bucket_form

app = Flask(__name__)

render_issue = 000
delete_issue = 1000


@app.route('/')
def home():
    """
    This renders the home page of master_gui.py
    :return: Renders master_home.html
    """
    try:
        return render_template('master_home.html', forms=forms)
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/New_Registration/<form_str>/<form_rdt>')
def new_create(form_str, form_rdt):
    """
    This function renders the web-page to register anything which admin wants
    :param form_str: List of fields
    :param form_rdt: Function to it will be redirected after successful creation of what admin wants
    :return: Renders registration.html with two parameters.
            1) formreq - List of fields are required to create what admin wants
            2) form_redirect - form_rdt
    """
    form_list = form_str.split(',')
    try:
        return render_template('registration.html', formreq=form_list, form_redirect=form_rdt)
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/Delete/<option>')
def delete_x(option):
    """
    This function is called when admin wants to delete an organisation, user, camera, or bucket
    :param option: This parameter stores what admin wants to delete
    :return: Renders delete_x.html with passing parameter name = option.
    """
    try:
        return render_template('delete_x.html', name=option)
    except:
        return redirect(url_for('error', error_str=sys.exc_info()[1], error_code=render_issue))


@app.route('/User_Created', methods=['POST'])
def user_new():
    """
    This function checks the values entered to create a new user and if everything is fine, it creates one.
    :return: Displays 'User Name' of the user created
    """
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    username = request.form[user_form[0]]
    password = request.form[user_form[1]]
    email = request.form[user_form[2]]
    orgcode = request.form[user_form[3]]
    display_name = request.form[user_form[4]]
    created_date_time = str(datetime.datetime.now())
    check = extract_info(functions.s_org_table, functions.s_org_code, orgcode)
    if check[0] == 228:
        oid = check[1][0][functions.s_org_id]
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
    """
    This function checks the values entered to create a new organisation and if everything is fine, it creates one.
    :return: Displays 'Org Code' of the organisation created
    """
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
    """
    This function checks the values entered to create a new bucket and if everything is fine, it creates one.
    :return: Displays 'Bucket Code' of the bucket created
    """
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
    """
    This function checks the values entered to create a new camera and if everything is fine, it creates one.
    :return: Displays 'Camera Code' of the camera created
    """
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    name = request.form[camera_form[0]]
    ctype = request.form[camera_form[1]]
    bucket_code = request.form[camera_form[2]]
    created_date_time = str(datetime.datetime.now())

    check = extract_info(functions.s_buc_table, functions.s_buc_code, bucket_code)
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
    """
    This function deletes the camera whose camera code is entered
    :return: Displays 'Deleted Successfully'
    """
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    camera_code = request.form['code']
    check = extract_info(functions.s_cam_table, functions.s_cam_code, camera_code)
    if check[0] == 228:
        camera_id = check[1][0][functions.s_cam_id]
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
    """
    This function deletes the bucket whose bucket code is entered
    :return: Displays 'Deleted Successfully'
    """
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    bucket_code = request.form['code']
    check = extract_info(functions.s_buc_table, functions.s_buc_code, bucket_code)
    if check[0] == 228:
        bucket_id = check[1][0][functions.s_buc_id]
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
    """
    This function deletes the user whose user id is entered
    :return: Displays 'Deleted Successfully'
    """
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    user_id = request.form['id']
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
    """
    This function deletes the organisation whose organisation code is entered
    :return: Displays 'Deleted Successfully'
    """
    test_connection = sql_connection()
    if test_connection[0] == 130:
        return redirect(url_for('error', error_str=test_connection[1], error_code=test_connection[0]))

    org_code = request.form['code']
    check = extract_info(functions.s_org_table, functions.s_org_code, org_code)
    if check[0] == 228:
        org_id = check[1][0][functions.s_org_id]
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
    """
    This function displays any error that occurs during the program and doesn't let the system to crash
    :param error_code: Code of the error manually assigned or assigned by system
    :param error_str: Error string manually defined or by system.
    :return: Displays error code and error string
    """
    return render_template('error.html', error=error_str, error_code=error_code)


if __name__ == '__main__':
    app.run(host='192.168.1.214', debug=True, port=5071, threaded=True)
