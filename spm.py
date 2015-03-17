#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:37:22 2015

requeriments click and python-virtualenv

@author: GERCOM
"""
import re
import click
import json
import urllib.request


FILE_CONF = "./spm.json"
FILE_METASDNLIST = 'metasdn.list'
CONTROLLERS = ['nox','pox','floodlight']
from pprint import pprint
json_data=open(FILE_CONF)

data = json.load(json_data)
#pprint(data)
json_data.close()

def install_app(path,ctr_type,app):
    if ctr_type == "nox":
        pass
    elif ctr_type == "pox":
        pass
    elif ctr_type == "floodlight":
        pass
    


@click.group()
def cli():
   pass

@cli.command()
@click.argument("controller")
@click.argument("application")
def install(controller,application):        
    
    "downloading app"
    urllib.request.urlretrieve(data['repository']+'/'+data['controller'][controller]['type']+'/'+application+'.zip', data['cache']+application+'.zip')
    
        
    print (data['controller'][controller])
    print(controller)
    click.echo('Initialized the database')

@cli.command()
@click.argument("controller")
@click.argument("application")
def remove():
    click.echo('Dropped the database')

@cli.command()
def update():
    click.echo('Dropped the database')

@cli.command()
def download():
    lista = {}
    for c in CONTROLLERS:
        url = data['repository']
        webFile = urllib.request.urlopen(url+'/'+ c)
        html = webFile.read()
        m = re.findall(r'href=[\'"]?([^\'" >]+)', str(html))
        lista[c] = m[1:]
        
    with open(FILE_METASDNLIST, 'w') as f:
        json.dump(lista, f, ensure_ascii=False)    
  
    click.echo('downloading...')


@cli.command()
def list():
    json_data=json.load(open(FILE_METASDNLIST))
      
    for k,v in json_data.items():
        print("Controller: " + k)
        print("Applications: "+ str(v))
     
    


if __name__ == '__main__':
    cli()        
        