from WatsonSearchInterface import WatsonSearchInterface

print("Enter a search word or phrase: ")
search = input()

wi = WatsonSearchInterface()

wi.printCrimes(search)


results = wi.createCrimeListObjects(search)

print(results[0].offenses)
