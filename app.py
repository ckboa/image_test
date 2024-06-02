# this is the api for save file.... May 30, 2024
# https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask
# https://medium.com/@brodiea19/flask-sqlalchemy-how-to-upload-photos-and-render-them-to-your-webpage-84aa549ab39e


from flask import Flask, request, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import imghdr
from flask_mysqldb import MySQL
from flask_cors import CORS
from datetime import datetime
 
app = Flask(__name__)
CORS(app)
 
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'test'
app.config['MYSQL_DB'] = 'esp_data'
mysql = MySQL(app)

upload = 'J:/pic_test/test2/test3'

app.config['UPLOAD'] = upload
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']



@app.route('/sensor_dth', methods=['POST'])
def add_dht():
    try:  
        data = request.get_json() 
        print(data)
        global temperature, humidity
        temperature = data['temperature']
        humidity = data['humidity']
        current_time = datetime.now()
        date_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print(date_time)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sensor_dht (temperature, humidity, date_time) VALUES (%s, %s, %s)", (temperature, humidity, date_time))
        mysql.connection.commit()
        cur.close()

        resp = jsonify(message="Data added successfully!")
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify(message="adding data error"), 500


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/')   
def main():   
    return render_template("render.html")   


@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        uploaded_file.save(os.path.join(app.config['UPLOAD'], filename))
    return '', 204

 
@app.route('/get_data')
def get_data():
    data = {'temperature': '10', 
            'humidity': '20'}
    return jsonify(data)


 
if __name__ == '__main__':
    #app.run(debug=True,host='0.0.0.0', port=4339, ssl_context='adhoc' )
    app.run(debug=True, port=4339)