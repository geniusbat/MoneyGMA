#!/bin/bash
cd /apps/MoneyGMA/backup.d
export PGPASSWORD='7hftc0A1vITotj'; pg_dump -h 127.0.0.1 -U mgma_user -d mgma_db -f mgma_backup.sql
tar -czf mgma_backup.tar.gz mgma_backup.sql --remove-files
mv mgma_backup.tar.gz ../mgma_backup.tar.gz
