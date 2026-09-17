import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

#####################
# versie 17.09.2026 #
#     snake_case    #
#####################

def selecteer_aantal_xas(df, aantal_xas):
    """ SELECTEER de eerste 'aantal_xas' waarden van het dataframe

    :param df (DataFrame): het dataframe waaruit geselecteerd moet worden
    :param aantal_xas (int): het aantal waarden op de x-as dat behouden moet blijven
    :return (DataFrame): een deelverzameling vooraan uit het dataframe

    """
    knip = df[0:aantal_xas]
    return knip

selecteerAantalXas = selecteer_aantal_xas

def knip_aantal_xas(df, aantal_xas):
    """ KNIP de eerste 'aantal_xas' waarden WEG uit het dataframe

    :param df (DataFrame): df het dataframe waaruit geknipt moet worden
    :param aantal_xas (int): het aantal waarden op de x-as dat verwijderd moet worden
    :return (DataFrame): een deelverzameling achteraan uit het dataframe met indexes vanaf 0, 1, 2, ...
    """
    knip = df[aantal_xas:]
    return knip.reset_index().drop("index", axis=1)

knipAantalXas = knip_aantal_xas

def selecteer_aantal_yas(df, kolom, aantal_yas):
    """ SELECTEER de eerste VERSCHILLENDE 'aantal_yas' waarden van het dataframe

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom op de y-as
    :param aantal_yas (int): het aantal waarden op de y-as dat behouden moet blijven
    :return (DataFrame): een deelverzameling vooraan uit het dataframe
    """
    ys = []
    index = 0
    while index < len(df) and len(ys) < aantal_yas:
        waarde = df.iloc[index][kolom]
        if not waarde in ys:
            ys.append(waarde)
        index = index + 1

    knip = df[0:index]
    return knip
selecteerAantalYas = selecteer_aantal_yas

def knip_aantal_yas(df, kolom, aantal_yas):
    """ knip de eerste VERSCHILLENDE 'aantal_yas' waarden WEG uit het dataframe

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom op de y-as
    :param aantal_yas (int): het aantal waarden op de y-as dat verwijderd moet worden
    :return (DataFrame): een deelverzameling achteraan uit het dataframe met indexes vanaf 0, 1, 2, ...
    """
    y_as = []
    index = 0
    while index < len(df) and len(y_as) < aantal_yas:
        waarde = df.iloc[index][kolom]
        if not waarde in y_as:
            y_as.append(waarde)
        index = index + 1

    knip = df[index:]
    return knip.reset_index().drop("index", axis=1)
knipAantalYas = knip_aantal_yas

def selecteer_tot_waarde(df, kolom, waarde, stijgende_flank = True):
    """ SELECTEER de rijen uit het dataframe tot de opgeven waarde voor de opgegeven kolom

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :param waarde (double): de grens voor de waarde in de opgegeven kolom
    :param stijgende_flank (boolean): indien true zit de functie op een stijgende flank
                                     en is 'waarde' een bovengrens; anders een ondergrens
    :return (DataFrame): een deelverzameling vooraan uit het dataframe
    """
    df = df.reset_index().drop("index", axis=1)
    if stijgende_flank:
       te_ver = df[df[kolom] >= waarde]
    else:
       te_ver = df[df[kolom] <= waarde]

    if len(te_ver) == 0:
        return df

    index = te_ver.index[0]
    knip = df[0:index]

    return knip.reset_index().drop("index", axis=1)
selecteer_tot_waarde = selecteer_tot_waarde

def knip_tot_waarde(df, kolom, waarde, stijgende_flank = True):
    """ KNIP de rijen uit het dataframe WEG tot de opgeven waarde voor de opgegeven kolom

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :param waarde (double): de grens voor de waarde in de opgegeven kolom
    :param stijgende_flank (boolean): indien true zit de functie op een stijgende flank
                                     en is 'waarde' een bovengrens; anders een ondergrens
    :return (DataFrame): een deelverzameling achteraan uit het dataframe met indexes vanaf 0, 1, 2, ...
    """
    df = df.reset_index().drop("index", axis=1)
    if stijgende_flank:
       te_ver = df[df[kolom] >= waarde]
    else:
       te_ver = df[df[kolom] <= waarde]
    if len(te_ver) == 0:
        return pd.DataFrame()

    index = te_ver.index[0]
    knip = df[index:]

    return knip.reset_index().drop("index", axis=1)
knip_tot_waarde = knip_tot_waarde

def selecteer_tot_percentage(df, kolom, percent, stijgende_flank = True):
    """ SELECTEER de rijen uit het dataframe tot het opgegeven percentage voor de opgegeven kolom

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :param percent (double): grens voor de waarde in de opgegeven kolom,
                             percent (van 0 tot 1) van het verschil tussen het minimum
                             en het maximum van de waardes in de opgegeven kolom
    :param stijgende_flank (boolean): indien true zit de functie op een stijgende flank
                                     en is 'waarde' een bovengrens; anders een ondergrens
    :return (DataFrame): een deelverzameling vooraan uit het dataframe
    """
    maximum = df[kolom].max()
    minimum = df[kolom].min()
    waarde = (maximum - minimum)*percent + minimum
    return selecteer_tot_waarde(df, kolom, waarde, stijgende_flank)
selecteerTotPercentage = selecteer_tot_percentage

def knip_tot_percentage(df, kolom, percent, stijgende_flank = True):
    """KNIP de rijen uit het dataframe WEG tot het opgegeven percentage voor de opgegeven kolom

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :param percent (double): grens voor de waarde in de opgegeven kolom,
                             percent (van 0 tot 1) van het verschil tussen het minimum
                             en het maximum van de waardes in de opgegeven kolom
    :param stijgende_flank (boolean): indien true zit de functie op een stijgende flank
                                     en is 'waarde' een bovengrens; anders een ondergrens
    :return (DataFrame): een deelverzameling achteraan uit het dataframe met indexes vanaf 0, 1, 2, ...
    """
    maximum = df[kolom].max()
    minimum = df[kolom].min()
    waarde = (maximum - minimum)*percent + minimum
    return knip_tot_waarde(df, kolom, waarde, stijgende_flank)
knipTotPercentage = knip_tot_percentage

# hulpfunctie voor zoektocht naar LokaalExtremum
def is_lokaal_extremum(y1, y2, stijgende_flank):
    return (y1 > y2 and stijgende_flank) or (y2 > y1 and not stijgende_flank)

def zoek_index_lokaal_extremum(df, kolom):
    """ bereken de index van het eerste LokaalExtremum

    :param df (DataFrame): het dataframe waarin gezocht wordt
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :return: de index van het eerste LokaalExtremum of len(df) als er geen LokaalExtremum is
    """
    if len(df) < 2:
        return len(df)

    if df.loc[0,kolom] <= df.loc[1,kolom]:
        stijgende_flank = True
    else:
        stijgende_flank = False

    index = 2
    while index < len(df) and not is_lokaal_extremum(df.loc[index - 1,kolom], df.loc[index,kolom], stijgende_flank):
        index = index + 1
    return index
zoekIndexLokaalExtremum = zoek_index_lokaal_extremum

def selecteer_tot_lokaal_extremum(df, kolom):
    """ SELECTEER de rijen uit het dataframe tot en met het eerstvolgende LokaalExtremum

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :return (DataFrame): een deelverzameling uit het dataframe tot en met het LokaalExtremum. Het volledige df als er geen LokaalExtremum was
    """
    index = zoek_index_lokaal_extremum(df, kolom)
    return df[0:index]
selecteerTotLokaalExtremum = selecteer_tot_lokaal_extremum

def knip_tot_lokaal_extremum(df, kolom):
    """ KNIP de rijen uit het dataframe WEG tot het eerstvolgende LokaalExtremum

    :param df (DataFrame): df het dataframe waaruit geselecteerd moet worden
    :param kolom (string): de naam van de kolom die gebruikt moet worden
    :return (DataFrame): een deelverzameling uit het dataframe vanaf het LokaalExtremum en met indexes vanaf 0, 1, 2, ...
                         Een leeg dataframe indien er geen LokaalExtremum was
    """
    index = zoek_index_lokaal_extremum(df, kolom)
    if index < len(df):
       knip = df[index-1:]
    else:
       knip = df[index:]
    return knip.reset_index().drop("index", axis=1)
knipTotLokaalExtremum = knip_tot_lokaal_extremum


#################################################################
# functies om te kunnen knippen op basis van functievoorschrift #
#################################################################

def x_overschrijdt_waarde(f, waarde, begin_x, eind_x, stapgrootte, stijgende_flank = True):
    """ zoek de eerste x waarvoor f(x) de opgegeven waarde overschrijdt

    :param f (functie: double -> double): het functievoorschrift met één parameter
    :param waarde (double): de waarde die overschreden moet worden
    :param begin_x (double): begin van het interval voor x
    :param eind_x (double): einde van het interval voor x
    :param stapgrootte (double): grootte tussen 2 opeenvolgende x-waarden
    :param stijgende_flank (boolean): indien true moet f(x) > waarde, indien false met f(x) < waarde
    :return (double): index waar f(x) de waarde overschrijdt; een getal > eind_x indien dat niet gebeurt
    """
    def overschrijdt(x):
        return (stijgende_flank and f(x) > waarde) or \
               (not stijgende_flank and f(x) < waarde)

    x = begin_x

    while not (overschrijdt(x)) and x < eind_x:
        x = x + stapgrootte

    return x
xOverschrijdtWaarde = x_overschrijdt_waarde

def x_maximaal(f, begin_x, eind_x, stapgrootte):
    """ zoek de (eerste) x die de maximale f(x) geeft

    :param f (functie: double -> double): het functievoorschrift met één parameter
    :param begin_x (double): begin van het interval voor x
    :param eind_x (double): einde van het interval voor x
    :param stapgrootte (double): grootte tussen 2 opeenvolgende x-waarden
    :return (double): index waar f(x) (de eerste keer) maximaal is
    """

    x = begin_x
    grootste = f(x)

    verschil = eind_x - begin_x
    aantal_geheel = verschil // stapgrootte
    aantal_float = verschil / stapgrootte

    if aantal_float > aantal_geheel:
        aantal = int(aantal_geheel)+1
        linspace_eind = begin_x + (aantal - 1) * stapgrootte
    else:
        aantal = int(aantal_geheel) + 1
        linspace_eind = eind_x

    for i in np.linspace(begin_x, linspace_eind, aantal):
        if f(i) > grootste:
            grootste = f(i)
            x = i

    return x
xMaximaal = x_maximaal

def x_minimaal(f, begin_x, eind_x, stapgrootte):
    """ zoek de (eerste) x die de minimale f(x) geeft

    :param f (functie: double -> double): het functievoorschrift met één parameter
    :param begin_x (double): begin van het interval voor x
    :param eind_x (double): einde van het interval voor x
    :param stapgrootte (double): grootte tussen 2 opeenvolgende x-waarden
    :return (double): index waar f(x) (de eerste keer) minimaal is
    """

    x = begin_x
    kleinste = f(x)

    verschil = eind_x - begin_x
    aantal_geheel = verschil // stapgrootte
    aantal_float = verschil / stapgrootte

    if aantal_float > aantal_geheel:
        aantal = int(aantal_geheel)+1
        linspace_eind = begin_x + (aantal - 1) * stapgrootte
    else:
        aantal = int(aantal_geheel) + 1
        linspace_eind = eind_x

    for i in np.linspace(begin_x, linspace_eind, aantal):
        if f(i) < kleinste:
            kleinste = f(i)
            x = i

    return x
xMinimaal = x_minimaal

def x_lokaal_extremum(f, begin_x, eind_x, stapgrootte):
    """ zoek de (eerste) x die een LokaalExtremum voor f(x) geeft

    :param f (functie: double -> double): het functievoorschrift met één parameter
    :param begin_x (double): begin van het interval voor x
    :param eind_x (double): einde van het interval voor x
    :param stapgrootte (double): grootte tussen 2 opeenvolgende x-waarden
    :return (double): index waar f(x) een LokaalExtremum vormt; een getal > eind_x indien dat niet gebeurt
    """

    x = begin_x
    if f(x) <= f(x+stapgrootte):
        stijgende_flank = True
    else:
        stijgende_flank = False

    while x  <= eind_x and not is_lokaal_extremum(f(x), f(x + stapgrootte), stijgende_flank):
        x = x + stapgrootte

    return x
xLokaalExtremum = x_lokaal_extremum

########################
#                      #
#  ZWEVEND GEMIDDELDE  #
#                      #
########################

def zwevend_gemiddelde(xs, n):
    ''' geef het zwevend gemiddelde terug uit xs met een periode van n

    :param xs ([double]): de lijst getallen waarvan je het zwevend gemiddelde wil
    :param n (int): de periode voor het zwevend gemiddelde, bv. 7
    :return ([float]): De lijst met het zwevend gemiddelde met de opgegeven periode.
                        De lijst die terug gegeven wordt, is even lang als in de invoerlijst xs
                        voor de eerste n-1 getallen wordt het gewogen gemiddelde van het begin tot het getal gegeven
    '''
    x_filt = list()
    x_filt.append(xs[0])

    for i in range(1, n):
        x_filt.append(np.mean(xs[0:i+1]))

    for i in range(n, len(xs)):
        x_filt.append(np.mean(xs[i-n+1:i+1]))
    return x_filt
zwevend_gemiddelde = zwevend_gemiddelde

########################
#                      #
#    CURVE FITTING     #
#                      #
########################

def fit_veelterm(xs, ys, graad):
    """ genereert functie die een veelterm-curve fit is in de opgegeven graad

    :param xs ([float]): lijst met x-waarden
    :param ys ([float]): lijst met y-waarden
    :param graad (int): de gewenste graad van de veelterm
    :return (functie float -> float): veeltermfunctie die de curve fit is van xs op ys
    """
    z = np.polyfit(xs,ys, graad)
    return np.poly1d(z)
fitVeelterm = fit_veelterm

def fit_exp(xs, ys):
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
fitExp = fit_exp

def fit_log(xs, ys):
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
fitLog = fit_log

def r_kwadraat(xs, ys, f):
    ''' geef de r²-waarde voor ys t.o.v. de functie toegepast op xs

    :param xs ([double]): waarden op de x-as
    :param ys ([double]): waarden op de y-as:
    :param f (functie: double -> double): functie toe te passen op xs
    :return: de r²-waarde tussen ys en f(xs). Des te dichter bij 1 des te beter
    '''
    correlaties = np.corrcoef(ys, list(map(f,xs)))
    r2 = correlaties[0, 1]
    return r2
rKwadraat = r_kwadraat

