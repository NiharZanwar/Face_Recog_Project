from flask import Flask, render_template, request, send_from_directory
from convert_to_excel import generate_xls
from Final_Project import sql_connection

app = Flask(__name__)
connection = sql_connection()


@app.route('/')
def index():
    message = "please enter valid credentials."
    return render_template('report_home.html', value=message)


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
    if request.form['choice'] == 'excel':
        file_name = generate_xls(id_type, i_d, from_dt, to_dt)
        return render_template('report_down.html', filename=file_name)
    else:
        with connection[1].cursor() as cursor:
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
                               "and timecapture between '{}' and '{}'".format(id_type, i_d, times_visited, from_dt,
                                                                              to_dt))
            field_names = [i[0] for i in cursor.description]
            return render_template('report_disp.html', data=cursor, field=field_names, x_id=id_type, x_code=i_d,
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


@app.route('/image/<path:filename>')
def down(filename):
    return send_from_directory('report_xls', filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='192.168.1.214', debug=True, port=5000, threaded=True)
