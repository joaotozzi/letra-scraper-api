import requests
import urllib
from bs4 import BeautifulSoup
from requests_html import HTML
from requests_html import HTMLSession
import re



def get_source(url):
  try:
    session = HTMLSession()
    response = session.get(url)
    return response
  
  except requests.exceptions.RequestException as e:
    print(e)


def scrape_google(query):
  query = urllib.parse.quote_plus(query)
  response = get_source("https://www.google.com.br/search?q=" + query)
  links = list(response.html.absolute_links)

  links_letras = []

  for url in links:
    if url.startswith('https://www.letras.mus.br/') and "/membros/" not in url:
      links_letras.append(url)

  return links_letras


def scrape_letras(urls, titulo_pesquisado):
  for url in urls:
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    titulo = soup.find('h1').get_text()
    artista = soup.find_all('span', itemprop="name")[2].get_text()
    paragrafos = soup.find_all('p')
    
    texto_formatado = []

    if re.search(titulo_pesquisado, titulo, re.IGNORECASE):
      for p in paragrafos:
        texto_formatado.append(p.get_text("|").split('|'))

      return {'titulo' : titulo, 'artista' : artista, 'linhas' : texto_formatado[:-3]}



def scrape(titulo, artista):
  query = "inurl:letras.mus.br " + titulo

  if artista:
    query = query + " " + artista

  urls = scrape_google(query)
  return scrape_letras(urls, titulo)