import os
import tempfile
import pytest
import string
from main import server
import json
test = server.test_client()
count = 0
with open('blns.base64.json') as f:
  data = json.load(f)
standard_ascii = [chr(i) for i in range(128)]
data.append(standard_ascii) #Adds all printable characters to naughty inputs
options = ["text", "title", "question", "subtitle", "author"]
for payload in data:
    for searchParam in options:
        testRequest = "/search?crime={}&options={}".format(payload, searchParam)
        response = test.get(testRequest)
        assert response.status == "200 OK"
        print("Test", count, "passed")
        count += 1
