print()
print("Unutar dvostrukih navodnika")
print('Unutar jednostrukih navodnika')
print("He's")
print('He\'s')
print('Firma: "Metro"')
print("Firma: \"Metro\"")
print('He\'s "GEN-Z"')

print('\t\tMENU:\n')
print('1. Enter data')
print('2. Read data')
print('0. Exit')

rijec1 = 'Stablo'
rijec2 = 'Krosnja'
tabulator = '\t'

print(rijec1)
print(rijec1,rijec2)
print(rijec1,rijec2,rijec1,sep='$$$',end='')
print("Test")
print(rijec1,'\t',rijec2,sep='$$$')
print('rijec1\trijec2',5,sep='$$$')

print()
print(8)
print(8*7)
print('Umnozak: ',8*7)
print(rijec1+rijec2,"Drvo")
print(rijec1+rijec2+"Drvo")

broj_eura = 50
oznaka_eura = '€'
print('Cijena s PDV =',broj_eura*1.25,oznaka_eura)
print('Cijena s PDV = ',broj_eura*1.25,' ',oznaka_eura,sep='')
# print("Cijena: "+broj_eura+oznaka_eura) # greska
print("Cijena s PDV = %.2f %s" % (broj_eura,oznaka_eura))
print("Cijena s PDV = {0:.2f} {1}".format(broj_eura,oznaka_eura))

import sys
sys.stdout.write('Cijena s PDV =' + ' ' + str(broj_eura)+' '+oznaka_eura+'\n')
