
from fileinput import filename
import re
from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

model= pickle.load(open('model.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    temp_array = list()

    if request.method == 'POST':
        Batting_Team = request.form['BattingTeam']
        if Batting_Team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0,0,0]
        elif Batting_Team == 'Delhi Capitals':
            temp_array = temp_array + [0,1,0,0,0,0,0,0,0,0]
        elif Batting_Team == 'Gujarat Titans':
            temp_array = temp_array + [0,0,1,0,0,0,0,0,0,0]
        elif Batting_Team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,0,1,0,0,0,0,0,0]
        elif Batting_Team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,0,1,0,0,0,0,0]
        elif Batting_Team == 'Lucknow Super Giants':
            temp_array = temp_array + [0,0,0,0,0,1,0,0,0,0]
        elif Batting_Team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,0,0,1,0,0,0]
        elif Batting_Team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,0,0,1,0,0]
        elif Batting_Team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,1,0]
        elif Batting_Team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,1]
            
            
        Bowling_Team = request.form['BowlingTeam']
        if Bowling_Team == 'Chennai Super Kings':
            temp_array = temp_array + [1,0,0,0,0,0,0,0,0,0]
        elif Bowling_Team == 'Delhi Capitals':
            temp_array = temp_array + [0,1,0,0,0,0,0,0,0,0]
        elif Bowling_Team == 'Gujarat Titans':
            temp_array = temp_array + [0,0,1,0,0,0,0,0,0,0]
        elif Bowling_Team == 'Kings XI Punjab':
            temp_array = temp_array + [0,0,0,1,0,0,0,0,0,0]
        elif Bowling_Team == 'Kolkata Knight Riders':
            temp_array = temp_array + [0,0,0,0,1,0,0,0,0,0]
        elif Bowling_Team == 'Lucknow Super Giants':
            temp_array = temp_array + [0,0,0,0,0,1,0,0,0,0]
        elif Bowling_Team == 'Mumbai Indians':
            temp_array = temp_array + [0,0,0,0,0,0,1,0,0,0]
        elif Bowling_Team == 'Rajasthan Royals':
            temp_array = temp_array + [0,0,0,0,0,0,0,1,0,0]
        elif Bowling_Team == 'Royal Challengers Bangalore':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,1,0]
        elif Bowling_Team == 'Sunrisers Hyderabad':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,1]
            
        
        venue_selection = request.form['Venue']
        if venue_selection == 'Arun Jaitley Stadium':
            temp_array = temp_array + [1,0,0,0,0,0,0,0,0,0]
        elif venue_selection == 'Dr DY Patil Sports Academy, Mumbai':
            temp_array = temp_array + [0,1,0,0,0,0,0,0,0,0]
        elif venue_selection == 'Eden Gardens, Kolkata':
            temp_array = temp_array + [0,0,1,0,0,0,0,0,0,0]
        elif venue_selection == 'MA Chidambaram Stadium, Chepauk':
            temp_array = temp_array + [0,0,0,1,0,0,0,0,0,0]
        elif venue_selection == 'M Chinnaswamy Stadium':
            temp_array = temp_array + [0,0,0,0,1,0,0,0,0,0]
        elif venue_selection == 'Narendra Modi Stadium, Ahmedabad':
            temp_array = temp_array + [0,0,0,0,0,1,0,0,0,0]
        elif venue_selection == 'Punjab Cricket Association IS Bindra Stadium':
            temp_array = temp_array + [0,0,0,0,0,0,1,0,0,0]
        elif venue_selection == 'Rajiv Gandhi International Stadium, Uppal':
            temp_array = temp_array + [0,0,0,0,0,0,0,1,0,0]
        elif venue_selection == 'Sawai Mansingh Stadium':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,1,0]
        elif venue_selection == 'Wankhede Stadium':
            temp_array = temp_array + [0,0,0,0,0,0,0,0,0,1]

        Current_Score = int(request.form['current_score'])
        Wickets_Left = int(request.form['wickets_left'])
        Overs = float(request.form['Overs'])
        Current_Run_Rate = float(request.form['current_run_rate'])
        Required_Run_Rate = float(request.form['required_run_rate'])

        temp_array = temp_array + [Current_Score,Wickets_Left,Overs,Current_Run_Rate,Required_Run_Rate]

        data = np.array([temp_array])
        my_prediction = int(model.predict(data)[[0]])

        return render_template('result.html',Final_Score = my_prediction)

if __name__ == '__main__':
	app.run(debug=True)