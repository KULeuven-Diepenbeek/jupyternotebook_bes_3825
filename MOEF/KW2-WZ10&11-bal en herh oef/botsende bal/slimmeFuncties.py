import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

#####################
# versie 08.12.2023 #
#####################

def selecteerAantalXas(df, aantalXas):
    """ SELECTEER de eerste 'aantalXas' waarden van het dataframe

    :param df (DataFrame): het dataframe waaruit geselecteerd moet worden
    :param aantalXas (int): het aantal waarden op de x-as dat behouden moet blijven
    :return (DataFrame): een deelverzameling vooraan uit het dataframe

    """
    knip = df[0:aantalXas]
    return knip

def knipAantalXas(df, aantalXas):
    """ KNIP de eerste 'aantalXas' waarden WEG uit het dataframe

    :param df (DataFrame): df het dataframe waaruit geknipt moet worden
    :param aantalXas (int): het aantal waarden op de x-as dat verwijderd moet worden
    :return (DataFrame): een deelverzameling achteraan uit het dataframe met indexes vanaf 0, 1, 2, ...
    """
    knip = df[aantalXas:]
    return knip.reset_index().drop("index", axis=1)


def selecteerAantalYas(df, kolom, aantalYas):
    """ SELECTEER de eerste VERSCHILLENDE 'aantalYas' waarden van het dataframe

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom op de y-as
    :param aantalYas (int): het aantal waarden op de y-as dat behouden moet blijven
    :return (DataFrame): een deelverzameling vooraan uit het dataframe
    """
    yAs = []
    index = 0
    while index < len(df) and len(yAs) < aantalYas:
        waarde = df.iloc[index][kolom]
        if not waarde in yAs:
            yAs.append(waarde)
        index = index + 1

    knip = df[0:index]
    return knip

def knipAantalYas(df, kolom, aantalYas):
    """ knip de eerste VERSCHILLENDE 'aantalYas' waarden WEG uit het dataframe

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom op de y-as
    :param aantalYas (int): het aantal waarden op de y-as dat verwijderd moet worden
    :return (DataFrame): een deelverzameling achteraan uit het dataframe met indexes vanaf 0, 1, 2, ...
    """
    yAs = []
    index = 0
    while index < len(df) and len(yAs) < aantalYas:
        waarde = df.iloc[index][kolom]
        if not waarde in yAs:
            yAs.append(waarde)
        index = index + 1

    knip = df[index:]
    return knip.reset_index().drop("index", axis=1)

def selecteerTotWaarde(df, kolom, waarde, stijgendeFlank = True):
    """ SELECTEER de rijen uit het dataframe tot de opgeven waarde voor de opgegeven kolom

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :param waarde (double): de grens voor de waarde in de opgegeven kolom
    :param stijgendeFlank (boolean): indien true zit de functie op een stijgende flank
                                     en is 'waarde' een bovengrens; anders een ondergrens
    :return (DataFrame): een deelverzameling vooraan uit het dataframe
    """
    df = df.reset_index().drop("index", axis=1)
    if stijgendeFlank:
       teVer = df[df[kolom] >= waarde]
    else:
       teVer = df[df[kolom] <= waarde]

    if len(teVer) == 0:
        return df

    index = teVer.index[0]
    knip = df[0:index]

    return knip.reset_index().drop("index", axis=1)

def knipTotWaarde(df, kolom, waarde, stijgendeFlank = True):
    """ KNIP de rijen uit het dataframe WEG tot de opgeven waarde voor de opgegeven kolom

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :param waarde (double): de grens voor de waarde in de opgegeven kolom
    :param stijgendeFlank (boolean): indien true zit de functie op een stijgende flank
                                     en is 'waarde' een bovengrens; anders een ondergrens
    :return (DataFrame): een deelverzameling achteraan uit het dataframe met indexes vanaf 0, 1, 2, ...
    """
    df = df.reset_index().drop("index", axis=1)
    if stijgendeFlank:
       teVer = df[df[kolom] >= waarde]
    else:
       teVer = df[df[kolom] <= waarde]
    if len(teVer) == 0:
        return pd.DataFrame()

    index = teVer.index[0]
    knip = df[index:]

    return knip.reset_index().drop("index", axis=1)

def selecteerTotPercentage(df, kolom, percent, stijgendeFlank = True):
    """ SELECTEER de rijen uit het dataframe tot het opgegeven percentage voor de opgegeven kolom

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :param percent (double): grens voor de waarde in de opgegeven kolom,
                             percent (van 0 tot 1) van het verschil tussen het minimum
                             en het maximum van de waardes in de opgegeven kolom
    :param stijgendeFlank (boolean): indien true zit de functie op een stijgende flank
                                     en is 'waarde' een bovengrens; anders een ondergrens
    :return (DataFrame): een deelverzameling vooraan uit het dataframe
    """
    maximum = df[kolom].max()
    minimum = df[kolom].min()
    waarde = (maximum - minimum)*percent + minimum
    return selecteerTotWaarde(df, kolom, waarde, stijgendeFlank)

def knipTotPercentage(df, kolom, percent, stijgendeFlank = True):
    """KNIP de rijen uit het dataframe WEG tot het opgegeven percentage voor de opgegeven kolom

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :param percent (double): grens voor de waarde in de opgegeven kolom,
                             percent (van 0 tot 1) van het verschil tussen het minimum
                             en het maximum van de waardes in de opgegeven kolom
    :param stijgendeFlank (boolean): indien true zit de functie op een stijgende flank
                                     en is 'waarde' een bovengrens; anders een ondergrens
    :return (DataFrame): een deelverzameling achteraan uit het dataframe met indexes vanaf 0, 1, 2, ...
    """
    maximum = df[kolom].max()
    minimum = df[kolom].min()
    waarde = (maximum - minimum)*percent + minimum
    return knipTotWaarde(df, kolom, waarde, stijgendeFlank)


# hulpfunctie voor zoektocht naar LokaalExtremum
def isLokaalExtremum(y1, y2, stijgendeFlank):
    return (y1 > y2 and stijgendeFlank) or (y2 > y1 and not stijgendeFlank)

def zoekIndexLokaalExtremum(df, kolom):
    """ bereken de index van het eerste LokaalExtremum

    :param df (DataFrame): het dataframe waarin gezocht wordt
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :return: de index van het eerste LokaalExtremum of len(df) als er geen LokaalExtremum is
    """
    if len(df) < 2:
        return len(df)

    if df.loc[0,kolom] <= df.loc[1,kolom]:
        stijgendeFlank = True
    else:
        stijgendeFlank = False

    index = 2
    while index < len(df) and not isLokaalExtremum(df.loc[index-1,kolom], df.loc[index,kolom], stijgendeFlank):
        index = index + 1
    return index

def selecteerTotLokaalExtremum(df, kolom):
    """ SELECTEER de rijen uit het dataframe tot en met het eerstvolgende LokaalExtremum

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :return (DataFrame): een deelverzameling uit het dataframe tot en met het LokaalExtremum. Het volledige df als er geen LokaalExtremum was
    """
    index = zoekIndexLokaalExtremum(df, kolom)
    return df[0:index]

def knipTotLokaalExtremum(df, kolom):
    """ KNIP de rijen uit het dataframe WEG tot het eerstvolgende LokaalExtremum

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :return (DataFrame): een deelverzameling uit het dataframe vanaf het LokaalExtremum en met indexes vanaf 0, 1, 2, ...
                         Een leeg dataframe indien er geen LokaalExtremum was
    """
    index = zoekIndexLokaalExtremum(df, kolom)
    if index < len(df):
       knip = df[index-1:]
    else:
       knip = df[index:]
    return knip.reset_index().drop("index", axis=1)



#################################################################
# functies om te kunnen knippen op basis van functievoorschrift #
#################################################################

def xOverschrijdtWaarde(f, waarde, beginX, eindX, stapgrootte, stijgendeFlank = True):
    """ zoek de eerste x waarvoor f(x) de opgegeven waarde overschrijdt

    :param f (functie: double -> double): het functievoorschrift met één parameter
    :param waarde (double): de waarde die overschreden moet worden
    :param beginX (double): begin van het interval voor x
    :param eindX (double): einde van het interval voor y
    :param stapgrootte (double): grootte tussen 2 opeenvolgende x-waarden
    :param stijgendeFlank (boolean): indien true moet f(x) > waarde, indien false met f(x) < waarde
    :return (double): index waar f(x) de waarde overschrijdt; een getal > eindX indien dat niet gebeurt
    """
    def overschrijdt(x):
        return (stijgendeFlank and f(x) > waarde) or \
               (not stijgendeFlank and f(x) < waarde)

    x = beginX

    while not (overschrijdt(x)) and x < eindX:
        x = x + stapgrootte

    return x

def xMaximaal(f, beginX, eindX, stapgrootte):
    """ zoek de (eerste) x die de maximale f(x) geeft

    :param f (functie: double -> double): het functievoorschrift met één parameter
    :param beginX (double): begin van het interval voor x
    :param eindX (double): einde van het interval voor y
    :param stapgrootte (double): grootte tussen 2 opeenvolgende x-waarden
    :return (double): index waar f(x) (de eerste keer) maximaal is
    """

    x = beginX
    grootste = f(x)

    verschil = eindX - beginX
    aantalGeheel = verschil // stapgrootte
    aantalFloat = verschil / stapgrootte

    if aantalFloat > aantalGeheel:
        aantal = int(aantalGeheel)+1
        linspaceEind = beginX + (aantal-1)*stapgrootte
    else:
        aantal = int(aantalGeheel) + 1
        linspaceEind = eindX

    for i in np.linspace(beginX, linspaceEind, aantal):
        if f(i) > grootste:
            grootste = f(i)
            x = i

    return x

def xMinimaal(f, beginX, eindX, stapgrootte):
    """ zoek de (eerste) x die de minimale f(x) geeft

    :param f (functie: double -> double): het functievoorschrift met één parameter
    :param beginX (double): begin van het interval voor x
    :param eindX (double): einde van het interval voor y
    :param stapgrootte (double): grootte tussen 2 opeenvolgende x-waarden
    :return (double): index waar f(x) (de eerste keer) minimaal is
    """

    x = beginX
    kleinste = f(x)

    verschil = eindX - beginX
    aantalGeheel = verschil // stapgrootte
    aantalFloat = verschil / stapgrootte

    if aantalFloat > aantalGeheel:
        aantal = int(aantalGeheel)+1
        linspaceEind = beginX + (aantal-1)*stapgrootte
    else:
        aantal = int(aantalGeheel) + 1
        linspaceEind = eindX

    for i in np.linspace(beginX, linspaceEind, aantal):
        if f(i) < kleinste:
            kleinste = f(i)
            x = i

    return x

def xLokaalExtremum(f, beginX, eindX, stapgrootte):
    """ zoek de (eerste) x die een LokaalExtremum voor f(x) geeft

    :param f (functie: double -> double): het functievoorschrift met één parameter
    :param beginX (double): begin van het interval voor x
    :param eindX (double): einde van het interval voor y
    :param stapgrootte (double): grootte tussen 2 opeenvolgende x-waarden
    :return (double): index waar f(x) een LokaalExtremum vormt; een getal > eindX indien dat niet gebeurt
    """

    x = beginX
    if f(x) <= f(x+stapgrootte):
        stijgendeFlank = True
    else:
        stijgendeFlank = False

    while x  <= eindX and not isLokaalExtremum(f(x), f(x+stapgrootte), stijgendeFlank):
        x = x + stapgrootte

    return x

########################
#                      #
#  ZWEVEND GEMIDDELDE  #
#                      #
########################

def zwevendGemiddelde(xs,n):
    ''' geef het zwevend gemiddelde terug uit xs met een periode van n

    :param xs ([double]): de lijst getallen waarvan je het zwevend gemiddelde wil
    :param n (int): de periode voor het zwevend gemiddelde, bv. 7
    :return ([float]): De lijst met het zwevend gemiddelde met de opgegeven periode.
                        De lijst die terug gegeven wordt, is even lang als in de invoerlijst xs
                        voor de eerste n-1 getallen wordt het gewogen gemiddelde van het begin tot het getal gegeven
    '''
    xFilt = list()
    xFilt.append(xs[0])

    for i in range(1, n):
        xFilt.append(np.mean(xs[0:i+1]))

    for i in range(n, len(xs)):
        xFilt.append(np.mean(xs[i-n+1:i+1]))
    return xFilt

########################
#                      #
#    CURVE FITTING     #
#                      #
########################

def fitVeelterm(xs,ys, graad):
    """ genereert functie die een veelterm-curve fit is in de opgegeven graad

    :param xs ([float]): lijst met x-waarden
    :param ys ([float]): lijst met y-waarden
    :param graad (int): de gewenste graad van de veelterm
    :return (functie float -> float): veeltermfunctie die de curve fit is van xs op ys
    """
    z = np.polyfit(xs,ys, graad)
    return np.poly1d(z)

def fitExp(xs, ys):
    """ genereert functie die een exponentiële curve fit is

    :param xs ([float]): lijst met x-waarden
    :param ys ([float]): lijst met y-waarden
    :return (functie float -> float): exponentiële functie die de curve fit is van xs op ys
    """

    # bron: https://towardsdatascience.com/basic-curve-fitting-of-scientific-data-with-python-9592244a2509
    def exponential(x, a, b):
        return a * np.exp(b * x)

    pars, cov = curve_fit(f=exponential, xdata=xs, ydata=ys, p0=[0, 0], bounds=(-np.inf, np.inf))

    return lambda x : pars[0] * np.exp(pars[1] * x)

def fitLog(xs, ys):
    """ genereert functie die een logaritmische curve fit is

    :param xs ([float]): lijst met x-waarden
    :param ys ([float]): lijst met y-waarden
    :return (functie float -> float): logaritmische functie die de curve fit is van xs op ys
    """

    # bron: https://towardsdatascience.com/basic-curve-fitting-of-scientific-data-with-python-9592244a2509 en
    #   en  https://stackoverflow.com/questions/3433486/how-to-do-exponential-and-logarithmic-curve-fitting-in-python-i-found-only-poly
    def logarithmic (x, a, b):
        return a + b * np.log(x)

    pars, cov = curve_fit(f=logarithmic , xdata=xs, ydata=ys, p0=[0, 0], bounds=(-np.inf, np.inf))

    return lambda x : pars[0] + pars[1] * np.log(x)

def rKwadraat(xs, ys, f):
    ''' geef de r²-waarde voor ys t.o.v. de functie toegepast op xs

    :param xs ([double]): waarden op de x-as
    :param ys ([double]): waarden op de y-as:
    :param f (functie: double -> double): functie toe te passen op xs
    :return: de r²-waarde tussen ys en f(xs). Des te dichter bij 1 des te beter
    '''
    correlaties = np.corrcoef(ys, list(map(f,xs)))
    r2 = correlaties[0, 1]
    return r2

