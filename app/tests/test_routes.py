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
            "Fedu": 3,
            "G1": 16, 
            "G2": 16,
            "Medu": 3,
            "absences": 20,
            "studytime": 1,
            "activities": 1,
            "failures": 1,
            "internet": 1,
        })

        assert response.status_code == 200
        assert int(response.data.strip()) == 0 or int(
            response.data.strip()) == 1
        
        # Testing missing args
        
        response = client.get(url, query_string={
            "Fedu": 3,
            "G1": 16,
            "G2": 16,
            "Medu": 3,
            "absences": 20,
            "studytime": 1,
            "activities": 1,
            "failures": 1,
        })

        assert response.status_code == 400

        # Testing additional args
        response = client.get(url, query_string={
            "Fedu": 3,
            "G1": 16,
            "G2": 16,
            "Medu": 3,
            "absences": 20,
            "studytime": 1,
            "activities": 1,
            "failures": 1,
            "internet": 1,
            "G3": 17,
        })

        assert response.status_code == 200

        # Testing invalid arg type
        response = client.get(url, query_string={
            "Fedu": "NaN",
            "G1": 16,
            "G2": 16,
            "Medu": 3,
            "absences": 20,
            "studytime": 1,
            "activities": 1,
            "failures": 1,
            "internet": 1,
        })

        assert response.status_code == 400

        # Testing special characters
        response = client.get(url, query_string={
            "Fedu": '1&',
            "G1": 16,
            "G2": 16,
            "Medu": 3,
            "absences": 20,
            "studytime": 1,
            "activities": 1,
            "failures": 1,
            "internet": 1,
        })
        assert response.status_code == 400

def test_invalid_address():
    with app.test_client() as client:
        # Testing invalid address
        response = client.get('/destory')
        assert response.status_code == 404

        # Testing invalid address
        response = client.get('/predict/studytime/1/failures/1')
        assert response.status_code == 404
