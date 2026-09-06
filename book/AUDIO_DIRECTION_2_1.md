# Zmierenie — Audio Direction 2.1

**Status:** PERFORMANCE REVISION / CONTENT FROZEN / VOICE PROFILE LOCKED / CALIBRATION RENDERED / LISTENING DECISION PENDING
**Date:** 2026-09-05
**Scope:** nanovo vyrenderovať 12 audioreflexií bez zmeny ich schváleného textu.

## Autoritatívny text
Zdrojový scenár zostáva nezmenený: `book/audio-script-master-sk-2026-09-01.md`.
PDF zostáva immutable. Táto revízia mení iba interpretáciu hlasu.

## Dôvod revízie
Obsah reflexií je schválený a funguje. Súčasné syntetické čítanie je miestami príliš herecké: priveľa dramatického zdvíhania hlasu, emocionálnych oblúkov, akcelerácie a zosilnenia najmä v druhých poloviciach a záveroch nahrávok.

Predchádzajúci release použil `eleven_multilingual_v2` s `stability=0.31`, `similarity_boost=0.75`, `style=0`, `speed=0.96`, `use_speaker_boost=true`. Nízkou stability sa vysvetľuje časť nežiaducej expresivity; ElevenLabs pri nižšej stability povoľuje širší emočný rozsah a vyššiu variabilitu.

## Voice interview — rozhodnutia Jozefa, 5. 9. 2026
1. Pri prirodzenej prednáške hovorí malej skupine približne ôsmich ľudí.
2. Najviac mu prekáža hereckosť: v druhej polovici a záveroch sa neprirodzene mení tempo a zosilňuje hlas. Chce stabilnejší prejav.
3. Dôležitú vetu prirodzene uvedie krátkou pauzou a potom ju povie o trochu dôraznejšie; nepotrebuje výrazné zvýšenie hlasu.
4. Záverečná otázka má byť osobná, tichšia, veľmi nenásilná a s miernym odľahčením.
5. Pri citlivých témach má byť hlas osobný a empatický. Patetickosť začína tam, kde prejav začne znieť hraný; vyhnúť sa „talianskemu“, teatrálnemu prednesu.
6. Tempo sa medzi analytickou a osobnou časťou môže prirodzene meniť; nemá byť mechanicky jednotné.
7. Séria má pôsobiť ako osobný podcastový dovetok ku kapitole. Dovetok môže byť dramaturgicky aj na konci kapitoly; nemusí fungovať ako úvod.
8. Hlavná negatívna inštrukcia: **„Nerob ma lepším, akým som.“** Hlas nemá Jozefa idealizovať, zväčšovať ani estetizovať.

## Zhrnutý interpretačný profil
- predstav si približne 8 poslucháčov, nie veľkú sálu;
- osobný podcastový dovetok, nie kázeň, audiokniha ani meditátorský výkon;
- stabilná hlasová energia, bez postupného dramatického „nabiehania“;
- prirodzené malé zmeny tempa podľa významu;
- dôležitý bod: krátka pauza pred vetou + mierny dôraz, nie zosilnenie do punch-line;
- citlivé témy: osobné a empatické, ale bez hraného smútku, vážnosti či vznešenosti;
- záverečná otázka: tichšie, osobne, nenásilne, mierne odľahčene;
- cieľom nie je „lepší hlas“, ale rozpoznateľná obyčajná Jozefova prednášková reč.

### Nerobiť
- herecké zdvíhanie hlasu;
- emocionálne swelly a dramatické oblúky;
- zrýchľovanie alebo zosilňovanie druhej polovice;
- patetické spomaľovanie;
- mystický/meditačný tón záverečnej otázky;
- teatrálny „taliansky“ prednes;
- estetizovanie Jozefa na uhladenejšiu alebo charizmatickejšiu verziu, než je jeho prirodzený prejav.

## ElevenLabs — kalibrácia
Najprv zachovať `eleven_multilingual_v2`, aby sa izolovala zmena réžie od zmeny modelu. Pri tomto modeli sa samostatný režijný prompt neposiela ako osobitný API parameter; hlavné páky sú voice settings, prirodzené členenie textu a regenerácia.

Rovnaký kompletný text kapitoly 03 generovať v troch variantoch:
- A: stability 0.58 / similarity 0.80 / style 0 / speed 0.98 / speaker boost on
- B: stability 0.65 / similarity 0.80 / style 0 / speed 0.97 / speaker boost on
- C: stability 0.72 / similarity 0.80 / style 0 / speed 0.97 / speaker boost on

Preferovaný kandidát pred posluchovým testom: B. Kapitola 03 je kalibračná, lebo kombinuje vysvetľovací tón, citlivú vážnejšiu pasáž a osobnú záverečnú otázku.

## Režijný brief — pre Studio / budúci model s direction prompting
Read this in Jozef's ordinary speaking voice, as if he were talking to a small group of about eight people after a lecture. This is a personal podcast-style afterthought to a chapter, not acting, preaching, audiobook narration, guided meditation, or dramatic storytelling. Keep the vocal energy stable across the whole piece. Allow small natural changes of pace between analytical and personal passages, but do not build intensity toward the second half or the ending. Before a genuinely important sentence, a short natural pause is appropriate; then give the sentence only slightly more emphasis, without raising the voice into a punch line. On sensitive subjects, sound personal and empathetic without performing sadness, solemnity, or moral gravity. Avoid theatrical pitch rises, emotional swells, suspense, exaggerated pauses, or an Italian-style dramatic delivery. The final question should be quieter, personal, non-intrusive and slightly lighter in tone, like a real question offered to eight listeners rather than a meditative climax. Do not make Jozef sound more polished, charismatic, profound, warm, or dramatic than he naturally is. The governing rule is: do not make him better than he is; make him recognizably himself.

## Historicky overená vykonávacia cesta
Pôvodná ElevenLabs produkcia už existovala a používala Professional Voice Clone `Jozef`. Produkčný receipt z 1. 9. 2026 a aktuálny lokálny `.env` potvrdzujú voice ID `GgshSttSyBqEDNtKedLz`. Starší identifikátor `htSeFhhpBaCgJzL05q6C` je neaktuálny a 6. 9. 2026 vrátil ElevenLabs `voice_not_found`.

Lokálny runner pôvodnej produkčnej vetvy:
`C:\Users\zufki\Claude\Projects\web tf.truni.sk\scripts\listening-edition\generate_audio.py`

Lokálne prostredie / secret boundary:
`C:\Users\zufki\Claude\Projects\web tf.truni.sk\scripts\listening-edition\`

`.env` bol pri pôvodnej produkcii uložený mimo zdrojového kódu a gitignored. Secret sa nikdy nekopíruje do GitHubu, Drive, chatu ani receiptov. Audio 2.1 má znovu použiť tento existujúci runner a existujúci lokálny secret, nie nový účet ani nový TTS provider.

Aktuálny technický stav 6. 9. 2026: Remote Desktop command channel je znovu funkčný. Kalibračná kapitola 03 bola lokálne vyrenderovaná vo všetkých troch profiloch A/B/C bez zmeny textu a bez zásahu do produkčných MP3. Výsledky sú pripravené na posluchové rozhodnutie Jozefa; až potom sa smie zvolený profil aplikovať na 12 kapitol.

Cloudový fallback v GitHub Actions je pripravený, ale je `workflow_dispatch` only a správne sa nespúšťa bez `ELEVENLABS_API_KEY` secretu v GitHub Actions. Kľúč sa do GitHubu neprenáša automaticky.

## Produkčný postup
1. Texty 12 reflexií nemeníme.
2. Voice profil je uzamknutý týmto dokumentom.
3. Prvý reálny render: iba kapitola 03, profil B, ako samostatný kalibračný MP3; živý audio súbor sa neprepisuje.
4. Po readbacku MP3 sa overí veľkosť, SHA-256, trvanie a dostupnosť na vypočutie.
5. Jozef vyhodnotí prirodzenosť; až podľa výsledku sa prípadne použije A/C alebo jemná úprava B.
6. Zvolený profil sa aplikuje na 12 kapitol; kvôli nedeterministickému TTS sa každá nahrávka stále samostatne posluchovo skontroluje.
7. Pred výmenou live MP3 sa urobí 12/12 QA: prirodzenosť, stabilita energie, tempo, dôrazy, pauzy, výslovnosť, absencia hereckosti, záverečná otázka a správne mapovanie kapitoly ↔ audio.
8. Starý audio release zostáva rollbackom, kým nový 12/12 neprejde QA.
