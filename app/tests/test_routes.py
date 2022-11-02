from flask import Flask

from app.handlers.routes import configure_routes

app = Flask(__name__)
configure_routes(app)

def test_base_route():
    with app.test_client() as client:

        url = '/'

        response = client.get(url)

        assert response.status_code == 200
        assert response.get_data() == b'try the predict route it is great!'

def test_predict_route():
    with app.test_client() as client:

        url = '/predict'

        # testing valid args

        response = client.get(url, query_string={
            "studytime": 1,
            "failures": 1,
            "absences": 20,
            "activities": True,
            "internet": True,
            "medu": 3,
            "fedu": 3,
        })

        assert response.status_code == 200

        # Testing missing args
        
        response = client.get(url, query_string={
            "studytime": 1,
            "failures": 1,
            "absences": 20,
            "activities": True,
            "internet": True,
        })

        assert response.status_code == 400

        # Testing additional args
        response = client.get(url, query_string={
            "studytime": 1,
            "failures": 1,
            "absences": 20,
            "activities": True,
            "internet": True,
            "medu": 3,
            "fedu": 3,
            "grade": 17,
        })

        assert response.status_code == 200

        # Testing invalid arg type
        response = client.get(url, query_string={
            "studytime": "NaN",
            "failures": 1,
            "absences": 20,
            "activities": True,
            "internet": True,
            "medu": 3,
            "fedu": 3,
        })

        assert response.status_code == 400

        # Testing special characters
        response = client.get(url, query_string={
            "studytime": '1&failures=1',
            "failures": 1,
            "absences": 20,
            "activities": True,
            "internet": True,
            "medu": 3,
            "fedu": 3,
        })

        assert response.status_code == 400

        # Testing malformed request body
        response = client.get(url, query_string=[1, 1, 20, True, True, 3, 3])

        assert response.status_code == 400

def test_invalid_address():
    with app.test_client() as client:
        # Testing invalid address
        response = client.get('/change')

        assert response.status_code == 404
