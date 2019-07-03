from flask import Flask, render_template, request, send_from_directory
from convert_to_excel import generate_xls
from functions import sql_connection

app = Flask(__name__)
connection = sql_connection()


@app.route('/')
def index():
    """
    Displays the homepage to input the details for viewing/downloading report
    :return: Renders report_home.html
    """
    message = "Enter the required details"      # message to be displayed on homepage
    return render_template('report_home.html', value=message)


@app.route('/generateReport', methods=['GET', 'POST'])
def generate_report():
    """
    Takes the values entered by the user and displays/downloads the report accordingly
    :return: Displays the report if 'View Report' is clicked or the download link if 'Download Report' is clicked
    """
    id_type = request.form['type']                      # Level of data to be fetched
    x_code = request.form['code']                       # Code of the required level
    i_d = x_code[3:]                                    # ID
    is_duplicate = request.form['Duplicate']            # Value of 'isduplicate'
    times_visited = request.form['Times_Visited']       # Value of 'timesvisited'
    xd_from = request.form['from_date']                 # Starting date of records to be searched
    xd_to = request.form['to_date']                     # Ending date of records to be searched
    xt_from = request.form['from_time']                 # Starting time of records to be searched
    xt_to = request.form['to_time']                     # Ending time of records to be searched

    from_dt = xd_from + ' ' + xt_from + ':00'           # Converting into proper datetime format
    to_dt = xd_to + ' ' + xt_to + ':00'                 # Converting into proper datetime format
    if request.form['choice'] == 'excel':               # checking if the user wants to download or view the report
        file_name = generate_xls(id_type, i_d, from_dt, to_dt)      # generate_xls is called to generate an excel
        return render_template('report_down.html', filename=file_name)
    else:
        with connection[1].cursor() as cursor:
            if (times_visited == "empty") & (is_duplicate == "empty"):
                cursor.execute("SELECT `isduplicate`, `timesvisited`, `timecapture`, `path` "
                               "FROM tx_face_id where {} = '{}' and "
                               "timecapture between '{}' and '{}'".format(id_type, i_d, from_dt, to_dt))
            elif times_visited == "empty":
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
            return render_template('report_display.html', data=cursor, field=field_names, x_id=id_type,
                                   x_code=x_code, xd_from=xd_from, xd_to=xd_to, xt_from=xt_from,
                                   xt_to=xt_to)


@app.route('/photo/<path:filename>')
def download_file(filename):
    """
    It displays the image in the report
    :param filename: Path of the image including it's name
    :return:
    """
    sep_path = filename.split('/')
    i = 1
    length = len(sep_path) - 2
    file_path = ''
    while i < length:
        file_path = file_path + sep_path[i] + '/'
        i += 1
    file_path = file_path + sep_path[length]
    name = sep_path[length + 1]
    return send_from_directory(file_path, name, as_attachment=True)


@app.route('/download_report/<path:filename>')
def down(filename):
    """
    To generate the download link of the report
    :param filename: File name of the report
    :return: Returns the file having name = filename from current_directory/report_xls/
    """
    return send_from_directory('report_xls', filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='192.168.1.214', debug=True, port=5000, threaded=True)
