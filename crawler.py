from bs4 import BeautifulSoup
import requests
import sys
import urllib2
import re
import ConfigParser
import os

url = 'http://www.bahianoticias.com.br/saude/artigos.html'
def buscar(url):
    lista = []
    urlocal = 'http://www.bahianoticias.com.br'

    contador = ConfigParser.ConfigParser()
    contador.read(['contador.ini'])
    i = contador.getint('DEFAULT','contador')

    path = os.path.dirname(__file__)
    print(path)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    for a in soup.findAll('a', {'class': 'btn-default'}):
        link = a['href']
        html = urllib2.urlopen(urlocal + link).read()
        i+=1
        soup = BeautifulSoup(html)
        for p in soup.findAll('div', {'class':'text-descricao'}):
            regex = re.compile(r'<[^<]*?>')
            descricao = regex.sub('', str(p))

            arquivo = open('arquivos/artigo'+str(i)+'.txt','w')
            arquivo.write(descricao)
            arquivo.close
            print '============================'
            print '\n' + descricao

    contador.set('DEFAULT','contador', i)
    with open('contador.ini','w') as config:
        contador.write(config)

    print "\n>> Total = %d \n " % i
    sys.exit()

for arg in sys.argv:
    if arg == "-l":
        buscar(url)
