import urllib.request
from multiprocessing.pool import ThreadPool
from tqdm import tqdm
import pickle
import os
import pandas as pd
import re


class Scrapper:
    def __init__(self, driver_path='/usr/lib/chromium-browser/chromedriver'):
        self.country_code = None
        self.ISO = None
        self.state_code = None
        self.state_ISO = None
        self.state_name = None
        self.columns = ['ISO', 'COUNTRY_CODE', 'STATE_CODE', 'STATE_ISO', 'SOURCE', 'TITLE', 'RESUME',
                        'PUBLICATION_DATE', 'URL',
                        'DOC_TYPE']
        self.resources = pd.DataFrame(
            columns=self.columns)
        self.path = None
        self.driver_path = driver_path

    def load_resources(self):
        try:
            self.resources = pickle.load(open("resources.p", "rb"))
        except Exception as e:
            print(e)

    def save_resources(self):
        pickle.dump(self.resources, open("resources.p", "wb"))
        print("Resources correctly saved")

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
        print("References loaded: {}".format(len(self.resources.keys())))
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
