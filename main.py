from modules.mexico.mexico import MexicoCamaraDiputados
from modules.elsalvador.elsalvador import ElSalvadorAsambleaLegislativa
from scrapper import Scrapper
from modules.peru.peru import PeruCongreso
from selenium_client import SeleniumClient







threads = 5

if __name__ == '__main__':
    selenium_client = SeleniumClient()


    scrapper = MexicoCamaraDiputados()
    scrapper.load_resources()
    scrapper.extract_information()

    scrapper = ElSalvadorAsambleaLegislativa()
    scrapper.load_resources()
    scrapper.extract_information()

    selenium_client.start()
    scrapper = PeruCongreso(selenium_client.browser)
    scrapper.load_resources()
    scrapper.extract_information()
    selenium_client.stop()


    scrapper.save_to_csv('muestra.csv')

    scrapper = Scrapper()
    scrapper.load_resources()
    scrapper.download_documents(threads=5)
