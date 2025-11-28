from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProject,
    QgsProcessingException
)
import shutil
import os
import zipfile

class ClonaGpkgProgettoChirurgico(QgsProcessingAlgorithm):
    INPUT_GPKG = 'INPUT_GPKG'
    OUTPUT_GPKG = 'OUTPUT_GPKG'
    OUTPUT_PROJECT = 'OUTPUT_PROJECT'

    def createInstance(self):
        return ClonaGpkgProgettoChirurgico()

    def name(self):
        return 'clonagpkgprogettochirurgico'

    def displayName(self):
        return 'Clona GeoPackage e Progetto (Metodo Chirurgico XML)'

    def group(self):
        return 'Utilità Progetto'

    def groupId(self):
        return 'utilita_progetto'

    def shortHelpString(self):
        return (
            "Clona un GeoPackage e aggiorna automaticamente tutti i riferimenti nel progetto QGIS.\n\n"
            "Come funziona:\n"
            "• Rileva automaticamente il GeoPackage utilizzato nel progetto corrente\n"
            "• Copia il GeoPackage nella nuova posizione specificata\n"
            "• Modifica chirurgicamente il codice XML del file di progetto (.qgs/.qgz)\n"
            "• Sostituisce tutti i riferimenti al vecchio GeoPackage con il nuovo\n\n"
            "Note importanti:\n"
            "• Il progetto deve essere salvato su disco (non nel GeoPackage)\n"
            "• Lo script rileva e blocca l'esecuzione se il progetto è dentro un GeoPackage\n"
            "• Il nuovo progetto deve essere nella stessa cartella del nuovo GeoPackage\n"
            "• I percorsi relativi (./) vengono mantenuti intatti"
        )

    def _find_current_gpkg(self):
        """Trova il primo GeoPackage utilizzato nel progetto corrente"""
        project = QgsProject.instance()

        # Cerca tra tutti i layer del progetto
        for layer in project.mapLayers().values():
            source = layer.source()
            # Controlla se la sorgente contiene un file .gpkg
            if '.gpkg' in source.lower():
                # Estrai il percorso del file (rimuovendo eventuali layer names dopo |)
                gpkg_path = source.split('|')[0]
                # Se il percorso è relativo, convertilo in assoluto
                if not os.path.isabs(gpkg_path):
                    project_dir = os.path.dirname(project.fileName())
                    gpkg_path = os.path.normpath(os.path.join(project_dir, gpkg_path))
                # Verifica che il file esista
                if os.path.exists(gpkg_path):
                    return gpkg_path

        return ''  # Ritorna stringa vuota se non trova nessun geopackage

    def initAlgorithm(self, config=None):
        # Trova il primo geopackage nel progetto corrente
        default_gpkg = self._find_current_gpkg()

        self.addParameter(
            QgsProcessingParameterFile(
                self.INPUT_GPKG,
                '1. GeoPackage ORIGINALE (Quello attuale)',
                behavior=QgsProcessingParameterFile.File,
                fileFilter='GeoPackage (*.gpkg)',
                defaultValue=default_gpkg
            )
        )
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_GPKG,
                '2. Salva NUOVO GeoPackage come...',
                fileFilter='GeoPackage (*.gpkg)'
            )
        )
        self.addParameter(
            QgsProcessingParameterFileDestination(
                self.OUTPUT_PROJECT,
                '3. Salva NUOVO Progetto come...',
                fileFilter='QGIS Project (*.qgz *.qgs)'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        # --- 1. PREPARAZIONE ---
        old_gpkg_full = self.parameterAsString(parameters, self.INPUT_GPKG, context)
        new_gpkg_full = self.parameterAsString(parameters, self.OUTPUT_GPKG, context)
        new_project_path = self.parameterAsString(parameters, self.OUTPUT_PROJECT, context)

        # Percorso del progetto ATTUALMENTE APERTO (che useremo come base)
        current_project_path = QgsProject.instance().fileName()

        if not current_project_path:
            raise QgsProcessingException("ERRORE: Salva il progetto corrente su disco prima di lanciare lo script!")

        # VALIDAZIONE: Verifica che il progetto corrente NON sia salvato dentro un GeoPackage
        if '|' in current_project_path:
            raise QgsProcessingException(
                "ERRORE: Il progetto corrente è salvato DENTRO un GeoPackage!\n\n"
                "Questo script funziona solo con progetti salvati su disco (.qgs/.qgz).\n\n"
                "Per favore:\n"
                "1. Vai su: Progetto > Salva con nome\n"
                "2. Salva il progetto come file .qgs o .qgz su disco\n"
                "3. Riapri il progetto appena salvato\n"
                "4. Esegui nuovamente questo script"
            )

        # VALIDAZIONE: Verifica che il nuovo progetto sia nella stessa cartella del nuovo GeoPackage
        new_gpkg_dir = os.path.dirname(os.path.abspath(new_gpkg_full))
        new_project_dir = os.path.dirname(os.path.abspath(new_project_path))

        if new_gpkg_dir != new_project_dir:
            raise QgsProcessingException(
                f"ERRORE: Il nuovo progetto deve essere salvato nella stessa cartella del nuovo GeoPackage!\n"
                f"Cartella GeoPackage: {new_gpkg_dir}\n"
                f"Cartella Progetto: {new_project_dir}\n"
                f"Per mantenere i percorsi relativi (./) funzionanti, salva entrambi i file nella stessa directory."
            )

        # Estraiamo SOLO i nomi dei file (es. 'confini.gpkg' e 'confini_v2.gpkg')
        # Questo è il trucco: sostituiremo solo questi, fregandocene del percorso C:\... o ./...
        old_filename = os.path.basename(old_gpkg_full)
        new_filename = os.path.basename(new_gpkg_full)

        feedback.pushInfo(f"Target sostituzione: '{old_filename}' -> '{new_filename}'")

        # --- 2. COPIA DATI ---
        feedback.pushInfo(f"Copia GeoPackage...")
        try:
            shutil.copy2(old_gpkg_full, new_gpkg_full)
        except Exception as e:
            raise QgsProcessingException(f"Errore copia file gpkg: {e}")

        # --- 3. LETTURA PROGETTO (XML) ---
        feedback.pushInfo("Lettura codice sorgente del progetto...")
        project_content = ""
        is_qgz = current_project_path.endswith('.qgz')
        
        if is_qgz:
            try:
                with zipfile.ZipFile(current_project_path, 'r') as z:
                    # Troviamo il file .qgs dentro lo zip
                    qgs_list = [f for f in z.namelist() if f.endswith('.qgs')]
                    if not qgs_list:
                         raise QgsProcessingException("File .qgs non trovato nel pacchetto .qgz")
                    # Leggiamo il contenuto XML
                    with z.open(qgs_list[0]) as f:
                        project_content = f.read().decode('utf-8')
            except Exception as e:
                raise QgsProcessingException(f"Errore lettura QGZ: {e}")
        else:
            # File .qgs normale
            try:
                with open(current_project_path, 'r', encoding='utf-8') as f:
                    project_content = f.read()
            except Exception as e:
                raise QgsProcessingException(f"Errore lettura QGS: {e}")

        # --- 4. SOSTITUZIONE CHIRURGICA ---
        # Contiamo quante volte appare il nome del vecchio file
        count = project_content.count(old_filename)
        
        if count == 0:
            feedback.reportError(f"ERRORE CRITICO: La stringa '{old_filename}' non è stata trovata nel file di progetto!")
            feedback.reportError("Il file nel progetto potrebbe chiamarsi diversamente o essere codificato.")
            return {}
        
        feedback.pushInfo(f"Trovate {count} occorrenze di '{old_filename}'. Eseguo sostituzione...")
        
        # IL NOCCIOLO DELLA QUESTIONE:
        # Questo cambia 'source=\"./confini.gpkg|...\"' in 'source=\"./confini_v2.gpkg|...\"'
        new_project_content = project_content.replace(old_filename, new_filename)

        # --- 5. SCRITTURA NUOVO PROGETTO ---
        feedback.pushInfo(f"Salvataggio nuovo progetto: {new_project_path}")

        if new_project_path.endswith('.qgz'):
            try:
                with zipfile.ZipFile(new_project_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
                    # Il nome del file interno al .qgz dovrebbe idealmente matchare il nome del progetto
                    internal_name = os.path.basename(new_project_path).replace('.qgz', '.qgs')
                    zout.writestr(internal_name, new_project_content)
            except Exception as e:
                raise QgsProcessingException(f"Errore scrittura QGZ: {e}")
        else:
            try:
                with open(new_project_path, 'w', encoding='utf-8') as f:
                    f.write(new_project_content)
            except Exception as e:
                raise QgsProcessingException(f"Errore scrittura QGS: {e}")

        feedback.pushInfo("OPERAZIONE COMPLETATA.")
        feedback.pushInfo("Apri manualmente il nuovo progetto per verificare.")

        return {self.OUTPUT_PROJECT: new_project_path}