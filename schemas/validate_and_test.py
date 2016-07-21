import json

import jsonschema
import requests


API_BASE = 'https://crash-stats.mozilla.com/api/{}/'


def main():
    schema = json.load(open('processed_crash.json'))
    jsonschema.Draft4Validator.check_schema(schema)
    print('Processed Crash schema is valid')

    print('Fetching data...')
    r = requests.get(
        API_BASE.format('SuperSearch'),
        params={
            'product': 'Firefox',
            '_columns': ['uuid'],
        }
    )
    search = r.json()

    print('Testing {} random recent crash reports'.format(len(search['hits'])))
    for hit in search['hits']:
        r = requests.get(
            API_BASE.format('ProcessedCrash'),
            params={'uuid': hit['uuid']}
        )
        print(r.url)
        crash = r.json()
        jsonschema.validate(crash, schema)

    print('Done testing, all crash reports passed.')


if __name__ == '__main__':
    main()