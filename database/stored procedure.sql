-- Create the stored procedure to handle login and hash password
CREATE PROCEDURE LoginUser
    @Username NVARCHAR(255),
    @Password NVARCHAR(255),
    @LoginResult INT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    -- Hash the input password using SHA-512 algorithm
    DECLARE @HashedPassword VARBINARY(64);
    SET @HashedPassword = HASHBYTES('SHA2_512', @Password);

    -- Check if the username and hashed password match in the admin table
    IF EXISTS (
        SELECT 1
        FROM admin
        WHERE name = @Username
        AND passHash = @HashedPassword
    )
    BEGIN
        -- Set login result to 1 for successful login
        SET @LoginResult = 1;
    END
    ELSE
    BEGIN
        -- Set login result to 0 for invalid credentials
        SET @LoginResult = 0;
    END;
END;
