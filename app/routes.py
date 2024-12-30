import os
import random

import psycopg2
from flask import Flask, render_template, request, redirect, session, jsonify

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

# Database Configuration
DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')
DATABASE_PORT = os.environ.get('DATABASE_PORT', '5432')
DATABASE_NAME = os.environ.get('DATABASE_NAME', 'book_recommendation')
DATABASE_USER = os.environ.get('DATABASE_USER', 'postgres')
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', '123456')

# Function to connect to SQLite database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            database=DATABASE_NAME,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
        return None


# Route for login page
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         userid = request.form['userid']
#         password = request.form['password']
#         if userid and password:
#
#             conn = get_db_connection()
#             cursor = conn.cursor()
#             cursor.execute("SELECT * FROM users WHERE u_name = %s AND u_password = %s", (userid, password))
#             user = cursor.fetchone()
#             cursor.close()
#             conn.close()
#
#             if user:
#                 session['userid'] = user[0]
#                 return redirect('/home')
#         else:
#             return render_template('login_new.html', error='Invalid userid or password.')
#     else:
#         return render_template('login_new.html', error=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        if userid and password:
            conn = get_db_connection()
            if conn is not None:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM users WHERE u_name = %s AND u_password = %s", (userid, password))
                    user = cursor.fetchone()
                finally:
                    cursor.close()
                    conn.close()

                if user:
                    session['userid'] = user[0]
                    return redirect('/home')
        return render_template('login_new.html', error='Invalid userid or password.')
    return render_template('login_new.html', error=None)



# Route for home page
@app.route('/home')
def home():
    if 'userid' in session:
        quiz_list = []
        # get all results from database
        user_id = session["userid"]
        conn = get_db_connection()
        cursor_new = conn.cursor()
        cursor_new.execute(f"SELECT res_time, personality FROM quiz_results WHERE user_id = %s", (user_id, ))
        all_results = cursor_new.fetchall()

        for num, (date, personality) in enumerate(all_results):
            cursor_new.execute(f"SELECT b_name FROM books WHERE personality = %s", (personality,))
            all_books = cursor_new.fetchall()
            all_books = [i[0] for i in all_books]
            all_books = random.sample(all_books, 5)
            quiz_list.append({"id": num+1, "timeTaken": date, "books": all_books, "result": personality})

        cursor_new.close()
        conn.close()

        return render_template('home_new.html', quiz_list=quiz_list)
    else:
        return render_template('login_new.html', error='Invalid userid or password.')


# Route for logout
@app.route('/logout')
def logout():
    session.pop('userid', None)
    return redirect('/login')


# Route for recommendation page
@app.route('/recommend-books', methods=['GET', 'POST'])
def recommend_books():
    books = []
    if 'userid' in session:
        if request.method == 'POST':
            personality = request.json.get('personality')
            conn = get_db_connection()
            cursor_books = conn.cursor()
            cursor_books.execute(f"insert into quiz_results(user_id, personality) values({session['userid']}, '{personality}')")
            cursor_books.execute(f"SELECT b_name FROM books WHERE personality = %s", (personality,))
            # Commit the changes
            conn.commit()
            all_books = cursor_books.fetchall()
            all_books = [i[0] for i in all_books]
            all_books = random.sample(all_books, 5)
            for book in all_books:
                books.append({"title": book, "image": f"/static/images/{book}.jpg"})
            cursor_books.close()
            conn.close()
            return jsonify(books)
        else:
            return render_template('recommend_books_new.html')
    else:
        return render_template('login_new.html', error='Invalid userid or password.')

# Route for About Us page
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

if __name__ == '__main__':
    app.run(debug=True)