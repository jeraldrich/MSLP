from multiprocessing import Process, cpu_count, Manager
from os import sys
import time
import logging
from Queue import Empty

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import asc

from producers import LargeFileParser, ChatMessageParser
from consumers import create_mysql_pool, batch_insert
from consumers.models import ChatMessage


CHAT_FILE = 'big_input'

logger = logging.getLogger('chat_message_parser')
logger.setLevel(logging.DEBUG)
logging.basicConfig()
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)


def producer_queue(queue, parser):
    for data in LargeFileParser(CHAT_FILE):
        parsed_data = parser.parse(data)
        queue.put(parsed_data)
    queue.put('STOP')


def consumer_queue(proc_id, queue):

    # shared pooled session per consumer proc
    mysql_pool = create_mysql_pool()
    session_factory = sessionmaker(mysql_pool)
    Session = scoped_session(session_factory)

    while True:
        try:
            time.sleep(0.01)
            consumer_data = queue.get(proc_id, 1)
            if consumer_data == 'STOP':
                logger.info('STOP received')
                # put stop back in queue for other consumers
                queue.put('STOP')
                break
            consumer_data_batch = []
            consumer_data_batch.append(consumer_data)
            if queue.qsize() > 500:
                for i in xrange(50):
                    consumer_data = queue.get(proc_id, 1)
                    consumer_data_batch.append(consumer_data)
            session = Session()
            batch_insert(session, consumer_data_batch)
            # logger.info(consumer_data)
        except Empty:
            pass


class ParserManager(object):

    def __init__(self):
        self.manager = Manager()
        self.queue = self.manager.Queue()
        self.NUMBER_OF_PROCESSES = cpu_count()
        self.parser = ChatMessageParser()

    def start(self):
        self.producer = Process(
            target=producer_queue,
            args=(self.queue, self.parser)
        )
        self.producer.start()

        self.consumers = [
            Process(target=consumer_queue, args=(i, self.queue,))
            for i in xrange(self.NUMBER_OF_PROCESSES)
        ]
        for consumer in self.consumers:
            consumer.start()

    def join(self):
        self.producer.join()
        for consumer in self.consumers:
            consumer.join()

if __name__ == '__main__':
    try:
        manager = ParserManager()
        manager.start()
        manager.join()
    except (KeyboardInterrupt, SystemExit):
        logger.info('interrupt signal received')
        sys.exit(1)
    except Exception, e:
        raise e
