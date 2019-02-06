# BruijnGraph

Les séquences d'ADN sont très longue et prennent beaucoup d'espace. Afin d'économiser du temps et de l'espace, il est possible de segmenter la séquence pour former des *k-mer*. Ici, on utilise des *k-mers* de longueur 21. 
Ces *k-mers* construisent un graph de Bruijn où un *k-mer* représente un noeud qui pointe vers le *k-mers* suivant, soit le prochain dans la séquence d'origine. 

On peut retrouver plusieurs fois un même *k-mer* dans une même séquence, c'est ainsi qu'on économise de l'espace.

On y fait l'implémentation d'une table de hachage qui est spécifique au graphe de Bruijn.


