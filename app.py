import numpy as np
import pickle
from flask import Flask, request, render_template
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

lc= LabelEncoder()

# Load the machine learning model
loaded_model = pickle.load(open("model.pkl", "rb"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Convert categorical form data to numeric labels
        TossWinner = float(lc.fit_transform([request.form['TossWinner']])[0])
        BattingTeam = float(lc.fit_transform([request.form['BattingTeam']])[0])
        BowlingTeam = float(lc.fit_transform([request.form['BowlingTeam']])[0])
        TossDecision = float(lc.fit_transform([request.form['TossDecision']])[0])
        batter = float(lc.fit_transform([request.form['batter']])[0])
        non_striker = float(lc.fit_transform([request.form['non_striker']])[0])
        bowler = float(lc.fit_transform([request.form['bowler']])[0])
        Venue = float(lc.fit_transform([request.form['Venue']])[0])
        First_Innings_total_score = float(request.form['First_Innings_total_score'])
        current_score = float(request.form['current_score'])
        wickets_left = float(request.form['wickets_left'])
        Overs = float(request.form['Overs'])
        current_run_rate = float(request.form['current_run_rate'])
        required_run_rate = float(request.form['required_run_rate'])
        # Convert form data into input features
        input_features = np.array([TossWinner,  BattingTeam, BowlingTeam,TossDecision, batter,non_striker,bowler,Venue,First_Innings_total_score,current_score,wickets_left,Overs,current_run_rate,required_run_rate])
        
        # Perform prediction
        result = loaded_model.predict(input_features)
        
        # Render the prediction result in a template
        return render_template("result.html", Final_Score=int(result),openet=First_Innings_total_score)

if __name__ == '__main__':
    app.run(debug=True)
