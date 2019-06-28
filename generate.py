from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import master
import pymysql

app = Flask(__name__)


def sql_connection():

    connection = pymysql.connect(host='192.168.1.222',
                                 user='Sparsh',
                                 password='Nihar@123',
                                 db='FaceData',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


@app.route('/')
def index():
    message = "please enter valid credentials."
    return render_template('india.html', value=message)


@app.route('/generateReport', methods=['GET', 'POST'])
def generate_report():
    id_type = request.form['type']
    i_d = request.form['code'][3:]
    is_duplicate = request.form['Duplicate']
    times_visited = request.form['Times_Visited']
    xd_from = request.form['from_date']
    xd_to = request.form['to_date']
    xt_from = request.form['from_time']
    xt_to = request.form['to_time']
    from_dt = xd_from + ' ' + xt_from + ':00'
    to_dt = xd_to + ' ' + xt_to + ':00'
    if request.form['submiT'] == 'excel':
        file_name = master.generate_xls(id_type, i_d, from_dt, to_dt)
        return render_template('det.html', filename=file_name)
    else:
        with sql_connection().cursor() as cursor:
            if (times_visited == "zero") & (is_duplicate == "zero"):
                cursor.execute("SELECT `isduplicate`, `timesvisited`, `timecapture`, `path` "
                               "FROM tx_face_id where {} = '{}' "
                               "and timecapture between '{}' and '{}'".format(id_type, i_d, from_dt, to_dt))
            elif times_visited == "zero":
                cursor.execute("SELECT `isduplicate`, `timesvisited`, `timecapture`, `path` "
                               "FROM tx_face_id where {} = '{}' and `isduplicate` = {} "
                               "and timecapture between '{}' and '{}'".format(id_type, i_d, is_duplicate,
                                                                              from_dt, to_dt))
            else:
                cursor.execute("SELECT `isduplicate`, `timesvisited`, `timecapture`, `path` "
                               "FROM tx_face_id where {} = '{}' and `timesvisited` = {} "
                               "and timecapture between '{}' and '{}'".format(id_type, i_d, times_visited, from_dt, to_dt))
            field_names = [i[0] for i in cursor.description]
            return render_template('ind2.html', data=cursor, field=field_names, x_id=id_type, x_code=i_d,
                                   xd_from=xd_from, xd_to=xd_to, xt_from=xt_from, xt_to=xt_to)


@app.route('/photo/<path:filename>')
def download_file(filename):

    sep_path = filename.split('/')
    i = 1
    lead = len(sep_path) - 2
    join_path = ''
    while i < lead:
        join_path = join_path + sep_path[i] + '/'
        i += 1
    join_path = join_path + sep_path[lead]
    n = sep_path[lead + 1]
    return send_from_directory(join_path, n, as_attachment=True)


@app.route('/hell/<path:filename>')
def down(filename):
    return send_from_directory('report_xls', filename, as_attachment=True)


"""
@app.route('/request', methods=['POST'])
def change_request():
    k = 0
    oid = request.form['Organisations']
    table_name = request.form['table_name']
    is_duplicate = request.form['Duplicate']
    times_visited = request.form['Times_Visited']
    with sql_connection().cursor() as cursor:
        cursor.execute("SELECT * FROM {} where `oid` = {}".format(table_name, oid))
        field_names = [i[0] for i in cursor.description]
        if times_visited == "":
            if is_duplicate != "":
                if 'isduplicate' in field_names:
                    cursor.execute("SELECT * FROM {} where `oid` = {} and `isduplicate` = {}".format(table_name, oid,
                                                                                                     is_duplicate))
        else:
            for i in times_visit:
                if i in field_names:
                    k = 1
                    cursor.execute("SELECT * FROM {} where `oid` = {} and {} = {}".format(table_name, oid, i,
                                                                                          times_visited))
                    break
            if (is_duplicate != "") & (k == 0):
                k = 0
                if 'isduplicate' in field_names:
                    cursor.execute("SELECT * FROM {} where `oid` = {} and `isduplicate` = {}".format(table_name, oid,
                                                                                                     is_duplicate))
        for i in path_names:
            if i in field_names:
                return render_template('ind.html', data=cursor, field=field_names, path1=i, o_id=oid, tables=table_name)
            return render_template('ind.html', data=cursor, field=field_names, path1='None', o_id=oid,
                                   tables=table_name)

"""

if __name__ == '__main__':
    app.run(host='192.168.1.206', debug=True, port=5000, threaded=True)
