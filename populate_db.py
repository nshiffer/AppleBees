import json
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('mMUZJ1o5cqe_73t_NZbhXTdl3i_NKgJSHsKAMLdsJRII')
discovery = DiscoveryV1(
    version='2019-04-30',
    authenticator=authenticator
)

discovery.set_service_url('https://api.us-east.discovery.watson.cloud.ibm.com/instances/f5def595-d626-42f0-916a-a372d312d7b8')

environments = discovery.list_collections("886ddeb7-bafa-47f4-b893-87a96da70bc2")
weeeee = discovery.query("886ddeb7-bafa-47f4-b893-87a96da70bc2","692d1d66-75c7-4e06-8c10-e2e0cbb08004")
# qopts = {'filter':{'enriched_text.concepts.text:"Rape"'}}
# my_query = discovery.query("system", coll_id, qopts)
print(weeeeee)