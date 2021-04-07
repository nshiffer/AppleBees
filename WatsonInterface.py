import json
import re
from ibm_watson import DiscoveryV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import Constants
from CrimeReport import CrimeReport
import datetime


class WatsonInterface:
    def __init__(self):
        self.authenticator = IAMAuthenticator(Constants.AUTHENTICATION)
        self.discovery = DiscoveryV1(
            version=Constants.DISCOVERY_VERSION,
            authenticator=self.authenticator
        )
        self.discovery.set_service_url(Constants.WATSON_URL)

    def parseCrimeList(self):
        results = []
        natural_language_options = ['P2020', 'P2021', 'CSA2020', 'CSA2021']

        for natural_language_selection in natural_language_options:
            queryResults = self.discovery.query(
                environment_id=Constants.ENVIORNMENT_ID,
                collection_id=Constants.COLLECTION_ID,
                natural_language_query=natural_language_selection,
                count=500
            ).get_result()

            results.append(queryResults)
        return results

    def printCrimes(self):
        results = self.parseCrimeList()
        for query in results:
            for i in range(len(query["results"])):
                try:
                    print(f'Crime Number: {query["results"][i]["title"][0]}')

                    # Finds dates and returns list
                    # List is in order of [Date/Time reported, Date/Time Started, Date/Time Ended]
                    # Crime is not guaranteed to have a Date/Time Ended
                    dates = re.findall(
                        "\\d{2}/\\d{2}/\\d{2} \\d{2}:\\d{2}",
                        query["results"][i]["question"][0])
                    print(f'Dates: {dates}')
                    
                    # Some crimes would have a '_' to separate the crime from the details
                    # Removed to make data more pure and easier for the user to read
                     # Some crimes would have a '_' to separate the crime from the details
                    # Removed to make data more pure and easier for the user to read
                    matchIndex = []
                    for match in re.finditer(r'_', query["results"][i]["text"]):
                        matchIndex.append(match.end()-1)
                    
                    offenseCleansed = query["results"][i]["text"].replace('_', '')
                    for i in range(len(matchIndex)):
                        offenseCleansed = offenseCleansed[:matchIndex[i]-1] + offenseCleansed[matchIndex[i]:]
                        matchIndex[:] = [match-1 for match in matchIndex]
                    

                    # Some crimes have multiple offenses which are usually separated by ';' character
                    # This is not guaranteed as formatting is a bit different for
                    # some crime reports
                    
                    offenseList = (offenseCleansed).split(';')
                    for i in range(len(offenseList)):
                        if offenseList[i][0] == ' ':
                            offenseList[i] = offenseList[i].replace(' ', '', 1)

                    print(f'Offense: {offenseList}')

                    print(f'Location: {query["results"][i]["subtitle"][0]}')

                    print(f'Disposition: {query["results"][i]["author"][0]}\n')
                except KeyError:
                    print("Watson Error in formating")

    def createCrimeListObjects(self):
        results = self.parseCrimeList()
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
                     # Some crimes would have a '_' to separate the crime from the details
                    # Removed to make data more pure and easier for the user to read
                    matchIndex = []
                    for match in re.finditer(r'_', query["results"][i]["text"]):
                        matchIndex.append(match.end()-1)
                    
                    offenseCleansed = query["results"][i]["text"].replace('_', '')
                    for i in range(len(matchIndex)):
                        offenseCleansed = offenseCleansed[:matchIndex[i]-1] + offenseCleansed[matchIndex[i]:]
                        matchIndex[:] = [match-1 for match in matchIndex]
                    

                    # Some crimes have multiple offenses which are usually separated by ';' character
                    # This is not guaranteed as formatting is a bit different for
                    # some crime reports
                    
                    offenseList = (offenseCleansed).split(';')
                    for i in range(len(offenseList)):
                        if offenseList[i][0] == ' ':
                            offenseList[i] = offenseList[i].replace(' ', '', 1)

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
                except KeyError:
                    print("Watson Error in formating")

        return crimeObjects
