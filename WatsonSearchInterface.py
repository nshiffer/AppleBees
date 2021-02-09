import json
import re
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import Constants
from CrimeReport import CrimeReport
import datetime


class WatsonSearchInterface:
    def __init__(self):
        self.authenticator = IAMAuthenticator(Constants.AUTHENTICATION)
        self.discovery = DiscoveryV1(
            version=Constants.DISCOVERY_VERSION,
            authenticator=self.authenticator
        )
        self.discovery.set_service_url(Constants.WATSON_URL)


    def querySearch(self, search):
        results = []
        queryResults = self.discovery.query(
            environment_id=Constants.ENVIORNMENT_ID,
            collection_id=Constants.COLLECTION_ID,
            natural_language_query=search,
            count=200
        ).get_result()

        results.append(queryResults)
        return results

    def printCrimes(self, search):
        results = self.querySearch(search)
        for query in results:
            for i in range(len(query["results"])):
                print(f'Crime Number: {query["results"][i]["title"][0]}')

                # Finds dates and returns list
                # List is in order of [Date/Time reported, Date/Time Started, Date/Time Ended]
                # Crime is not guaranteed to have a Date/Time Ended
                dates = re.findall(
                    "\\d{2}/\\d{2}/\\d{2} \\d{2}:\\d{2}",
                    query["results"][i]["text"])
                print(f'Dates: {dates}')

                # Some crimes have multiple offenses which are usually separated by ';' character
                # This is not guaranteed as formatting is a bit different for
                # some crime reports
                offenseList = (query["results"][i]["question"][0]).split(';')
                print(f'Offense: {offenseList}')

                print(f'Location: {query["results"][i]["subtitle"][0]}')

                print(f'Disposition: {query["results"][i]["author"][0]}\n')

    def createCrimeListObjects(self, search):
        results = self.querySearch(search)
        crimeObjects = []
        for query in results:
            for i in range(len(query["results"])):
                crimeID = query["results"][i]["title"][0]
                # Finds dates and returns list
                # List is in order of [Date/Time reported, Date/Time Started, Date/Time Ended]
                # Crime is not guaranteed to have a Date/Time Ended
                dates = re.findall(
                    "\\d{2}/\\d{2}/\\d{2} \\d{2}:\\d{2}",
                    query["results"][i]["text"])
                date_format_string = '%m/%d/%y %H:%M'
                reportDate = datetime.datetime.strptime(
                    dates[0], date_format_string)
                crimeStart = datetime.datetime.strptime(
                    dates[1], date_format_string)
                crimeEnd = None if len(dates) < 3 else datetime.datetime.strptime(
                    dates[2], date_format_string)
                # Some crimes have multiple offenses which are usually separated by ';' character
                # This is not guaranteed as formatting is a bit different for
                # some crime reports
                offenseList = (query["results"][i]["question"][0]).split(';')
                location = query["results"][i]["subtitle"][0]
                disposition = query["results"][i]["author"][0]
                crime = CrimeReport(
                    crimeID,
                    reportDate,
                    crimeStart,
                    crimeEnd,
                    offenseList,
                    location,
                    disposition)
                crimeObjects.append(crime)

        return crimeObjects
