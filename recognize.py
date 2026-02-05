import requests
import json
import os
import sys

# Configuració de l'API DeepFace
DEEPFACE_API_URL = "http://localhost:5005/verify"
DB_PATH = "db" # Ruta local on buscar imatges per iterar
REMOTE_DB_PATH = "/app/db" # Ruta dins del contenidor per referenciar

def recognize_face(image_path):
    """
    Identifica una persona comparant la imatge amb la base de dades local
    fent servir l'endpoint /verify de DeepFace.
    """
    if not os.path.exists(image_path):
        print(f"Error: No s'ha trobat la imatge {image_path}")
        return None

    # Codificar la imatge d'entrada a base64
    import base64
    with open(image_path, "rb") as img_file:
        img_b64 = base64.b64encode(img_file.read()).decode('utf-8')
    
    img1_payload = f"data:image/jpeg;base64,{img_b64}"

    # Iterar sobre les cares conegudes a la carpeta db/
    if not os.path.exists(DB_PATH):
        print(f"Error: No existeix el directori {DB_PATH}")
        return None

    known_people = [d for d in os.listdir(DB_PATH) if os.path.isdir(os.path.join(DB_PATH, d))]
    
    for person in known_people:
        person_dir = os.path.join(DB_PATH, person)
        # Buscar imatges de la persona
        for filename in os.listdir(person_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Construir la ruta remota (dins del contenidor) de la imatge de referència
                # Ex: /app/db/salvador/photo1.jpg
                img2_path = f"{REMOTE_DB_PATH}/{person}/{filename}"
                
                payload = {
                    "img1": img1_payload,
                    "img2": img2_path,
                    "model_name": "VGG-Face",
                    "detector_backend": "opencv",
                    "distance_metric": "cosine"
                }
                
                try:
                    #print(f"Comparant amb {person} ({filename})...")
                    response = requests.post(DEEPFACE_API_URL, json=payload)
                    response.raise_for_status()
                    result = response.json()
                    
                    if result.get("verified") is True:
                        return person
                        
                except Exception as e:
                    # Si falla una comparació, continuem
                    # print(f"Error comparant amb {filename}: {e}")
                    pass

    return "Unknown"

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
