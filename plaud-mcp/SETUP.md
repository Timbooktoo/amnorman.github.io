# Plaud Note instellen in Claude Desktop

Deze handleiding legt uit hoe je jouw Plaud Note-opnames beschikbaar maakt in Claude Desktop. Eénmalig instellen, daarna werkt het automatisch.

---

## Wat heb je nodig?

- Claude Desktop (al geïnstalleerd)
- Je Plaud-accountgegevens (email + wachtwoord)
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

## Stap 2 — Pas de Claude Desktop config aan

### Zoek het configuratiebestand

**macOS**
1. Open Finder
2. Druk op `Cmd + Shift + G`
3. Plak: `~/Library/Application Support/Claude/`
4. Open `claude_desktop_config.json` in een teksteditor

**Windows**
1. Open Verkenner
2. Plak in de adresbalk: `%APPDATA%\Claude`
3. Open `claude_desktop_config.json` in Kladblok of een andere teksteditor

> Het bestand bestaat nog niet? Maak het aan met precies die naam op die locatie.

### Voeg de Plaud-koppeling toe

Vervang de inhoud van het bestand (of voeg toe als er al iets in staat) met:

```json
{
  "mcpServers": {
    "plaud": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/timbooktoo/amnorman.github.io#subdirectory=plaud-mcp",
        "plaud-mcp"
      ],
      "env": {
        "PLAUD_EMAIL": "jouw@email.com",
        "PLAUD_PASSWORD": "jouwwachtwoord"
      }
    }
  }
}
```

Vervang `jouw@email.com` en `jouwwachtwoord` door je eigen Plaud-gegevens.

> **Heb je al andere servers in je config?** Voeg dan alleen het `"plaud": { ... }` blok toe binnen de bestaande `"mcpServers"` sectie.

---

## Stap 3 — Herstart Claude Desktop

Sluit Claude Desktop volledig af en open het opnieuw. Bij de eerste vraag over je opnames downloadt Claude de koppeling automatisch — dit duurt een halve minuut.

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
- Controleer of email en wachtwoord correct zijn in de config
- Controleer of het JSON-bestand geldig is (geen ontbrekende komma's of haakjes)
- Herstart Claude Desktop opnieuw

**`uvx` wordt niet herkend**
- Sluit Terminal/PowerShell en open het opnieuw na de installatie
- macOS: voer `source ~/.bashrc` of `source ~/.zshrc` uit

**Het bestand `claude_desktop_config.json` bestaat niet**
- Maak het aan als nieuw tekstbestand met exact die naam op de aangegeven locatie
