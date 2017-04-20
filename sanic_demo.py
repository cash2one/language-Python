#!/usr/bin/env python
# coding: utf-8

from sanic import Sanic
from sanic.response import json

app = Sanic()

@app.route('/')
async def home(request):
    return json({'helo': 'world'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
