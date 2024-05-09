-- Create Universities Table
CREATE TABLE Universities (
    university_id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(255) NOT NULL,
    location NVARCHAR(255) NOT NULL,
    website NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX),
    ranking INT,
    img_data IMAGE  -- New column to store image data
);


-- Create Programs Table
CREATE TABLE Programs (
    program_id INT PRIMARY KEY IDENTITY(1,1),
    university_id INT FOREIGN KEY REFERENCES Universities(university_id),
    name NVARCHAR(255) NOT NULL,
    description NVARCHAR(MAX)
);

-- Create AdmissionRequirements Table
CREATE TABLE AdmissionRequirements (
    requirement NVARCHAR(MAX) NOT NULL
);

-- Create Fees Table
CREATE TABLE Fees (
    fee_id INT PRIMARY KEY IDENTITY(1,1),
    program_id INT FOREIGN KEY REFERENCES Programs(program_id),
    description NVARCHAR(MAX),
    amount DECIMAL(18, 2)
);
