class Contact:
    def __init__(self, id, first_name, last_name, phone):
        self.id=id
        self.first_name=first_name
        self.last_name=last_name
        self.phone=phone
 
    def print_contact(self):
        print(f'ID: {self.id}\tName: {self.first_name}\tSurname: {self.last_name}\tPhone: {self.phone}')
 
address_book={} #key je id, value je citavi contact objekt
 
try:
    with open('adresar.txt','r') as fr:
        for line in fr:
            line=line.rstrip()
            line_parts=line.split(';')
            contact=Contact(line_parts[0],line_parts[1],line_parts[2],line_parts[3])
            address_book[contact.id]=contact
except Exception as e:
    print(f'Dogodila se pogreska {e}')
 
for key, value in address_book.items():
    print(key, end='\t')
    value.print_contact()