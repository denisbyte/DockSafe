import subprocess
import json
import shutil
import logging

def ensure_trivy():
    #Vérification de l'installation de trivy
    if not shutil.which("trivy"):
        raise RuntimeError("Trivy n'est pas installé")
    else:
        logging.info("Trivy est installé et peut etre utilsé")



def scan_image(image_name):
    #Scanne de l'image Docker
    ensure_trivy()
    logging.info(f"Scan de l'image {image_name} téléchargé depuis le Docker Hub")

    #Exécution de la commande trivy en format json
    result = subprocess.run(
      ["trivy", "image", "--no-progress", "--format", "json", image_name],
      capture_output=True,
      text=True

    )

    """
    Trivy renvoie les valeurs suivantes:
    sain = 0
    vulnérabilités = 5
    """
    if result.returncode not in (0 , 5):
        raise RuntimeError(f"Erreur Trivy: {result.stderr or result.stdout}")
    if not result.stdout.strip():
        logging.error("Aucun résultat JSON reçu de Trivy, voici la sortie brute:")
        logging.error(result.stderr)
        raise RuntimeError("Trivy n' a retourné aucun rapport JSON")

    #Conversion de la sortie json en dictionnaire python
    report = json.loads(result.stdout)
    logging.info("Scan terminé avec succès")
    return report

# Fonction résumant les vulnérabilités

def sumarize_vulnerabilities(report):


    severities = ["UNKNOWN", "LOW", "MEDIUM", "HIGH", "CRITICAL"]
    counts = {s: 0 for s in severities}
    for result in report.get("Results", []):
        for vulnerable in result.get("Vulnerabilities", []):
            sta = vulnerable.get("Severity", "UNKNOWN").upper()
            if sta in counts:
                counts[sta] = counts[sta] + 1

            else:
                counts["UNKNOWN"] += 1
        
    
    return counts

