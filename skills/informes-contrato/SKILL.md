---
name: informes-contrato
description: Generador de informes financieros y operativos para contratos de Condugas. Analiza P&G, producción, costos, márgenes y tendencias de contratos de gas y acueducto. Activar cuando el usuario envíe un Excel de contrato, un PBI, pida análisis de producción vs costos, P&G por contrato, margen operativo, evolución mensual, comparación YoY, o cualquier análisis de desempeño de un contrato específico (OYMA, OYM Z2, Boyacá, Valle, Jericó, Floridablanca, Bucaramanga, Pérdidas, etc). También activar cuando pida extraer datos de Odoo para generar el informe, o cuando mencione análisis cruzado con indicadores macroeconómicos.
---

# Informes de Contrato — Condugas

Generador de análisis financiero-operativo para contratos de infraestructura de gas y acueducto.

## Fuentes de datos (en orden de preferencia)

1. **Excel enviado por Sebastián** — P&G, base de asientos contables, producción
2. **Odoo** — API disponible (`condugas-sa.odoo.com`, ver TOOLS.md)
3. **Power BI** — Archivos .pbix (extraer modelo de datos)
4. **Web** — Indicadores macro (IPC, IPP, tasa BanRep, PIB sector, etc.)

## Estructura del Excel base (referencia OYMA)

### Hoja "PRODUCCION OYMA"
Columnas: MES, PRODUCCION, ANHO, ADMINISTRACION, COSTO DIRECTO, COSTOS TOTALES, UAI
- Granularidad: mensual
- PRODUCCION = ingresos facturados al cliente (EPM)
- COSTOS TOTALES = sumatoria de costos operativos
- UAI = Utilidad Antes de Impuestos (Producción - Costos Totales)

### Hoja "BASE AD"
Columnas: Cuenta, Nombre Cuenta, Nit, Nombre Nit, Documento Ref, Fecha, Nro Registro, Comprobante, Procedencia, Documento, Detalle, Centro De Costos, Debito, Credito, Saldo, Tipo, Naturaleza
- 132,000+ registros de asientos contables
- Centro de Costos: 7001 (Admin), 7002 (Operativo), etc.
- Plan de cuentas colombiano (4xxx ingresos, 5xxx gastos, 6xxx costos)

## Tres capas de análisis obligatorias

### Capa 1: Análisis Lineal (lo obvio, lo directo)
- Producción mensual y tendencia (MoM, YoY)
- Margen operativo (UAI/Producción) por mes
- Costos totales vs producción — ratio de eficiencia
- Evolución de costos directos vs admin
- Comparación acumulada YTD actual vs anterior
- Top 10 proveedores/terceros por monto
- Concentración de costos por tipo de cuenta

### Capa 2: Elementos aparentemente no conectados
- **Estacionalidad**: ¿los meses de baja producción coinciden con algo? (lluvias, festivos, ciclos EPM)
- **Anomalías**: meses donde UAI es negativo — ¿qué pasó? Cruzar con detalle de BASE AD
- **Proveedores nuevos**: ¿aparecen NITs nuevos en periodos de costos altos?
- **Correlación nómina vs producción**: ¿más gente = más producción?
- **Reintegros y deducciones**: patrones de descuentos a empleados (celulares, materiales)
- **Cruces entre contratos**: traslados de inventario entre CIAs (Condugas Comercial, Urabá, Mantenimiento Z3)

### Capa 3: Contexto macro y sectorial
Buscar en web y agregar comparación con:
- **IPC y IPP Colombia** — impacto en reajustes de contrato
- **Tasa BanRep** — costo financiero implícito
- **Sector gas/acueducto** — noticias regulatorias, EPM, GDO
- **Riesgo regional** — indicadores del departamento donde opera
- **Ciclo de inversión pública** — licitaciones, presupuestos municipales
- **Tipo de cambio** — si hay insumos importados

## Formato de salida

```
## 1. Resumen Ejecutivo
(3 líneas máximo — estado del contrato en una frase, tendencia, alerta principal)

## 2. Métricas Clave
| Métrica | Periodo Actual | Anterior | Var % | Señal |
|---------|---------------|----------|-------|-------|

## 3. Análisis de Producción
(Gráfico tendencia + comentario de tendencia MoM/YoY)

## 4. Análisis de Costos
(Desglose por tipo, top proveedores, evolución)

## 5. Margen y Eficiencia
(UAI/Producción, tendencia, meses negativos y por qué)

## 6. Elementos No Lineales
(Hallazgos de la Capa 2 — anomalías, correlaciones, patrones ocultos)

## 7. Contexto Macro
(Indicadores relevantes y cómo impactan este contrato)

## 8. Riesgos y Alertas
(Máximo 5, priorizados)

## 9. Recomendaciones
(3-5 acciones concretas)

## 10. Brechas de Información
([DATO FALTANTE] con impacto declarado)
```

## Contratos conocidos de Condugas
| Contrato | Analítica Odoo | Cliente | Tipo |
|----------|---------------|---------|------|
| O&M Aguas (OYMA) | - | EPM | Acueducto |
| O&M Z2 | 6 | EPM | Gas |
| Boyacá | 1 | - | Gas |
| Bucaramanga | 2 | - | Gas |
| Floridablanca | 3 | - | Gas |
| Jericó | 4 | EPM | Gas |
| Valle | 9 | GDO | Gas |
| Pérdidas | 8 | EPM | Gas |
| OZZLO | 7 | - | - |
| Admin Central | 10 | - | Overhead |

## Restricciones
- NO inventar datos. Usar `[DATO FALTANTE]` si falta algo.
- Separar claramente datos del Excel vs supuestos vs datos macro.
- Si el Excel tiene inconsistencias, declararlas explícitamente.
- Priorizar hallazgos accionables sobre descripciones.
- Gráficos y tablas siempre que haya datos.

## Archivo de análisis recurrentes
Mantener `references/informes-generados.md` actualizado con cada informe que se genera, para trackear evolución y no repetir.
