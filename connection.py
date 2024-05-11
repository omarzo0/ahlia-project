import odbc  # Assuming you are using pyodbc for database connectivity
# Database connection parameters
DRIVER_NAME = 'SQL Server'
SERVER_NAME = 'Mohamed\\MSSQLSERVER01'
DATABASE_NAME = 'project'

def connect(limit=None):
    try:
        # Establish a connection
        connection_string = f""" 
            DRIVER={{{DRIVER_NAME}}};
            SERVER={SERVER_NAME};
            DATABASE={DATABASE_NAME};
            Trust_Connection=yes;
        """
        conn = odbc.connect(connection_string)

        # Close the connection
        conn.close()

        return True  # Return True if connection successful
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return False  # Return False if connection fails
