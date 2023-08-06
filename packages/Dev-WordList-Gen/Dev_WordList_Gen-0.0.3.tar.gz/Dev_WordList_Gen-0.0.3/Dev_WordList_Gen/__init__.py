import itertools as it
"""
chrs=input("Words :")
mins=int(input("Min Length:"))
maxs=int(input("Max Length:"))
"""

def dev_generate(chrs,mins,maxs):
    for i in range(mins,maxs+1, 1):
        for combination in it.product(chrs, repeat=i):
            #fo=open("wordlist.txt","a")
            char=''.join(combination)
            print(char)
            #print(char, file=fo)
        #fo.close()
    return("wordlist.txt was Created Sucessfully.")
