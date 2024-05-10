import os
import base64
from flask import Flask, render_template, request
import pypyodbc as odbc

app = Flask(__name__, static_url_path='/static')

# Configure the template folder to be the current directory
app.template_folder = os.path.abspath(os.path.dirname(__file__))

# Database connection parameters
DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'Mohamed\\MSSQLSERVER01'
DATABASE_NAME = 'project'

def get_universities(limit=None):
    try:
        # Establish a connection
        connection_string = f""" 
            DRIVER={{{DRIVER_NAME}}};
            SERVER={SERVER_NAME};
            DATABASE={DATABASE_NAME};
            Trust_Connection=yes;
        """
        conn = odbc.connect(connection_string)

        # Define the SQL query to select universities with rank, img_data, and location
        sql_query = f"SELECT TOP {limit} name, description, ranking, img_data, location, website FROM universities ORDER BY ranking"

        # Execute the query and fetch all results
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return rows
    except Exception as e:
        print(f"Error fetching universities: {e}")
        return None

@app.route('/')
def fetch_universities():
    universities = get_universities(limit=3)  # Limit to the first 3 universities
    if universities:
        images = []
        for row in universities:
            encoded_image = base64.b64encode(row[3]).decode('utf-8')  # Encode bytes to base64 string
            images.append(encoded_image)

        return render_template('index.html', universities=universities, images=images)
    else:
        return 'No universities found'

# Define route for the universities page
@app.route('/universities')
def display_universities():
    universities = get_universities(limit=20)
    if universities:
        images = []
        for row in universities:
            encoded_image = base64.b64encode(row[3]).decode('utf-8')  # Encode bytes to base64 string
            images.append(encoded_image)

        return render_template('universities.html', universities=universities, images=images)
    else:
        return 'No universities found'

@app.route('/compare', methods=['POST'])
def compare_universities():
    selected_universities = request.form.getlist('selected_universities')
    # Perform database query to get data for selected universities
    # Replace the placeholders with actual database query and processing logic
    university_data = []
    for university_name in selected_universities:
        # Example query
        university_data.append(get_university_data(university_name))  # Implement get_university_data function
    return render_template('compare.html', university_data=university_data)

# Dummy function to simulate fetching university data from the database
# Dummy function to simulate fetching university data from the database
def get_university_data(university_name):
    try:
        # Establish a connection
        connection_string = f""" 
            DRIVER={{{DRIVER_NAME}}};
            SERVER={SERVER_NAME};
            DATABASE={DATABASE_NAME};
            Trust_Connection=yes;
        """
        conn = odbc.connect(connection_string)

        # Define the SQL query to fetch university data
        sql_query = f"SELECT * FROM universities WHERE name = ?"

        # Execute the query with the university_name parameter
        cursor = conn.cursor()
        cursor.execute(sql_query, (university_name,))
        row = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        if row:
            images = []
            encoded_image = base64.b64encode(row[6]).decode('utf-8')  # Encode bytes to base64 string
            images.append(encoded_image)
            
            # Construct a dictionary containing university data
            university_data = {
                'name': row[1],  # Assuming name is the first column in your database table
                'image': row[6],  # Assuming image path or URL is the second column
                'description': row[4],  # Assuming description is the third column
                'location': row[2],  # Assuming location is the fourth column
                'website': row[3],  # Assuming website URL is the fifth column
                'rank': row[5]  # Assuming rank is the sixth column
            }
            return university_data
        else:
            return None  # University not found
    except Exception as e:
        print(f"Error fetching university data: {e}")
        return None

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
