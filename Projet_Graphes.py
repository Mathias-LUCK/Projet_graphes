import tkinter as tk
from tkinter import ttk
import math
import time 
import os
import pygame

k = -1
liste, visites = [], []

#Implémentation d'un graphe non orienté
#Définition de la classe Sommet
#Cette classe va permetre de définir un sommet comme un objet
#Un objet de la classe sommet à deux attribut : une clé (étiquette) et une couleur

class Sommet:
    #Constructeur qui se lance automatiquement à l'appel de la classe
    #attribut du constructeur : cle, couleur
    
    def __init__(self,valeur_cle):
        self.cle=valeur_cle
        self.couleur="blanc" #Par défaut, le sommet est de couleur blanc
        #méthode qui renvoie la clé (valeur) du sommet

    def get_cle(self):
        return self.cle
        #méthode qui renvoie la couleur du sommet

    def get_couleur(self):
        return self.couleur
        #méthode qui change la couleur du sommet qui devient noir

    def set_couleur_noir(self):
        self.couleur="noir"
        #Définition de la classe Graphe
        #Cette classe va permetre de définir un graphe comme un objet
        #Un objet de la classe Graphe à deux attribut : une liste qui contient les sommets du graphe
        #Attention, les sommets sont des objets, la clé est un attribut de l'objet !
        #Un dictionnaire qui contient les listes d'adjacence des sommet du graphe

    def set_couleur_blanc(self):
        self.couleur="blanc"

    def __repr__(self):
        return str(self.cle)

class Graphe:
    #Constructeur qui se lance automatiquement à l'appel de la classe
    #attribut du constructeur : listeS, dico_graphe
    def __init__(self):
        #Création de la liste qui contient les sommets (objet) du graphe
        self.listeS=[]
        #Création d'un dictionnaire qui contient les listes d'adjacence de chaque sommet
        # Le dictionnaire fonctionne sur des couples clé/valeur
        #clé : un sommet, valeur : liste qui contient les sommets voisins
        #dico_graphe={sA:[sB,SC,sD],sB:.......}
        self.dico_graphe={}
        #méthode qui ajoute un objet de la classe Sommet

    def ajouter_sommet(self,s):
        self.listeS.append(s)
        #Lorsque l'on ajoute un sommet, on n'a pas encore placé les arêtes, sa liste d'adjacences est vide
        self.dico_graphe[s]=[]
        #méthode qui ajoute une arête entre deux sommets

    def ajouter_arete(self,s1,s2):
        #Ajoute le sommet s2 à la liste d'adjacence de s1
        self.dico_graphe[s1].append(s2)
        #méthode qui retourne la liste d'adjacence d'un Sommet

    def supprimer_arete(self,s1,s2):
        #Ajoute le sommet s2 à la liste d'adjacence de s1
        self.dico_graphe[s1].remove(s2)
        #méthode qui retourne la liste d'adjacence d'un Sommet

    def supprimer_sommet(self,s):
        self.listeS.remove(s)
        nouveau_dico = {} 
        for sommet in self.dico_graphe : 
            if sommet != s : nouveau_dico[sommet] = []
        self.dico_graphe = nouveau_dico
        for sommet in self.dico_graphe :
            try : self.dico_graphe[sommet].remove(s)
            except ValueError : pass

    def get_liste_adjacence(self,s):
        return self.dico_graphe[s]
    
    def affichage_graphe(self):
        for s in self.listeS:
            print(s.get_cle(),end=" : ")
        for vk in self.get_liste_adjacence(s):
            print(vk.get_cle(),end=" /")
            print("")#Pour le retour à la ligne
        print(self.dico_graphe)

    def set_couleur_blanc_tout(self) :
        for s in self.listeS :
            s.set_couleur_blanc()

    def parcours_en_profondeur(self, s):
        self.affichage_graphe()
        # Marquer tous les sommets comme non visités
        for sommet in self.listeS:
            sommet.set_couleur_blanc()

        liste = []
        # Appel de la fonction récursive pour le parcours en profondeur
        return self._dfs_visite(s, liste)

    def _dfs_visite(self, s, liste_resultat):
        # Marquer le sommet s comme visité
        s.set_couleur_noir()
        liste_resultat.append(s.get_cle())  # Affichage du sommet visité (ou autre traitement)

        # Visiter tous les voisins non visités de s
        for voisin in self.get_liste_adjacence(s):
            if voisin.get_couleur() == "blanc":
                self._dfs_visite(voisin, liste_resultat)
        return liste_resultat

G = Graphe()
chemin_fichier = os.path.abspath(__file__)

class GraphGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Visualisation de graphes")
        self.master.geometry(f"{300}x{100}+{(master.winfo_screenwidth()-300)//2}+{(master.winfo_screenheight()-100)//2}")
        self.master.configure(bg="#e4e4e4")
        self.label = tk.Label(master,bg="#e4e4e4", text="Choisissez le type de graphe :")
        self.label.grid(row=2,column=2, columnspan=2, padx=(50, 5), pady=(20,10))
        self.master.iconbitmap(os.path.join(os.path.dirname(chemin_fichier), 'graph.ico'))

        self.button_oriented = tk.Button(master, bg="#bfbfbf", text="Graphe Orienté", command=self.transition1)
        self.button_oriented.grid(row=3,column=2,padx=(50, 5), pady=(0,10))
        self.button_non_oriented = tk.Button(master,bg="#bfbfbf", text="Graphe non orienté", command=self.transition2)
        self.button_non_oriented.grid(row=3,column=3,padx=(5, 10), pady=(0,10))

        self.config_possibles = {
            '5' : [0, 1, 0,
                  1, 1, 1,
                  0, 1, 0], 
            '6a' : [1, 1, 1, 1,
                    0, 1, 1, 0],
            '6b' : [0, 1, 0, 1, 0,
                    1, 0, 1, 0, 1,
                    0, 1, 0, 1, 0],
            '7a' : [0, 1, 1, 0,
                   1, 1, 1, 1,
                   0, 1, 0, 0],
            '7b' : [0, 1, 1, 0,
                   1, 0, 0, 1,
                   0, 0, 1, 0],
            '8a' : [0, 1, 1, 0,
                   1, 1, 1, 1,
                   0, 1, 1, 0],
            '8b' : [0, 1, 1, 0,
                    1, 0, 0, 1,
                   1, 0, 0, 1,
                   0, 1, 1, 0]

        }

        self.animation_id = None
        self.temps = None

    def selectionner(self, event) :
        self.sommets_cliqués = []
        entree = self.entry.get()
        if entree == '' : return
        self.entry.delete(0, "end")
        caracteres = 'azertyuiopqsdfghjklmwxcvbn'
        chiffres = '0123456789'
        if len(sommets)==8 : 
            nb_sommet = tk.Toplevel()
            nb_sommet.title("   Attention") # Nomme la fenêtre
            nb_sommet.geometry(f"{230}x{40}+{(nb_sommet.winfo_screenwidth() - 230) // 2}+{(nb_sommet.winfo_screenheight() - 40) // 2}") #Place la fenêtre au milieu de l'écran
            nb_sommet.iconbitmap(os.path.join(os.path.dirname(chemin_fichier), 'warning.ico'))
            message_erreur = tk.Label(nb_sommet, text = "Vous avez entré trop de sommets.")
            message_erreur.grid(row = 0, column = 0, columnspan = 2, padx = 8, pady = 10)
            nb_sommet.grab_set()
            nb_sommet.mainloop()
            return
        if len(entree) != 1 :
            taille_sommet = tk.Toplevel()
            taille_sommet.title("Attention") # Nomme la fenêtre
            taille_sommet.geometry(f"{282}x{45}+{(taille_sommet.winfo_screenwidth() - 282) // 2}+{(taille_sommet.winfo_screenheight() - 45) // 2}") #Place la fenêtre au milieu de l'écran
            taille_sommet.iconbitmap(os.path.join(os.path.dirname(chemin_fichier), 'warning.ico'))
            message_erreur = tk.Label(taille_sommet, text = "Un sommet ne peut pas avoir plus d'un caractère.")
            message_erreur.grid(row = 0, column = 0, columnspan = 2, padx = (8,0), pady = (10,0))
            taille_sommet.grab_set()
            taille_sommet.mainloop()
            return
        if sommets!=[] :
            if (sommets[0] in caracteres) and (entree in chiffres) or  (sommets[0] in chiffres) and (entree in caracteres): 
                taille_sommet = tk.Toplevel()
                taille_sommet.title("Attention") # Nomme la fenêtre
                taille_sommet.geometry(f"{245}x{45}+{(taille_sommet.winfo_screenwidth() - 245) // 2}+{(taille_sommet.winfo_screenheight() - 45) // 2}") #Place la fenêtre au milieu de l'écran
                taille_sommet.iconbitmap(os.path.join(os.path.dirname(chemin_fichier), 'warning.ico'))
                message_erreur = tk.Label(taille_sommet, text = "Les sommets doivent être de même type.")
                message_erreur.grid(row = 0, column = 0, columnspan = 2, padx = (8,0), pady = (10,0))
                taille_sommet.grab_set()
                taille_sommet.mainloop()
                return
        if entree not in caracteres and entree not in chiffres : 
            taille_sommet = tk.Toplevel()
            taille_sommet.title("Attention") # Nomme la fenêtre
            taille_sommet.geometry(f"{330}x{45}+{(taille_sommet.winfo_screenwidth() - 330) // 2}+{(taille_sommet.winfo_screenheight() - 45) // 2}") #Place la fenêtre au milieu de l'écran
            taille_sommet.iconbitmap(os.path.join(os.path.dirname(chemin_fichier), 'warning.ico'))
            message_erreur = tk.Label(taille_sommet, text = "Les sommets doivent être des caractères alphanumériques.")
            message_erreur.grid(row = 0, column = 0, columnspan = 2, padx = (8,0), pady = (10,0))
            taille_sommet.grab_set()
            taille_sommet.mainloop()
            return
        if entree in sommets :
            taille_sommet = tk.Toplevel()
            taille_sommet.title("Attention") # Nomme la fenêtre
            taille_sommet.geometry(f"{306}x{45}+{(taille_sommet.winfo_screenwidth() - 306) // 2}+{(taille_sommet.winfo_screenheight() - 45) // 2}") #Place la fenêtre au milieu de l'écran
            taille_sommet.iconbitmap(os.path.join(os.path.dirname(chemin_fichier), 'warning.ico'))
            message_erreur = tk.Label(taille_sommet, text = "Il ne peut pas y avoir de doublons dans les sommets.")
            message_erreur.grid(row = 0, column = 0, columnspan = 2, padx = (8,0), pady = (10,0))
            taille_sommet.grab_set()
            taille_sommet.mainloop()
            return
        
        sommets.append(entree)
        entree = Sommet(str(entree))
        G.ajouter_sommet(entree)
        for sommet in G.listeS :
            G.dico_graphe[sommet] = []

        self.entry.delete(0, "end")
        chaine = ''
        for i in sommets :
            chaine += ',' + ' ' + i 
        self.visu.config(text = "Sommets : " + chaine[1:])
        self.matrice = [[0] * len(sommets) for _ in range(len(sommets))]
        texte = "Matrice d'adjacence :\n" + '  ' + '  '.join(sommets)
        for i in range(len(sommets)) :
            texte += '\n' + sommets[i] + ' ' + str(self.matrice[i])
        self.matrice_texte.config(text=texte)
        self.resultat_p_prof.config(text="")
        self.resultat_p_larg.config(text="")
        self.creer_objets()

    def transition1(self) :
        self.orienté = True
        self.creer_graphe()

    def transition2(self) :
        self.orienté = False
        self.creer_graphe()
    
    def retour(self) :
        if self.choix_sommets:
            self.reset()
            self.choix_sommets.destroy()
        main()

    def creer_graphe(self):
        global sommets, liste
        self.sommets_cliqués = []
        self.master.destroy()
        self.choix_sommets = tk.Tk()
        self.choix_sommets.iconbitmap(os.path.join(os.path.dirname(chemin_fichier), 'graph.ico'))
        sommets = []
        self.choix_sommets.geometry("750x650+{}+{}".format((self.choix_sommets.winfo_screenwidth()-600)//2, (self.choix_sommets.winfo_screenheight()-720)//2))
        self.choix_sommets.configure(bg="#e4e4e4")
        self.label = tk.Label(self.choix_sommets,bg="#e4e4e4", text="Choisissez les sommets :")
        self.visu = tk.Label(self.choix_sommets, bg="#e4e4e4",  text="Sommets : aucun")
        self.entry = tk.Entry(self.choix_sommets)
        valeur_entree = self.entry.get() 
        self.canvas1 = tk.Canvas(self.choix_sommets, width=500, height=500, bg="white")
        self.canvas1.grid(row=3, column=0, columnspan=4, padx=(50, 0), pady=(0,10))
        self.canvas1.create_rectangle(3,3,500,500, outline = "black", width = 3)
        
        self.resultat_p_prof = tk.Label(self.choix_sommets, bg="#e4e4e4", text="")  # Crée un widget Label avec le texte vide
        self.resultat_p_larg = tk.Label(self.choix_sommets, bg="#e4e4e4", text="")  # Crée un widget Label avec le texte vide
        self.matrice_texte = tk.Label(self.choix_sommets, bg="#e4e4e4", text="Matrice d'adjacence :\naucune")
        self.matrice_texte.grid(row=3, column=5, pady=(0,200))
        self.bouton_aide = tk.Button(self.choix_sommets, bg="#bfbfbf", text="Aide", command=self.afficher_aide)
        
        if valeur_entree:
            sommets.append(valeur_entree)
        self.Parcours_Largeure = tk.Button(self.choix_sommets, bg="#bfbfbf", text="Parcours Largeur", command=lambda : self.Faire_Parcours_Largeur())
        self.Parcours_Profondeure = tk.Button(self.choix_sommets, bg="#bfbfbf", text="Parcours Profondeur", command=lambda : self.Faire_Parcours_Profondeur())
        self.button = tk.Button(self.choix_sommets, bg="#bfbfbf", text="Ajouter le sommet", command=self.selec)
        self.effacer = tk.Button(self.choix_sommets, bg="#bfbfbf", text="Effacer", command=self.reset)
        self.menu=tk.Button(self.choix_sommets,bg="#bfbfbf", text="Retour", command=self.retour)
        self.entry.bind("<KeyPress-Return>", self.selectionner)
        self.choix_sommets.title("Choix des sommets")
        self.label.grid(row=0, column=0, columnspan=2, padx=(10, 5), pady=(0,10))
        self.entry.grid(row=1, column=0)
        self.button.grid(row=1, column=1)
        self.Parcours_Largeure.grid(row=3, column=5, pady=(300, 0))
        self.resultat_p_larg.grid(row=3, column=5, pady=(405, 5))
        self.Parcours_Profondeure.grid(row=3, column=5, pady=(120, 5))
        self.resultat_p_prof.grid(row=3, column=5, pady=(180, 5))
        self.visu.grid(row=2, column=0, columnspan=2, padx=(10, 5), pady=(0,10))
        self.effacer.grid(row=4, column=0, padx=(130, 0))
        self.menu.grid(row=4, column=1)
        self.bouton_aide.grid(row=4, column=2, padx=(0, 50))
        self.select_sommet = [False, None]
        self.playing = True

        # Charger le son
        self.sound_path = os.path.join(os.path.join(os.path.dirname(chemin_fichier), 'Musique.mp3'))
        pygame.mixer.init()
        pygame.mixer.music.load(self.sound_path)

        # Créer le curseur pour le volume
        self.volume_slider = ttk.Scale(self.choix_sommets, from_=0, to=1, orient="horizontal", command=self.update_volume)
        self.volume_slider.set(0.3)  # Initialiser le volume à 0.5
        self.volume_slider.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        style = ttk.Style()
        style.configure("TScale", background="#e4e4e4")
        # Créer les boutons
        self.play_button = tk.Button(self.choix_sommets, text="Jouer la musique", command=self.play_and_stop_sound)
        self.play_button.grid(row=1, column=3, padx=5, pady=5, sticky="ew")
        self.play_and_stop_sound()

    def update_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume)) 

    def play_and_stop_sound(self):
        if not self.playing :
            pygame.mixer.music.play(-1)  # -1 indique de jouer en boucle
            self.playing = True
            self.play_button.config(text="Arrêter la musique")
        else : 
            pygame.mixer.music.stop()
            self.playing = False
            self.play_button.config(text="Jouer la musique")

    def Faire_Parcours_Largeur(self) :
        self.select_sommet = [True, "Largeur"]
        self.sommets_cliqués = []

    def Faire_Parcours_Profondeur(self) :
        self.select_sommet = [True, "Profondeur"]
        self.sommets_cliqués = []

    def afficher_aide(self) :
        info = tk.Tk()
        info.geometry("800x160+{}+{}".format((info.winfo_screenwidth()-800)//2, (info.winfo_screenheight()-160)//2))
        info.resizable(False, False)
        info.iconbitmap(os.path.join(os.path.dirname(chemin_fichier), 'help.ico'))
        info.configure(bg="#e4e4e4")
        info.title("Aide")
        label_info = tk.Label(info, bg="#e4e4e4", text=
                              'Choix du type de graphe : dans le menu 1, choisissez "Graphe Orienté" ou "Graphe Non-orienté" selon le graphe que vous voulez créer.'
                            + '\nChoix des sommets : tapez le nom d\'un sommet, puis cliquez sur "Ajouter le sommet" ou appuyer sur entrée. Tous les sommets doivent être de'
                            + '\n                                      même type (soit chiffres soit lettres), des caractères alphanumériques, doivent avoir exactement un caractère et ne peuvent' 
                            + '\n                                      pas exister en double.'
                            + '\nSuppression d\' un sommet : pour supprimer un sommet, double cliquez sur le sommet en question avant que l\'animation de sélection ne se termine. \n                               Attention : supprimer un sommet supprime toutes les connections existantes.'
                            + '\nCréation du graphe : pour créer des liens entre deux sommets, cliquez sur le premier puis sur le deuxième.'
                            + '\nParcours en largeur : pour effectuer un parcours en largeur, cliquez sur "Parcours largeur".'
                            + '\nParcours en profondeur : pour effectuer un parcours en profondeur, cliquez sur "Parcours profondeur".'
                            + '\nRetour : si vous voulez changer de type de graphe, cliquez sur "Retour".', justify="left")
        label_info.pack()

        
    def reset(self) :
        global sommets, G
        sommets = []
        self.sommets_cliqués = []
        G = Graphe()
        self.visu.config(text="Sommets : aucun")
        self.matrice_texte.config(text="Matrice d'adjacence :\naucune")
        self.resultat_p_prof.config(text="")
        self.resultat_p_larg.config(text="")
        self.creer_objets()

    def selec(self) :
        self.selectionner(None)
        return
    
    def Afficher_Parcours_Largeur(self, liste_resultats2) :
        texte = ""
        for i, sommet in enumerate(liste_resultats2):
            texte += sommet
            if i < len(liste_resultats2) - 1:  # Vérifie si ce n'est pas le dernier sommet
                texte += " -> "
            # et utilisez-le pour configurer le texte
            self.resultat_p_larg.config(text=texte)

    def Parcours_Largeur(self, liste_resultats2, g2, sommet_depart2):
        global liste
        from collections import deque
     
        s2 = sommet_depart2
        # Initialisez une file pour parcourir les sommets
        file = deque([s2])
        # Marquez le sommet de départ comme visité
        s2.set_couleur_noir()
        
        while file:
            s2 = file.popleft()  # Prenez le premier sommet de la file
            liste_resultats2.append(s2.get_cle())  # Ajoutez le sommet à la liste des résultats
            
            # Liste d'adjacence des voisins de s
            liste_voisins2 = g2.get_liste_adjacence(s2)
            for sk2 in liste_voisins2:
                if sk2.get_couleur() == "blanc":
                    sk2.set_couleur_noir()  # Marquez le voisin comme visité
                    file.append(sk2)  # Ajoutez le voisin à la file
                    
        # Après avoir exploré tous les sommets, affichez le parcours en largeur
        self.Afficher_Parcours_Largeur(liste_resultats2)
        g2.set_couleur_blanc_tout()
        liste = []
       
    def Afficher_Parcours_Profondeur(self, liste_resultats, g):
        global liste, visites
        visites = []
        texte = ""
        for i, sommet in enumerate(liste_resultats):
            if sommet not in texte : 
                texte += sommet
                if i < len(liste_resultats) - 1:  # Vérifie si ce n'est pas le dernier sommet
                    texte += " -> "

        self.resultat_p_prof.config(text=texte)
        g.set_couleur_blanc_tout()
        liste = []

    def Parcours_Profondeur(self, liste_resultats, g, sommet_depart):
             self.Afficher_Parcours_Profondeur(g.parcours_en_profondeur(sommet_depart), g)

    def Afficher_Matrice_Adjacence(self, sommet1, sommet2):
        # Remplissez la matrice avec les connexions des arêtes
        sommet1_index = G.listeS.index(sommet1)
        sommet2_index = G.listeS.index(sommet2)

        self.matrice[sommet1_index][sommet2_index] = 1
        texte = "Matrice d'adjacence :\n" + '  ' + '  '.join(sommets)
        for i in range(len(sommets)) :
            texte += '\n' + sommets[i] + ' ' + str(self.matrice[i])
        self.matrice_texte.config(text=texte)
    
    def creer_objets(self):
        x = 50
        y = 50
        k = 1
        self.canvas1.destroy()
        self.config = '6aa'
        self.canvas = tk.Canvas(self.choix_sommets, width=500, height=500, bg="white")
        self.canvas.grid(row=3, column=0, columnspan=4, padx=(50, 5), pady=(0,10))
        self.canvas.create_rectangle(3,3,500,500, outline = "black", width = 3)
        if len(sommets) in [7,8] :
            x = 75
            y = 75
            j = 0
            for i in range(1, 17) :
                try :
                    if self.config_possibles['8b'][k-1] == 1 :
                        if j<len(sommets) :
                            cercle = self.canvas.create_oval(x, y, x+50, y+50, outline="black", fill="white")  # Dessiner le cercle
                            self.canvas.create_text(x+25, y+25, text=sommets[j])  # Ajouter le texte du sommet à l'intérieur du cercle
                            # Associer un événement de clic à chaque cercle
                            self.canvas.tag_bind(cercle, "<Button-1>", lambda event, nom_sommet=G.listeS[j]: self.cercle_clique(event, nom_sommet))
                            j += 1
                except IndexError : break
                x += 100 
                if k%4==0 : 
                    y += 100
                    x = 75
                k+=1
        else :
            if len(sommets)==1 : 
                x = 225
                y = 225
            if len(sommets)==2 :
                x = 175
                y = 225
            if len(sommets)in[3,4] :
                x = 175
                y = 175
            if len(sommets) == 5 :
                x = 125
                y = 225
            if len(sommets) == 6 :
                x = 125
                y = 175
            for i, sommet in enumerate(G.listeS):
                    cercle = self.canvas.create_oval(x, y, x+50, y+50, outline="black", fill="white")  # Dessiner le cercle
                    self.canvas.create_text(x+25, y+25, text=sommet)  # Ajouter le texte du sommet à l'intérieur du cercle
                    # Associer un événement de clic à chaque cercle
                    self.canvas.tag_bind(cercle, "<Button-1>", lambda event, nom_sommet=sommet: self.cercle_clique(event, nom_sommet))
                    if len(sommets)<=4 :
                        if i%2 == 0:
                            x += 100
                        else :
                            y += 100
                            x-= 100
                            if len(sommets)==3 : x += 50
                    elif len(sommets)==5 :
                        x += 100
                        if k == 1 : 
                            x = 225
                            y -= 82
                            
                        if k == 2 :
                            x,y =(325,225)
                            
                        if k == 3 :
                            x = 175
                            y += 100
                            
                    elif len(sommets) == 6 : 
                        if self.config == '6a' :
                            x += 100
                        else :
                            x += 100
                            if k == 1 : 
                                x = 225
                                y -= 100
                            
                            if k == 2 :
                                x,y =(325,175)
                            
                            if k == 3 :
                                x,y =(125,300)
                            
                            if k == 4 :
                                x,y =(325,300)
                            
                            if k == 5 :
                               x,y =(225,375) 
                    else :
                        if self.config_possibles['7/8'][k-1] == 1 :
                            cercle = self.canvas.create_oval(x, y, x+50, y+50, outline="black", fill="white")  # Dessiner le cercle
                            self.canvas.create_text(x+25, y+25, text=sommet)  # Ajouter le texte du sommet à l'intérieur du cercle
                            # Associer un événement de clic à chaque cercle
                            self.canvas.tag_bind(cercle, "<Button-1>", lambda event, nom_sommet=sommet: self.cercle_clique(event, nom_sommet))
                            x += 100 
                        if k%4==0 : 
                            y += 100
                            x = 50
                    k += 1

    def suppr_sommet(self, event, sommet):
        global sommets
        if len(sommets) == 0 : 
            self.reset()
            return
        G.supprimer_sommet(sommet)
        sommets.remove(str(sommet))
        if sommets == [] :
            self.visu.config(text="Sommets : aucun")
        else : 
            self.visu.config(text="Sommets : " + ", ".join(sommets))
        texte = "Matrice d'adjacence :\n" + '  ' + '  '.join(sommets)
        for i in range(len(sommets)) :
            texte += '\n' + sommets[i] + ' ' + str(self.matrice[i])
        self.matrice_texte.config(text=texte)
        self.creer_objets()
        self.resultat_p_prof.config(text="")
        self.resultat_p_larg.config(text="")

    def cercle_clique(self, event, nom_sommet):
        global sommets
        if self.animation_id is not None:
            # Si une animation est en cours, arrêtez-la
            self.canvas.after_cancel(self.animation_id)
        cercle_id = event.widget.find_closest(event.x, event.y)[0]
        event.widget.itemconfigure(cercle_id, fill="#2cc3a8")
        couleur_actuelle = event.widget.itemcget(cercle_id, "fill")
        # Récupérer les coordonnées du cercle
        coords = event.widget.coords(cercle_id)
        # Calculer les coordonnées du centre du cercle
        centre_x = (coords[0] + coords[2]) / 2
        centre_y = (coords[1] + coords[3]) / 2
        self.animation_en_cours = True
        self.sommets_cliqués.append((centre_x, centre_y, nom_sommet))
        self.animation_id = self.canvas.after(40, lambda: self.revenir_blanc(event.widget, cercle_id, couleur_actuelle, 20))
        if self.select_sommet == [True, "Profondeur"] :
            self.Parcours_Profondeur(liste, G, nom_sommet)
            self.select_sommet = [False, None]
            self.cercle_cliqués = []
            return
        elif self.select_sommet == [True, "Largeur"] :
            self.Parcours_Largeur(liste, G, nom_sommet)
            self.select_sommet = [False, None]
            self.cercle_cliqués = []
            return
        if self.temps is None : self.temps = time.time()
        else : 
            if time.time() - self.temps <= 0.4: 
                try : 
                    if self.sommets_cliqués[0] == self.sommets_cliqués[1] :
                        self.suppr_sommet(event, nom_sommet)
                        self.sommets_cliqués = []
                        return
                except IndexError : pass
            else : 
                self.temps = time.time()

        if len(self.sommets_cliqués)==2 :
            x1, y1 = self.sommets_cliqués[0][0], self.sommets_cliqués[0][1]
            x2, y2 = self.sommets_cliqués[1][0], self.sommets_cliqués[1][1]
            if len(sommets)<4 :
                self.sommets_cliqués = []
                return
            if self.sommets_cliqués[1][2] in G.get_liste_adjacence(self.sommets_cliqués[0][2]) :
                G.supprimer_arete(self.sommets_cliqués[0][2], self.sommets_cliqués[1][2])
                if not self.orienté : 
                    try : G.supprimer_arete(self.sommets_cliqués[1][2], self.sommets_cliqués[0][2])
                    except ValueError : pass
                self.supprimer_fleche(self.canvas, x1, y1, x2, y2)
            else : 
                G.ajouter_arete(self.sommets_cliqués[0][2],self.sommets_cliqués[1][2])
                if self.sommets_cliqués[0][2] == self.sommets_cliqués[1][2] :
                    self.fleche_circulaire(self.canvas, x1, y1, self.orienté)
                else :
                    if not self.orienté : 
                        G.ajouter_arete(self.sommets_cliqués[1][2],self.sommets_cliqués[0][2])
                    self.draw_arrow_with_stop(self.canvas, x1, y1, x2, y2, 25, self.orienté)
            self.Afficher_Matrice_Adjacence(self.sommets_cliqués[0][2], self.sommets_cliqués[1][2])
            if not self.orienté : self.Afficher_Matrice_Adjacence(self.sommets_cliqués[1][2], self.sommets_cliqués[0][2])
            self.sommets_cliqués = []


    def fleche_circulaire(self, canvas, x1, y1, orienté) : 
        cercle = canvas.create_oval(x1 - 15, y1 - 45, x1 + 15, y1-15, outline="black")
        canvas.tag_lower(cercle)
        tag = f"fleche_{x1}_{y1}"  
        canvas.addtag_withtag(tag, cercle)
        if orienté : 
            arrow = canvas.create_line(x1-12, y1-24, x1-11, y1-22, arrow=tk.LAST)
            tag = f"fleche2_{x1}_{y1}"  
            canvas.addtag_withtag(tag, arrow)

    def revenir_blanc(self, canvas, cercle_id, couleur_actuelle, steps):
        # Calculer les composantes de couleur pour la transition
        orange_rgb = canvas.winfo_rgb("#2cc3a8")
        blanc_rgb = canvas.winfo_rgb("white")
        delta_r = (blanc_rgb[0] - orange_rgb[0]) / steps
        delta_g = (blanc_rgb[1] - orange_rgb[1]) / steps
        delta_b = (blanc_rgb[2] - orange_rgb[2]) / steps

        # Changer progressivement la couleur du cercle de orange à blanc
        for i in range(steps+1):
            # Calculer la couleur intermédiaire
            couleur_intermediaire = "#%04x%04x%04x" % (
                int(orange_rgb[0] + delta_r * i),
                int(orange_rgb[1] + delta_g * i),
                int(orange_rgb[2] + delta_b * i)
            )
            # Changer la couleur du cercle
            canvas.itemconfigure(cercle_id, fill=couleur_intermediaire)
            # Mettre à jour l'affichage
            canvas.update_idletasks()
            # Attendre un petit moment avant la prochaine étape
            canvas.after(4)

    # Fonction pour calculer les coordonnées du point d'arrêt de la flèche
    def calculer_point_arret(self, x1, y1, x2, y2, distance):
        # Calculer la distance entre les deux points
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # Calculer les ratios de x et y pour déplacer le point d'arrêt
        if dist == 0 : return x2, y2
        ratio = distance / dist
        x_stop = x2 - (x2 - x1) * ratio
        y_stop = y2 - (y2 - y1) * ratio
        return x_stop, y_stop

    def supprimer_fleche(self, canvas, x1, y1, x2, y2):
        # Rechercher l'identifiant de l'élément graphique représentant la flèche
        if self.sommets_cliqués[0][2] != self.sommets_cliqués[1][2] : 
            tag = f"fleche_{x1}_{y1}_{x2}_{y2}"  
            try :
                fleche_id = canvas.find_withtag(tag)[0]
            except IndexError:
                tag = f"fleche_{x2}_{y2}_{x1}_{y1}"  
                fleche_id = canvas.find_withtag(tag)[0]
            if fleche_id:
                canvas.delete(fleche_id)  # Supprimer le premier élément avec ce tag'''
        else : 
            tag1 = f"fleche_{x1}_{y1}"
            fleche_id1 = canvas.find_withtag(tag1)[0]
            canvas.delete(fleche_id1)
            if self.orienté :
                tag2 = f"fleche2_{x1}_{y1}"
                fleche_id2 = canvas.find_withtag(tag2)[0]
                canvas.delete(fleche_id2)

    # Fonction pour dessiner une flèche avec un point d'arrêt
    def draw_arrow_with_stop(self, canvas, x1, y1, x2, y2, distance, oriente):
        # Calculer les coordonnées du point d'arrêt de la flèche
        x_stop, y_stop = self.calculer_point_arret(x1, y1, x2, y2, distance)
        # Dessiner la ligne principale de la flèche
        if oriente:
            ligne = canvas.create_line(x1, y1, x_stop, y_stop, arrow=tk.LAST)
        else:
            ligne = canvas.create_line(x1, y1, x_stop, y_stop)
        tag = f"fleche_{x1}_{y1}_{x2}_{y2}"
        canvas.addtag_withtag(tag, ligne)
        canvas.tag_lower(ligne)

def main():
    root = tk.Tk()
    app = GraphGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()