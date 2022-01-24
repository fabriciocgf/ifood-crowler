from selenium import webdriver
from bs4 import BeautifulSoup
import json
import pandas as pd
from tqdm import tqdm

options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--window-size=1920,1080")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

def getNamePhone(site, ch):
    ch.get(site)
    time.sleep(1)
    source = wd.page_source
    soup = BeautifulSoup(source, 'html.parser')

    script = soup.find_all('script', {"type": "application/ld+json"})  # find the "Place" that we want to dive in
    script_BM = soup.find_all('script', {"id": "__NEXT_DATA__"})  # find the "Place" that we want to dive in

    for idx in script:
        jsondata = idx.contents[0]

    newDictionary = json.loads(str(jsondata))
    try:
        if newDictionary["name"] != "iFood":
            try:
                telefone = newDictionary["telephone"]  # getting the telephone and so on..
            except KeyError as error:
                telefone = "-"

            try:
                nome = newDictionary['name']
            except KeyError as error:
                nome = "-"

            try:
                tipo = newDictionary["servesCuisine"]
            except KeyError as error:
                tipo = "-"

            try:
                nomerua = newDictionary['address']['streetAddress']
            except KeyError as error:
                nomerua = "-"

            try:
                bairro = newDictionary['address']['addressLocality']
            except KeyError as error:
                bairro = "-"

            try:
                CEP = newDictionary['address']['postalCode']
            except KeyError as error:
                CEP = "-"

            try:
                Latitude = newDictionary['geo']['latitude']
            except KeyError as error:
                Latitude = "-"

            try:
                Longitude = newDictionary['geo']['longitude']
            except KeyError as error:
                Longitude = "-"

            try:
                hora = newDictionary['openingHoursSpecification']
                segunda = []
                terca = []
                quarta = []
                quinta = []
                sexta = []
                sabado = []
                domingo = []
            except KeyError as error:
                hora = "-"

            for i in hora:
                if i['dayOfWeek'] == 'http://schema.org/Monday':
                    segunda = i['opens'] + '|' + i[
                        'closes']  # here we need to make a for function because we have a matrix in the web site
            for i in hora:
                if i['dayOfWeek'] == 'http://schema.org/Tuesday':
                    terca = i['opens'] + '|' + i['closes']
            for i in hora:
                if i['dayOfWeek'] == 'http://schema.org/Wednesday':
                    quarta = i['opens'] + '|' + i['closes']
            for i in hora:
                if i['dayOfWeek'] == 'http://schema.org/Thursday':
                    quinta = i['opens'] + '|' + i['closes']
            for i in hora:
                if i['dayOfWeek'] == 'http://schema.org/Friday':
                    sexta = i['opens'] + '|' + i['closes']
            for i in hora:
                if i['dayOfWeek'] == 'http://schema.org/Saturday':
                    sabado = i['opens'] + '|' + i['closes']
            for i in hora:
                if i['dayOfWeek'] == 'http://schema.org/Sunday':
                    domingo = i['opens'] + '|' + i['closes']

            for idx in script_BM:
                jsondata = idx.contents[0]

            newDictionary_BM = json.loads(
                str(jsondata))  # here is the same thing as before, but the info is allocated in a different part os the web site
            try:
                KA = newDictionary_BM['props']['initialState']['restaurant']['details']['tags']
            except KeyError as error:
                KA = "-"
            categoria = []
            if "KEY_ACCOUNT" in KA:
                categoria = "Key Account"
            elif "CONTA_ESTRATEGICA" in KA:
                categoria = "City Key Account"
            else:
                categoria = "Normal"

            if "SO_TEM_NO_IFOOD" in KA:
                contrato = "Exclusivo"
            else:
                contrato = "Não Exclusivo"

            try:
                data = newDictionary_BM['props']['initialState']['restaurant']['details']['groups']
            except KeyError as error:
                data = "-"
            bm = []
            for i in data:
                if i['type'] == 'BUSINESS_MODEL':
                    bm = i['name']
            try:
                sr = newDictionary_BM['props']['initialState']['restaurant']['details']['superRestaurant']
            except KeyError as error:
                sr = "-"

            try:
                numrating = newDictionary_BM['props']['initialState']['restaurant']['details']['userRatingCount']
            except KeyError as error:
                numrating = "-"

            try:
                rating = newDictionary_BM['props']['initialState']['restaurant']['details']['evaluationAverage']
            except KeyError as error:
                rating = "-"


        else:
            nome = "Link inválido"
            telefone = ""
            tipo = ""
            nomerua = ""
            bairro = ""
            CEP = ""
            Latitude = ""
            Longitude = ""
            hora = ""
            bm = ""
            categoria = ""
            contrato = ""
            segunda = ""
            terca = ""
            quarta = ""
            quinta = ""
            sexta = ""
            sabado = ""
            domingo = ""
            sr = ""
            rating = ""
            numrating = ""
    except KeyError as error:
        nome = "Link inválido"
        telefone = ""
        tipo = ""
        nomerua = ""
        bairro = ""
        CEP = ""
        Latitude = ""
        Longitude = ""
        hora = ""
        bm = ""
        categoria = ""
        contrato = ""
        segunda = ""
        terca = ""
        quarta = ""
        quinta = ""
        sexta = ""
        sabado = ""
        domingo = ""
        sr = ""
        rating = ""
        numrating = ""

    return nome, telefone, tipo, nomerua, bairro, CEP, Latitude, Longitude, bm, categoria, contrato, sr, rating, numrating, segunda, terca, quarta, quinta, sexta, sabado, domingo

df = pd.read_excel('links_ssa.xlsx', index_col=None, header=None) #reading the excel file with the links

lista = []

total = len(df.index)

wd = webdriver.Chrome(options=options) # abrir navegador

for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    lista.append(list(getNamePhone(row[0], wd)))
    lista[index].append(str(row[0]))

wd.close() # Fechar navegador

df = pd.DataFrame(lista, columns=['Nome', 'Tel', 'tipo', 'Endereço', 'Bairro', 'CEP', 'Lat', 'Long', 'Business Model',
                                  'Categoria', 'Contrato', 'SuperRs', 'rating', 'numrating', 'Segunda', 'Terça',
                                  'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo', 'Link'])
# creating the excel file with all the things that we returned
df.sort_values('Nome', inplace=True)

df.to_excel("Telefones_ssar_ifood.xlsx", index=False) #creating the excel file with all the things that we returned
