# Guida al Contributo

Grazie per l'interesse nel contribuire a questo progetto!

## Come Contribuire

1. Fai un fork del repository
2. Crea un branch per la tua feature (`git checkout -b feature/nome-feature`)
3. Committa le tue modifiche seguendo le convenzioni (vedi sotto)
4. Pusha il branch (`git push origin feature/nome-feature`)
5. Apri una Pull Request

## Convenzioni per i Commit

Questo progetto utilizza [Conventional Commits](https://www.conventionalcommits.org/it/) per mantenere il changelog organizzato.

### Formato

```
<tipo>: <descrizione breve>

[corpo opzionale]

[footer opzionale]
```

### Tipi di Commit

- `feat:` - Nuova funzionalità (aggiunta alla sezione "Aggiunto" del CHANGELOG)
- `fix:` - Correzione di bug (aggiunta alla sezione "Corretto")
- `docs:` - Modifiche alla documentazione
- `refactor:` - Refactoring del codice (sezione "Modificato")
- `perf:` - Miglioramenti delle prestazioni
- `test:` - Aggiunta o modifica di test
- `chore:` - Modifiche che non cambiano il codice sorgente
- `style:` - Modifiche di formattazione
- `ci:` - Modifiche ai file di configurazione CI

### Esempi

```bash
# Nuova funzionalità
git commit -m "feat: aggiungi validazione percorsi GeoPackage e progetto"

# Correzione bug
git commit -m "fix: correggi gestione percorsi relativi su Windows"

# Documentazione
git commit -m "docs: aggiorna README con screenshot interfaccia"

# Refactoring
git commit -m "refactor: migliora metodo _find_current_gpkg per maggiore leggibilità"
```

## Aggiornamento Manuale del CHANGELOG

Se preferisci aggiornare manualmente il CHANGELOG, segui il formato [Keep a Changelog](https://keepachangelog.com/it/1.0.0/):

1. Apri `CHANGELOG.md`
2. Nella sezione `[Non rilasciato]`, aggiungi la tua modifica sotto la categoria appropriata:
   - **Aggiunto** - per nuove funzionalità
   - **Modificato** - per modifiche a funzionalità esistenti
   - **Deprecato** - per funzionalità che saranno rimosse
   - **Rimosso** - per funzionalità rimosse
   - **Corretto** - per correzioni di bug
   - **Sicurezza** - per vulnerabilità corrette

### Esempio

```markdown
## [Non rilasciato]

### Aggiunto
- Validazione che impedisce l'esecuzione se i file non sono nella stessa cartella

### Corretto
- Risolto problema con percorsi Unicode su Windows
```

## Aggiornamento Automatico del CHANGELOG

### Opzione 1: GitHub Actions (automatico)

Il workflow `.github/workflows/changelog.yml` aggiorna automaticamente il CHANGELOG quando una PR viene mergiata su `main`.

### Opzione 2: git-cliff (manuale)

Installa git-cliff:
```bash
cargo install git-cliff
```

Genera il changelog:
```bash
# Aggiorna il CHANGELOG con tutti i commit
git cliff --config .cliff.toml --output CHANGELOG.md

# Genera il changelog per una versione specifica
git cliff --config .cliff.toml --tag v0.2.0 --output CHANGELOG.md
```

### Opzione 3: auto-changelog (manuale)

Installa auto-changelog:
```bash
npm install -g auto-changelog
```

Genera il changelog:
```bash
auto-changelog --config .changelogrc.json
```

## Versionamento

Questo progetto segue il [Semantic Versioning](https://semver.org/lang/it/):

- **MAJOR** (X.0.0): Modifiche incompatibili con versioni precedenti
- **MINOR** (0.X.0): Nuove funzionalità compatibili con versioni precedenti
- **PATCH** (0.0.X): Correzioni di bug compatibili con versioni precedenti

### Creazione di una Nuova Release

1. Aggiorna il CHANGELOG spostando le modifiche da `[Non rilasciato]` a una nuova versione
2. Crea un tag git:
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```

## Testing

Prima di inviare una PR:

1. Testa lo script su QGIS con diversi tipi di progetti (.qgs e .qgz)
2. Verifica il funzionamento con percorsi relativi e assoluti
3. Controlla che la documentazione sia aggiornata

## Stile del Codice

- Segui le convenzioni PEP 8 per il codice Python
- Usa commenti chiari e descrittivi
- Mantieni le funzioni brevi e focalizzate
- Documenta le funzioni complesse con docstring

## Domande?

Apri una [issue](https://github.com/pigreco/clona-gpkg-progetto/issues) per domande o discussioni!
