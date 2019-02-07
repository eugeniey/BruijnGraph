import gzip
from itertools import islice
import random 
import time

class HashMap:
	'''
	Classe HashMap
	Il s'agit d'une table de hachage. 
	La fonction de hachage transforme une chaîne de caractère en un entier en utilisant 
	sa représentation en base 36. La scompression est MAD.
	'''

	class _Item:
		'''
		Classe Item imbriquée.
		Cette classe permet d'enregistrer des paires (clef,valeur)
		'''

		__slots__ = '_key', '_value'
	 
		def __init__( self, k, v = None):
			# Constructeur instancie la clef k (k-mer) avec la valeur v (lettre de transition)
			self._key = k
			# Une liste immutable de boolean pour tenir compte des transitions possibles.
			# L'alphabet est de cardinalité 4.
			self._value = [False, False, False, False]
			self._ajouterValeur(v)

		def _ajouterValeur(self, v):
			# Cette fonction ajoute une valeur v de transitions aux valeurs de l'item
			if v is None:
				return
			self._value[HashMap._ALPHABET[v]] = True

		def __eq__( self, other ):
			return self._key == other._key

		def __ne__( self, other ):
			return not( self == other )
	 
		def __lt__( self, other ):
			return self._key < other._key
	 
		def __ge__( self, other ):
			return self._key >= other._key
	 
		def __str__( self ):
			return "<" + str( self._key ) + "," + str( self._value ) + ">"
	 
		def key( self ):
			# getter pour la clef
			return self._key
	 
		def value( self ):
			# getter pour les valeurs
			return self._value

	_AVAIL = object() # Sentienelle
	# Dictionnaire bi-directionnel pour l'alphabet des nucléotides
	_ALPHABET = {'A': 0,'C': 1,'G': 2,'T': 3} 
	_REVERSE_ALPHABET = { 0 : 'A', 1 : 'C', 2 : 'G', 3 : 'T'}

	def __init__(self, cap = 11000000, premier = 109345121, facteurCharge = 0.75):
		'''
		Constructeur pour la table de hachage.
		le cap est la longueur initiale de la table, premier est un nombre permier
		pour la compression MAD et facteurCharge la borne de tolérance sur le facteur 
		de charge pour redimmensionner dynamiquement la table.
		'''

		# Pour le redimensionnement
		self._facteur = facteurCharge
		# Table initialement vide
		self._table = cap * [None]
		# Grandeur de la table
		self._N = cap
		# Nombre d'éléments dans la table
		self._n = 0
		# Nombres pour la compression MAD
		self._premier = premier
		self._echelle = 1 + random.randrange(premier-1) 
		self._decalage = random.randrange(premier)


	def _codeHachage(self, kmer): 
		'''
		Code de hachage. 
		Cette fonction prend en paramètre une chaîne de caractère de l'alphabet {A,C,G,T}
		et retourne un entier. On utilise la représention en de la chaîne de caractère en base
		36 pour retourner l'entier.
		'''


		return int(kmer,36)


	def _compression(self, entier):
		'''
		Fonction de compression MAD
		Prend un entier en paramètre, retourne une position dans la table
		'''
		return (entier * self._echelle + self._decalage) % self._premier % self._N


	def _hachage(self, kmer):
		'''
		Fonction de hachage
		Cette fonction jumelle le code de hachage et la fonction de compression
		'''
		return self._compression(self._codeHachage(kmer))


	def __getitem__(self, kmer):
		'''
		Opérateur __getitem___
		Cette fonction accède et retourne la valeur de la clef du k-mer.
		Lance une KeyError si on ne trouve pas le kmer dans la table.
		'''
		
		indice = self._hachage(kmer)
		trouve, case = self._emplacement(kmer, indice)

		if not trouve:
			raise KeyError('Clef invalide : ' + kmer)
		
		# On retourne les valeurs
		item = self._table[case]
		valeurs = set()
		for i in range(4):
			valeur = item.value()[i]
			if valeur:
				valeurs.add(HashMap._REVERSE_ALPHABET[i])
		return valeurs


	def __setitem__(self, kmer, valeur):
		'''
		Opérateur __setitem___
		La fonction cherche le k-mer. S'il existe, on modifie ses valeurs, 
		sinon on ajoute l'item à la table.
		'''

		indice = self._hachage(kmer)
		trouve, case  = self._emplacement(kmer, indice)


		if trouve:
			# On ajoute la valeur
			self._table[case]._ajouterValeur(valeur)
		else:
			# On ajoute le k-mer au dictionnaire
			self._table[case] = self._Item(kmer,valeur)
			self._n += 1
		self._redimension()


	def __delitem__(self, kmer):
		'''
		Opérateur __delitem__
		Supprime le kmer de la table s'il y est et retourne sa valeur.
		Retourne false si la clé n'est pas dans la table.
		'''

		indice = self._hachage(kmer)
		trouve, case  = self._emplacement(kmer, indice)

		if not trouve:
			return False

		valeur = self._table[case].value()
		self._table[case] = HashMap._AVAIL
		return valeur


	def _emplacement(self, kmer, indice):
		'''
		Sondage linéaire
		Retourne un tuple: (Vrai, indice) si le k-mer 
		est dans la table à l'indice indice ou (Faux, case disponible)
		si le k-mer n'y est pas. 
		'''
		caseDisponible = None 
		while True:
			if self._estDisponible(indice):
				if caseDisponible is None:
					caseDisponible = indice
				# Le k-mer n'est pas dans le dictionnaire
				if self._table[indice] is None:
					return (False, caseDisponible)			
			elif kmer == self._table[indice].key():
				# Match
				return (True, indice)
			# La case à l'indice est disponible 
			
			# On itère sur la case suivante
			indice = (indice + 1) % self._N
		

	def _estDisponible(self, indice):
		'''
		Retourne True si la case à l'indice en paramètre 
		est disponible et Faux sinon.
		'''
		case = self._table[indice]
		return case is None or case is HashMap._AVAIL


	def _redimension(self):
		'''
		Redimensionner dynamiquement si nécessaire
		On utilise une stratégie multiplicative.
		'''
		if self._n > self._facteur * self._N:
			table = self._table
			taille = self._N*2-1 # Constante multiplicative 2
			self._N = taille
			self._n = 0
			self._table = taille * [None]
			# Re-hachage
			for item in table:
				if not (item is None or item is HashMap._AVAIL) :
					k = item.key()
					for i in range(4):
						valeur = item.value()[i]
						if valeur:
							self[k] = HashMap._REVERSE_ALPHABET[i]


	def __iter__(self):
		# Retourne des str 
		for j in range(len(self._table)):
			if not self._estDisponible(j):
				yield self._table[j].key()						


class DeBrujinGraph: 

	def __init__(self, nodes, k=21):
		'''
		Constructeur du graphe.
		On prend en paramètre un itérateur de noeuds (séquences) ainsi qu'une longueur pour les k-mer.
		'''

		# Structure de dictionnaire pour encoder les noeuds et les transitions
		self._dictionnaire = HashMap()

		# Ajout des noeuds
		for seq in nodes:
			l = len(seq)
			for i in range(l - k + 1):
				kmer = seq[i:i+k]
				self._dictionnaire[kmer] = None

		# Ajout des transitions
		for kmer in self._dictionnaire:		
			suc = self.successors(kmer)
			for s in suc:
				self._dictionnaire[kmer] = s[-1]


	def __contains__(self, N: str) -> bool: 
		try:
			self._dictionnaire[N]
		except KeyError:
			return False
		return True


	def __iter__(self):
		return self.nodes() # retourne un itérable sur les noeuds du graphe


	def load_factor(self) -> float: 
		'''Retourne le facteur de charge de la table de hachage.
		'''
		return (self._dictionnaire._n/self._dictionnaire._N)


	def add(self, N: str): 
		'''Cette fonction permet d'ajouter un noeud dans le graphe et les transitions possibles associées.
		'''
		pred = self.predecessors(N)
		suc = self.successors(N)

		for i in pred:
			self._dictionnaire[i] = N[-1]

		for j in suc:
			self.dictionnaire[N] = j[-1]


	def remove(self, N: str): 
		del self.dictionnaire[N]


	def nodes(self): 
		return self._dictionnaire.__iter__()


	def predecessors(self, N: str): 
		'''
		Cette fonction retourne une liste des prédecesseurs du noeuds en argument
		'''

		candidats = self.predecesseurCandidat(N)
		predecesseurs = []

		for i in candidats:
			if i in self:
				predecesseurs.append(i)

		return predecesseurs


	def successors(self, N: str) : 
		'''
		Cette fonction retourne une liste des successeurs du noeuds en argument
		'''
		candidats = self.successeurCandidat(N)
		successeurs = []

		for i in candidats:
			if i in self:
				successeurs.append(i)

		return successeurs


	def successeurCandidat(self, N: str):

		suffixe = N[1:len(N)]
		candidats = []
		for i in HashMap._ALPHABET:
			candidats.append(suffixe+i)
		return candidats


	def predecesseurCandidat(self, N: str):

		prefixe = N[0:len(N)-1]
		candidats = []
		for i in HashMap._ALPHABET:
			candidats.append(i + prefixe)
		return candidats


	def sansPred(self):
		''' Cette méthode retourne un iterateur des noeuds sans prédecesseurs
		'''
		for noeud in self._dictionnaire:
			if(len(self.predecessors(noeud))==0):
				yield(noeud)


	def nSansPred(self, n):
		''' Cette méthode retourne une liste de n noeuds sans prédecesseurs
		'''

		noeuds = []
		i = 0
		for noeud in self.sansPred():
			if i >= n:
				break
			noeuds.append(noeud)
			i += 1

		return noeuds


	def parcours(self, racine):
		'''
		Cette fonction prend un noeud sans predecesseur
		en paramètre et retourune une liste des chemins 
		finis possibles depuis ce noeuds.
		On fait un parcours en profondeur sans repasser
		plusieurs fois par les mêmes arêtes.
		'''

		# liste des chemins possibles depuis la racine
		chemins = []

		sequence = racine
		# dictionnaire des transitions
		# tiens en compte des transitions possibles 
		# d'un sommet sous forme de str
		d = {}
		# Noeud courant pour le parcours
		courant = racine

		# On empile l'état à chaque branchement pour le figer 
		# (courant, sequence, d)
		pile = []

		while True:

			enfants = self.successors(courant)

			# On est au bout d'une séquence 
			if not(enfants):
				# le chemin est complet, on l'ajoute
				chemins.append(sequence)

				# On n'a pas de branchement possible
				if not(pile):
					break

				# On reprend où on était au dernier branchement
				etat = pile.pop()
				courant = etat[0]
				sequence = etat[1]
				d = etat[2]
				continue

			# On branche sur le seul enfant possible
			# On n'a rien à faire dans la pile
			elif len(enfants)==1:

				sequence += enfants[0][-1]
				courant = enfants[0]
				continue

			# Il y a plusieurs branchements possibles
			# On garde la trace du choix dans la pile
			elif len(enfants)>1:

				for enfant in enfants:

					dSuiv = d.copy()

					if courant not in d:
						dSuiv[courant] = enfant[-1]
						pile.append((enfant, sequence + enfant[-1], dSuiv))
					# Si le courant est dans le dictionnaire 
					# Et qu'il n'a pas déjà de transitions vers l'enfant
					elif enfant[-1] not in d[courant]: 
						# On l'ajoute
						dSuiv[courant] += enfant[-1]
						pile.append((enfant, sequence + enfant[-1], dSuiv))
						
				etat = pile.pop()
				courant = etat[0]
				sequence = etat[1]
				d = etat[2]

		return chemins