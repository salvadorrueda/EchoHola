import requests
import json
import os
import sys

# Configuració de l'API DeepFace
DEEPFACE_API_URL = "http://localhost:5005/find"
DB_PATH = "/app/db" # Ruta dins del contenidor
LOCAL_DB_PATH = "./db"

def recognize_face(image_path):
    """
    Envia una imatge a l'API de DeepFace per trobar coincidències.
    """
    if not os.path.exists(image_path):
        print(f"Error: No s'ha trobat la imatge {image_path}")
        return None

    # Nota: L'API /find acostuma a necessitar la ruta de la db i la imatge font
    # Usarem base64 o ruta si el contenidor té accés. 
    # Com que hem muntat ./db:/app/db, passarem la ruta /app/db
    
    # Per simplicitat en aquest exemple, assumim que la imatge es passa com a path
    # Si la imatge no està al volum, l'hauríem d'enviar com a base64 (l'API ho suporta)
    
    import base64
    with open(image_path, "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode('utf-8')

    payload = {
        "img": f"data:image/jpeg;base64,{img_b64}",
        "db_path": DB_PATH,
        "detector_backend": "opencv",
        "enforce_detection": False,
        "align": True
    }

    try:
        response = requests.post(DEEPFACE_API_URL, json=payload)
        response.raise_for_status()
        results = response.json()
        
        # Els resultats de /find venen en una llista de dataframes (com a llistes en JSON)
        if results and 'results' in results and len(results['results']) > 0:
            matches = results['results'][0] # Primer match de la primera cara trobada
            if len(matches) > 0:
                # El path del match conté el nom de la subcarpeta que és el nom de la persona
                # Exemple: /app/db/salvador/foto1.jpg
                match_path = matches[0]['identity']
                name = match_path.split('/')[-2]
                return name
        
        return "Unknown"
    except Exception as e:
        print(f"Error connectant amb DeepFace: {e}")
        return None

def greet(name):
    """
    Genera una salutació per veu.
    """
    if name == "Unknown":
        text = "Hello! I don't recognize you yet, but welcome."
    else:
        text = f"Hello, {name.capitalize()}! Nice to see you again."
    
    print(f"Greeting: {text}")
    # Aquí integrarem el sistema de veu que l'usuari ja té (echovoice)
    os.system(f'echovoice "{text}"')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 recognize.py <path_to_image>")
    else:
        img_path = sys.argv[1]
        print(f"Analyzing {img_path}...")
        identity = recognize_face(img_path)
        if identity:
            greet(identity)
