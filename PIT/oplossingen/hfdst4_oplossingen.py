import math
import numpy as np
import random
from pcinput import *

# hulpfunctie die lijst van 'aantal' willekeurige getallen <= bovengrens genereert
def genereerLijst(aantal, bovengrens):
    lijst = []
    for i in range(0,aantal):
        lijst.append(random.randint(0, bovengrens))
    return lijst

# oef. 1
lijst246 = [2, 4, 6]
lijst1357 = [1,3,5,7]
print("Som zou 12 moeten zijn:", sum(lijst246))
print("Som zou 16 moeten zijn:", sum(lijst1357))
print("Product zou 48 moeten zijn:", np.product(lijst246))
print("Product zou 105 moeten zijn:", np.product(lijst1357))
print("Gemiddelde zou 4 moeten zijn:", np.mean(lijst246))
print("Gemiddelde zou 4 moeten zijn:", np.mean(lijst1357))
print("Mediaan zou 4 moeten zijn:", np.median(lijst246))
print("Mediaan zou 4 moeten zijn (want even aantal elementen en dan gemiddelde 2 middelste):", np.median(lijst1357))

# oef. 2: np.add gaat niet omdat de lijsten niet even lang zijn

# oef. 3
cumProductAdd = np.cumproduct(np.add([4,2,1], [1,2,4]))
print("cumulatief product van optelling zou [5,20,100] moeten zijn", cumProductAdd)

# oef. 4
rangeLijst = range(11, 31)
linLijst = np.linspace(25, 120, 20)
# redenering: maakt geen verschil want som(ai+bi) = som(ai)+som(bi)
addThenSum = sum(np.add(rangeLijst, linLijst))
sumThenPlus = sum(rangeLijst)+sum(linLijst)
if addThenSum == sumThenPlus:
    print("Onze redenering was correct.")
else:
    print("Oei. Foutje...")

# oef. 5 (met TDD)
def filterAfwijkingen(lijst):
    avg = np.mean(lijst)
    return filter(lambda x : abs(x-avg)<avg/4, lijst)

def filterAfwijkingen2(lijst):
    avg = np.mean(lijst)
    # kan ook met de list-comprehension
    return [x for x in lijst if abs(x-avg)<avg/4]

########################
#   oef 6.             #
########################

# met for
def veelvouden(ondergrens, bovengrens, getal):
    lijst = list()
    for n in range(ondergrens, bovengrens):
        if n % getal == 0:
            lijst.append(n)
    return lijst

# met list comprehension
def veelvouden2(ondergrens, bovengrens, getal):
    return [n for n in range(ondergrens, bovengrens) if n % getal == 0]

########################
#   oef 7             #
########################

# met for
def aantalVeelvouden2(lijst, getal):
    aantal = 0
    for n in lijst:
        if n % getal == 0:
            aantal = aantal + 1
    return aantal

# met list comprehension
def aantalVeelvouden(lijst, getal):
    return len([n for n in lijst if n % getal == 0])

########################
#   oef 8              #
########################
def lidgeld(leeftijd):
    if leeftijd < 16:
        return 0
    elif leeftijd < 24:
        return 10
    else:
        return 20

voorbeeldLeeftijden1 = [17, 11, 8, 18, 21, 34, 25, 12, 5, 16]
voorbeeldLeeftijden2 = [7, 11, 8, 9, 25, 25, 49, 31]
# (meer voorbeelden in de testen)

# berekenLidgelden neemt een lijst met leeftijden
# en geeft de lijst met lidgelden per persoon terug
def berekenLidgelden(leeftijden):
    return list(map(lidgeld, leeftijden))

# berekenLidgeldTotaal neemt een lijst met leeftijden
# en geeft het totale lidgeld voor deze groep terug
def berekenLidgeldTotaal(leeftijden):
    lidgelden = list(map(lidgeld, leeftijden))
    # of: lidgelden = berekenLidgelden(leeftijden)
    return sum(lidgelden)

def betalendeLeden(leeftijden):
    return filter(lambda l: lidgeld(l) > 0, leeftijden)

########################
#   oef 8.             #
########################

# met for
def inBeideLijsten(lijst1, lijst2):
    uitkomst = list()
    for x in lijst1:
        if x in lijst2:
            uitkomst.append(x)
    return uitkomst

# met list comprehension
def inBeideLijsten2(lijst1, lijst2):
    return [x for x in lijst1 if x in lijst2]

########################
#   oef 9.             #
########################

def inEenLijst(lijst1, lijst2):
    uitkomst = list()
    for x in lijst1:
        if not x in lijst2:
            uitkomst.append(x)
    for x in lijst2:
        if not x in lijst1:
            uitkomst.append(x)
    return uitkomst

def inEenLijst2(lijst1, lijst2):
    eenNietIn2 = [x for x in lijst1 if not x in lijst2]
    tweeNietIn1 = [x for x in lijst2 if not x in lijst1]
    return eenNietIn2 + tweeNietIn1

########################
#   oef 11.             #
########################

def somParen(n):
    return [(x,y) for x in range(1,n) for y in range(1,n) if x + y == n]

def somParen2(n):
    return [(x, n-x) for x in range(1,n)]

########################
#   oef 12             #
########################
def changeCaseLetter(letter):
    if letter.isupper():
        return letter.lower()
    else:
        return letter.upper()

def changeCase(woord):
    return ''.join([changeCaseLetter(letter) for letter in woord])

def changeCaseGemakkelijk(woord):
    return ''.join([letter.swapcase() for letter in woord])

########################
#   oef 13             #
########################
def upperlower(woord, n):
    if n%2 == 0:
        return woord[n].upper()
    else:
        return woord[n].lower()

def varieerCase(woord):
    return ''.join([upperlower(woord, i) for i in range(0, len(woord))])