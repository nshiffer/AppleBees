import datetime
import re
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV1

import Constants
from CrimeReport import CrimeReport


class WatsonSearchInterface:
    def __init__(self):
        self.authenticator = IAMAuthenticator(Constants.AUTHENTICATION)
        self.discovery = DiscoveryV1(
            version=Constants.DISCOVERY_VERSION,
            authenticator=self.authenticator
        )
        self.discovery.set_service_url(Constants.WATSON_URL)


    def querySearch(self, search, field):
        results = []
        queryResults = self.discovery.query(
            environment_id=Constants.ENVIORNMENT_ID,
            collection_id=Constants.COLLECTION_ID,
            query=search,
            sort=field,
            count=300
        ).get_result()

        results.append(queryResults)
        return results

    def printCrimes(self, search):
        results = self.querySearch(search)
        for query in results:
            for i in range(len(query["results"])):
                try:
                    print(i)
                    print(f'Crime Number: {query["results"][i]["title"][0]}')

                    # Finds dates and returns list
                    # List is in order of [Date/Time reported, Date/Time Started, Date/Time Ended]
                    # Crime is not guaranteed to have a Date/Time Ended
                    dates = re.findall(
                        "\\d{2}/\\d{2}/\\d{2} \\d{2}:\\d{2}",
                        query["results"][i]["question"][0])
                    print(f'Dates: {dates}')

                    # Some crimes have multiple offenses which are usually separated by ';' character
                    # This is not guaranteed as formatting is a bit different for
                    # some crime reports
                    offenseList = (query["results"][i]["text"]).split(';')
                    print(f'Offense: {offenseList}')

                    print(f'Location: {query["results"][i]["subtitle"][0]}')

                    print(f'Disposition: {query["results"][i]["author"][0]}\n')
                except KeyError:
                    print("Watson Error in formating")

    def createCrimeListObjects(self, search, field):
        results = self.querySearch(search, field)
        crimeObjects = []
        for query in results:
            for i in range(len(query["results"])):
                try:
                    crimeID = query["results"][i]["title"][0]
                    # Finds dates and returns list
                    # List is in order of [Date/Time reported, Date/Time Started, Date/Time Ended]
                    # Crime is not guaranteed to have a Date/Time Ended
                    dates = re.findall(
                        "\\d{2}/\\d{2}/\\d{2} \\d{2}:\\d{2}",
                        query["results"][i]["question"][0])
                    date_format_string = '%m/%d/%y %H:%M'
                    reportDate = datetime.datetime.strptime(
                        dates[0], date_format_string)
                    crimeStart = datetime.datetime.strptime(
                        dates[1], date_format_string)
                    crimeEnd = None if len(dates) < 3 else datetime.datetime.strptime(
                        dates[2], date_format_string)
                    # Some crimes would have a '_' to separate the crime from the details
                    # Removed to make data more pure and easier for the user to read
                    matchIndex = []
                    for match in re.finditer(r'_', query["results"][i]["text"]):
                        matchIndex.append(match.end()-1)
                    
                    offenseCleansed = query["results"][i]["text"].replace('_', '')
                    for j in range(len(matchIndex)):
                        offenseCleansed = offenseCleansed[:matchIndex[j]-1] + offenseCleansed[matchIndex[j]:]
                        matchIndex[:] = [match-1 for match in matchIndex]
                    

                    # Some crimes have multiple offenses which are usually separated by ';' character
                    # This is not guaranteed as formatting is a bit different for
                    # some crime reports
                    
                    offenseList = (offenseCleansed).split(';')

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
                    if len(query["results"][i]["title"]) == 1:
                        crimeObjects.append(crime)
                except KeyError:
                    print("Watson Error in formating")
        return crimeObjects
