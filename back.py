import os
import base64
from flask import Flask, render_template, request, jsonify
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

from flask import render_template
import base64

@app.route('/')
def fetch_universities():
    universities = get_universities(limit=3)  # Limit to the first 3 universities
    if universities:
        # Count the total number of universities
        total_universities = count_total_universities()

        images = []
        for row in universities:
            encoded_image = base64.b64encode(row[3]).decode('utf-8')  # Encode bytes to base64 string
            images.append(encoded_image)

        return render_template('index.html', universities=universities, images=images, total_universities=total_universities)
    else:
        return 'No universities found'
def count_total_universities():
    try:
        # Establish a connection
        connection_string = f""" 
            DRIVER={{{DRIVER_NAME}}};
            SERVER={SERVER_NAME};
            DATABASE={DATABASE_NAME};
            Trust_Connection=yes;
        """
        conn = odbc.connect(connection_string)

        # Define the SQL query to count universities
        sql_query = "SELECT COUNT(*) FROM universities"

        # Execute the query
        cursor = conn.cursor()
        cursor.execute(sql_query)
        total_count = cursor.fetchone()[0]

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return total_count
    except Exception as e:
        print(f"Error counting universities: {e}")
        return 0  # Return 0 if an error occurs


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
    selected_universities = get_university_data()
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

        university_data_list = []
        for university_name in selected_universities:
            # Execute the query with the university_name parameter
            cursor = conn.cursor()
            cursor.execute(sql_query, (university_name,))
            row = cursor.fetchone()

            if row:
                # Encode the image data to base64
                encoded_image = base64.b64encode(row[6]).decode('utf-8')  # Assuming image data is in the 7th column

                # Construct a dictionary containing university data
                university_data = {
                    'name': row[1],  # Assuming name is the first column
                    'image': f"data:image/jpeg;base64,{encoded_image}",  # Include base64 encoded image data
                    'description': row[4],  # Assuming description is the fifth column
                    'location': row[2],  # Assuming location is the third column
                    'website': row[3],  # Assuming website URL is the fourth column
                    'rank': row[5]  # Assuming rank is the sixth column
                }
                university_data_list.append(university_data)
            else:
                # University not found, handle this case as needed
                pass

            # Close the cursor for this iteration
            cursor.close()

        # Close the connection after all iterations
        conn.close()

        return render_template('compare.html', universities=university_data_list)
    except Exception as e:
        print(f"Error fetching university data: {e}")
        # Return an error response or redirect to an error page
        return render_template('error.html', message="Error fetching data")
def get_university_data():
    selected_universities = request.form.getlist('selected_universities')
    return selected_universities


# Define route for the colleges page
@app.route('/colleges')
def colleges():
    return render_template('colleges.html')

# Define route for the choose major page
@app.route('/choose_major')
def choose_major():
    return render_template('choose_major.html')

@app.route('/home')
def home():
    return render_template('./admin/adminpanel.html')

if __name__ == '__main__':
    app.run(debug=True)
