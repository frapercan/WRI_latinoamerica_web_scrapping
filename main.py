from modules.mexico.mexico import MexicoCamaraDiputados
from modules.elsalvador.elsalvador import ElSalvadorAsambleaLegislativa
from scrapper import Scrapper

threads = 5
driver_path = '/usr/lib/chromium-browser/chromedriver'

if __name__ == '__main__':
    #scrapper = MexicoCamaraDiputados()
    #scrapper.load_resources()
    #scrapper.extract_information()
    #scrapper = ElSalvadorAsambleaLegislativa()
    #scrapper.load_resources()
    #scrapper.extract_information()
    #scrapper.save_to_csv('muestra.csv')
    scrapper = Scrapper()
    scrapper.load_resources()
    scrapper.download_documents(threads=5)
