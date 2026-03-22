# Optimización de Tokens — Plan de Eficiencia

## Lo que gastó tokens hoy
1. **Procesar Excel 466k registros 3+ veces** (mismo cálculo repetido)
2. **Generar HTML completo desde cero** (presentaciones largas)
3. **Análisis iterativo** (correcciones múltiples)
4. **Búsqueda de colores** (grep extensivo)

## Optimizaciones inmediatas

### 1. Pre-procesar datos una sola vez
```bash
# Crear summaries permanentes
python3 scripts/condugas-summary.py > datos/summary-2026-03.json
# Reutilizar el JSON, no reprocesar Excel
```

### 2. Templates reutilizables
```html
<!-- Template base presentación -->
<style>/* Paleta Condugas fija */</style>
<div class="slide-template">{{content}}</div>
```
- Generar contenido, no estructura completa
- Paletas de marca guardadas como CSS

### 3. Scripts especializados por tarea
```javascript
// scripts/odoo-quick-check.js - 3 líneas de output
// scripts/excel-monthly-summary.js - solo datos necesarios
// scripts/contratos-status.js - semáforo automático
```

### 4. Cachear análisis frecuentes
```json
// cache/contratos-jan2026.json
{"oyma": {"prod": 1263, "uai": -280, "margin": -22.2}}
```

### 5. Subagents para procesamiento pesado
- **Análisis Excel** → subagent especializado
- **Generación reportes** → subagent con templates
- **Yo coordino**, ellos procesan

## Plan específico próximos días

### Mañana (20 marzo):
1. Crear `scripts/excel-to-json.py` (una vez)
2. Guardar summaries en `datos/`
3. Template base presentaciones en `templates/`

### Datos vs análisis:
- **Scripts hacen datos** (rápido, local)
- **Yo hago análisis** (preguntas, insights, decisiones)
- **Reutilizar en lugar de regenerar**

### Ejemplo optimizado:
```bash
# En lugar de procesar 466k registros:
cat datos/summary-mar2026.json | jq '.enero2026.contratos' 
# 50 tokens vs 5000 tokens
```

## Métricas objetivo
- **Antes**: 466k registros → 5000+ tokens
- **Después**: Summary JSON → 200 tokens
- **Saving**: 95% menos tokens para mismo output

## ¿Priorizamos qué optimizar primero?
1. **Excel processing** (mayor impacto)
2. **Presentación templates** 
3. **Scripts de análisis rápido**
4. **Subagents para tareas pesadas**