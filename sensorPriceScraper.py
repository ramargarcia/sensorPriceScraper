#!/usr/bin/env python
# coding: utf-8

#Importamos las librerias que vamos a usar, csv para el dataset, urrlib para la peticion a la url y bs4 para extraer las partes
#del codigo html en las que estamos interesados.

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

#Creamos el diccionario donde almacenamos el nombre del sensor, su precio y el rating con claves distintas, 
#creamos tambien una lista donde los elementos seran los direccionarios creados por cada item.
sensor_info = {}
sensor_list = []

#en nuestro caso hemos escogido una categoria en concreto en sparkfun.com
url = "https://www.sparkfun.com/categories/146"
html = urlopen(url)

soup = BeautifulSoup(html, 'lxml')
type(soup)

#Almacenamos todos los items en los que estamos interesados, es decir partes del codigo HTML que pertenece a cada sensor
item_containers = soup.find_all('div', class_ = "tile product-tile has_addl_actions grid ")
print(type(item_containers))
print(len(item_containers))

#Y recorremos cada item (sensor) que hemos almacenado para coger los datos individuales
for container in item_containers:
    name = container.span.text
    
    sensor_price = container.find('span', class_ = "price")
    sensor_price = sensor_price.text
    
#Algunos productos no estan evaluados y da error al intentar capturar ese dato, por lo tanto introducimos un mecanismo de excepcion.
    try:
      sensor_rating = container.find('span',attrs= {'class' : "product-rating"})["title"]
  
    except:
      sensor_rating = "Not evaluated"
 #almacenamos la informacion de cada sensor en un diccionario que a guardaremos a su vez en una lista que contendra todos los diccionarios
 #uno por elemento
    sensor_info = {'name' : name, 'sensor_price' : sensor_price, 'sensor_rating' : sensor_rating}
    sensor_list.append(dict(sensor_info))


keys = sensor_list[0].keys()


#finalmente guardaremos la lista y sus diccionarios en un csv, especificamos las cabeceras que deseamos
with open('sensorPriceScraper.csv','w') as f:
    w = csv.writer(f)
    fieldnames = ['Sensor name', 'Sensor price', 'Rating']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    
    writer.writeheader()
    writer = csv.DictWriter(f, keys)
    writer.writerows(sensor_list)
        

      
    








