# MSLP - Multiprocessing SQLAlchemy Largefile Processing

Example using Python 3 multiprocessing to parse large files:
http://blog.jeremyaldrich.net/en/latest/multiprocessing_sqlalchemy_largefile_processing.html

- Parses file of any size (1GB+) 
- Inserts file contents into mysql using SQLAlchemy per processor in batch inserts
- Processes 10million+ rows of json by reading file, filtering through SQLAlchemy models,  and inserting into MySQL in 2 minutes and 70-100MB memory consistently
- Processing speed increases per cpu avaliable: from multiprocessing import cpu_count; cpu_count()

This takes advantage of multiple processors. Able to parse a file of any size by splitting it into seperate file chunks, and yielding each line to a consumer queue.

The main process parses the file and is the producer. Due to disk IO limitations, only one producer parses the file, but can be easily increased if you run this on SSD for example.

For every core you have, a seperate process will be spawned and handle SQLAlchemy integrity checks, parsing, and insertion into MySQL using batch inserts.

Parses and stores 10 million messages in a transactional database in around 2-3 minutes. Generates results in 1 minute. Processor usage around 7%-20% per core. Total memory usage between 70-100MB total.

Generates a result file for you to check against.

- If using virtualbox, allocate multiple processors to your VM. Settings>System>Processor and increase processor count
