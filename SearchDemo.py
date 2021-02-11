from WatsonSearchInterface import WatsonSearchInterface

print("Enter a search word or phrase: ")
search = input()

wi = WatsonSearchInterface()

results2 = wi.printCrimes(search)
