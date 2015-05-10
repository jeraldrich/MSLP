from itertools import chain, islice
import os
import time
import logging

logger = logging.getLogger('chat_message_parser')

class LargeFileParser(object):

    def __init__(self, filename):
        self.filename = filename
        self.split_files = []
        # lines per split file
        self.split_every = 100000
        self._split_large_file()

    def __iter__(self):
        logger.info('yielding')
        while self.split_files:
            split_file = self.split_files.pop()
            with open(split_file, 'rU') as f:
                lines = f.readlines()
                for line in lines:
                    yield line
            logger.info('removing split_file')
            os.remove(split_file)
        lines = None
        logger.info('end')

    def _split_large_file(self):
        """
        from http://codereview.stackexchange.com/a/57400
        """
        if not os.path.isfile(self.filename):
            raise Exception(
                'file does not exist:{0}'.format(self.filename)
            )
        def _chunks(chunk_iterable, n):
           chunk_iterable = iter(chunk_iterable)
           while True:
               yield chain([next(chunk_iterable)], islice(chunk_iterable, n-1))
        with open(self.filename) as bigfile:
            for i, lines in enumerate(_chunks(bigfile, self.split_every)):
                file_split = '{}.{}'.format(self.filename, i)
                with open(file_split, 'w') as f:
                    f.writelines(lines)
                self.split_files.append(file_split)
        #logger.info(self.split_files)
        return True
