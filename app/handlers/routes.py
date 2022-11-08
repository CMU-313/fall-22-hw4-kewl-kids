import this
from flask import Flask, abort, jsonify, request
import joblib
import pandas as pd
import numpy as np
import os

def configure_routes(app):

    this_dir = os.path.dirname(__file__)
    model_path = os.path.join(this_dir, "model.pkl")
    clf = joblib.load(model_path)

    @app.route('/')
    def hello():
        return "try the predict route it is great!"


    @app.route('/predict')
    def predict():
        #use entries from the query string here but could also use json
        studytime = request.args.get('studytime')
        failures = request.args.get('failures')
        absences = request.args.get('absences')
        activities = request.args.get('activities')
        internet = request.args.get('internet')
        medu = request.args.get('Medu')
        fedu = request.args.get('Fedu')
        g1 = request.args.get('G1')
        g2 = request.args.get('G2')
        if not (studytime and failures and absences and activities and internet and medu and fedu and g1 and g2):
            abort(400)
        if not (studytime.isnumeric() and failures.isnumeric() and absences.isnumeric() and activities.isnumeric() and internet.isnumeric() and medu.isnumeric() and fedu.isnumeric() and g1.isnumeric() and g2.isnumeric()):
            abort(400)
        query_df = pd.DataFrame({'Fedu': pd.Series(fedu), 'G1': pd.Series(g1), 'G2': pd.Series(g2), 'Medu': pd.Series(medu),
                                 'absences': pd.Series(absences), 'activities': pd.Series(activities), 'failures': pd.Series(failures), 
                                 'internet': pd.Series(internet), 'studytime': pd.Series(studytime)})
        prediction = clf.predict(query_df)
        return jsonify(np.ndarray.item(prediction))
