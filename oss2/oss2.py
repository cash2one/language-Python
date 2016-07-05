#!/usr/bin/env python
# -*- coding: utf-8 -*-

import oss2

def upload(file_name):
    key = ''
    secret = ''
    endpoint = ''
    bucket_val = ''

    auth = oss2.Auth(key, secret)
    bucket = oss2.Bucket(auth, endpoint, bucket_val)
    return bucket.put_object_from_file(file_name, file_name)

if __name__ == '__main__':
    upload('test.jpg')

