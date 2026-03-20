# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

### GoodNotes (Google Drive backup)

- **Carpeta raíz**: `1SLKkJ6eiW2g1QPv5bA7BDHI6_wJBEI7w`
- **Service account**: siendo-reader@dona-490704.iam.gserviceaccount.com
- **Key**: `.secrets/gdrive-service-account.json`
- **Script**: `scripts/gdrive-goodnotes.js` (recent/download/tree)
- **Contenido**: Mayormente archivo histórico (2019-2023). Monitorear `modifiedTime` para detectar nuevas notas.
- **Carpetas**:
  1. Actividad Frecuente (estudio, cursos, coaching)
  2. Revisión Mensual O Mayor (comités, productividad, equipo)
  3. Sueños Y Proyectos
  4. Archivo Y Respaldo (docs firmados, empresas, contratos)

### Calendarios Outlook (Condugas)

- **Condugas (comités/operativo)**: `https://outlook.office365.com/owa/calendar/8c12db6105eb4786b770ae61733320ed@condugas.com.co/6d8d874a98ef47e0a90ff3135a2caba43884463006160896695/calendar.ics`
- **Calendario personal**: `https://outlook.office365.com/owa/calendar/8c12db6105eb4786b770ae61733320ed@condugas.com.co/3155a61ea006408f919e5cee75d634c316960069565115828488/calendar.ics`
- **Formato**: ICS público (no requiere auth)
- **Timezone**: SA Pacific Standard Time (COL, UTC-5)

### Odoo (Condugas)

- **URL**: `https://condugas-sa.odoo.com`
- **API Key**: stored (provided 2026-03-18)
- **Usage**: ERP de Condugas — contabilidad, nómina, compras, proyectos

### Whoop

- **Client ID**: `9b9c4912-aa1a-4670-ad5d-781cca10368a`
- **Client Secret**: stored in env
- **Auth**: OAuth2 client_secret_post
- **Token endpoint**: `https://api.prod.whoop.com/oauth/oauth2/token`
- **API base**: `https://api.prod.whoop.com/developer/v1`
- **User ID**: 32141597
- **Endpoints confirmados**: /cycle (strain, HR, kilojoules)
- **Nota**: Recovery y sleep dan 404 — posiblemente requieren ciclo cerrado con sueño completo
- **Token caduca**: cada 3600s, usar refresh_token para renovar

**Consultar ciclos:**
```bash
curl -s -H "Authorization: Bearer $WHOOP_TOKEN" 'https://api.prod.whoop.com/developer/v1/cycle?limit=3'
```

### Limitless AI

- **API Key**: stored in env `LIMITLESS_API_KEY`
- **Endpoint**: `https://api.limitless.ai/v1/lifelogs`
- **Header**: `X-API-Key: $LIMITLESS_API_KEY`
- **Usage**: Transcripciones del día para briefing diario

**Consultar transcripciones de hoy:**
```bash
curl -s -H "X-API-Key: $LIMITLESS_API_KEY" "https://api.limitless.ai/v1/lifelogs?limit=3curl -s -H "X-API-Key: $LIMITLESS_API_KEY" "https://api.limitless.ai/v1/lifelogs?limit=10&date=$(date +%Y-%m-%d)"date=$(date +%Y-%m-%d)"
```

**Consultar transcripciones de ayer:**
```bash
curl -s -H "X-API-Key: $LIMITLESS_API_KEY" "https://api.limitless.ai/v1/lifelogs?limit=10&date=$(date -d yesterday +%Y-%m-%d)"
```
