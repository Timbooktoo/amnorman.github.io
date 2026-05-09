---
name: food-audit
description: Voer een interne voedselveiligheidsaudit uit op basis van FSSC 22000, BRC Global Standard of IFS Food. Gebruik dit wanneer een gebruiker een interne audit wil uitvoeren, auditbevindingen wil vastleggen of een auditrapport wil genereren. Scant de repository naar bestaande voedselveiligheidsdocumenten en stelt gerichte vragen per clausule.
---

# Interne Voedselveiligheidsaudit Skill

Begeleidt Claude bij het uitvoeren van een gestructureerde interne voedselveiligheidsaudit op basis van FSSC 22000 (v6), BRC Global Standard for Food Safety (Issue 9) of IFS Food (versie 8). Analyseert bestaande documenten in de repository en stelt gerichte vragen aan de auditor per hoofdstuk/clausule. Alle interactie verloopt in het Nederlands.

---

## Auditorjargon en classificaties

| Code | Naam | Definitie |
|------|------|-----------|
| **C** | Conformiteit | Voldoet aan de eis, bewijs aanwezig |
| **OFI** | Kans op verbetering | Conformiteit aanwezig, maar verbetering wenselijk |
| **OBS** | Observatie | Kleine tekortkoming zonder directe impact op voedselveiligheid |
| **MNC** | Kleine non-conformiteit | Gedeeltelijke afwijking van een eis, voedselveiligheid niet in gevaar |
| **HNC** | Grote non-conformiteit | Volledige afwijking van een eis of meerdere kleine NCs voor dezelfde eis |
| **KR** | Kritieke bevinding | Directe bedreiging voor voedselveiligheid (BRC/IFS) |

Deadlines corrigerende maatregelen: **KR = onmiddellijk**, **HNC = 30 dagen**, **MNC = 90 dagen**

---

## Workflow

Maak een takenlijst van alle stappen in deze workflow en werk ze één voor één af.

### Stap 1 — Initialisatie

Stel de volgende vragen in één bericht aan de gebruiker:

```
Welkom bij de interne voedselveiligheidsaudit assistent.

Voordat we beginnen, heb ik enkele gegevens nodig:

1. **Bedrijfsnaam / locatie**: Welk bedrijf of welke locatie wordt geauditeerd?
2. **Auditor**: Wat is uw naam (interne auditor)?
3. **Auditdatum**: Wat is de datum van de audit? (standaard: vandaag)
4. **Norm**: Welke norm wilt u auditeren?
   - A) FSSC 22000 (versie 6)
   - B) BRC Global Standard for Food Safety (Issue 9)
   - C) IFS Food (versie 8)
5. **Scope**: Wilt u de volledige audit uitvoeren of specifieke hoofdstukken?
   - Volledig (alle hoofdstukken)
   - Gedeeltelijk (geef aan welke hoofdstukken, bijv. "alleen HACCP en traceerbaarheid")
6. **Productcategorie**: Wat voor type voedingsproducten produceert het bedrijf?
```

Sla de antwoorden op als context voor alle volgende stappen en voor het rapport.

### Stap 2 — Documentverkenning

Zoek systematisch naar voedselveiligheidsdocumenten in de huidige werkdirectory:

```bash
find . -type f \( \
  -iname "*haccp*" -o -iname "*hazard*" -o -iname "*gevaar*" -o \
  -iname "*kwaliteit*" -o -iname "*quality*" -o -iname "*handboek*" -o -iname "*manual*" -o \
  -iname "*procedure*" -o -iname "*werkinstructie*" -o -iname "*sop*" -o \
  -iname "*traceer*" -o -iname "*traceability*" -o \
  -iname "*allergen*" -o -iname "*allergeen*" -o \
  -iname "*schoonmaak*" -o -iname "*cleaning*" -o -iname "*hygi*" -o \
  -iname "*certific*" -o -iname "*brc*" -o -iname "*fssc*" -o -iname "*ifs*" -o \
  -iname "*audit*" -o -iname "*inspectie*" -o \
  -iname "*leverancier*" -o -iname "*supplier*" -o \
  -iname "*kalibratie*" -o -iname "*calibrat*" -o \
  -iname "*temperatuur*" -o -iname "*temperature*" -o -iname "*monitoring*" -o \
  -iname "*klacht*" -o -iname "*complaint*" -o -iname "*recall*" -o -iname "*terugroep*" -o \
  -iname "*risico*" -o -iname "*risk*" -o -iname "*food_fraud*" -o -iname "*vaccp*" \
\) 2>/dev/null | sort
```

Lees de gevonden bestanden indien relevant. Maak een **documentinventaris**:

| Document | Bestandspad | Relevant voor |
|----------|-------------|---------------|
| (per gevonden document invullen) | | |

Communiceer naar de gebruiker welke documenten gevonden zijn en welke ontbreken. Begin daarna met de audit.

### Stap 3 — Audit uitvoeren per clausule

Doorloop de clausules van de gekozen norm interactief. Groepeer vragen per thema (max 7 per ronde). Verwijs altijd naar gevonden documenten ("Ik heb uw HACCP-plan gevonden — wanneer was de laatste herziening?"). Registreer elke bevinding direct (zie Stap 4).

---

#### NORM A: FSSC 22000 versie 6

**[H4] Context van de organisatie**
```
1. Beschikt u over een gedocumenteerde contextanalyse (interne/externe kwesties, 
   behoeften van belanghebbenden)? Is deze bijgewerkt?
2. Is er een gedocumenteerde FSMS-scope (welke producten, locaties en processen zijn 
   inbegrepen/uitgesloten)?
3. Zijn alle relevante wet- en regelgevende eisen geïdentificeerd (nationaal + EU)?
4. Is het FSMS geïntegreerd in de bedrijfsprocessen?
```

**[H5] Leiderschap**
```
1. Is er een ondertekend voedselveiligheidsbeleid, gecommuniceerd naar alle medewerkers?
2. Zijn rollen, verantwoordelijkheden en bevoegdheden schriftelijk vastgelegd?
3. Is er een benoemde Voedselveiligheidsmanager (Food Safety Team Leader) 
   met aantoonbare opleiding?
4. Ondersteunt het topmanagement actief het FSMS (deelname directiebeoordeling, 
   beschikbaar stellen middelen)?
```

**[H6] Planning**
```
1. Is er een risicoanalyse voor het FSMS (risico's en kansen) met bijbehorende maatregelen?
2. Zijn voedselveiligheidsdoelstellingen SMART geformuleerd en worden deze gemonitord?
3. Is er een wijzigingsbeheer-procedure voor geplande wijzigingen in het FSMS?
```

**[H7] Ondersteuning**
```
1. Is er een actuele competentiematrix voor functies met invloed op voedselveiligheid?
2. Worden trainings- en opleidingsbehoeften jaarlijks geëvalueerd, inclusief 
   effectiviteitscontrole na trainingen?
3. Is de documentatiestructuur beschreven (beheer, versiebeheer, archivering, bewaartermijnen)?
4. Is er een intern en extern communicatieplan voor voedselveiligheid?
```

**[H8.1] Randvoorwaardenprogramma's (PRPs)**
```
1. Zijn PRPs gedocumenteerd voor (bevestig welke aanwezig zijn):
   □ Gebouwconstructie en -indeling
   □ Reiniging en desinfectie
   □ Plaagbeheersing
   □ Waterbeheersing
   □ Afvalbeheer
   □ Leveranciersbeoordeling
   □ Preventie van kruiscontaminatie
   □ Persoonlijke hygiëne
2. Worden PRPs regelmatig geverifieerd? Is er bewijs (registraties)?
```

**[H8.2] HACCP-plan**
```
1. Is het HACCP-plan gebaseerd op de 7 Codex-beginselen, inclusief volledig 
   processchema en productbeschrijving?
2. Is er een volledige gevarenanalyse (biologisch, chemisch, fysisch, allergenen)?
3. Zijn CCPs geïdentificeerd met kritische grenzen, monitoring, corrigerende maatregelen 
   en verificatieactiviteiten, inclusief registraties?
4. Wanneer was de laatste herziening van het HACCP-plan?
5. Zijn alle HACCP-teamleden getraind? Zijn trainingsbewijzen aanwezig?
```

**[H8.3] Traceerbaarheid**
```
1. Dekt het traceerbaarheidssysteem de volledige keten 
   ("one step back, one step forward")?
2. Is de traceertijd getest en gedocumenteerd? Wat was het resultaat?
3. Is er een gedocumenteerde recall/terugroepprocedure? 
   Wanneer was de laatste mock recall?
```

**[H8.4] Allergenen**
```
1. Is er een actuele lijst van alle aanwezige allergenen (grondstoffen, 
   hulpstoffen, reinigingsmiddelen)?
2. Is er een allergenenbeheerplan inclusief maatregelen voor kruisbesmetting 
   (scheiding, productieplanning, schoonmaakvalidatie)?
3. Worden allergeninformatie op etiketten gecontroleerd bij receptuurwijzigingen?
4. Worden medewerkers getraind in allergenenrisico's?
```

**[H8.5] Vreemdlichaambeheer & overige beheersmaatregelen**
```
1. Is er een vreemdlichaambeleid (glas, hard plastic, metaaldetectie/röntgen)? 
   Worden detectieapparaten gecalibreerd en gevalideerd?
2. Zijn er maatregelen voor het voorkomen van chemische contaminatie?
3. Worden leverancierscertificaten en specificaties bijgehouden voor kritische grondstoffen?
4. Is er een procedure voor het beheer van non-conform product 
   (identificatie, segregatie, vrijgave/vernietiging)?
```

**[H9] Prestatie-evaluatie**
```
1. Is er een jaarlijks intern auditprogramma dat alle FSMS-elementen dekt?
   Worden audits uitgevoerd door bevoegde, onafhankelijke auditeurs?
2. Worden auditbevindingen gedocumenteerd en tijdig opgevolgd?
3. Is er een formele directiebeoordeling (management review)? 
   Wanneer was de laatste beoordeling?
4. Worden KPIs voor voedselveiligheid gemonitord en gerapporteerd?
```

**[H10] Verbetering**
```
1. Is er een procedure voor non-conformiteiten en corrigerende maatregelen 
   (inclusief oorzaakanalyse)?
2. Worden klachten geregistreerd, geanalyseerd en gebruikt voor verbetering?
3. Kunt u een voorbeeld geven van een recente systeemverbetering?
```

---

#### NORM B: BRC Global Standard for Food Safety Issue 9

**[§1] Senior management commitment**
```
1. Is er een ondertekend voedselveiligheids- en kwaliteitsbeleid gecommuniceerd 
   naar alle niveaus?
2. Plant het senior management voedselveiligheidsbijeenkomsten? 
   Is er bewijs van opvolging (notulen)?
3. Is er een Food Fraud Vulnerability Assessment (VACCP)?
4. Is er een Food Defence plan (bescherming tegen opzettelijke besmetting)?
5. Zijn voedselveiligheidsdoelstellingen meetbaar en worden ze gemonitord?
```

**[§2] Voedselveiligheidsplan — HACCP**
```
1. Is het HACCP-plan gedocumenteerd op basis van Codex Alimentarius 7 principes?
2. Omvat de gevarenanalyse: biologisch, chemisch, fysisch, allergenen, 
   voedselfraude en food defence?
3. Zijn CCPs en/of oPRPs geïdentificeerd met kritische grenzen, monitoring, 
   corrigerende maatregelen en verificatie?
4. Wanneer was de laatste volledige herziening van het HACCP-plan?
5. Worden HACCP-registraties bijgehouden en regelmatig geverifieerd?
```

**[§3] Kwaliteitsmanagementsysteem**
```
1. Is er een gedocumenteerd documentbeheersysteem (versies, goedkeuring, archivering)?
2. Is er een intern auditprogramma dat alle BRC-eisen dekt (minstens jaarlijks)?
3. Is er een Approved Supplier List? Hoe worden nieuwe leveranciers beoordeeld?
4. Is er een procedure voor specificatiebeheer (grondstoffen, eindproducten, verpakking)?
5. Is er een klachtenbeheersysteem met trendanalyse?
6. Worden CAPA's (corrigerende en preventieve maatregelen) systematisch beheerd?
```

**[§4] Locatienormen**
```
1. Is de locatie-indeling gedocumenteerd? Zijn hoog/laag-risicozones gescheiden?
2. Is er een gevalideerd reinigings- en desinfectieprogramma?
   Worden microbiologische oppervlaktemonsters genomen?
3. Is er een gedocumenteerd plaagbeheerprogramma (intern/extern)? 
   Zijn trendrapporten beschikbaar?
4. Is er een onderhoudsprogramma voor gebouwen en apparatuur?
5. Zijn wateranalyses beschikbaar (kwaliteit, legionella indien van toepassing)?
```

**[§5] Productbeheersing**
```
1. Is er een volledig allergenenbeheerplan inclusief kruisbesmettingsrisicoanalyse?
   Worden allergenenschoonmaken gevalideerd?
2. Is er een Food Authenticity Assessment (VACCP) met geïmplementeerde maatregelen?
3. Worden productspecificaties regelmatig herzien bij wijzigingen?
4. Is er een procedure voor etiketcontrole en -goedkeuring?
5. Is er een gevalideerd houdbaarheidsonderzoek voor eindproducten?
```

**[§6] Procesbeheersing**
```
1. Zijn productie-instructies en toleranties gedocumenteerd voor kritische processen?
2. Worden meet- en meetmiddelen gekalibreerd? Is er een kalibratieprogramma 
   met registraties?
3. Is er een gelabeld en gesegregeerd systeem voor non-conform product?
4. Worden productcontroles (gewicht, temperatuur, organoleptisch) geregistreerd?
5. Is er een formele procedure voor vrijgave van eindproducten?
```

**[§7] Personeel**
```
1. Is er een persoonlijke hygiënebeleid? Worden nieuwe medewerkers en bezoekers 
   geïnformeerd?
2. Is er een trainingsmatrix? Worden trainingen op effectiviteit beoordeeld?
3. Is er een ziekteverzuimbeleid voor voedselveiligheidskritische ziekten 
   (maag-darm, geelzucht, huidinfecties)?
4. Worden medewerkers getraind in allergenenbewustzijn?
5. Is er een beleid voor sieraden, nagels, haar en persoonlijke bezittingen 
   in productiegebieden?
```

---

#### NORM C: IFS Food versie 8

**[H1] Governance en betrokkenheid**
```
1. Is er een ondertekend voedselveiligheids- en kwaliteitsbeleid gecommuniceerd 
   naar alle medewerkers?
2. Is er een Food Defence beoordeling met geïmplementeerde maatregelen?
3. Is er een VACCP (Food Fraud Vulnerability Assessment)?
4. Zijn voedselveiligheidsdoelstellingen meetbaar en worden deze gemonitord?
5. Voert het topmanagement regelmatig een management review uit met opvolging?
```

**[H2] Voedselveiligheids- en kwaliteitsmanagementsysteem**
```
1. Is het HACCP-plan volledig gedocumenteerd (gevarenanalyse, CCPs, monitoring, verificatie)?
2. Is er een documentbeheerprocedure (versies, goedkeuring, archivering, bewaartermijnen)?
3. Is er een intern auditprogramma dat alle IFS-vereisten dekt?
4. Is er een Approved Supplier List met risicogebaseerde leveranciersbeoordeling?
5. Is er een klachten- en incidentbeheerprocedure met trendanalyse?
```

**[H3] Middelenbeheer**
```
1. Is er een trainingsmatrix en worden opleidingsbehoeften jaarlijks beoordeeld?
   Zijn trainingsbewijzen aanwezig voor voedselveiligheidskritische functies?
2. Is er een persoonlijke hygiënebeleid inclusief training bij indiensttreding?
3. Is er een ziekteverzuimbeleid voor voedselveiligheidskritische ziekten?
4. Zijn onderhoud en kalibratie van apparatuur gedocumenteerd en bijgehouden?
5. Zijn wateranalyses beschikbaar (microbiologisch en chemisch)?
```

**[H4] Planning en productieproces**
```
1. Is de locatie-indeling gedocumenteerd? Zijn risicozones gescheiden?
2. Is er een gevalideerd reinigings- en desinfectieprogramma met verificatieresultaten?
3. Is er een allergenenbeheerplan met kruisbesmettingsanalyse en 
   gevalideerde allergenenschoonmaken?
4. Zijn productiespecificaties en toleranties gedocumenteerd voor kritische processen?
5. Dekt het traceerbaarheidssysteem "one step back, one step forward"? 
   Is de traceertijd getest?
6. Is er een recall-procedure? Wanneer was de laatste mock recall?
7. Worden producten vrijgegeven via een formeel vrijgaveproces?
```

**[H5] Metingen, analyses en verbetering**
```
1. Is er een intern auditprogramma (frequentie, scope, bevoegdheid van auditeurs)?
2. Worden product- en procesmonitoringresultaten geanalyseerd voor verbetering?
3. Is er een CAPA-systeem met root cause analyses?
4. Zijn er KPIs voor voedselveiligheid en kwaliteit, gerapporteerd aan het management?
5. Kunt u een voorbeeld geven van recente continue verbetering?
```

---

### Stap 4 — Bevindingen registreren

Na elk blok vragen, leg per clausule vast:
- Clausulenummer en omschrijving
- Bewijsstuk (gevonden document of antwoord van auditor)
- Classificatie: **C / OFI / OBS / MNC / HNC / KR**
- Toelichting (max 2 zinnen)
- Bij MNC/HNC/KR: beschrijf de vereiste corrigerende maatregel en deadline

### Stap 5 — Genereer het auditrapport

Na het doorlopen van alle geselecteerde clausules, genereer het rapport en sla op als:
`audit-rapport-[NORM]-[DATUM]-[BEDRIJFSNAAM].md`
(bijv. `audit-rapport-FSSC22000-2026-05-09-BakkerijDeGouden.md`)

Gebruik het volgende sjabloon:

---

```markdown
# Intern Audit Rapport — Voedselveiligheid

---

## Rapportgegevens

| Veld | Waarde |
|------|--------|
| **Bedrijf / Locatie** | [BEDRIJFSNAAM] |
| **Productcategorie** | [PRODUCTTYPE] |
| **Norm** | [NORM + VERSIE] |
| **Auditdatum** | [DATUM] |
| **Auditor (intern)** | [NAAM AUDITOR] |
| **Auditscope** | [VOLLEDIG / GEDEELTELIJK: specificeer hoofdstukken] |
| **Rapportdatum** | [RAPPORTDATUM] |
| **Rapportstatus** | Concept |

---

## Uitvoerende Samenvatting

### Algemene beoordeling

[2-4 zinnen over de algemene status van het voedselveiligheidsmanagementsysteem]

### Conformiteitsscore

| Classificatie | Aantal | % van geauditeerde clausules |
|---------------|--------|------------------------------|
| Conformiteit (C) | [n] | [%] |
| Kans op verbetering (OFI) | [n] | [%] |
| Observatie (OBS) | [n] | [%] |
| Kleine non-conformiteit (MNC) | [n] | [%] |
| Grote non-conformiteit (HNC) | [n] | [%] |
| Kritieke bevinding (KR) | [n] | [%] |
| **Totaal geauditeerd** | **[n]** | **100%** |

### Sterke punten

- [Sterk punt 1]
- [Sterk punt 2]

### Aandachtsgebieden

- [Aandachtsgebied 1]
- [Aandachtsgebied 2]

---

## Bevindingen per Clausule

### [Sectie, bijv. "FSSC 22000 — H4: Context van de organisatie"]

| Clausule | Eis (samenvatting) | Bevinding | Classificatie | Opmerking |
|----------|--------------------|-----------|---------------|-----------|
| 4.1 | [eis] | [bevinding] | C | [toelichting] |

[Herhaal per hoofdstuk/sectie]

---

## Non-conformiteiten

### Grote Non-conformiteiten (HNC) — deadline 30 dagen

| # | Clausule | Beschrijving | Vereiste maatregel | Deadline | Status |
|---|----------|--------------|--------------------|----------|--------|
| HNC-01 | [clausule] | [beschrijving] | [maatregel] | [datum] | Open |

### Kleine Non-conformiteiten (MNC) — deadline 90 dagen

| # | Clausule | Beschrijving | Vereiste maatregel | Deadline | Status |
|---|----------|--------------|--------------------|----------|--------|
| MNC-01 | [clausule] | [beschrijving] | [maatregel] | [datum] | Open |

### Kritieke Bevindingen (KR) — onmiddellijke actie vereist

| # | Clausule | Beschrijving | Vereiste actie | Status |
|---|----------|-------------|----------------|--------|
| KR-01 | [clausule] | [beschrijving] | [actie] | **URGENT** |

*(Verwijder secties die niet van toepassing zijn)*

---

## Observaties en Kansen voor Verbetering

| # | Clausule | Observatie / OFI | Aanbeveling |
|---|----------|-----------------|-------------|
| OBS-01 | [clausule] | [observatie] | [aanbeveling] |
| OFI-01 | [clausule] | [kans] | [aanbeveling] |

---

## Documentbeoordeling

| Document | Aangetroffen | Actueel | Opmerking |
|----------|-------------|---------|-----------|
| Kwaliteitshandboek | ✓ / ✗ | Ja / Nee / Onbekend | |
| HACCP-plan | ✓ / ✗ | | |
| PRP-documenten | ✓ / ✗ | | |
| Traceerbaarheidsprocedure | ✓ / ✗ | | |
| Allergenenbeleid | ✓ / ✗ | | |
| Reinigingsprogramma | ✓ / ✗ | | |
| Trainingsmatrix | ✓ / ✗ | | |
| Intern auditprogramma | ✓ / ✗ | | |
| Leveranciersgoedkeuringslijst | ✓ / ✗ | | |
| Recall-procedure | ✓ / ✗ | | |
| Directiebeoordeling (laatste) | ✓ / ✗ | | |

---

## Opvolgingsplan

| Ref. | Maatregel | Verantwoordelijke | Deadline | Verificatiemethode |
|------|-----------|-------------------|----------|--------------------|
| HNC-01 | [maatregel] | [naam/functie] | [datum] | [hoe te verifiëren] |
| MNC-01 | [maatregel] | [naam/functie] | [datum] | [hoe te verifiëren] |

---

## Handtekeningen / Accordering

| Rol | Naam | Datum | Handtekening |
|-----|------|-------|--------------|
| Interne auditor | [naam] | [datum] | _________________ |
| Voedselveiligheidsmanager | [naam] | [datum] | _________________ |
| Directie / Management | [naam] | [datum] | _________________ |

---

## Bijlagen

- Bijlage A: Documentinventaris (gevonden bestanden in repository)
- Bijlage B: Auditchecklist (gestelde vragen en antwoorden)

---

*Intern gebruik — ter voorbereiding op externe certificeringsaudits.*
*Norm: [NORM] | Skill versie: 1.0 | Gegenereerd op: [DATUM]*
```

---

### Stap 6 — Afsluitende samenvatting

Geef de gebruiker een afsluitende samenvatting:

```
## Audit afgerond

**Bedrijf**: [naam]  
**Norm**: [norm + versie]  
**Auditdatum**: [datum]  
**Scope**: [volledig/gedeeltelijk]

### Resultaten op hoofdlijnen:
- ✅ Conformiteiten: [n]
- 📋 OFI's / Observaties: [n]
- ⚠️ Kleine non-conformiteiten (MNC): [n]
- 🔴 Grote non-conformiteiten (HNC): [n]
- 🚨 Kritieke bevindingen (KR): [n]

### Rapport opgeslagen als:
`[bestandsnaam].md`

### Aanbevolen vervolgstappen:
1. [Urgentste actie, bijv. "Sluit HNC-01 binnen 30 dagen af"]
2. [Tweede prioriteit]
3. Bespreek rapport met het voedselveiligheidsteam en/of directie

Het rapport is klaar voor bespreking en verdere opvolging.
```

## Onderbreking tussentijds

Als de audit niet volledig is afgerond, bied de gebruiker de volgende opties:

```
De audit is gedeeltelijk uitgevoerd. Nog niet geauditeerde clausules:
[lijst]

Wilt u:
A) Verdergaan waar we gebleven zijn
B) Een tussentijds rapport genereren met de huidige bevindingen
C) De audit later hervatten (ik vat de openstaande punten samen)
```
