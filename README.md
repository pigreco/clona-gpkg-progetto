# Clona GeoPackage e Progetto (Metodo Chirurgico XML)

Script QGIS Processing per duplicare un GeoPackage e aggiornare automaticamente i riferimenti nel progetto QGIS utilizzando la modifica diretta del codice XML.

## 📋 Descrizione

Questo script ignora le impostazioni di QGIS e modifica direttamente il codice XML del file di progetto. Sostituisce il nome del file GeoPackage vecchio con quello nuovo ovunque lo trovi (anche nei percorsi relativi `./`).

## ✨ Caratteristiche

- Copia un GeoPackage esistente in una nuova posizione
- Modifica chirurgicamente il file di progetto QGIS (`.qgs` o `.qgz`)
- Sostituisce tutti i riferimenti al vecchio GeoPackage con il nuovo
- Supporta sia progetti compressi (`.qgz`) che non compressi (`.qgs`)
- Mantiene percorsi relativi intatti

## 🚀 Utilizzo

1. Apri il tuo progetto QGIS che usa il GeoPackage da duplicare
2. **Salva il progetto** (importante: lo script richiede un progetto salvato su disco)
3. Esegui lo script tramite la Processing Toolbox
4. Fornisci i seguenti parametri:
   - **GeoPackage ORIGINALE**: Il file `.gpkg` attuale
   - **Salva NUOVO GeoPackage come**: Il percorso e nome del nuovo file `.gpkg`
   - **Salva NUOVO Progetto come**: Il percorso e nome del nuovo progetto (`.qgs` o `.qgz`)

## ⚠️ Note Importanti

- Assicurati di salvare il Nuovo Progetto nella stessa cartella (o una sottocartella simile) rispetto al Nuovo GeoPackage, altrimenti il percorso relativo `./` potrebbe non trovare il file
- Il progetto corrente deve essere salvato prima di eseguire lo script
- Lo script conta e riporta quante occorrenze del vecchio nome file sono state trovate e sostituite
- Dopo l'esecuzione, apri manualmente il nuovo progetto per verificare che tutto funzioni correttamente

## 📦 Installazione

1. Copia il file `clona_gpkg_progetto.py` nella cartella degli script di QGIS:
   - Linux: `~/.local/share/QGIS/QGIS3/profiles/default/processing/scripts/`
   - Windows: `C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\processing\scripts\`
   - macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/processing/scripts/`

2. Riavvia QGIS o aggiorna gli script dalla Processing Toolbox

## 🔧 Requisiti

- QGIS 3.x
- Python 3.x (incluso con QGIS)

## 📝 Licenza

Vedi il file [LICENSE](LICENSE) per i dettagli.

## 🤝 Contributi

Contributi, problemi e richieste di funzionalità sono benvenuti!

## 👤 Autore

**pigreco**

---

*Metodo Chirurgico XML - Modifica diretta del codice sorgente del progetto QGIS*