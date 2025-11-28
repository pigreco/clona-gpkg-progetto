from qgis.core import (
    QgsProcessing,
    QgsProcessingAlgorithm,
    QgsProcessingParameterFile,
    QgsProcessingParameterFileDestination,
    QgsProcessingParameterString,
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
            "Questo script ignora le impostazioni di QGIS e modifica direttamente "
            "il codice XML del file di progetto.\n"
            "Sostituisce il nome del file vecchio con quello nuovo ovunque lo trovi (anche nei percorsi relativi ./).\n"
            "Nota: Assicurati di salvare il Nuovo Progetto nella stessa cartella (o una sottocartella simile) rispetto al Nuovo GeoPackage, altrimenti il percorso relativo ./ potrebbe non trovare il file."
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