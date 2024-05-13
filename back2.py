from flask import Flask, request, render_template
import pyodbc
import os

app = Flask(__name__, static_url_path='/static')
app.template_folder = os.path.abspath(os.path.dirname(__file__))

def connect():
    try:
        DRIVER_NAME = 'SQL Server'
        SERVER_NAME = 'Mohamed\\MSSQLSERVER01'
        DATABASE_NAME = 'project'
        connection_string = f"DRIVER={DRIVER_NAME};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trust_Connection=yes;"
        return pyodbc.connect(connection_string)
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    try:
        conn = connect()
        if conn:
            cursor = conn.cursor()
            # Prepare to call the stored procedure with output parameter for login result
            cursor.execute("EXECUTE LoginUser @Username=?, @Password=?", username, password)
            
            # Fetch the result set after executing the stored procedure
            row = cursor.fetchone()
            print (row)
            if row and row[0] == '1':
                cursor.close()
                conn.close()
                return "Login successful"
            else:
                return "Invalid credentials or user not found"

    except pyodbc.Error as e:
        return f"Database error: {e}"

    

if __name__ == '__main__':
    app.run(debug=True)
