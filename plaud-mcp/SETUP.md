# Plaud Note instellen in Claude Desktop

Deze handleiding legt uit hoe je jouw Plaud Note-opnames beschikbaar maakt in Claude Desktop. Eénmalig instellen, daarna werkt het automatisch.

---

## Wat heb je nodig?

- Claude Desktop (al geïnstalleerd)
- Je Plaud bearer token (zie hieronder)
- `uv` — een klein hulpprogramma om de koppeling te draaien

---

## Stap 1 — Installeer `uv`

**macOS / Linux** — open Terminal en voer uit:
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows** — open PowerShell en voer uit:
```
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Sluit Terminal / PowerShell daarna en open het opnieuw.

---

## Stap 2 — Zoek je Plaud bearer token

1. Ga naar [plaud.ai](https://www.plaud.ai) en log in
2. Open de browser DevTools (F12) → tabblad **Network**
3. Laad een pagina opnieuw en zoek een API-aanroep naar `api.plaud.ai`
4. Kopieer de waarde na `Bearer ` uit de `Authorization` header

---

## Stap 3 — Pas de Claude Desktop config aan

### Zoek het configuratiebestand

**macOS**
1. Open Finder → `Cmd + Shift + G` → plak: `~/Library/Application Support/Claude/`
2. Open `claude_desktop_config.json`

**Windows**
1. Open Verkenner → plak in adresbalk: `%APPDATA%\Claude`
2. Open `claude_desktop_config.json`

> Het bestand bestaat nog niet? Maak het aan met precies die naam op die locatie.

### Voeg de Plaud-koppeling toe

```json
{
  "mcpServers": {
    "plaud": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Timbooktoo/amnorman.github.io#subdirectory=plaud-mcp",
        "plaud-mcp"
      ],
      "env": {
        "PLAUD_TOKEN": "jouw-bearer-token"
      }
    }
  }
}
```

Vervang `jouw-bearer-token` door het token uit stap 2.

> **Windows:** als `uvx` niet werkt, zie de [README](README.md#installing-without-uvx) voor de alternatieve installatiemethode met pip.

> **Heb je al andere servers in je config?** Voeg dan alleen het `"plaud": { ... }` blok toe binnen de bestaande `"mcpServers"` sectie.

---

## Stap 4 — Herstart Claude Desktop

Sluit Claude Desktop volledig af (systeemvak → Afsluiten) en open het opnieuw.

---

## Controleer of het werkt

Stel Claude de volgende vraag:

> "Lijst mijn Plaud-opnames"

Als het goed is zie je een overzicht van je opnames. Je kunt daarna ook vragen:

- "Geef me de samenvatting van \[naam opname\]"
- "Zoek opnames over \[onderwerp\]"
- "Welke opnames heb ik deze week gemaakt?"

---

## Problemen?

**Claude toont geen Plaud-opnames**
- Controleer of het bearer token correct is gekopieerd (geen spaties voor of na)
- Controleer of het JSON-bestand geldig is (geen ontbrekende komma's of haakjes)
- Herstart Claude Desktop opnieuw

**`uvx` wordt niet herkend**
- Sluit Terminal/PowerShell en open het opnieuw na de installatie
- Windows: gebruik het volledige pad naar `uvx.exe` (voer `where.exe uvx` uit in PowerShell)
- Zie [README](README.md#installing-without-uvx) voor de pip-installatiemethode als alternatief

**Server disconnected**
- Controleer dat `"args"` uit drie losse strings bestaat (zie config hierboven)
- Sla het bestand op en herstart Claude Desktop volledig
