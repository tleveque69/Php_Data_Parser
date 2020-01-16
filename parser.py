import requests
from bs4 import BeautifulSoup

URL = "http://base-donnees-publique.medicaments.gouv.fr/index.php"
data = {"page": 1,
        "affliste": 0,
        "affNumero": 0,
        "isAlphabet": 0,
        "inClauseSubst": 0,
        "nomSubstances": '',
        "typeRecherche": 0,
        "choixRecherche": 'pathologie',
        "paginationUsed": 0,
        "txtCaracteres": '',
        "radLibelle": 2,
        "txtCaracteresSub": '',
        "radLibelleSub": 4,
        "txtCaracteresPath": 'Mal des transports',
        "btnPatho.x": 14,
        "btnPatho.y": 15,
        "radLibellePath": 6}

f = open('outputFile.txt', 'r')
x = f.readlines()
pathologies = [y.replace('\n', '') for y in x]
r = requests.get(URL, data)
html = r.content  # the HTML code you've written above
print(html)
parsed_html = BeautifulSoup(html, features="html.parser")
#Not find this class attribute print(parsed_html.find(attrs={"class": "navBarGauche"}))
f.close()
