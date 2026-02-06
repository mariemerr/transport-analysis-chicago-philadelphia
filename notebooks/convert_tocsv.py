import xml.etree.ElementTree as ET
import csv
import os

def process_all_rdf(input_folder, output_csv):
    # Définition des espaces de noms (namespaces)
    namespaces = {
        'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'ds': 'https://data.cityofchicago.org/resource/jyb9-n7fm/'
    }

    fieldnames = ['Route', 'Date', 'day_type', 'total_rides']
    
    # On ouvre le fichier CSV une seule fois en mode écriture ('w') pour créer l'en-tête
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Lister tous les fichiers dans le dossier
        files = [f for f in os.listdir(input_folder) if f.endswith('.rdf')]
        print(f"Extraction de {len(files)} fichiers en cours...")

        for filename in files:
            file_path = os.path.join(input_folder, filename)
            
            try:
                tree = ET.parse(file_path)
                root = tree.getroot()

                for description in root.findall('rdf:Description', namespaces):
                    route = description.find('ds:route', namespaces)
                    date = description.find('ds:date', namespaces)
                    daytype = description.find('ds:daytype', namespaces)
                    rides = description.find('ds:rides', namespaces)

                    if route is not None and date is not None:
                        writer.writerow({
                            'Route': route.text,
                            'Date': date.text,
                            'day_type': daytype.text if daytype is not None else '',
                            'total_rides': rides.text if rides is not None else '0'
                        })
                print(f"Succès : {filename}")
            except Exception as e:
                print(f"Erreur lors de la lecture de {filename} : {e}")

    print(f"\nTerminé ! Toutes les données sont regroupées dans : {output_csv}")

# --- CONFIGURATION ---
dossier_source = 'data/rdf_CTA__Ridership__Daily_by_Route_routes_2001_2025'
fichier_final = 'data/raw/Avg_By_Route_Chicago.csv'

# Lancement du traitement
process_all_rdf(dossier_source, fichier_final)