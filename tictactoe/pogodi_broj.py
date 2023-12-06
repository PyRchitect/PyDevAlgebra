# TEMPLATE ALGORITHM:

def pogodi_broj(broj,start, end,korak=1,sirina=0):

    if start==end: return start

    print(f"{korak:0>{2}}. korak",end=" ")
    poloviste = int((start+end)/2)
    
    if broj in list(range(start,poloviste+1)):             
        print(f"> broj je u 1. bucketu :: start: {start:0>{sirina}}, end: {poloviste:0>{sirina}}")
        return pogodi_broj(broj,start,poloviste,korak+1,sirina)
    else:        
        print(f"> broj je u 2. bucketu :: start: {poloviste:0>{sirina}}, end: {end:0>{sirina}}")
        return pogodi_broj(broj,poloviste+1,end,korak+1,sirina)
            
def main():
    
    test_start = 1
    test_end = 1024
    # broj = rn.randint(test_start,test_end)
    broj = int(input("\n> unesi broj: "))

    result = pogodi_broj(broj,test_start,test_end,sirina=len(str(test_end)))

    print(f"\nodgovor: {result}, zadano: {broj}")

main()