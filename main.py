import collections
import sys
import time

class ArbreLexico(dict):
    """ 
    On choisit de représenter l'arbre lexicographique par une table de hachage 
    (i.e., en Python, par un dictionnaire)
    """
    def __init__(self,ensMots=()):
        self.sortie=set()
        for i,mot in enumerate(ensMots):
            v = self.ajoutMot(mot)
            v.sortie.add(i) # le noeud v correspond au i-ème mot de l'ensemble

    def ajoutMot(self,mot):
        " insertion d'un mot dans l'arbre lexicographique"
        v = self  # on part de la racine de l'arbre
        for car in mot:
            if car not in v:  # si aucun arc issu de v est étiqueté par car
                v[car] = ArbreLexico()  # alors on le crée
            v = v[car]  # on descend dans l'arbre via l'arc étiqueté par car
        return v

    def recherche(self,mot):
        """ retourne le noeud v de l'arbre associé à mot (s'il existe)
        ça sert pour la construction à la main de la fonction de suppléance
        sinon inutile car inefficace
        """        
        v = self  
        for car in mot:
            if car not in v: return None
            v = v[car]  
        return v

    def labeliser(self):
        """ attribue à chaque noeud de l'arbre lexicographique son label via 
        un parcours en largeur;
        ça peut servir pour les tests sinon pas utile """
        laFile=collections.deque()
        self.label = '' # la racine de l'arbre correspond au mot vide
        laFile.append(self)
        while len(laFile) > 0:
            cour = laFile.popleft()
            for car in cour:
                fils = cour[car]
                fils.label = cour.label+car
                laFile.append(fils)

class AhoCorasick(ArbreLexico):
    """ 
    L'automate de Aho-Corasick associé à un ensemble de mots est 
    l'arbre lexicographique associé à cet ensemble et 
    couplé à la fonction de suppléance et la fonction de sortie 
    """
    def __init__(self,ensMots=()):
        ArbreLexico.__init__(self,ensMots)
        self.ensMots = ensMots
        self.lgrMots = [len(mot) for mot in ensMots]
        self.labeliser()
        self.consSuppleanceSortie()
                

    def transition(self,etat,car):
        """
        retourne le noeud atteint après lecture de car partant du noeud etat
        """
        while etat.label!='' and self.fils(etat,car) is None:
            etat=etat.suppleance
        if self.fils(etat,car) is not None:
            etat=self.fils(etat,car)
        return etat
        #  À ÉCRIRE
    
    def fils(self,etat,car):
        for i in etat:
            if(i==car):
                return etat[i]
        return None
        
    def consSuppleanceSortie(self):
        """ 
        Construction des fonctions de suppléance et de sortie 
        via un parcours en largeur de l'arbre lexicographique
        """
        laFile = collections.deque()
        #  On initialise la file avec les descendants directs de la racine,
        #  ils ont la racine comme image par la fonction de suppléance
        for p in self.values():
            p.suppleance = self
            laFile.append(p)
        #  À COMPLÉTER
        while len(laFile) > 0:
            cour = laFile.popleft()
            for i in cour:
                p=self.fils(cour,i)
                p.suppleance=self.transition(cour.suppleance,i)
                laFile.append(p)
                #sortie
                if p.label in self.ensMots:
                    for j in (p.suppleance).sortie:
                        p.sortie.add(j)
                else:
                    p.sortie=(p.suppleance).sortie
                    
                #######
    def analyser(self,texte):
        liste=[]
        etat=self
        for index,car in enumerate(texte):
            while etat.label!='' and self.fils(etat,car) is None:
                etat=etat.suppleance
            if self.fils(etat,car) is not None:
                etat=self.fils(etat,car)
                if len(etat.sortie)>0:
                    for z in etat.sortie:
                        t=(z,index)
                        liste.append(t)
        return liste
            
                
   
        
        
    def __repr__(self):
        self.label = 'mot vide'
        laFile = collections.deque()
        s = "** %s\n" %self.label
        for c in self:
            laFile.append(self[c])
            s+="\t%s : %s\n" %(c,self[c].label)
        while len(laFile) > 0:
            cour = laFile.popleft()            
            s += "\n** %s\n\tsuppléance : %s\n" %(cour.label,cour.suppleance.label)
            for c in cour:
                laFile.append(cour[c])
                s += '\t%s : %s\n' %(c,cour[c].label)
            if len(cour.sortie)>0:
                s += "\tsortie %s\n" %cour.sortie
        return s

if __name__ == '__main__':

    with open(sys.argv[1], 'r') as my_file:
        texte=my_file.read()
        texte = texte.strip()

    print("Veuillez entrer les motifs à rechercher dans le texte,  CTRL+D pour marquer la fin des mots")
    motifs=[]
    for line in sys.stdin:
        motifs.append(line[:len(line)-1])

    a = AhoCorasick(tuple(motifs))

    start = time.time()
    res=a.analyser(texte)
    end = time.time()

    print(res)
    print("nombre d'occurrences=%s" %(len(res)))
    print("temps d'execution %f" %(end - start))