# BruijnGraph

Les séquences d'ADN sont très longue et prennent beaucoup d'espace. Afin d'économiser du temps et de l'espace, il est possible de segmenter la séquence pour former des *k-mers*. Ici, on utilise des *k-mers* de longueur 21. 
Ces *k-mers* construisent un graph de Bruijn où un *k-mer* représente un noeud qui pointe vers le *k-mers* suivant, soit le prochain dans la séquence d'origine. On peut retrouver plusieurs fois un même *k-mer* dans une même séquence, c'est ainsi qu'on économise de l'espace.
Ci-dessous se trouve un exemple d'un graphe de Bruijn pour un alphabet sur {0,1} et des *k-mers* de longueur 3.

![capture1](https://user-images.githubusercontent.com/47392583/52370305-87f7e100-2a20-11e9-81fd-445b47584232.PNG)

Dans ce projet on trouve,

1. L'implémentation d'une table de hachage pour faire le graphe de Bruijn. 

2. L'implémentation d'un graph de Bruijn.

3.  *k-mers* dans le fichier 


