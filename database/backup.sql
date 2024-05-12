USE project;  -- Specify your database name

DECLARE @BackupPath NVARCHAR(255) = 'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER01\MSSQL\Backup\project_backup' 
                                   + REPLACE(CONVERT(VARCHAR(20), GETDATE(), 120), ':', '') + '.bak';

BEGIN TRY
    -- Perform the backup
    BACKUP DATABASE project TO DISK = @BackupPath WITH INIT, FORMAT, COMPRESSION;

    -- Return true if backup succeeds
    SELECT 'true' AS BackupResult;
END TRY
BEGIN CATCH
    -- Return false and error message if backup fails
    SELECT 'false' AS BackupResult, ERROR_MESSAGE() AS ErrorMessage;
END CATCH
