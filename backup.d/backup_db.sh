#!/bin/bash
<<<<<<< HEAD
cd /apps/MoneyGMA/backup.d
export PGPASSWORD='7hftc0A1vITotj'; pg_dump -h 127.0.0.1 -U mgma_user -d mgma_db -f mgma_backup.sql
tar -czf mgma_backup.tar.gz mgma_backup.sql --remove-files
=======
cd <directory of backup files>
export PGPASSWORD='<password>'; pg_dump -h 127.0.0.1 -U mgma_user -d mgma_db -f mgma_backup.sql
tar -czf mgma_backup.tar.gz mgma_backup.sql --remove-files
#Move file to parent directory. 
>>>>>>> e6a7a100a220fa6cc6525822a351bcc02904758f
mv mgma_backup.tar.gz ../mgma_backup.tar.gz
