from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', selected_date='', no_data=False)

@app.route('/attendance', methods=['POST'])
def attendance():
    selected_date = request.form.get('selected_date')
    selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
    formatted_date = selected_date_obj.strftime('%Y-%m-%d')

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()

    cursor.execute("SELECT name, time FROM attendance WHERE date = ?", (formatted_date,))
    attendance_data = cursor.fetchall()

    conn.close()

    if not attendance_data:
        return render_template('index.html', selected_date=selected_date, no_data=True)
    
    return render_template('index.html', selected_date=selected_date, attendance_data=attendance_data)

if __name__ == '__main__':
    app.run(debug=True)























# from flask import Flask, render_template, request
# import logging
# import cv2
# import numpy as np
# import dlib
# import os
# import shutil
# import time

# app = Flask(__name__)

# # Use frontal face detector of Dlib
# detector = dlib.get_frontal_face_detector()

# # Global variables
# current_frame_faces_cnt = 0
# existing_faces_cnt = 0
# ss_cnt = 0
# path_photos_from_camera = "data/data_faces_from_camera/"
# current_face_dir = ""

# # Create folders to save face images and csv
# if not os.path.isdir(path_photos_from_camera):
#     os.mkdir(path_photos_from_camera)


# # Delete old face folders
# def clear_data():
#     folders_rd = os.listdir(path_photos_from_camera)
#     for folder in folders_rd:
#         shutil.rmtree(path_photos_from_camera + folder)
#     if os.path.isfile("data/features_all.csv"):
#         os.remove("data/features_all.csv")
#     return "Face images and 'features_all.csv' removed!"


# # Start from person_x+1
# def check_existing_faces_cnt():
#     if os.listdir(path_photos_from_camera):
#         # Get the order of latest person
#         person_list = os.listdir(path_photos_from_camera)
#         person_num_list = []
#         for person in person_list:
#             person_order = person.split('_')[1].split('_')[0]
#             person_num_list.append(int(person_order))
#         return max(person_num_list)
#     # Start from person_1
#     else:
#         return 0


# @app.route('/')
# def index():
#     return render_template('index.html')


# @app.route('/register', methods=['POST'])
# def register_face():
#     global existing_faces_cnt, current_face_dir
#     input_name = request.form['name']
#     existing_faces_cnt = check_existing_faces_cnt()
#     existing_faces_cnt += 1
#     if input_name:
#         current_face_dir = path_photos_from_camera + \
#                            "person_" + str(existing_faces_cnt) + "_" + input_name
#     else:
#         current_face_dir = path_photos_from_camera + \
#                            "person_" + str(existing_faces_cnt)
#     os.makedirs(current_face_dir)
#     return render_template('index.html', message='Face folder created!')


# @app.route('/clear', methods=['POST'])
# def clear_faces():
#     global existing_faces_cnt
#     existing_faces_cnt = 0
#     msg = clear_data()
#     return render_template('index.html', message=msg)


# @app.route('/save', methods=['POST'])
# def save_face():
#     global current_frame_faces_cnt, ss_cnt, current_face_dir
#     if current_frame_faces_cnt == 1:
#         frame = request.form['frame']
#         img_bytes = frame.split(',')[1]
#         img = np.frombuffer(img_bytes, np.uint8)
#         img = cv2.imdecode(img, cv2.IMREAD_COLOR)
#         cv2.imwrite(current_face_dir + "/img_face_" + str(ss_cnt) + ".jpg", img)
#         ss_cnt += 1
#         return render_template('index.html', message='Face image saved!')
#     else:
#         return render_template('index.html', message='No face in current frame!')


# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     app.run(debug=True)
