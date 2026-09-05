# Zmierenie Release 2.0 — fakultný server-native deployment

## Cieľ
Nasadiť viacstránkovú webovú učebnicu priamo na fakultnú infraštruktúru bez závislosti od GitHub Pages a bez ručnej editácie Drupal node 621, pokiaľ živá stránka stále používa pôvodný iframe pattern.

## Overený deployment artefakt
GitHub Actions workflow `Build Faculty Release` vytvára jeden reprodukovateľný balík z adresára `book/`.

Aktuálne overený artefakt:
- názov: `zmierenie-faculty-release-2.0`
- workflow run: `33991350715`
- artifact id: `9976720470`
- veľkosť ZIP artefaktu: `39 730 356 B`
- artifact digest: `sha256:4eee43c57a16b4b537721e886099da86ea01fee5387a376075e248e6a16964da`
- build/inspection/upload: PASS
- simulovaný HTTP deploy pod `/sites/default/files/zmierenie/`: PASS

HTTP smoke-test rozbalil release presne do budúcej fakultnej cesty a overil všetkých 12 kapitol, index, CSS, JS a range requesty na audio 01 a 12.

Vo vnútri artefaktu je `zmierenie-faculty-release-2.0.tar.gz` a jeho `.sha256`. Samotný tarball obsahuje webový release s `DEPLOYMENT.json` a `SHA256SUMS` pre jednotlivé súbory.

## Predpoklad existujúcej produkcie
Pôvodný produkčný balík používal Drupal Full HTML iframe:
`/sites/default/files/zmierenie/index.html`

Ak je tento iframe na `https://tf.truni.sk/zmierenie-ucebnica` stále aktívny, node 621 sa nemení. Mení sa iba statický balík v adresári `sites/default/files/zmierenie/`.

## Obsah Release 2.0
Zdrojom balíka je obsah adresára `book/` v tomto repozitári. Do cieľového adresára sa nasadí obsah `book/` priamo do koreňa, takže výsledok obsahuje napr.:
- `index.html`
- `chapter-01.html` až `chapter-12.html`
- `uvod.html`, `zaver.html`, `prilohy.html`, `literatura.html`
- `chapter.css`, `chapter.js`, `book-ui.css`, `book.js`, `theme-bridge.js`
- `audio/`

Stabilné PDF zostáva mimo tohto balíka na:
`https://tf.truni.sk/sites/default/files/book/zmierenie-ucebnica.pdf`

## Odporúčaný release pattern
Na serveri nepoužívať deštruktívne prepisovanie bez rollbacku. Odporúčaná štruktúra:

```text
sites/default/files/zmierenie-releases/
  2.0-<timestamp>/
sites/default/files/zmierenie -> zmierenie-releases/2.0-<timestamp>/
```

Ak hosting/súborový systém nepovoľuje symlink v public files, použiť dočasný adresár + atómové premenovanie:
1. nahrať do `zmierenie.new/`,
2. smoke-test súborov,
3. `zmierenie/` premenovať na `zmierenie.prev/`,
4. `zmierenie.new/` premenovať na `zmierenie/`,
5. po live QA ponechať `zmierenie.prev/` do ukončenia rollback okna.

## Akceptačný test
Pred označením LIVE COMPLETE overiť anonymne:
1. `/zmierenie-ucebnica` HTTP 200,
2. obsah knihy ukazuje 12 kapitol,
3. kapitoly 01, 05, 11 a 12 sa otvoria,
4. audio na týchto kapitolách sa načíta,
5. pri audiu je označenie syntetického hlasu,
6. PDF odkaz vracia stabilné finálne PDF,
7. mobilná šírka bez horizontálneho overflow,
8. poznámky/progres fungujú v localStorage,
9. žiadne 404 na lokálnych CSS/JS/audio assetoch.

## Rollback
Ak smoke-test zlyhá, okamžite obnoviť predchádzajúci adresár/symlink. Drupal node ani PDF sa pri tomto deployment pattern-e nemenia.

## Produkčná hranica
Deploy sa vykoná až cez autorizovaný SSH/SFTP/Git/hostingový kanál. Žiadne heslá ani secrets sa neukladajú do repozitára.