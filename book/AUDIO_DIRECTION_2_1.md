# Zmierenie — Audio Direction 2.1

**Status:** PERFORMANCE REVISION / CONTENT FROZEN
**Date:** 2026-09-05
**Scope:** nanovo vyrenderovať 12 audioreflexií bez zmeny ich schváleného textu.

## Autoritatívny text
Zdrojový scenár zostáva nezmenený: `book/audio-script-master-sk-2026-09-01.md`.
PDF zostáva immutable. Táto revízia mení iba interpretáciu hlasu.

## Dôvod revízie
Obsah reflexií je schválený a funguje. Súčasné syntetické čítanie je miestami príliš herecké: priveľa dramatického zdvíhania hlasu, emocionálnych oblúkov a dôrazov, ktoré nezodpovedajú prirodzenému prednáškovému prejavu Jozefa.

Predchádzajúci release použil `eleven_multilingual_v2` s `stability=0.31`, `similarity_boost=0.75`, `style=0`, `speed=0.96`, `use_speaker_boost=true`. Nový baseline má odstrániť prehnanú expresivitu.

## Cieľový prejav
- prirodzený slovenský mužský hlas Jozefa, nie herecká interpretácia;
- skúsený vysokoškolský pedagóg, ktorý hovorí malej skupine alebo jednému poslucháčovi;
- prednáškovo-konverzačný tón: jasný, premýšľavý, vecný, ľudský;
- pokojná energia bez patetickosti;
- dôrazy iba tam, kde by vznikli prirodzene pri vysvetľovaní myšlienky;
- minimálne melodické „hranenie“ viet;
- nezdvíhať hlas pri dramatických alebo citlivých vetách;
- nevytvárať umelé napätie pred pointou;
- otázky na konci nevyslovovať mysticky ani teatrálne — ako skutočnú otázku poslucháčovi;
- prirodzené krátke pauzy medzi významovými celkami, nie prehnané ticho;
- záver mierne spomaliť, ale bez meditátorského afektu.

## ElevenLabs — pracovný baseline
Model: najprv zachovať `eleven_multilingual_v2`, aby sme izolovali zmenu réžie od zmeny modelu.

Testovať rovnaký úsek v troch variantoch:
- A: stability 0.58 / similarity 0.80 / style 0 / speed 0.98 / speaker boost on
- B: stability 0.65 / similarity 0.80 / style 0 / speed 0.97 / speaker boost on
- C: stability 0.72 / similarity 0.80 / style 0 / speed 0.97 / speaker boost on

Preferovaný kandidát pred posluchovým testom: B.

## Režijný prompt pre ElevenLabs
Read this in Jozef's natural speaking voice, as an experienced university lecturer speaking to a small group or to one attentive listener. The delivery should feel like thoughtful live teaching, not acting, narration, preaching, meditation performance, or dramatic storytelling. Keep the voice grounded, calm, intellectually clear, warm but restrained. Use natural conversational intonation and only modest emphasis where a lecturer would spontaneously stress an important idea. Avoid theatrical rises in pitch, emotional swells, emphatic punch lines, suspense, solemnity, and exaggerated pauses. Do not raise the voice on sensitive or dramatic sentences. Let difficult ideas remain serious without performing seriousness. Keep a steady, unhurried pace with small natural variations. Pauses should follow meaning and breathing, not create drama. The final question should sound like a genuine open question offered to the listener, slightly slower and softer, but still natural and unsentimental. Overall impression: Jozef explaining something he has thought about deeply, in his ordinary lecture voice, with presence and simplicity.

## Voice interview — otázky na doladenie
Voice má Jozefovi klásť otázky po jednej, nie ako dotazník. Cieľom je zachytiť jeho prirodzený prednáškový prejav.

1. Keď prednášaš dobre a cítiš sa prirodzene, komu máš pocit, že hovoríš — celej miestnosti, malej skupine alebo jednému konkrétnemu človeku?
2. Čo ti na súčasných nahrávkach znie najviac cudzo: výška hlasu, tempo, príliš silné dôrazy, dlhé pauzy, alebo celková „hereckosť“?
3. Keď chceš na prednáške zdôrazniť dôležitú vetu, čo robíš prirodzene — spomalíš, stíšiš hlas, zopakuješ myšlienku, alebo mierne zvýšiš dôraz?
4. Ako znie tvoj prirodzený záver pri otázke pre poslucháčov? Skôr vecne, osobne, tichšie, alebo s malým úsmevom/odľahčením?
5. Pri citlivých témach — zranenie, moc, hanba, konflikt — chceš znieť viac neutrálne-odborne alebo osobne a empaticky? Kde je hranica, za ktorou už cítiš patetickosť?
6. Je prirodzené, aby sa tempo medzi analytickou a osobnou časťou trochu menilo, alebo chceš takmer jednotné tempo celej série?
7. Má séria pôsobiť skôr ako krátke pokračovanie prednášky, alebo ako osobný podcastový dovetok ku kapitole?
8. Keby si mal jednou vetou povedať ElevenLabs, čomu sa má pri imitovaní tvojho hlasu za každú cenu vyhnúť, čo by to bolo?

Po odpovediach Voice zhrnie iba 5–7 režijných pravidiel a jeden krátky negatívny zoznam „nerobiť“. Nesmie meniť text reflexií.

## Produkčný postup
1. Texty 12 reflexií nemeníme.
2. Voice rozhovor doplní iba interpretačný profil.
3. Vyberie sa jedna reprezentatívna kapitola na A/B/C kalibráciu.
4. Porovnajú sa tri stability pri identickom texte a ostatných nastaveniach.
5. Zvolený profil sa aplikuje na 12 kapitol.
6. Pred výmenou live MP3 sa urobí posluchový QA všetkých 12: prirodzenosť, tempo, dôrazy, pauzy, výslovnosť, absencia hereckosti a správne mapovanie kapitoly ↔ audio.
7. Starý audio release zostáva rollbackom, kým nový 12/12 neprejde QA.
