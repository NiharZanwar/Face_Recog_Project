from flask import Flask, render_template, request, send_from_directory
import pymysql


def sql_connection():
    connection = pymysql.connect(host='192.168.1.222',
                                 user='Sparsh',
                                 password='Nihar@123',
                                 db='FaceData',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection


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
def is_none(n):
    if type(n) == 'NoneType':
        return True
    else:
        return False
"""


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


"""
ql_query(id_type, i_d, from_dt, to_dt):
    connection = sql_connection()[1]
    with connection.cursor() as cursor:
        query = "SELECT * from tx_face_id where {} = '{}'" \
                 " and timecapture between '{}' and '{}'".format(id_type, i_d, from_dt, to_dt)
        cursor.execute(query)
        result = cursor.fetchall()
        return result
"""
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = "my precious"

extra = ['Product_Type', 'Geography', 'Third']


@app.route("/category", methods=["GET", "POST"])
def index():
"""
"""Render form and handle form submission"""
"""
    form = TestForm(request.form)
    form.category_1.choices = [('', 'Select a Category')] + [(x) for x in enumerate(extra,1)]
    chosen_category_1 = None
    chosen_category_2 = None
    chosen_category_3 = None
    return render_template('index.html', form=form)

@app.route("/category/<int:category_1_id>/", methods=["POST"])
def get_request(category_1_id):
    data = [(x) for x in enumerate(extra,1)
        if x[0] != category_1_id]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

foodList = ['76', '87', '78']
foodKind = ['delhi', 'suxxex']


@app.route('/', methods=['GET', 'POST'])
def index():
    # foodList = [ i.type for i in db.session.query(FoodType)]
    return render_template('killer.html', food=foodList)


@app.route('/foodkind', methods=['GET', 'POST'])
def foodkind():
        selection = request.form['foodChoice']
        # foodKind = [ i.kind for i in db.session.query(FoodType).filter(FoodKind == selection)]
        return render_template('killer.html', foodChoice=foodKind)


food = {
    'fruit': ['apple', 'banana', 'cherry'],
    'vegetables': ['onion', 'cucumber'],
    'meat': ['sausage', 'beef'],
}


@app.route('/get_food/<foodkind>')
def get_food(foodkind):
    if foodkind not in food:
        return jsonify([])
    else:
        return jsonify(food[foodkind])

"""
if __name__ == '__main__':
    app.run(host='192.168.1.206', debug=True, port=5000, threaded=True)
