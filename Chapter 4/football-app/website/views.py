from flask import Blueprint, render_template, request, flash
from .models import Message, Note
from . import db
import pickle
import numpy as np
import pandas as pd

views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template("home.html")

@views.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@views.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        if len(message) < 2:
            flash('Your message is too short', category='error')
        else:
            new_message = Message(name=name, email=email, message=message)
            db.session.add(new_message)
            db.session.commit()
            flash('Message Sent!', category='success')
        
    return render_template("contact.html")

@views.route("/predict", methods=['GET', 'POST'])
def predict():

    home_array = list()
    away_array = list()
    STANDINGS_PATH = r'C:\Users\Igor\Documents\GitHub\football-app\website\data\eplstandings.csv'
    ENCODINGS_PATH = r'C:\Users\Igor\Documents\GitHub\football-app\website\data\encodings.csv'
    model = pickle.load(open('model.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))
    standings = pd.read_csv(STANDINGS_PATH).set_index('Team')
    encodings = pd.read_csv(ENCODINGS_PATH).set_index('Team').T.to_dict('list')
    
    if request.method == 'POST':
        home_team = request.form['home-team']
        away_team = request.form['away-team']
        home_array = home_array + encodings[home_team]
        away_array = away_array + encodings[away_team]

        hthg = int(request.form['hthg'])
        athg = int(request.form['athg'])
        htp = int(request.form['htp'])
        atp = int(request.form['atp'])
        
        ht_lp = standings.loc[home_team,'2021']
        at_lp = standings.loc[away_team,'2021']
        diff_lp = ht_lp - at_lp
        diff_pts = htp - atp

        scaled = scaler.transform(np.array([[hthg, athg, htp, atp, ht_lp, at_lp, diff_lp, diff_pts]]))
        data = np.concatenate((scaled.flatten(), np.array(home_array), np.array(away_array)))
        data = data.reshape(1, -1)
        prediction = pd.DataFrame(model.predict_proba(data))
        home = round((prediction.iloc[0,2]) * 100, 2)
        away = round((prediction.iloc[0,0]) * 100, 2)
        draw = round((prediction.iloc[0,1]) * 100, 2)

        return render_template('predict.html', home=home, away=away, draw=draw, home_team=home_team, away_team=away_team)
    else:
        return render_template('predict.html')

