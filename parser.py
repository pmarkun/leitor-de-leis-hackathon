import urllib2
from lxml.etree import fromstring, parse
import os, codecs
from itertools import chain
import json, urllib2, html2text
from lxml import html

BASE = 'http://www2.camara.leg.br/'
def urlopen(url):
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    xml = urllib2.urlopen(req)
    return xml

def lerLei(leipath):
    with codecs.open(leipath, 'r', encoding='iso-8859-1') as leixml:
        lei = {}  
        leixml = leixml.read()
        try:
            soup = fromstring(leixml.encode('iso-8859-1'))
            lei['path'] = leipath.split('.')[0]
            lei['description'] = soup.xpath('//primeiraementa')[0].text
            lei['title'] = soup.xpath('//titulo')[0].text
            lei['tipo'] = soup.xpath('//tiponorma')[0].text
            lei['numero'] = soup.xpath('//numeronorma')[0].text
            lei['ano'] = soup.xpath('//anonorma')[0].text
            lei['url'] = BASE +soup.xpath('//url')[0].text
            lei['date'] = soup.xpath('//dataassinatura')[0].text
        except:
            print 'Porra encoding'
        return lei

def getLei(l):
    arquivo = 'public/data/'+l['tipo']+'-'+l['numero']+'-'+l['ano']+'.json'
    if not os.path.isfile(arquivo):
        print "Getting text from " + l['title']
        soup = urlopen(l['url'])
        soup = html.parse(soup).getroot()
        new_url = soup.xpath('//a[contains(@href, "publicacaooriginal")]')[0].get("href")
        l['url'] = '/'.join(l['url'].split('/')[:-1])+'/'+new_url
        soup = html.parse(urlopen(l['url'])).getroot()
        l['raw'] = html.tostring(soup.xpath('//div[@class="textoNorma"]/div[@class="texto"]')[0])
        l['text'] = html2text.html2text(l['raw'])
        jason = open(arquivo, 'w')
        jason.write(json.dumps(l, indent=4))
        jason.close()

def fairy_wear_boots():
    return [lerLei(lei) for lei in chain(*[[root+'/'+xml for xml in files] for root,sub,files in os.walk('legislacao')])]


for fairy in fairy_wear_boots():
    if fairy.has_key('path') and '/lei/' in fairy['path']:
        getLei(fairy)