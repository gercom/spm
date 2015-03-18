#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 15:37:22 2015

requeriments click and python-virtualenv

@author: GERCOM
"""
import re,os
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

def install_app(path,controller,app):
    ctr_type = data['controller'][controller]['type']
    os.system("mkdir /tmp/"+app)
    os.system("rm -rf  /tmp/"+app+"/*")
    print(data['cache']+app+'.zip') 
    os.system("unzip "+data['cache']+app+".zip -d /tmp/"+app+"/")    
    if ctr_type == "nox":
        pass
    elif ctr_type == "pox":
        os.system("cp /tmp/"+app+"/*.py "+data['controller'][controller]['path']+"ext/")
    elif ctr_type == "floodlight":
        pass
    


@click.group()
def cli():
   pass

####
@cli.command()
@click.argument("controller")
@click.argument("application")
def install(controller,application):        
    
    print(data['repository']+'/'+data['controller'][controller]['type']+'/'+application+'.zip', data['cache']+application+'.zip')
    urllib.request.urlretrieve(data['repository']+'/'+data['controller'][controller]['type']+'/'+application+'.zip', data['cache']+application+'.zip')
    
    install_app(data['controller'][controller]['path'],controller,application)    

    click.echo('Instalação Completa!!!')

####
@cli.command()
@click.argument("controller")
@click.argument("application")
def remove(controller,application):
    click.echo('Dropped the database')

####
@cli.command()
@click.argument("controller")
@click.argument("application")
def update(controller,application):
    install(controller,application)

####
@cli.command()
def download():
    "Download lista pacotes"
    lista = {}
    for c in CONTROLLERS:
        url = data['repository']
        webFile = urllib.request.urlopen(url+'/'+ c)
        html = str(webFile.read()).replace('.zip','') 
        m = re.findall(r'href=[\'"]?([^\'" >]+)', str(html))
        lista[c] = m[1:]
        
    with open(FILE_METASDNLIST, 'w') as f:
        json.dump(lista, f, ensure_ascii=False)    
  
    click.echo('downloading...')

####
@cli.command()
def list():
    json_data=json.load(open(FILE_METASDNLIST))
      
    for k,v in json_data.items():
        print("Controller: " + k)
        print("Applications: "+ str(v))
     
    

if __name__ == '__main__':
    cli()        
        
