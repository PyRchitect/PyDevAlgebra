# cijena struje 1 kn/kWh
# utrošeno je 250 kWh

dani_u_godini = 365

jedinicna_cijena = 1
godisnja_potrosnja = 250

dnevna_potrosnja = godisnja_potrosnja/dani_u_godini
dnevni_trosak = dnevna_potrosnja*jedinicna_cijena
print("Obračun:")
print("- "*20)
moj_format = '.2f'
print(f"> godišnja potrošnja: {godisnja_potrosnja} kWh")
print(f"> prosječna dnevna potrošnja: {dnevna_potrosnja:{moj_format}} kWh/dan")
print(f"> jedinična cijena: {jedinicna_cijena} kn/kWh")
print(f"> prosječni dnevni trošak: {dnevni_trosak:{moj_format}} kn/dan")