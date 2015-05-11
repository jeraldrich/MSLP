# MSLP - Multiprocessing SQLAlchemy Largefile Processor
INSTALL NOTES:

- have mysql installed
- sudo apt-get install libmysqlclient-dev
- sudo apt-get install mysql
- have mysql running
- configure settings.py with MYSQL credentials
- have virtualenv installed
- python bootstrap.py
- source venv/bin/activate 
- python generate_chat_file.py (or set CHAT_LOG in settings)
- python parse_chat_file.py

This takes advantage of multiple processors. Able to parse a file of any size by splitting it into seperate file chunks, and yielding each line to a consumer queue.

The main process parses the file and is the producer. Due to disk IO limitations, only one producer parses the file. 

For every core you have, a seperate process will be spawned and handle SQLAlchemy integrity checks, parsing, and insertion into MySQL using batch inserts.

Parses and stores 10 million messages in a transactional database in around 2-3 minutes. Generates results in 1 minute. Processor usage around 25% per core. Total memory usage between 70-120MB 

Generates a result file for you to check against.

- If using virtualbox, allocate multiple processors to your VM. Settings>System>Processor and increase processor count
