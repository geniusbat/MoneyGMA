#!/bin/bash
#It is preferred to backup postgres db
curl --header "Authorization: Token <token>" https://moneygma.duckdns.org/api/expense -o files/expenses_backup