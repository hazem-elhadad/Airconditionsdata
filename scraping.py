from alkh import alkhunaizan_scraping
from swsg import swsg_scraping
from alman import almanea_scraping
from xcite import xcite_scraping
from Mergfiles import mergingfiles
from black import blackbox_scraping
f = open("keys.txt", "r", encoding="utf8")
catagories = f.readlines()
for cat in catagories:
    if "swsg" in cat:
        swsg_scraping(cat)
    if "xcite" in cat:
        xcite_scraping(cat)
    if "almanea" in cat:
        almanea_scraping(cat)
    if "alkhunaizan" in cat:
        alkhunaizan_scraping(cat)
    if "blackbox" in cat:
        blackbox_scraping(cat)

mergingfiles()
