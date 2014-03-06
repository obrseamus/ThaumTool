#!/usr/bin/python
import pprint
import sys
import subprocess as sp
import itertools 
from clint.textui import colored


def addDepth( depth):
    for aspect, parents in aspect2parents.items():
        for neighbor in aspectDepth2neighbors[aspect][depth]:
            aspectDepth2neighbors[aspect][depth+1] |= aspectDepth2neighbors[neighbor][1]
            
#    pp = pprint.PrettyPrinter(indent=2,width=1)
#    pp.pprint(aspectDepth2neighbors)

def printStep(depth):
  totalChosen = 0
  output = '\n'
  for chosen in sorted(aspect2chosen.keys()):
    if aspect2chosen[chosen]:
      output += colored.green(chosen.ljust(17))
      totalChosen += 1
  print (output)
  for aspect in sorted(aspect2parents.keys()):
    row = ""
    found = 0
    for chosen in sorted(aspect2chosen.keys()):
      #print(aspect +":"+ chosen)
      if aspect2chosen[chosen]:
        if aspect in aspectDepth2neighbors[chosen][depth]:
          row+= ("  "+aspect).ljust(17)
          found+=1
        else:
          row+= " "*17
    if found == totalChosen:
      print(colored.red(row))
    elif found > 1:
      print(colored.yellow(row))
    elif found ==1 :
      print(row)
    
aspect2parents  = {
    'Aer' : []
    , 'Alienis' : ['Vacuos','Tenebrae']
    , 'Aqua' : []
    , 'Arbor' : ['Terra','Herba']
    , 'Auram' : ['Praecantatio','Aer']
    , 'Bestia' : ['Motus','Victus']
    , 'Cognitio' : ['Terra','Spiritus']
    , 'Corpus' : ['Mortuus','Bestia']
    , 'Exanimis' : ['Motus','Mortuus']
    , 'Fabrico' : ['Humanus','Instrumentum']
    , 'Fames' : ['Victus','Vacuos']
    , 'Gelum' : ['Aqua','Ordo']
    , 'Granum' : ['Victus','Terra']
    , 'Herba' : ['Granum','Terra']
    , 'Humanus' : ['Bestia','Cognitio']
    , 'Ignis' : []
    , 'Instrumentum' : ['Humanus','Ordo']
    , 'Iter' : ['Motus','Terra']
    , 'Limus' : ['Victus','Aqua']
    , 'Lucrum' : ['Humanus','Fames']
    , 'Lux' : ['Aer','Ignis']
    , 'Machina' : ['Motus','Instrumentum']
    , 'Messis' : ['Granum','Humanus']
    , 'Metallum' : ['Saxum','Ordo']
    , 'Meto' : ['Messis','Humanus']
    , 'Mortuus' : ['Victus','Perditio']
    , 'Motus' : ['Aer','Ordo']
    , 'Ordo' : []
    , 'Pannus' : ['Instrumentum','Bestia']
    , 'Perditio' : []
    , 'Perfodio' : ['Humanus','Saxum']
    , 'Permutatio' : ['Motus','Aqua']
    , 'Potentia' : ['Ordo','Ignis']
    , 'Praecantatio' : ['Vacuos','Potentia']
    , 'Sano' : ['Victus','Victus']
    , 'Saxum' : ['Terra','Terra']
    , 'Sensus' : ['Aer','Spiritus']
    , 'Spiritus' : ['Victus','Mortuus']
    , 'Telum' : ['Instrumentum','Perditio']
    , 'Tempestas' : ['Aer','Aqua']
    , 'Tempus' : ['Vacuos','Ordo']
    , 'Tenebrae' : ['Vacuos','Lux']
    , 'Terra' : []
    , 'Tutamen' : ['Instrumentum','Terra']
    , 'Vacuos' : ['Aer','Perditio']
    , 'Venenum' : ['Aqua','Mortuus']
    , 'Victus' : ['Aqua','Terra']
    , 'Vinculum' : ['Motus','Perditio']
    , 'Vitium' : ['Praecantatio','Perditio']
    , 'Vitreus' : ['Saxum','Aqua']
    , 'Volatus' : ['Aer','Motus']
};
aspectDepth2neighbors = {};
aspect2chosen = {};
for aspect, parents in aspect2parents.items():
    aspectDepth2neighbors[aspect]={};
    aspectDepth2neighbors[aspect][1]=set();
    aspectDepth2neighbors[aspect][2]=set();
    aspectDepth2neighbors[aspect][3]=set();

    aspect2chosen[aspect] = False

for aspect, parents in aspect2parents.items():
    for newneighbor in parents:
        aspectDepth2neighbors[aspect][1].add(newneighbor)
        aspectDepth2neighbors[newneighbor][1].add(aspect)
addDepth(1)
addDepth(2)

columnNum = 4
rowofAspects = []
headers = []

for i,aspect in enumerate(sorted(aspectDepth2neighbors.keys())):
    rowofAspects.append(sorted(aspectDepth2neighbors[aspect][1]))
    headers.append(aspect.ljust(15));
    if i%columnNum == columnNum -1:
        transposedRowofAspects = itertools.zip_longest(*rowofAspects)
        print (colored.green("".join(headers)))
        for row in transposedRowofAspects:
            print ("".join("  "+(word or "").ljust(13) for word in row))
        print ("")
        rowofAspects = []
        headers  = []
        
transposedRowofAspects = itertools.zip_longest(*rowofAspects)
print (colored.green("".join(headers)))
for row in transposedRowofAspects:
    print ("".join("  "+(word or "").ljust(13) for word in row))
print ("")
output = '';

choice = True;
looping = True;
while looping:
  while choice:
    sp.call('cls',shell=True)

    for i,aspect in enumerate(sorted(aspectDepth2neighbors.keys())):
      if aspect2chosen[aspect]:
        output += colored.green(("%s. %s" %( i, aspect)).ljust(17))
      else:
        output +=("%s. %s" %( i, aspect)).ljust(17)
      if i%columnNum == columnNum -1:
        print (output)
        output = ''
      if i%(columnNum*3) == columnNum -1:
        output= "\n"
  
    print (output)
    output = ''
    choice = input('Which aspects? c)lear, x)it\n')

    if choice == "c":
      aspect2chosen.update({aspect: False for aspect in aspect2chosen})
      continue
    if choice == "x":
      sys.exit(0)
    try:
      choice = eval(choice)
    except:
      continue
    if choice > 50:
      continue
    
    print (sorted(aspectDepth2neighbors.keys())[choice])
    aspect2chosen[sorted(aspectDepth2neighbors.keys())[choice]] = not aspect2chosen[sorted(aspectDepth2neighbors.keys())[choice]]
    print ("")
  printStep(1)
  printStep(2)
  printStep(3)
  choice = input('Press a key to choose again.')
  choice = True

    
  


