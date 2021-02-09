from WatsonSearchInterface import WatsonSearchInterface

print("Enter a search word or phrase: ")
search = input()

wi = WatsonSearchInterface()

results1 = wi.printCrimes(search)
print(results1)

results = wi.createCrimeListObjects(search)
print(results)