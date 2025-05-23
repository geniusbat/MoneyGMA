#!/bin/bash
cd <directory of backup files>
export PGPASSWORD='<password>'; pg_dump -h 127.0.0.1 -U mgma_user -d mgma_db -f mgma_backup.sql
tar -czf mgma_backup.tar.gz mgma_backup.sql --remove-files
#Move file to parent directory. 
mv mgma_backup.tar.gz ../mgma_backup.tar.gz
