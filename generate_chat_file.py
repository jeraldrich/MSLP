import uuid
from random import randint, choice, shuffle

from faker import Factory

from settings import CHAT_LOG


fake = Factory.create()


def generate_online_status():
    pk = uuid.uuid1()
    _type = 'status'
    _from = 'operator{0}'.format(randint(0, 5))
    site_id = '{0}'.format(randint(0, 9))
    online_choices = ['online', 'offline']
    is_online = choice(online_choices)
    timestamp = fake.date_time()
    timestamp = timestamp.toordinal()
    row = (
        '{{"id":"{pk}","type":"{_type}","from":"{_from}",',
        '"site_id":"{site_id}","timestamp":{timestamp},',
        '"data":{{"status":"{is_online}"}}}}\n',
    )
    row_str = ''.join(row).format(
        pk=pk,
        _type=_type,
        _from=_from,
        site_id=site_id,
        timestamp=timestamp,
        is_online=is_online
    )
    return row_str


def generate_chat_message():
    pk = uuid.uuid1()
    _type = 'message'
    _from = 'visitor{0}'.format(randint(0, 99))
    site_id = '{0}'.format(randint(0, 9))
    message = fake.text().encode('ascii', errors='ignore')
    message = message.replace('\r', '')
    message = message.replace('\n', '')
    timestamp = fake.date_time()
    timestamp = timestamp.toordinal()
    row = (
        '{{"id":"{pk}","type":"{_type}","from":"{_from}",',
        '"site_id":"{site_id}","timestamp":{timestamp},',
        '"data":{{"message":"{message}"}}}}\n',
    )
    row_str = ''.join(row).format(
        pk=pk,
        _type=_type,
        _from=_from,
        site_id=site_id,
        timestamp=timestamp,
        message=message
    )
    return row_str

if __name__ == '__main__':
    online_status = [generate_online_status() for i in range(100)]
    messages = [generate_chat_message() for i in range(100000)]
    results = online_status + messages
    shuffle(results)
    # generate duplicate messages
    for i in range(500):
        results.append(choice(results))
    shuffle(results)
    with open(CHAT_LOG, 'w') as f:
        f.writelines(results)
    print 'results file created: {0}'.format(CHAT_LOG)
