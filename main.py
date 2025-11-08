import argparse
import logging
import logging.config
import sys

from downalder import pull_image
from scanner import scan_image, sumarize_vulnerabilities

#Configuration du logger(messages affichés à l'ecran)

logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s - %(levelname)s -%(message)s", #format de l'heure dans les logs
    datefmt="%H:%M:%S"
)

def main():
    parser = argparse.ArgumentParser(
        description="Télecharge une image depuis Docker Hub et fais le scan avec Trivy"
    )
    parser.add_argument(
        "image",
        help="Nom complet de l'image Docker à analyser (ex: nginx:latest) "
        
        )
    args = parser.parse_args()
    image_name = args.image

    try:
        #Télechargement de l'image depuis Docker Hub
        logging.info(f"[1/3] Téléchargement de l'image  '{image_name}'")
        pull_image(image_name)
        logging.info("[1/3] Télechargement terminé avec succès")

        #Scan de l'image avec Trivy
        logging.info(f"[2/3] Scan de sécurité de l'image '{image_name}' en cours...")
        report = scan_image(image_name)
        logging.info("[2/3] Scan terminé avec succès")

        #Résumé des vulnérabilités
        logging.info("[3/3] Génération du résumé des vunlérabilités")
        summary = sumarize_vulnerabilities(report)
        print("-------------------------------------")
        for severity, count in summary.items():
            print(f"  {severity:<10} {count}")
        logging.info("Analyse complète terminé")

    except Exception as e:
        logging.error(f"Erreur : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


