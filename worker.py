# import os
import time
import sys
from utils import add_listener

# import redis
# from rq import Worker, Queue, Connection

# listen = ['high', 'default', 'low']

# redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

# conn = redis.from_url(redis_url)

# if __name__ == '__main__':
#     with Connection(conn):
#         worker = Worker(map(Queue, listen))
#         worker.work()
if __name__ == '__main__':
    while True:
        returnval = add_listener()
        sys.stderr.write(str(returnval) + '\n')
        time.sleep(1)
