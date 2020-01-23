import requests
from bs4 import BeautifulSoup

URL = 'http://base-donnees-publique.medicaments.gouv.fr/index.php'
data = {'page': 1,
        'affliste': 0,
        'affNumero': 0,
        'isAlphabet': 0,
        'inClauseSubst': 0,
        'nomSubstances': '',
        'typeRecherche': 2,
        'choixRecherche': 'pathologie',
        'paginationUsed': 0,
        'txtCaracteres': '',
        'radLibelle': 2,
        'txtCaracteresSub': '',
        'radLibelleSub': 4,
        'txtCaracteresPath': 'Acné'.encode('iso-8859-1'),
        'btnPatho.x': 14,
        'btnPatho.y': 15,
        'radLibellePath': 6
        }
result = []


def parse_medecine(html_page, patho):
    medsresult = html_page.findAll(attrs={'class': 'ResultRowDeno'})
    for med in medsresult:
        medname = med.find('a')
        result.append([medname.contents[0].split(',')[0], patho])


def main():
    f = open('outputFile.txt', 'r')
    x = f.readlines()
    pathologies = [y.replace('\n', '') for y in x]
    pathologies = list(filter(None, pathologies))
    for patho in pathologies:
        data = {'page': 1,
                'affliste': 0,
                'affNumero': 0,
                'isAlphabet': 0,
                'inClauseSubst': 0,
                'nomSubstances': '',
                'typeRecherche': 2,
                'choixRecherche': 'pathologie',
                'paginationUsed': 0,
                'txtCaracteres': '',
                'radLibelle': 2,
                'txtCaracteresSub': '',
                'radLibelleSub': 4,
                'txtCaracteresPath': patho.encode('iso-8859-1'),
                'btnPatho.x': 14,
                'btnPatho.y': 15,
                'radLibellePath': 6
                }
        r = requests.post(URL, data=data)
        html = r.content  # the HTML code you've written above
        parsed_html = BeautifulSoup(html, features='html.parser')
        parse_medecine(parsed_html, patho)
        numberofpage = str(parsed_html.find(attrs={'class': 'navBarGauche'})).rstrip('</div>')
        if (numberofpage == 'None'):
            try:
                error = parsed_html.find(attrs={'class': 'messageRechercheSub'})
                if (error.find("span").contents[0]):
                    values = parsed_html.findAll(attrs={'name': 'lstSubstances[]'})
                    for val in values:
                        if (str(val.get('value').split('|')[1]) == patho):
                            data['lstSubstances[]'] = val.get('value')
                            data['affliste'] = 1
                            r = requests.post(URL, data=data)
                            html = r.content  # the HTML code you've written above
                            parsed_html = BeautifulSoup(html, features='html.parser')
                            parse_medecine(parsed_html, patho)
                            numberofpage = str(parsed_html.find(attrs={'class': 'navBarGauche'})).rstrip('</div>')
                        else:
                            pass
            except:
                numberofpage = "0/0"
        for i in range(int(numberofpage.split('/')[1])):
            data['page'] = i
            r = requests.post(URL, data=data)
            html = r.content  # the HTML code you've written above
            parsed_html = BeautifulSoup(html, features='html.parser')
            parse_medecine(parsed_html, patho)
    f.close()
    return result

main()
