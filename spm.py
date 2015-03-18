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
import fileinput

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
    os.system("unzip "+data['cache']+app+".zip -d /tmp/"+app+"/")    
    if ctr_type == "nox":
        pass
    elif ctr_type == "pox":
        os.system("cp /tmp/"+app+"/*.py "+data['controller'][controller]['path']+"ext/")
    elif ctr_type == "floodlight":
        work_dir = data['controller'][controller]['path']                 
        fp = work_dir+"src/main/resources/floodlightdefault.properties"
        app_name = app.split("-")[0]        
        new_module = "."+app_name.lower()+"."+app_name.capitalize()
        
        ##copy module
        os.system("mkdir "+work_dir+"src/main/java/net/floodlightcontroller/"+app_name)
        os.system("cp /tmp/"+app+"/*.java "+work_dir+"src/main/java/net/floodlightcontroller/"+app_name+"/")
        
        #add module            
        new_line = "net.floodlightcontroller"+ new_module + ",\\"

        for line in fileinput.input(fp, inplace=True):
            print(line.replace("net.floodlightcontroller.core.internal.FloodlightProvider,\\", "net.floodlightcontroller.core.internal.FloodlightProvider,\\\n"+new_line), end='')
        
        
        os.system("echo '\nnet.floodlightcontroller"+new_module+ "' >> " + work_dir+"src/main/resources/META-INF/services/net.floodlightcontroller.core.module.IFloodlightModule")
        #src/main/resources/floodlightdefault.properties
                

    


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
        
