import random as rn
popunjena_lista=[] #izgenerirana
aktivna_lista=['_' for _ in range(36)] #popunjavaju igraci
"""
for _ in range(36):
    aktivna_lista.append('_')
"""

def generiraj_listu(broj_stupaca=6): #4 ili 6
    broj_polja=broj_stupaca*broj_stupaca
    popunjena_lista=[]
    slovo=65 #ascii kod slova
    for _ in range(broj_polja//2):
        popunjena_lista.append(chr(slovo))
        popunjena_lista.append(chr(slovo))
        slovo+=1
    #print(popunjena_lista)
    rn.shuffle(popunjena_lista)
    #print(popunjena_lista)
    return popunjena_lista 

def ispisi_listu(primljena_lista):
    if len(primljena_lista)==36:
        prijelom=6
    else:
        prijelom=4
    for slovo in range(65,65+prijelom):
        print('\t',chr(slovo),sep='',end='')
    print('\n','_'*50,sep='',end='')
    for indeks, polje in enumerate(primljena_lista):
        if indeks%prijelom==0:
            print('\n',indeks//prijelom+1,'\t',sep='',end='')
        print(polje,'\t',sep='',end='')
    print()
    
def single_player():
    #print(popunjena_lista)
    #print(aktivna_lista)
    if len(popunjena_lista)==36:
        prijelom=6
    else:
        prijelom=4
    poljeXN=input('Unesi polje u obliku SR gdje je S stupac slovcani (A->), a R redak brojcani (1->): ')
    stupac=ord(poljeXN[0].upper())-65 # stupac od 0 do 5 ASCII vrijednost slova A je 65
    redak=int(poljeXN[1])-1 # redak od 0 do 5
    polje1=redak*prijelom+stupac # npr. za B3 (B->1, 3->2, pr=6) -> redak*prijelom+stupac=2*6+1=13
    poljeXN=input('Unesi polje u obliku SR gdje je S stupac slovcani (A->), a R redak brojcani (1->): ')
    stupac=ord(poljeXN[0].upper())-65 # stupac od 0 do 5 ASCII vrijednost slova A je 65
    redak=int(poljeXN[1])-1 # redak od 0 do 5
    polje2=redak*prijelom+stupac # npr. za B3 (B->1, 3->2, pr=6) -> redak*prijelom+stupac=2*6+1=13
    print(polje1,polje2)



popunjena_lista=generiraj_listu()
print(popunjena_lista)
ispisi_listu(popunjena_lista)
#print(aktivna_lista)
print()
ispisi_listu(aktivna_lista)
print()
#prijelom=6 