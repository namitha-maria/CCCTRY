from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Secret key for session management
app.secret_key = 'your_secret_key'  # Change this to a secure key

# Function to get a database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Chinnu1811",
        database="CampusCareerConnect"
    )

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/studenthome')
def home2():
    return render_template('home2.html')
@app.route('/home')
def home():
    if 'loggedin' in session:  # Ensure the user is logged in before accessing home
        return render_template('home.html')
    return redirect(url_for('student_login'))  # Redirect to login if not logged in

@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['studentEmail']
        password = request.form['studentPassword']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for better readability

        cursor.execute("SELECT * FROM Users WHERE Email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user['Password'], password):  # Assuming 'Password' is the correct column name
            if user['Role'] == 'Student':  # Ensure role is 'Student'
                session['loggedin'] = True
                session['id'] = user['UserID']
                session['email'] = user['Email']
                session['role'] = user['Role']

                flash("Login successful!", "success")
                return redirect(url_for('home2'))  # Redirect to home after login
            else:
                flash("You are not registered as a student.", "danger")

        else:
            flash("Invalid email or password", "danger")

    return render_template('SL.html')  # Return login page on GET request or failed login

@app.route('/student-MI')
def student_MI():
    return render_template('MI.html')

@app.route('/student-at')
def student_at():
    return render_template('AT.html')

@app.route('/student-cc')
def student_cc():
    return render_template('CC.html')

@app.route('/student-pd')
def student_pd():
    return render_template('PD.html')

@app.route('/student-ai')
def student_ai():
    return render_template('AI.html')

@app.route('/student-qna')
def student_qna():
    return render_template('Q&A.html')
@app.route('/student-ad')
def student_ad():
    return render_template('AD.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/alumni-login')
def alumni_login():
    return render_template('AL.html')

@app.route('/admin-login')
def admin_login():
    return render_template('ADL.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Insert into Users table
            cursor.execute("INSERT INTO Users (Name, Email, Password, Role) VALUES (%s, %s, %s, %s)", 
                           (name, email, password, role))
            conn.commit()
            user_id = cursor.lastrowid  # Get new UserID

            # Insert into respective role-specific table
            if role == "Student":
                batch_year = request.form['batch_year']
                cursor.execute("INSERT INTO Student (UserID, student_id, batch_year) VALUES (%s, %s, %s)", 
                               (user_id, user_id, batch_year))
            elif role == "Alumni":
                grad_year = request.form['grad_year']
                company = request.form.get('company', '')
                designation = request.form.get('designation', '')
                bio = request.form.get('bio', '')
                cursor.execute("INSERT INTO Alumni (UserID, alumni_id, grad_year, company, designation, bio) VALUES (%s, %s, %s, %s, %s, %s)", 
                               (user_id, user_id, grad_year, company, designation, bio))
            elif role == "Admin":
                position = request.form['position']
                cursor.execute("INSERT INTO Admin (UserID, admin_id, position) VALUES (%s, %s, %s)", 
                               (user_id, user_id, position))

            conn.commit()
            flash("Registration successful!", "success")
            return redirect(url_for('student_login'))

        except mysql.connector.Error as e:
            flash(f"Error: {str(e)}", "danger")
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
