import urllib.request
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import pickle
import os
import pandas as pd
import re
import json


class Document:
    def __init__(self, iso, country_code, state_code, state_iso, source, official_id, concept,
                 title, resume, publication_date,
                 url, doc_type, scraping_status=None, timestamp=None):
        self.iso = iso
        self.country_code = country_code
        self.state_code = state_code
        self.state_iso = state_iso
        self.source = source
        self.official_id = official_id
        self.concept = concept
        self.title = title
        self.resume = resume
        self.publication_date = publication_date
        self.url = url
        self.doc_type = doc_type
        self.scraping_status = scraping_status
        self.timestamp = timestamp

    def to_dataframe(self):
        with open('config.json') as config_file:
            columns = json.load(config_file)['columns']
        df = pd.DataFrame(
            [[self.iso, self.country_code, self.state_code, self.state_iso, self.source, self.official_id, self.concept,
             self.title, self.resume, self.publication_date, self.url, self.doc_type, self.scraping_status,
             self.timestamp]], columns=columns)
        return df





class Scrapper:
    def __init__(self, browser=None):
        self.country_code = None
        self.ISO = None
        self.state_code = None
        self.state_ISO = None
        self.state_name = None
        with open('config.json') as config_file:
            columns = json.load(config_file)['columns']
        self.columns = columns
        self.resources = pd.DataFrame(
            columns=self.columns)
        self.browser = browser
        with open('concepts.json') as config_file:
            concepts = json.load(config_file)
        self.concepts = concepts
        self.maintainer = "Undefined"


    def load_resources(self):
        try:
            self.resources = pickle.load(open("resources.p", "rb"))
        except Exception as e:
            print(e)

    def save_resources(self):
        pickle.dump(self.resources, open("resources.p", "wb"))
        print("Resources correctly saved")

    def add_resource(self,dataframe):
        self.resources = pd.concat([self.resources, dataframe], ignore_index=True)

    def save_to_csv(self, name):
        self.resources.to_csv(name)

    def extract_information(self):
        pass

    def download_documents(self, threads):
        results = ThreadPool(threads).imap(self.download_url, self.resources.values)
        for i in results:
            pass

    def download_url(self, resource):
        resource = pd.DataFrame([resource], columns=self.columns)
        resource_dict = dict.fromkeys(['COUNTRY_CODE', 'STATE_CODE', 'FILENAME', 'DIRNAME', 'URL'])
        resource_dict['COUNTRY_CODE'] = resource['COUNTRY_CODE'][0]
        resource_dict['STATE_CODE'] = resource['STATE_CODE'][0]
        resource_dict['FILENAME'] = resource['URL'][0].split('/')[-1]
        resource_dict['DIRNAME'] = os.path.join(os.path.dirname(__file__),
                                                "codes/" + resource_dict['COUNTRY_CODE'] + "/" + resource_dict[
                                                    'FILENAME'])
        resource_dict['URL'] = resource['URL'][0]

        if not os.path.isfile(resource_dict['DIRNAME']):
            try:
                with DownloadProgressBar(unit='B', unit_scale=True,
                                         miniters=1, desc=resource_dict['FILENAME'])as t:
                    urllib.request.urlretrieve(resource_dict['URL'], filename=resource_dict['DIRNAME'],
                                               reporthook=t.update_to)
            except Exception as e:
                print(e)

    def resume(self):
        print("Country code:{}".format(self.country_code))
        print("Country name:{}".format(self.ISO))
        print("State code:{}".format(self.state_code))
        print("State name:{}".format(self.state_name))
        print("References loaded: {}".format(self.resources[['COUNTRY_CODE' == self.country_code]]))
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "codes/" + self.country_code + "")
        print("Avaliable documents: {}".format(len(os.listdir(filename))))

    def url_regcheck(self, possible_url):
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        return re.fullmatch(regex, possible_url)


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

