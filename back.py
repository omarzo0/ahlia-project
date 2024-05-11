import os
import base64
from flask import Flask, render_template, request, jsonify
import pypyodbc as odbc

app = Flask(__name__, static_url_path='/static')

# Configure the template folder to be the current directory
app.template_folder = os.path.abspath(os.path.dirname(__file__))

def connect():
    try:
        import pyodbc
        # Database connection parameters
        DRIVER_NAME = 'SQL Server'
        SERVER_NAME = 'Mohamed\\MSSQLSERVER01'
        DATABASE_NAME = 'project'

        # Establish a connection
        connection_string = f"DRIVER={DRIVER_NAME};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trust_Connection=yes;"
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_universities(limit=None):
    try:
        conn = connect()  # Connect to the database
        if conn:
            cursor = conn.cursor()
            # Define the SQL query to select universities with rank, img_data, and location
            sql_query = f"SELECT TOP {limit} name, description, ranking, img_data, location, website FROM universities ORDER BY ranking"
            # Execute the query and fetch all results
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return rows
        else:
            return None
    except Exception as e:
        print(f"Error fetching universities: {e}")
        return None
    
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
        conn = connect()
        if conn:
            cursor = conn.cursor()
            sql_query = "SELECT COUNT(*) FROM universities"
            cursor.execute(sql_query)
            total_count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
            return total_count
        else:
            return 0
    except Exception as e:
        print(f"Error counting universities: {e}")
        return 0


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
        conn = connect()
        if conn:
            cursor = conn.cursor()
            university_data_list = []

            # Define the SQL query to fetch university data
            sql_query = "SELECT * FROM universities WHERE name = ?"

            for university_name in selected_universities:
                cursor.execute(sql_query, (university_name,))
                rows = cursor.fetchall()  # Use fetchall if expecting multiple rows

                for row in rows:
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

            # Close the cursor and connection
            cursor.close()
            conn.close()

            return render_template('compare.html', universities=university_data_list)
    except Exception as e:
        print(f"Error fetching university data: {e}")
        # Close the cursor and connection in case of exception
        cursor.close()
        conn.close()
        # Return an error response or redirect to an error page
        return render_template('error.html', message="Error fetching data")

def get_university_data():
    selected_universities = request.form.getlist('selected_universities')
    return selected_universities


# Define route for the colleges page
@app.route('/colleges')
def colleges():
  universities = get_universities(limit=20)  # Limit to the first 3 universities
  if universities:
        return render_template('colleges.html', universities=universities)
  else:
     return 'No universities found'
  
@app.route('/programs', methods=['POST'])
def programs():
    uni_name = request.form.get('uni_name')  # Use get instead of getlist for single value
    try:
        conn = connect()
        if conn:
            cursor = conn.cursor()
            university_data_list = []

            # Define the SQL query to fetch university ID based on name
            sql_query_uni_id = "SELECT university_id FROM universities WHERE name = ?"
            cursor.execute(sql_query_uni_id, (uni_name,))
            uni_row = cursor.fetchone()

            if uni_row:
                uni_id = uni_row[0]
                # Define the SQL query to fetch programs based on university ID
                sql_query_programs = "SELECT name FROM programs WHERE university_id = ?"
                cursor.execute(sql_query_programs, (uni_id,))
                program_rows = cursor.fetchall()

                for program_row in program_rows:
                    program_name = program_row[0]
                    # Check if the program's image exists in the images table
                    sql_query_image = "SELECT img FROM images WHERE name LIKE ?"
                    cursor.execute(sql_query_image, (f'{program_name}%',))
                    image_row = cursor.fetchone()

                    if image_row and image_row[0]:  # Image found in the images table
                        encoded_image = base64.b64encode(image_row[0]).decode('utf-8')  # Encode image data
                        image_data = f"data:image/jpeg;base64,{encoded_image}"
                    else:  # Image not found in images table, fetch from universities table
                        sql_query_uni_image = "SELECT img_data FROM universities WHERE name = ?"
                        cursor.execute(sql_query_uni_image, (uni_name,))
                        uni_image_row = cursor.fetchone()

                        if uni_image_row and uni_image_row[0]:  # Image found in universities table
                            encoded_image = base64.b64encode(uni_image_row[0]).decode('utf-8')  # Encode image data
                            image_data = f"data:image/jpeg;base64,{encoded_image}"
                        else:
                            image_data = None

                    university_data_list.append({'name': program_name, 'image_data': image_data})

            # Close the cursor and connection
            cursor.close()
            conn.close()

            return render_template('uni.html', programs=university_data_list, uni_name=uni_name)
        else:
            return render_template('error.html', message="Database connection error")
    except Exception as e:
        print(f"Error fetching programs: {e}")
        # Close the cursor and connection in case of exception
        cursor.close()
        conn.close()
        # Return an error response or redirect to an error page
        return render_template('error.html', message="Error fetching data")




# Define route for the choose major page
@app.route('/choose_major')
def choose_major():
    return render_template('choose_major.html')

@app.route('/home')
def home():
    return render_template('./admin/adminpanel.html')

if __name__ == '__main__':
    app.run(debug=True)