"""Verify the local sample API can dispatch a task and read its worker result."""
import argparse
import json
import time
from urllib.request import Request, urlopen


def read_json(url, *, post=False):
    with urlopen(Request(url, method='POST' if post else 'GET'), timeout=5) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:5000')
    args = parser.parse_args()
    base = args.base_url.rstrip('/')
    task = read_json(base + '/api/process_data', post=True)
    task_id = task.get('task_id')
    if not isinstance(task_id, str) or not task_id:
        raise RuntimeError('Task submission did not return an identifier')
    for _ in range(30):
        if read_json(base + '/api/tasks/' + task_id) == {'status': 'processed'}:
            print('Worker executed the sample task and the API returned its result.')
            return
        time.sleep(1)
    raise RuntimeError('Worker result was not available before the deadline')


if __name__ == '__main__':
    main()
