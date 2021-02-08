import json
import re
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


authenticator = IAMAuthenticator('ghODqOQRw_e9AHE4Eqg0QbcT6jdfLi9pBcS7xbSSY58Z')
discovery = DiscoveryV1(
    version='2021-01-31',
    authenticator=authenticator
)

discovery.set_service_url('https://api.us-east.discovery.watson.cloud.ibm.com/instances/7fc37f80-f2a5-4059-9db6-dbe6808abf9c')

e_id = '5401113d-17ca-48a1-8627-c534df11a1fb'
c_id = 'd3e37d16-11f1-4be9-9db5-40b1f3f98c62'
queryResults = []

queryResults.append(discovery.query(
  environment_id = e_id,
  collection_id = c_id,
  natural_language_query='P2020',
  count = 200
).get_result())

queryResults.append(discovery.query(
  environment_id=e_id,
  collection_id=c_id,
  natural_language_query='P2021',
  count = 200
).get_result())

queryResults.append(discovery.query(
  environment_id=e_id,
  collection_id=c_id,
  natural_language_query='CSA2020',
  count = 200
).get_result())

queryResults.append(discovery.query(
  environment_id=e_id,
  collection_id=c_id,
  natural_language_query='CSA2021',
  count = 200
).get_result())


crimeList = []
for query in queryResults:
  for i in range(len(query["results"])):
    print(f'Crime Number: {query["results"][i]["title"][0]}')

    #Finds dates and returns list
    #List is in order of [Date/Time reported, Date/Time Started, Date/Time Ended]
    #Crime is not guaranteed to have a Date/Time Ended
    dates = re.findall("\d{2}/\d{2}/\d{2} \d{2}:\d{2}", query["results"][i]["text"])
    print(f'Dates: {dates}')

    #Some crimes have multiple offenses which are usually separated by ';' character
    #This is not guaranteed as formatting is a bit different for some crime reports
    offenseList = (query["results"][i]["question"][0]).split(';')
    print(f'Offense: {offenseList}')

    print(f'Location: {query["results"][i]["subtitle"][0]}')

    print(f'Disposition: {query["results"][i]["author"][0]}\n')
