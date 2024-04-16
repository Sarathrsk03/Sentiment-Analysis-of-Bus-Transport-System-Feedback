from flask import Flask, request, render_template,jsonify
import mysql.connector
from busSentiment import busSentimentModule

app = Flask(__name__)

# Create MySQL connection
conn = mysql.connector.connect(
    host="bhhpopoqjplvcksubdvw-mysql.services.clever-cloud.com",
    user="uiziojsebpp5sdnx",
    password="3uwSFhZEzqkZaqKVbO6e",
    database="bhhpopoqjplvcksubdvw"
)

@app.route("/", methods=['GET'])
def indexPage():
    return render_template('index.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    try:
        cursor = conn.cursor()

        name = request.form['name']
        email = request.form['email']
        bus_route = request.form['bus_route']
        driver_behaviour = request.form['driver_behaviour']
        bus_condition = request.form['bus_condition']
        general_behaviour = request.form['general_behaviour']

        # Calculate sentiments
        driver_sentiment = busSentimentModule(driver_behaviour)
        bus_sentiment = busSentimentModule(bus_condition)
        general_sentiment = busSentimentModule(general_behaviour)

        # Insert feedback data into the database
        sql = "INSERT INTO FeedBack (name, email, bus_route, driver_behaviour, driver_sentiment, bus_condition, bus_sentiment, general_behaviour, general_sentiment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, email, bus_route, driver_behaviour, driver_sentiment, bus_condition, bus_sentiment, general_behaviour, general_sentiment)
        cursor.execute(sql, val)

        conn.commit()
        cursor.close()

        return "Feedback submitted successfully!"
    except Exception as e:
        return str(e)
    
from flask import render_template

@app.route("/report-page", methods=['GET'])
def render_report_page():
    return render_template('report.html')

@app.route("/report", methods=['GET'])
def generateNegative():
    sql = "SELECT bus_route, driver_behaviour, bus_condition, general_behaviour FROM FeedBack WHERE driver_sentiment = 'Negative' OR bus_sentiment = 'Negative' OR general_sentiment = 'Negative';"
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        # Fetch all rows
        rows = cursor.fetchall()
        # Convert rows to list of dictionaries
        feedback_list = []
        for row in rows:
            feedback = {
                'bus_route': row[0],
                'driver_behaviour': row[1],
                'bus_condition': row[2],
                'general_behaviour': row[3]
            }
            feedback_list.append(feedback)
        return jsonify(feedback_list)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
