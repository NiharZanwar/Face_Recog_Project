from flask import Flask, render_template, request, send_from_directory
from Final_Project import sql_connection


app = Flask(__name__)

render_issue = 000
path_names = ['path', 'FacePath', 'face_path_1']
times_visit = ['timesvisited', 'TimesVisited']
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def login_done():
    return render_template('hey1.html')


@app.route('/request', methods=['POST'])
def change_request():
    k = 0
    oid = request.form['Organisations']
    table_name = request.form['table_name']
    is_duplicate = request.form['Duplicate']
    times_visited = request.form['Times_Visited']
    with sql_connection()[1].cursor() as cursor:
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
                if 'isduplicate' in field_names:
                    cursor.execute("SELECT * FROM {} where `oid` = {} and `isduplicate` = {}".format(table_name, oid,
                                                                                                     is_duplicate))
        for i in path_names:
            if i in field_names:
                return render_template('ind.html', data=cursor, field=field_names, path1=i, o_id=oid, tables=table_name)
            return render_template('ind.html', data=cursor, field=field_names, path1='None', o_id=oid,
                                   tables=table_name)


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


if __name__ == '__main__':
    app.run(host='192.168.1.206', debug=True, port=5000, threaded=True)
