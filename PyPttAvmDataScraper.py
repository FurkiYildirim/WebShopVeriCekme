"""
Made by: (dc)! Kontragerilla ღ ヅ#1019 / (github) https://github.com/FurkiYildirim
"""

from requests import get
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from sys import argv


class PttAvm:
    """
    PttAvm'de veri çekme işlemleri fonskiyonlarını içerir
    """

    def __init__(self, nameOfItem):
        """
        :param nameOfItem:
        """
        self.list_of_item = []

        # PttAvm'nin ana adresi
        self.main_url = f"https://www.pttavm.com/arama?q={nameOfItem}"

    def find_all_items(self) -> None:
        """
        :return:type:str
        """
        page = 1
        itemNo = 0

        while True:
            req = get(url=self.main_url + f"&page={page}").text
            soup = BeautifulSoup(req, 'html.parser')

            # Sayfadaki bütün eşyaların bulunduğu divler
            all_items = soup.find_all("div", attrs={'class': 'product-list-box-container transition-all duration-250'})
            for i in all_items:
                fiyat = i.find("div", attrs={'class': 'price-box-price'})

                link = i.find("a", attrs={"data-v-0f698b2c": "", "data-v-b412de44": ""})

                # Eşyaların özelliklerini buluyor
                fiyat = str(fiyat).split()[-3]
                isim = str(link).split(" ")[3].split("?")[0].split("href=")[1][2::].split("-p-")[0]
                link = "https://www.pttavm.com/" + str(link).split(" ")[3].split("?")[0].split("href=")[1][2::]

                # eşyaları ekliyoru listeye

                self.list_of_item.append({itemNo: {"isim": isim, "fiyat": fiyat, "link": link}})
                itemNo += 1

            if not all_items:
                break

            else:
                page += 1

        return None

    def pretty_table_show(self):
        """
        :return:
        """
        # Bulunan verileri tabloya aktarıyor

        # Eşyaları yükleme işlemi gerçekleiyor
        self.find_all_items()

        table = PrettyTable()
        # Sütun isimleri
        columns = ["Eşya Numarası", "Eşya İsim", "Fiyatı", "Link"]
        # Tabloya aktarma işlemi
        table.field_names = columns

        item_no = 0

        # eşya listesini okuyup satırlara ekleme işlemini yapıyor
        for item in self.list_of_item:
            table.add_row([str(item_no), item[item_no]['isim'], item[item_no]['fiyat']+"TL", item[item_no]['link']])
            item_no += 1

        # Tabloyu ekrana yazdırıyor
        print(table)

        return None


def args():
    """commnads
    --item : Eşya ismi
    """
    commands = ['--item', '--help']
    argLine = argv[1::]

    # commands_with_parameter = []  # [(command, paramter)...]
    commands_with_parameterDict = {}  # {command: parameter}

    for param in argLine:
        if param in commands:
            command = commands[commands.index(param)]
            if command == "--help":
                parameter = "help"
            else:
                parameter = argLine[argLine.index(param) + 1]

            commands_with_parameterDict.update({command: parameter})

    return commands_with_parameterDict
# Yatığımız sınıfı uygulama haline getiriyoruz
def main():
    """
    :return:
    """
    try:
        if args().get('--help') == "help":
            print("""
            
            --help : Komut listesini çıkarır
            --item <eşyaIsmi> : Aracancak eşyayı PttAvm Sitesinde bulu tabloya yazar
            
            """)

        if args().get('--item') is not None:
            avm = PttAvm(args().get('--item'))
            avm.pretty_table_show()
    except KeyError:
        ...


#  Kütüphane olarak kullanılabilir
if __name__ == '__main__':
    main()
