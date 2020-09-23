from requests import get
from bs4 import BeautifulSoup
import pickle
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from scrapper import Scrapper, Document
import pandas as pd
import re
import datetime
import requests



class PeruCongreso(Scrapper):
    def __init__(self, browser):
        super().__init__()
        self.source = "CONGRESO de la REPÚBLICA del PERÚ"
        self.country_code = '178'
        self.ISO = 'PERU'
        self.URL = "http://www.leyes.congreso.gob.pe/LeyNumePP.aspx?xNorma=0"
        self.REF_URL = "http://www.diputados.gob.mx/LeyesBiblio/"
        self.path = os.path.dirname(__file__)
        self.browser = browser
        self.date = {"start": "09092019", "end": "09092020"}
        self.maintainer = "Francisco Pérez"

    def extract_information(self):
        self.browser.get(self.URL)
        element = self.browser.find_element_by_xpath("//select[@id='ctl00_ContentPlaceHolder1_DdlTipoBusqueda']")
        all_options = element.find_elements_by_tag_name("option")
        for option in all_options:
            print(option.get_attribute("text"))
            if option.get_attribute("text") == "Por fecha de publicación":
                option.click()

        element = self.browser.find_element_by_xpath("//input[@id='ctl00_ContentPlaceHolder1_TxtFechaIni']")
        element.click()
        for i in range(10):
            element.send_keys(Keys.LEFT);
        element.send_keys(self.date['start'])

        element = self.browser.find_element_by_xpath("//input[@id='ctl00_ContentPlaceHolder1_TxtFechaFin']")
        element.click()
        for i in range(10):
            element.send_keys(Keys.LEFT);
        element.send_keys(self.date['end'])

        element = self.browser.find_element_by_name("ctl00$ContentPlaceHolder1$BtnConsultar")
        element.click()
        num_pages = int(self.browser.find_element(by=By.ID,
                                                  value="ctl00_ContentPlaceHolder1_GwDetalle_ctl23_LblNroPagina").text.split(
            " ")[-1][:-1])
        print(num_pages)
        for _ in range(num_pages):
            element = self.browser.find_element_by_tag_name('table')
            table_rows = element.find_elements_by_tag_name('tr')[1:-1]

            anchors = [table_row.find_element_by_tag_name('a') for table_row in table_rows]
            normas = [table_row.find_elements_by_tag_name('td')[0].text for table_row in table_rows]
            dates = [datetime.datetime.strptime(table_row.find_elements_by_tag_name('td')[2].text, "%d/%m/%Y") for table_row in table_rows]
            resumes = [table_row.find_elements_by_tag_name('td')[3].text for table_row in table_rows]

            main_page = self.browser.current_window_handle
            for anchor,resume,norma,date in zip(anchors,resumes,normas,dates):
                try:
                    anchor.click()
                except:
                    self.browser.close()
                    self.browser.switch_to_window(main_page)
                    continue
                window_after = self.browser.window_handles[1]
                print(window_after)
                self.browser.switch_to_window(window_after)
                title = self.browser.find_element(by=By.ID, value="titulo01").text
                id = self.browser.find_element(by=By.ID, value="titulo01").text.split(' ')[-1]

                print('hola')
                try:
                    url = self.browser.find_element(by=By.ID, value="DvDetalle_LinkLey").get_attribute('href')

                except NoSuchElementException :
                    url = "http://www.leyes.congreso.gob.pe/Documentos/2016_2021/ADLP/Texto_Consolidado/{}-TXM.pdf".format(id)
                    if not requests.head(url).ok:
                        url = "http://www.leyes.congreso.gob.pe/Documentos/2016_2021/ADLP/Normas_Legales/{}-LEY.pdf".format(
                            id)
                        print(url)
                        if not requests.head(url).ok:
                            print("{} not retreived")
                            self.browser.close()
                            self.browser.switch_to_window(main_page)
                            continue




                try:
                    doc_format = url.split(".")[-1]
                except AttributeError:
                    continue
                self.browser.close()
                self.browser.switch_to_window(main_page)
                sample = Document(self.ISO, self.country_code, self.state_code, self.state_ISO, self.source,
                                  id, norma, title, resume, date, url, doc_format).to_dataframe()
                self.add_resource(sample)
            moved = False
            while not moved:
                print('moving page')
                try:
                    self.browser.find_element(by=By.ID,
                                              value="ctl00_ContentPlaceHolder1_GwDetalle_ctl23_ImgBtnSiguiente").click()
                    moved = True
                except:
                    pass
        self.save_resources()
