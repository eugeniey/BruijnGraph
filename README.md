# BruijnGraph

Les séquences d'ADN sont très longue et prennent beaucoup d'espace. Afin d'économiser du temps et de l'espace, il est segmenter la séquence pour former des *k-mer*. Ici, on utilise des *k-mers* de longueur 21. 
Ces *k-mers* construisent un graph de Bruijn où un *k-mer* représente un noeud et pointe vers le *k-mers* suivant, soit le prochain dans la séquence d'origine. 


 on peut retrouver plusieurs fois un même noeud. 

On y fait l'implémentation d'une table de hachage qui est spécifique au graphe de Bruijn.
