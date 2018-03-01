### Random substitution (crypto) : easy

#### Write-up

C'est un chiffrement qui se base sur une substitution aléatoire des lettres. Ci dessous une manière qui permet de résoudre le challenge en utilisant les fréquences d'apparitions des lettres de l'alphabet dans un texte en anglais.

NB: Pour simplifier, les lettres en majuscules sont les lettres chiffrées et les lettres miniscules sont les lettres déchiffrées

A chaque étape on doit regarder notre texte pour voir s'il y a des mots qui sont en train de se former pour essayer de deviner les lettres manquantes.

On a utilisé ce site qui facilite énormément la résolution d'un challenge de ce type: http://practicalcryptography.com/ciphers/simple-substitution-cipher/

D'abord on doit voir les combinaisons de trois lettres les plus fréquentes dans notre texte: `RMC`,`BQE`,`BEI`,`CER`,`RBQ`,`HEV`,`KAC`,`MHY`,`HYZ`,`TCE`,`DCA`,`YQL`,`RQK` -> on voit parmi ces combinaisons de trois lettres celles qui forment des mots entiers pour les remplacer avec `the` et `and` -> remplacer `RMC` par `the` et `HEV` par `and` (bqe, bei, cer, rbq ne forment pas des mots).

Après, on doit voir les combinaisons de deux lettres identiques les plus fréquentes dans notre texte: `SS`,`OO` -> `AA` est très fréquent donc c'est probablement ss donc on remplace `A` par `s` (y a une seule occurence de `oo` c'est pour cette raison qu'on ne l'a pas remplacé).

Si on regarde notre texte à cette étape on voit qu'il y a un mot à deux lettres dont l'une est déchiffré (le `t`): `Bt` on essaie donc de deviner le `B` correspond à quoi? les mots à deux lettres le plus fréquentes qui se terminent par t sont soit `it` soit `at` et comme on a déja trouvé que probablement le `H` correspord à `a` donc on peut conclure que `B` correspond à `i`.

Aussi, il y a un autre mot à deux lettres qui commence par `t`: `tQ` donc c'est probablement `to` donc on remplace `Q` par `o` qui est logique car Q est très fréquent dans notre chiffré et `o` est très fréquent dans la langue anglaise.

A cette étape, on n'a pas beaucoup de choix mais on peut essayer de deviner quelques mots par exemple on a un mot qui est devenu presque clair `PDesentations` qui a une très forte possibilité d'être `presentations` donc on essaye de remplacer `P` par `p` et `D` par `r` et voir ce que ça va donner.

Cette dernière tentative a éclairci un autre mot qui est `interestinI` qui est probalement `interesting` donc on remplace `I` par `g`.

On a maintenant `aroKnd` qui est probalement `around` donc on remplace `K` par `u`.

On a maintenant `Yapture` qui est probalement `capture` donc on remplace `Y` par `c`.

On a maintenant `securitJ` qui est probalement `security` donc on remplace `J` par `y`.

On a maintenant `coLpetition` qui est probalement `competition` donc on remplace `L` par `m`.

On a maintenant deux occurences de `Fhich` qui est probalement `which` donc on remplace `F` par `w`.

On a maintenant `weOcome` qui est probalement `welcome` donc on remplace  `O` par  `l`.

On a aussi les mots `hacZing` et `hacZers` qui sont `hacking` et `hackers` donc on remplace `Z` par `k`.

On a maintenant `proXessionals` qui est probalement `professionals` donc on remplace `X` par `f`.

Finalement, on a `eTent`, `loTe` et `conTention` qu'on peut facilement voir qu'ils sont `event`, `love` et `convention` donc on remplace `T` par `v`.

Et à la fin, on obtient:
```
Welcome to the Toulouse Hacking Convention which is an event of talks and presentations based around
IT security and followed by a Capture the Flag competition. The Toulouse Hacking Convention aims
to bring together professionals, researchers and hackers from across the domain. The classical modern
cryptography is interesting and useful. The key is i love crypto.
```

Donc, pour déchiffrer notre flag on utilise https://aesencryption.net/ et on met comme clé `i love crypto` ce qui donne: `THC18{cryptography_art}`


#### Preparation

Ce challenge est préparé en utilisant le siteweb "http://practicalcryptography.com/ciphers/simple-substitution-cipher/" en mettant comme plaintext "Welcome to the Toulouse Hacking Convention which is an event of talks and presentations based around IT security and followed by a Capture the Flag competition. The Toulouse Hacking Convention aims to bring together professionals, researchers and hackers from across the domain. The classical modern cryptography is interesting and useful. The key is i love crypto."
et comme key "hwyvcximbgzoleqpsdarktfujn".
