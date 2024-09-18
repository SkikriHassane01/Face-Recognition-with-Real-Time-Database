import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": "https://faceattendancewithrealtimedb-default-rtdb.firebaseio.com/"
    },
)

ref = db.reference("Students")
data = {
    "1234": {
        "name": "Elon Mask",
        "major": "Economic",
        "starting_year": 2019,
        "total_attendance": 2,
        "standing": "G",
        "year": 1,
        "last_attendance_time": "2024-08-00:43:32",
    },
        "2673": {
        "name": "Mark Zeugerberg",
        "major": "Robotics",
        "starting_year": 2020,
        "total_attendance": 3,
        "standing": "B",
        "year": 2,
        "last_attendance_time": "2024-08-00:43:32",
    },
        "4673": {
        "name": "Hassane Skikri",
        "major": "data science",
        "starting_year": 2021,
        "total_attendance": 9,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2024-08-00:43:32",
    },
        "5578": {
        "name": "Jeff Bezos",
        "major": "physics",
        "starting_year": 2022,
        "total_attendance": 10,
        "standing": "B",
        "year": 5,
        "last_attendance_time": "2024-08-00:43:32",
    },
        "7653": {
        "name": "larry Ellison",
        "major": "Math",
        "starting_year": 2023,
        "total_attendance": 20,
        "standing": "G",
        "year": 2,
        "last_attendance_time": "2024-08-00:43:32",
    },
}

for key, value in data.items():
    ref.child(key).set(value)