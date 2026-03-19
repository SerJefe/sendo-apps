# 🎯 Siendo — Workspace de Sebastián Sánchez

Asistente integral operado por IA. Conecta calendarios, transcripciones, Odoo, GoodNotes y más para briefings diarios y gestión ejecutiva.

## Estructura

```
├── SOUL.md                  # Identidad y vibe del asistente
├── USER.md                  # Perfil de Sebastián
├── MEMORY.md                # Memoria de largo plazo
├── TOOLS.md                 # APIs, calendarios, credenciales (referencias)
├── HEARTBEAT.md             # Checklist del heartbeat (briefing, radar, etc)
├── IDENTITY.md              # Nombre y emoji del asistente
├── AGENTS.md                # Reglas de comportamiento del workspace
├── tareas-activas.md        # Tareas priorizadas (actualizado diariamente)
│
├── archivos/
│   ├── briefing_system.md   # Formato de briefing de 9 secciones
│   ├── asistente_personal.xlsx
│   └── perfil_sebastian_gpt5.md
│
├── memory/
│   └── YYYY-MM-DD.md        # Logs diarios
│
├── reportes/
│   ├── cxp_dashboard.html   # Dashboard CxP interactivo (Chart.js, offline)
│   └── cxp_snapshot_*.json  # Snapshots semanales para comparar tendencia
│
├── scripts/
│   ├── gdrive-goodnotes.js  # Acceso a GoodNotes via Google Drive API
│   └── odoo-cxp-report.js   # Genera snapshot CxP desde Odoo
│
├── Guias_seguidores/        # 60+ herramientas HTML interactivas (SERJEFE)
└── condugas-inbox-agent/    # Micro-servicio clasificador correos/WhatsApp
```

## Integraciones activas

| Servicio | Estado | Notas |
|----------|--------|-------|
| **Odoo** (Condugas) | ✅ | API vía JSON-RPC. Dashboard CxP en Finance. Cron cada 3h. |
| **Limitless AI** | ✅ | Transcripciones diarias para briefing |
| **Google Drive** (GoodNotes) | ✅ | Service account, backup de cuadernos (archivo histórico 2019-2023) |
| **Calendarios Outlook** | ⚠️ | ICS conectados, pero solo muestran 2025. Pendiente calendario 2026. |
| **Whoop** | ⚠️ | OAuth2 configurado, pero recovery/sleep dan 404 |
| **Todoist** | ❓ | Inbox agent existe, verificar si sigue en uso |

## Briefing diario

Se ejecuta automáticamente entre 5:00-9:00 AM COL con el formato de 9 secciones:

1. Panorama en una frase
2. Lo más importante detectado (máx 5)
3. Pendientes activos reales
4. Riesgos o tensiones (máx 5)
5. Recomendación de foco (sí/no/delegar)
6. Acciones prioritarias (3-7 con impacto y urgencia)
7. Ajuste personal según energía
8. Oportunidades con IA (máx 3)
9. Vacíos de información

Formato completo en `archivos/briefing_system.md`.

## Reportes

### Dashboard CxP (Odoo)
- **En Odoo**: Tableros → Finance → "Sanidad CxP - Pagos Pendientes" (ID 17)
  - 4 gráficos: barras proveedor, barras vencimiento, pie distribución, línea tendencia
  - Datos en tiempo real desde account.move.line
- **HTML offline**: `reportes/cxp_dashboard.html` (abrir en browser)
- **Snapshot semanal**: `node scripts/odoo-cxp-report.js`

### Filtros guardados en Odoo
- 📊 CxP Sanidad - Todos los pendientes
- 🔴 CxP Vencidas
- 📅 CxP Aging por Vencimiento

## Cron jobs activos

| Job | Frecuencia | Qué hace |
|-----|-----------|----------|
| Revisión Odoo | Cada 3 horas | Revisa pagos draft, mensajes y actividades pendientes |
| Briefing matutino | Diario 5-9 AM COL | Calendario + Limitless + tareas → briefing 9 secciones |

## Scripts

```bash
# Listar archivos recientes en GoodNotes
node scripts/gdrive-goodnotes.js recent 7

# Descargar un PDF de GoodNotes
node scripts/gdrive-goodnotes.js download <fileId> <output.pdf>

# Generar snapshot CxP desde Odoo
node scripts/odoo-cxp-report.js
```

## Equipo Condugas (referencia rápida)

| Nombre | Rol | Odoo |
|--------|-----|------|
| Andre (Andrea Bernal) | Dir. Financiero | user 20, partner 860 |
| Ema (Emanuel Quevedo) | Desarrollador | partner 1053 (sin usuario) |
| Sebastián | Gerente | user 19, partner 865 |

---

*Workspace mantenido por Siendo 🎯 — Asistente integral de Sebastián Sánchez Acevedo*
