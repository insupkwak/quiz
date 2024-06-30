from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import mysql.connector
import random
from mysql.connector import errorcode

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    connection = mysql.connector.connect(
        host="svc.sel5.cloudtype.app",
        port=31200,
        user="mariadb",
        password="1234",
        database="mariadb"
    )
    return connection



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    session['score'] = 0
    session['asked_questions'] = []
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    if session['asked_questions']:
        placeholders = ','.join(['%s'] * len(session['asked_questions']))
        query = f"SELECT * FROM countries WHERE id NOT IN ({placeholders}) ORDER BY RAND() LIMIT 1"
        cursor.execute(query, tuple(session['asked_questions']))
    else:
        query = "SELECT * FROM countries ORDER BY RAND() LIMIT 1"
        cursor.execute(query)

    country = cursor.fetchone()
    if not country:
        return redirect(url_for('result', all_correct='true'))

    session['asked_questions'].append(country['id'])

    query = "SELECT capital_name FROM countries WHERE id != %s ORDER BY RAND() LIMIT 3"
    cursor.execute(query, (country['id'],))
    wrong_capitals = cursor.fetchall()
    cursor.close()
    connection.close()

    options = [country['capital_name']] + [wrong['capital_name'] for wrong in wrong_capitals]
    random.shuffle(options)

    return render_template('quiz.html', country=country, options=options)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    selected_option = request.form['capital']
    correct_answer = request.form['correct_answer']
    if selected_option == correct_answer:
        session['score'] += 1
        flash("정답입니다!", "success")
    else:
        return redirect(url_for('result', all_correct='false'))
    
    return redirect(url_for('quiz'))

@app.route('/result')
def result():
    all_correct = request.args.get('all_correct') == 'true'
    score = session.get('score', 0)
    return render_template('result.html', score=score, all_correct=all_correct)



@app.route('/save_score', methods=['POST'])
def save_score():
    data = request.get_json()
    player_name = data['player_name']
    score = session.get('score', 0)
    
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO scores (player_name, score) VALUES (%s, %s)", (player_name, score))
        connection.commit()
        return jsonify(success=True)
    except mysql.connector.Error as err:
        print(err.msg)
        return jsonify(success=False)
    finally:
        cursor.close()
        connection.close()


@app.route('/get_scores')
def get_scores():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT player_name, score FROM scores ORDER BY score DESC, id ASC LIMIT 10")
    scores = cursor.fetchall()
    cursor.close()
    connection.close()

    ranked_scores = []
    last_score = None
    rank = 0
    skip = 1

    for i, row in enumerate(scores):
        if last_score is None or row['score'] != last_score:
            rank += skip
            skip = 1
        else:
            skip += 1
        row['rank'] = rank
        last_score = row['score']
        ranked_scores.append(row)

    return jsonify(ranked_scores)
    

if __name__ == '__main__':

 
    app.run(debug=True)

