import docker
import logging

#Permet de faire la communication avec le serveur docker installé sur la machine hote
client = docker.from_env()

#Fonction de Connexion
def docker_login(username = None, password = None):
    if username and password:
        client.login(username = username, password=password)
        logging.info("Authentification avec succès sur DockerHub")

    else:
        logging.info("Aucune authentification requise(image public)")


#Fonction de récupération d'image

def pull_image(image_name):
    logging.info(f"Télechargement de l'image {image_name} depuis Docker Hub")
    #Téléchargement de l'image avec client Docker avec flux d'evenements
    for line in client.api.pull(image_name, stream=True, decode=True):
        if"status" in line:
            print(line["status"])


    #Affichage des informations de tag de l'image téléchargé
    logging.info(f"Télechargement terminé :{image_name}")
    