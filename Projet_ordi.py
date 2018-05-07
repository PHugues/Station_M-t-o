#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Codé par Martin CLAISSE, Ambroise LINQUETTE et Pierre HUGUES, élèves de TS2 année 2015/2016
#Projet : Station Météo


#Importation de tous les modules requis pour le programme
import math
import time
import sys
import urllib2
import json
import socket
import smtplib

#Variables
reponse = str()
compteur = int()
compteur2 = int() 
actualisation = bool()
nouvel_essai = bool()
error_nombre = bool()
erreur_reseau = bool()
envoi_email = bool()
temp = float()
main = dict()
ville = str()

#Initialisation de certaines variables
nouvel_essai = True
envoi_email = True
REMOTE_SERVER = "www.google.com"
compteur = 0

#On a ici une boucle "nouvel_essai" qui permet de redemander plusieurs villes différentes sans avoir à relancer le programme
while nouvel_essai is True:
    
#On demande la ville dont on souhaite savoir la température et on la formate afin qu'elle commence bien par une majuscule
    ville = raw_input("De quelle ville souhaitez-vous afficher la température ? \n")
    ville = ville.lower()
    ville = ville.capitalize()

    error_nombre = True
    erreur_reseau = True

#On s'assure ici qu'on ne rentre pas un chiffre comme nom de ville
    while error_nombre is True:
        try:
            ville = str(ville)
            assert ville == int(ville)
        except ValueError:
            error_nombre = False
            pass
        except AssertionError:
            print " Vous devez saisir un nom de ville."
            ville = raw_input("De quelle ville souhaitez-vous afficher la température ? \n")

#Si on rentre "Froide" ou "Cold" comme nom de ville, le programme comprend qu'il doit transformer la variable ville pour lui attribuer la valeur
#"Antarctique" qui est l'endroit le plus froid du monde et où les températures sont tout le temps inférieurs à 0, le tout pour tester l'envoi de l'email
    if ville in ['Froide', 'Cold']:
        ville = "Antarctique"
        print "La ville la plus froide est Antarctique."
    
    actualisation = True


#On utilise une boucle "actualisation" pour que le message se réaffiche à intervalles réguliers sur l'afficheur Pi-lite
    while actualisation is True:
        
#On vérifie que l'ordinateur est bien connecté à Internet
        def test_internet():
            """Permet de tester la connection à un serveur distant."""
            try:
                host = socket.gethostbyname(REMOTE_SERVER)
                s = socket.create_connection((host, 80), 2)
                return True #On est connecté
            except:
                pass
                return False #On est pas connecté

#Si le test de connexion renvoie la booléenne "Fausse", c'est à dire que l'ordinateur n'est pas connecté, on ferme le programme
        if test_internet() is False:
            print "Vous n'êtes pas connectés à Internet. Veuillez vérifier votre connexion et réessayer."
            time.sleep(2)
            exit()
            
#Ouverture de l'API de OpenWeather et transformation en fichier .json afin de recuperer les donnees meteorologiques
        f = urllib2.urlopen('http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=146694a4bd2586a32740cd1953cc0a94'.format(ville))
        json_string = f.read()
        
#Analyse du fichier .json
        parsed_json = json.loads(json_string)

#Récupération du dictionnaire main qui contient la variable "température" souhaitée
        main = parsed_json['main']
        weather = parsed_json['weather']
        wind = parsed_json['wind']
        city = parsed_json['name']

#Afin de récupérer la température on utilise la clé "temp" du dictionnaire et on fait de même pour les autres dictionnaires
        temp = float(main['temp'])
        weather2 = weather[0] #Ici weather est une liste, et weather2 est un dictionnaire
        meteo = str(weather2['main'])
        vent = float(wind['speed'])

#On affiche sur l'ordinateur la température
        print "En ce moment, la temperature à {} est de {} °C.".format(city, temp)
        print "La vitesse du vent est de {} km/h.".format(vent)

#On demande a l'utilisateur s'il souhaite entrer une nouvelle ville
        reponse = raw_input("Voulez vous reessayer avec une autre ville ? oui/non/stop \n ")
        
#On vérifie que c'est bien une réponse acceptable, afin de savoir ce que l'utilisateur souhaite faire
        while reponse not in ["oui", "Oui", "O", "o", "non", "Non", "N", "n", "stop", "s", "Stop", "S"]:
            print "Ce n'est pas une réponse acceptable."
            reponse = raw_input("Voulez vous réessayer avec une autre ville ? oui/non \n")      

#Si l'utilisateur répond "oui" dans ce cas on coupe la boucle "actualisation" ce qui ramène l'utilisateur au début du programme demandant quelle ville il souhaite
        if reponse in ["oui", "Oui", "O", "o"]:
            nouvel_essai = True
            actualisation = False
            compteur = 0

#Si l'utilisateur répond "non", dans ce cas on ne change pas la ville et on reste dans la boucle "actualisation" et c'est toujours la meme ville qui s'affiche
        elif reponse in ["non", "Non", "N", "n"]:
            nouvel_essai = False
            actualisation = True
            compteur = 0

#Et si la réponse est "stop", dans ce cas on arrete le programme
        elif reponse in ["stop", "s", "Stop", "S"]:
            exit()
