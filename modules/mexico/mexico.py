from requests import get
from bs4 import BeautifulSoup
import pickle
import os
from scrapper import Scrapper, Document
import pandas as pd
import re
import datetime


class MexicoCamaraDiputados(Scrapper):
    def __init__(self):
        super().__init__()
        self.source = "La Cámara de Diputados"
        self.country_code = '145'
        self.ISO = 'MEX'
        self.URLs = "http://www.diputados.gob.mx/LeyesBiblio/index.htm"
        self.REF_URL = "http://www.diputados.gob.mx/LeyesBiblio/"
        self.path = os.path.dirname(__file__)
        self.law_refs = []
        self.law_refs_exclude_list = ['ref/cpeum.htm']
        self.maintainer = "Francisco Pérez"

    def extract_information(self):
        publications_page = get(self.URLs).content
        soup = BeautifulSoup(publications_page, features="html.parser")
        anchors = soup.find_all('a')
        for anchor in anchors:
            try:
                href = anchor['href']
                title = anchor.text.strip()
            except Exception:
                continue

            if 'ref' in href:
                if href not in self.law_refs_exclude_list:
                    self.law_refs.append([href, re.sub('\s+', ' ', title)])
        print("Downloading ")
        for ref, title in self.law_refs:

            content_url = self.REF_URL + ref
            publications_page = get(content_url).content
            soup = BeautifulSoup(publications_page, features="html.parser")
            tds = soup.find_all('td')
            for td in tds:
                index_text = re.sub('\s+', ' ', td.text).strip()
                if index_text.isdigit() or index_text == "Orig":
                    try:
                        info_block = td.find_parent('tr').find_all('td')[1].find_all('p')
                    except Exception:
                        continue
                    resume = re.sub('\s+', ' ', info_block[0].text).strip()
                    try:
                        date = info_block[1].text.split("DOF")[1].strip()[:10]
                        date = datetime.datetime.strptime(date, "%d-%m-%Y")
                    except Exception:
                        continue
                    url = self.REF_URL + '/ref/' + info_block[1].find('a')['href']
                    if "_ima" not in url:
                        doc_format = url.split('.')[-1]
                        sample = Document(self.ISO, self.country_code, self.state_code, self.state_ISO, self.source,
                                          None, None, title, resume, date, url, doc_format).to_dataframe()
                        self.add_resource(sample)

        self.save_resources()
