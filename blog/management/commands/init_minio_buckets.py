import json
import os
import sys
import time

import requests
from minio import Minio


def init_minio():
    endpoint = os.getenv('MINIO_ENDPOINT', 'minio:9000')
    access_key = os.getenv('MINIO_ACCESS_KEY')
    secret_key = os.getenv('MINIO_SECRET_KEY')

    if not all([access_key, secret_key]):
        print('Missing MinIO credentials')
        return False

    print('Initializing MinIO buckets...')
    print(f'  Endpoint: {endpoint}')
    print(f'  Access Key: {access_key}')

    print('⏳ Waiting for MinIO to be ready...')
    for i in range(30):
        response = requests.get('http://minio:9000/minio/health/live', timeout=5)
        if response.status_code == 200:
            print('MinIO is ready!')
            break
        if i == 29:
            print('MinIO not ready after 30 attempts')
            return False
        time.sleep(2)

    try:
        client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=False)

        buckets = ['django-static', 'django-media']

        for bucket in buckets:
            if not client.bucket_exists(bucket):
                client.make_bucket(bucket)
                print(f'Created bucket: {bucket}')

                if bucket == 'django-static':
                    policy = {
                        'Version': '2012-10-17',
                        'Statement': [
                            {
                                'Effect': 'Allow',
                                'Principal': {'AWS': '*'},
                                'Action': ['s3:GetObject'],
                                'Resource': [f'arn:aws:s3:::{bucket}/*'],
                            }
                        ],
                    }

                    client.set_bucket_policy(bucket, json.dumps(policy))
                    print(f'Set public policy for: {bucket}')
            else:
                print(f'ℹBucket already exists: {bucket}')

        print('MinIO buckets initialized successfully!')
        return True

    except Exception as e:
        print(f'Error initializing MinIO: {e}')
        return False


if __name__ == '__main__':
    success = init_minio()
    sys.exit(0 if success else 1)
