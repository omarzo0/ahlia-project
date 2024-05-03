import os
import base64
from flask import Flask, render_template
import pypyodbc as odbc

app = Flask(__name__, static_url_path='/static')

# Configure the template folder to be the current directory
app.template_folder = os.path.abspath(os.path.dirname(__file__))

# Database connection parameters
DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'Mohamed\\MSSQLSERVER01'
DATABASE_NAME = 'project'

def get_universities():
    # Establish a connection
    connection_string = f""" 
        DRIVER={{{DRIVER_NAME}}};
        SERVER={SERVER_NAME};
        DATABASE={DATABASE_NAME};
        Trust_Connection=yes;
    """
    conn = odbc.connect(connection_string)

    # Define the SQL query to select universities with rank and img_path
    sql_query = "SELECT name, description, ranking, img_data FROM universities WHERE ORDER BY ranking"

    # Execute the query and fetch all results
    cursor = conn.cursor()
    cursor.execute(sql_query)
    rows = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return rows

@app.route('/')
def fetch_universities():
    universities = get_universities()
    if universities:
        images = []
        for row in universities:
            encoded_image = base64.b64encode(row[3]).decode('utf-8')  # Encode bytes to base64 string
            images.append(encoded_image)

        return render_template('universities.html', universities=universities, images=images)
    else:
        return 'No universities found'

# Define route for the universities page
@app.route('/index')
def universities():
    return render_template('index.html')

# Define route for the colleges page
@app.route('/colleges')
def colleges():
    return render_template('colleges.html')

# Define route for the choose major page
@app.route('/choose_major')
def choose_major():
    return render_template('reqsystem.html')

if __name__ == '__main__':
    app.run(debug=True)
