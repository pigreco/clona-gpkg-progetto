# Changelog

Tutte le modifiche significative a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/it/1.0.0/),
e questo progetto aderisce al [Semantic Versioning](https://semver.org/lang/it/).

## [Non rilasciato]

### Aggiunto
- **Controllo progetti dentro GeoPackage**: Lo script ora rileva se il progetto corrente è salvato dentro un GeoPackage e blocca l'esecuzione con istruzioni chiare per l'utente
- Validazione che impedisce l'esecuzione se il nuovo progetto non è nella stessa cartella del nuovo GeoPackage
- Disclaimer nel README che avverte che l'algoritmo è in fase di testing
- Screenshot dell'interfaccia nel README
- File CHANGELOG.md con storico completo delle modifiche
- File CONTRIBUTING.md con guida per i contributori
- Configurazione per aggiornamento automatico del changelog (.changelogrc.json, .cliff.toml)
- GitHub Actions workflow per aggiornamento automatico del changelog

### Modificato
- Migliorato `shortHelpString()` con informazioni più dettagliate e strutturate
- Aggiornato README con nuove funzionalità e note importanti
- Messaggio di errore più chiaro e dettagliato quando il progetto non è salvato

### Rimosso
- Rimossa funzionalità sperimentale di salvataggio progetto nel GeoPackage (non supportata adeguatamente dalle API di QGIS)

## [0.1.0] - 2025-01-28

### Aggiunto
- Rilevamento automatico del GeoPackage utilizzato nel progetto corrente
- Precompilazione automatica del campo "GeoPackage ORIGINALE" nell'interfaccia
- Metodo `_find_current_gpkg()` che cerca il primo GeoPackage tra i layer del progetto
- Gestione di percorsi relativi e conversione in percorsi assoluti

### Modificato
- Parametro `INPUT_GPKG` ora include `defaultValue` con il GeoPackage rilevato automaticamente

## [0.0.1] - 2025-01-28

### Aggiunto
- Prima versione dello script "Clona GeoPackage e Progetto (Metodo Chirurgico XML)"
- Copia di un GeoPackage esistente in una nuova posizione
- Modifica chirurgica del file di progetto QGIS (.qgs/.qgz)
- Sostituzione di tutti i riferimenti al vecchio GeoPackage con il nuovo
- Supporto per progetti compressi (.qgz) e non compressi (.qgs)
- Mantenimento dei percorsi relativi intatti
- Conteggio e report delle occorrenze sostituite
- Gestione errori per progetti non salvati
- README con documentazione completa
- File LICENSE

[Non rilasciato]: https://github.com/pigreco/clona-gpkg-progetto/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/pigreco/clona-gpkg-progetto/compare/v0.0.1...v0.1.0
[0.0.1]: https://github.com/pigreco/clona-gpkg-progetto/releases/tag/v0.0.1
