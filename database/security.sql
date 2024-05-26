-- Create a role for database operations
CREATE ROLE db_creator;

-- Create a user for managing the database
CREATE USER db_admin WITH PASSWORD = 'ahliaproject12';

-- Assign the role to the user
ALTER ROLE db_creator ADD MEMBER db_admin;

-- Grant necessary permissions to the role
GRANT CREATE TABLE TO db_creator;
GRANT SELECT, INSERT, UPDATE, DELETE ON SCHEMA::dbo TO db_creator;

-- Switching to the db_admin user to execute the table creation
EXECUTE AS USER = 'insert';