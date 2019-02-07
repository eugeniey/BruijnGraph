import graph
import gzip
from itertools import islice
import random 
import time
import string


def main():
	## Encoder tous les k-mer dans une instance du graphe
	# k = 21, cap = 11 000 000

	# generateur de séquence
	sequences =  read_fastq('reads.fastq.gz')
	graphe = graph.DeBrujinGraph(sequences)


	## Parcourir le graphe pour obtenir des segments contigüs
	# 100 noeuds sans prédecesseurs
	noeuds = graphe.nSansPred(100)

	# Chemins possibles depuis les noeuds
	chemins = []

	# On ajoute les chemins de chaque noeuds à la liste 
	for i in range(len(noeuds)):
		sequences = graphe.parcours(noeuds[i])
		chemins.append(sequences)


	## Écriture des chemins dans un fichier fasta
	ofile = open("contig.fa","w")

	# on parcours les séquences issues des noeuds sans prédecesseur
	for i in range(len(chemins)):
		# identifiant du noeud
		ID = identifiant()
		# Si le noeud a plusieurs chemins 
		for j in range(len(chemins[i])):
			ofile.write(">" + ID + "\n" + chemins[i][j] + "\n")

	ofile.close()


	# Compression du fasta en gzip pour la lecture
	in_file = "contig.fa"
	in_data = open(in_file,"rb").read()
	out_gz = "contig.fa"
	gzf = gzip.open(out_gz,"wb")
	gzf.write(in_data)
	gzf.close()


	# Création du fichier
	ofile = open("occurences.bed","w")

	# On compare les contigs dans chaque séquence de référence 
	for i in read_fasta("GCF_000002985.6_WBcel235_rna.fna.gz"):
		for j in read_fasta("contig.fa"):
			# Indice de la séquence trouvée
			trouve = (i[1]).find(j[1])

			if trouve>=0:
				reference = i[0]
				start = str(trouve+1)
				end = str(trouve+len(j[1])+1)
				contig = j[0]
				# On ajoute l'occurence
				ofile.write(reference + "\t" + start + "\t" + end + "\t" + contig + "\n")

	# Fermeture du fichier
	ofile.close()

	# Compression en gzip
	in_file = "occurences.bed"
	in_data = open(in_file,"rb").read()
	out_gz = "occurences.bed"
	gzf = gzip.open(out_gz,"wb")
	gzf.write(in_data)
	gzf.close()


def identifiant():
	''' Retourne un identifiant "unique"
	'''
	return ''.join(random.choices(string.ascii_uppercase, k=10))


def read_fastq(path):
	''' Fonction pour lire les séquences (uniquement) du fichier fastq
	'''
	with gzip.open(path, 'rt') as f:
		for line in f:
			sequence = f.readline().rstrip()
			_ = f.readline()
			quality = f.readline().rstrip()
			yield sequence


def read_fasta(path):
	'''Fonction pour lire les fichiers fasta
	'''
	with gzip.open(path, 'rt') as f:
		identifiant, seq = None, None
		for line in f:
			if line[0] == '>':
			# yield current record
				if identifiant is not None:
					yield identifiant, seq
				# start a new record
				identifiant = line[1:].rstrip()
				seq = ''
			else:
				seq += line.rstrip()

main()