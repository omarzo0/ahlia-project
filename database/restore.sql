-- Restore script example
DECLARE @backupPath NVARCHAR(255);
SET @backupPath = 'path';

-- Restore full backup
RESTORE DATABASE [YourDatabaseName]
FROM DISK = @backupPath + 'project.bak'
WITH NORECOVERY, 
     MOVE 'project' TO 'path.mdf',
     MOVE 'project' TO 'path.ldf';

-- Restore differential backup
RESTORE DATABASE [YourDatabaseName]
FROM DISK = @backupPath + 'project.bak'
WITH NORECOVERY;

-- Restore transaction log backups
RESTORE LOG [YourDatabaseName]
FROM DISK = @backupPath + 'project.bak'
WITH NORECOVERY;

-- Complete the restore process
RESTORE DATABASE [project]
WITH RECOVERY;
