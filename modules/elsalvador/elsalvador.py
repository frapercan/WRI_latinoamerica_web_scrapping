from requests import get
from bs4 import BeautifulSoup
import pickle
import os
from scrapper import Scrapper
import pandas as pd
import datetime



class ElSalvadorAsambleaLegislativa(Scrapper):
    def __init__(self):
        super().__init__()
        self.source = "Asamblea Legislativa"
        self.country_code = '70'
        self.ISO = 'SLV'
        self.URLs = ["https://www.asamblea.gob.sv/decretos/decretosporanio/{}/0".format(year) for year in range(2020,2015 , -1)]
        self.REF_URL = "https://www.asamblea.gob.sv"
        self.path = os.path.dirname(__file__)
        self.law_refs = []

    def extract_information(self):
        for url in self.URLs:
            print("Extracting references from: {}".format(url))
            publications_page = get(url).content
            soup = BeautifulSoup(publications_page, features="html.parser")
            anchors = soup.find_all("a",)
            for anchor in anchors:
                data_url = anchor.get('data-load-url')
                if data_url != None:
                    self.law_refs.append(data_url.split(" ")[0])
            print("Extracting references from: {} finished".format(url))
            
        for law_ref in self.law_refs:
            print(self.REF_URL + law_ref)
            law_page = get(self.REF_URL + law_ref).content
            soup = BeautifulSoup(law_page, features="html.parser")
            try:
                title = soup.find("h1", class_="js-quickedit-page-title page-title").text
            except Exception as e:
                print("{} title isn't avaliable".format(law_ref))
                continue

            try:
                panel = soup.find("div", class_="panel panel-info")
                if panel.find("td"):
                    date = panel.find("td").text
                    date = datetime.datetime.strptime(date.strip(),"%d/%m/%Y")
                    print(date)
            except Exception as e:
                print("{} date isn't avaliable".format(law_ref))
                continue
            try:
                resume = soup.find("small").text
            except Exception as e:
                print("{} resume isn't avaliable".format(law_ref))
            try:
                url =  soup.find('a', class_ ="btn btn-info center-block")['href']


            except Exception as e:
                print("{} link for download isn't avaliable".format(law_ref))
                continue
            url = self.REF_URL + url
            doc_format = url.split('.')[-1]
            if self.url_regcheck(url):
                print(True)
                if doc_format in ['pdf','doc']:
                    sample = pd.DataFrame([[self.ISO, self.country_code, self.state_code, self.state_ISO, self.source, title, resume, date, url, doc_format]], columns = self.columns)
                    self.resources = pd.concat([self.resources,sample], ignore_index=True)
                else:
                    print(url,doc_format)
            else:
                print(False)
                print(url,doc_format)
        self.save_resources()




