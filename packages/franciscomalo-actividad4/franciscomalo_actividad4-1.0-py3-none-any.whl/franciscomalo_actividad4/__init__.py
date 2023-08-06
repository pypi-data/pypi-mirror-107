def primos_hata(a):
	for i in range (1,a+1):
		contador=0
		for j in range (1, i):
			if i%j==0: contador+=1
		if contador >= 2: print(i,"No es primo") 
		else: print(i, " Es primo")
primos_hata(25)