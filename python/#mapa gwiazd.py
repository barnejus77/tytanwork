#mapa gwiazd
gwiazdy = [2, 5, 1, 4, 3,6,6,2,4,1,5]

for h in range(5,0,-1):
    for b in gwiazdy:
        if b >= h:
            print("*",end=" ")
        else:
            print(".",end=" ")
    print()
ran=len(gwiazdy)+1
for i in range(1,ran):
        print(i, end=" ")   
print()
#paragon of zgroza od Gemini
produkty = ["Chleb", "Mleko", "Czekolada XXL", "Sok"]
ceny = [4.50, 3.20, 15.00, 6.00]
i=0
s = sum(ceny)
for l in range(len(produkty)+1):
    print(f"{produkty[i]:.<25}{ceny[i]:5.2f}")
    i = i+1
    if i == len(produkty):
        print(30*"-")
        print(f"SUMA {s:25.2f}")
        break

slowa = ["Python", "Jest", "Super", "Zabawa"]
for i in slowa:
    print(f"|{i:^13}|")
   
