import json
import logging
from datetime import datetime

from consumers.models import ChatMessage


logger = logging.getLogger('chat_message_parser')

class ChatMessageParser():

    def parse(self, data):
        """
        parse each line in the log and populate log data with matched pattern
        """
        json_message = json.loads(data)
        # logger.info('json data is {0}'.format(json_message['data']))
        chat_message = None
        if json_message['type'] == 'message':
            chat_message = ChatMessage(
                id=json_message['id'],
                _from=json_message['from'],
                _type=json_message['type'],
                site_id=json_message['site_id'],
                data=json_message['data']['message'],
                timestamp=json_message['timestamp'],
            )
        elif json_message['type'] == 'status':
            chat_message = ChatMessage(
                id=json_message['id'],
                _from=json_message['from'],
                _type=json_message['type'],
                site_id=json_message['site_id'],
                data=json_message['data']['status'],
                timestamp=json_message['timestamp'],
            )
        else:
            logger.error('Invalid json status detected'.format(chat_message))
            return None
        # convert timestamp str to datetime
        chat_message.timestamp = datetime.fromtimestamp(int(json_message['timestamp']))

        return chat_message
