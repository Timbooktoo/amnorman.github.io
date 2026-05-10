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

## Stap 2 — Zoek je Plaud headers

Plaud's API vereist sinds voorjaar 2026 twee dingen die je beide uit DevTools haalt: een **bearer token** én een **user-id hash**.

1. Ga naar [web.plaud.ai](https://web.plaud.ai) en log in
2. Open DevTools (F12) → tabblad **Network** → vink **Preserve log** aan
3. Klik in de Plaud-UI op **My Files** of een opname zodat er API-calls verschijnen
4. Klik op een request naar `api.plaud.ai/...` (filter eventueel op `api.plaud.ai`)
5. Onder **Request Headers** kopieer je twee waarden:
   - `authorization: Bearer eyJ...` → alleen het stuk **na** `Bearer ` → dit wordt `PLAUD_TOKEN`
   - `x-pld-user: <64-tekens hex>` → de hele hex-string → dit wordt `PLAUD_USER_ID`

> Zie je geen `x-pld-user` in de request headers? Stel hem dan niet in — de koppeling probeert zonder. Als je in Claude Desktop daarna `Plaud auth-fout` ziet, zoek hem alsnog en voeg toe.

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
        "PLAUD_TOKEN": "jouw-bearer-token",
        "PLAUD_USER_ID": "jouw-x-pld-user-waarde"
      }
    }
  }
}
```

Vervang beide waarden door wat je in stap 2 hebt gekopieerd.

> Optionele extra env-vars:
> - `PLAUD_DEVICE_ID` — standaardwaarde `[object Object]` (letterlijk, hardcoded; alleen overschrijven als Plaud's API verandert)
> - `PLAUD_TIMEZONE` — standaard `Europe/Brussels`
> - `PLAUD_EMAIL` + `PLAUD_PASSWORD` — alleen invullen als je wil dat de koppeling automatisch een nieuwe token ophaalt zodra de huidige verloopt

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
- Controleer of het bearer token correct is gekopieerd (geen spaties voor of na, en zonder het woord `Bearer`)
- Controleer of het JSON-bestand geldig is (geen ontbrekende komma's of haakjes)
- Herstart Claude Desktop opnieuw

**Foutmelding "Plaud auth-fout" of "invalid auth header"**
- `PLAUD_USER_ID` ontbreekt of klopt niet → kopieer hem opnieuw vers uit DevTools (zie stap 2)
- Token is ouder dan ~9 maanden → vraag een verse token aan via DevTools
- Bekijk de logs voor details: Claude Desktop → Settings → Developer → MCP logs → zoek regels die beginnen met `[plaud-mcp]`

**`uvx` wordt niet herkend**
- Sluit Terminal/PowerShell en open het opnieuw na de installatie
- Windows: gebruik het volledige pad naar `uvx.exe` (voer `where.exe uvx` uit in PowerShell)
- Zie [README](README.md#installing-without-uvx) voor de pip-installatiemethode als alternatief

**Server disconnected**
- Controleer dat `"args"` uit drie losse strings bestaat (zie config hierboven)
- Sla het bestand op en herstart Claude Desktop volledig
