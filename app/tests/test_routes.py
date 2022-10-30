from flask import Flask

from app.handlers.routes import configure_routes

# import logging



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
            "age": 19,
            "health": 1,
            "absences": 17,
        })

        assert response.status_code == 200

        # Testing missing args
        
        response = client.get(url, query_string={
            "age": 19,
            "health": 1,
        })

        assert response.status_code == 400

        # Testing additional args
        response = client.get(url, query_string={
            "age": 19,
            "health": 1,
            "absences": 17,
            "grade": 17,
        })

        assert response.status_code == 200

        # Testing invalid arg type
        response = client.get(url, query_string={
            "age": 'NaN',
            "health": 1,
            "absences": 17,
        })

        assert response.status_code == 400

        # Testing special characters
        response = client.get(url, query_string={
            "age": '1&health=2',
            "absences": 17,
        })

        assert response.status_code == 400

        # Testing malformed request body
        response = client.get(url, query_string=[19, 1, 17])

        assert response.status_code == 400

def test_invalid_address():
    with app.test_client() as client:
        # Testing invalid address
        response = client.get('/change')

        assert response.status_code == 404


