-- Create trigger for INSERT on Universities
CREATE TRIGGER trg_AfterInsertUniversity
ON Universities
AFTER INSERT
AS
BEGIN
    INSERT INTO UniversityLog (university_id, action, new_name, new_location, new_website, new_description, new_ranking)
    SELECT university_id, 'INSERT', name, location, website, description, ranking
    FROM inserted;
END;

-- Create trigger for UPDATE on Universities
CREATE TRIGGER trg_AfterUpdateUniversity
ON Universities
AFTER UPDATE
AS
BEGIN
    INSERT INTO UniversityLog (university_id, action, old_name, new_name, old_location, new_location, old_website, new_website, old_description, new_description, old_ranking, new_ranking)
    SELECT d.university_id, 'UPDATE', d.name, i.name, d.location, i.location, d.website, i.website, d.description, i.description, d.ranking, i.ranking
    FROM deleted d
    INNER JOIN inserted i ON d.university_id = i.university_id;
END;
-- Ensure the referenced university exists before inserting a program
CREATE TRIGGER trg_BeforeInsertProgram
ON Programs
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM Universities WHERE university_id IN (SELECT university_id FROM inserted))
    BEGIN
        INSERT INTO Programs (university_id, name, description)
        SELECT university_id, name, description
        FROM inserted;
    END
    ELSE
    BEGIN
        RAISERROR ('Invalid university_id in Programs table', 16, 1);
    END
END;
-- Automatically insert a default admission requirement when a new program is created
CREATE TRIGGER trg_AfterInsertProgram
ON Programs
AFTER INSERT
AS
BEGIN
    INSERT INTO AdmissionRequirements (requirement)
    SELECT 'Default Requirement'
    FROM inserted;
END;
-- Create trigger for INSERT on Fees
CREATE TRIGGER trg_AfterInsertFee
ON Fees
AFTER INSERT
AS
BEGIN
    INSERT INTO FeeLog (fee_id, program_id, description, amount, action)
    SELECT fee_id, program_id, description, amount, 'INSERT'
    FROM inserted;
END;
-- Ensure the referenced program exists before inserting a fee
CREATE TRIGGER trg_BeforeInsertFee
ON Fees
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM Programs WHERE program_id IN (SELECT program_id FROM inserted))
    BEGIN
        INSERT INTO Fees (program_id, description, amount)
        SELECT program_id, description, amount
        FROM inserted;
    END
    ELSE
    BEGIN
        RAISERROR ('Invalid program_id in Fees table', 16, 1);
    END
END;
-- Create trigger for INSERT on Images
CREATE TRIGGER trg_AfterInsertImage
ON images
AFTER INSERT
AS
BEGIN
    INSERT INTO ImageLog (img_id, name, action)
    SELECT img_id, name, 'INSERT'
    FROM inserted;
END;