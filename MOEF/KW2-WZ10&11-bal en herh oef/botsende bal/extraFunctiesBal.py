#####################
# versie 12/10/2025 #
#####################

from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot
def plotTweeKolommen(data, kolomLinksY, kolomRechtsY, marker = None):
    """ maak een figuur met één plot met twee verschillende assen

    :param data (DataFrame): het dataframe waar de gegevens uit komen
    :param kolomLinksY (string): de naam van de kolom die op de linkse y-as moet komen
    :param kolomRechtsY (string): de naam van de kolom die op de rechtse y-as moet komen
    :param marker (string, optional): type marker voor de datapunten
    """

    xAs = data['Tijd (s)']
    yAsLinks = data[kolomLinksY]
    yAsRechts = data[kolomRechtsY]

    as1 = host_subplot(111)

    kleur = 'tab:red'
    as1.set_xlabel('Tijd (s)')
    as1.set_ylabel(kolomLinksY, color=kleur)
    as1.plot(xAs, yAsLinks, color=kleur , marker = marker)
    as1.tick_params(axis='y', labelcolor=kleur)

    kleur = 'tab:blue'
    as2 = as1.twinx()
    as2.set_xlabel('Tijd (s)')
    as2.set_ylabel(kolomRechtsY, color=kleur)
    as2.plot(xAs, yAsRechts, color=kleur, marker = marker)
    as2.tick_params(axis='y', labelcolor=kleur)


    as1.grid(True)
    plt.show()
