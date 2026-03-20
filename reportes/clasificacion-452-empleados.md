# Clasificación Estratégica 452 Empleados Condugas

## Marco de Clasificación con Gobierno de Datos

### Principio Base: "Solo eliminar con datos duros y sin riesgo contractual"

## Categoría A: MANTENER (Estimado 180-220 personas)

### Subcategoría A1: Operativos Contractuales (120-150 personas)
**Criterio:** Aparecen explícitamente en contratos con clientes o son requeridos por normativa.

**Ejemplos identificados:**
- **Técnicos de gas:** Requeridos por EPM en OYMA R1
- **Supervisores HSEQ:** Obligatorios por normativa en todos los contratos
- **Operadores equipos:** Específicos por contrato Valle/Boyacá
- **Personal certificado:** Con licencias específicas para cada proyecto

**Validación:** Revisar cada contrato cliente y verificar headcount mínimo requerido.

### Subcategoría A2: Decisores/Estratégicos (25-35 personas)
**Criterio:** Toman decisiones que impactan P&L o relaciones clave.

**Lista actual conocida:**
- **Sebastián** (CEO)
- **Directores:** Juan Guillermo, Cami, Carlos, Andrea, William, Nelson, Natalia, Claudia
- **Gerentes de obra** por contrato principal
- **Coordinadores técnicos** con autonomía de decisión
- **Relacionistas clave** con clientes (EPM, GDO, etc.)

**Validación:** ¿Sus decisiones afectan resultado mensual >$50M?

### Subcategoría A3: Especialistas Únicos (25-35 personas)
**Criterio:** Conocimiento/relación que no se puede reemplazar a corto plazo.

**Ejemplos:**
- **Especialista normativa** específica por cliente
- **Técnicos equipos especiales** (solo ellos saben operarlos)
- **Relacionistas proveedores** clave (descuentos/términos especiales)

**Validación:** ¿Su salida implicaría >3 meses recuperar capacidad?

## Categoría B: OPTIMIZAR (Estimado 100-150 personas)

### Subcategoría B1: Productivos Parciales (60-80 personas)
**Criterio:** 30-70% del tiempo en tareas productivas, resto automatizable.

**Perfiles típicos:**
- **Coordinadores** que mezclan gestión humana con reportes rutinarios
- **Analistas** que hacen análisis real pero también compilación de data
- **Asistentes** que apoyan decisores pero también hacen tareas rutinarias

**Optimización:** Mantener persona, automatizar las tareas rutinarias, enfocar en valor humano.

### Subcategoría B2: Reentrenables (40-70 personas)
**Criterio:** Capacidad demostrada pero en funciones que se automatizan.

**Ejemplos:**
- **Contadores** que hacen conciliación manual → análisis financiero estratégico
- **Coordinadores logística** → gestión relaciones proveedores
- **Asistentes administrativos** → atención personalizada clientes

**Plan:** Reentrenamiento 2-4 semanas hacia funciones de mayor valor.

## Categoría C: ELIMINAR (Estimado 80-120 personas)

### Subcategoría C1: Rutinas Automatizables (50-70 personas)
**Criterio:** >70% tiempo en tareas que ya están automatizadas.

**Tareas típicas:**
- **Data entry** manual cuando ya hay integración automática
- **Reconciliaciones** manuales cuando hay conciliación automática  
- **Reportes** manuales cuando hay dashboards automáticos
- **Validaciones** manuales cuando hay validaciones automáticas

**Eliminación:** Inmediata post-automatización funcionando estable.

### Subcategoría C2: Funciones Duplicadas (20-30 personas)
**Criterio:** Hacen exactamente lo mismo que otra persona o sistema.

**Ejemplos:**
- **Dos asistentes** para un director (cuando uno es suficiente)
- **Validador** de datos que ya valida automáticamente el sistema
- **Reporteador** manual cuando hay reportes automáticos

### Subcategoría C3: Improductivos Documentados (10-20 personas)
**Criterio:** Data histórica demuestra que no agregan valor medible.

**Identificación:** 
- Timesheet muestra <30% tiempo en tareas productivas
- Sin entregables concretos en últimos 6 meses  
- Sin relaciones clave contractuales o comerciales

## Proceso de Clasificación con Datos Duros

### Semana 1: Mapeo Individual
```python
employee_classification = {
    'name': 'Employee Name',
    'current_contract': 'OYMA_R1',
    'monthly_cost': 5000000,  # COP
    'productive_hours_week': 25,
    'routine_hours_week': 15,
    'automation_potential': 12,
    'client_contract_required': True/False,
    'decision_authority_level': 'High/Medium/Low/None',
    'unique_knowledge_skills': ['skill1', 'skill2'],
    'classification_proposed': 'A1/A2/A3/B1/B2/C1/C2/C3'
}
```

### Validación Cruzada
**Legal (Dr. Camilo Marín):**
- Revisar contrato laboral individual
- Verificar no hay cláusulas especiales
- Confirmar proceso liquidación estándar

**Contractual (Clientes):**
- Verificar en contratos EPM, GDO, etc. si especifican personal mínimo
- Confirmar roles requeridos por normativa
- Validar que eliminación no afecta cumplimiento

**Operacional (Directores):**
- Juan Guillermo: Estrategia y relaciones
- Cami: Operación y técnicos
- Carlos: Nuevos negocios y comercial
- Andrea: Financiero y administrativo

### Timesheet Obligatorio (5 días)
**Categorías de tiempo:**
- **Decisiones/Estrategia:** Reuniones de decisión, análisis estratégico
- **Relaciones clave:** Cliente, proveedor, equipo
- **Análisis productivo:** Data → insights → recomendaciones  
- **Gestión humana:** Desarrollo, resolución conflictos
- **Rutina automatizable:** Reports, reconciliaciones, data entry
- **Tiempo improductivo:** Esperas, reuniones sin decisión

## Cronograma de Eliminación Secuencial

### Marzo 27-31: Primera Eliminación (Batch 1)
**Candidatos:** Categoría C1 + C2 con >90% automatización completa
**Estimado:** 20-30 personas
**Criterio:** Tareas 100% automatizadas Y sin riesgo contractual

### Abril 7-11: Segunda Eliminación (Batch 2)  
**Candidatos:** Resto Categoría C1 + C3 con data validada
**Estimado:** 30-50 personas
**Criterio:** 2 semanas validación post-automatización

### Abril 14-18: Eliminación Final (Batch 3)
**Candidatos:** Categoría C2 + C3 restantes
**Estimado:** 20-40 personas  
**Criterio:** Confirmación que estructura optimizada funciona

## Ahorros Calculables por Categoría

### Categoría C: Eliminación Completa
- **80-120 personas × $4-8M promedio = $320-960M mensual**
- **Ahorro anual:** $3.8-11.5 mil millones

### Categoría B: Optimización  
- **100-150 personas liberando 30-50% tiempo**
- **Productividad aumentada:** $200-400M mensual equivalente
- **Valor agregado:** Enfoque en crecimiento vs rutina

### Categoría A: Potenciación
- **180-220 personas 100% enfocadas en valor humano único**
- **ROI maximizado:** Cada peso invertido en salario = mayor retorno

## Criterios de Reversión (Si algo sale mal)

### Alertas Rojas que detienen eliminación:
1. **Cliente se queja** de servicio deteriorado
2. **Proceso automático falla** >24h sin solución  
3. **Error crítico** en datos financieros
4. **Riesgo legal** identificado post-eliminación

### Plan de Contingencia:
- **Contratos temporales** para roles críticos eliminados
- **Outsourcing** de procesos específicos
- **Rehire** de personas clave si es necesario

## Decisiones Inmediatas Requeridas

### ¿Aprobar clasificación y cronograma?
**Riesgo:** Controlado con gobierno de datos
**Beneficio:** $4-12 mil millones anuales ahorro
**Timeline:** Abril 25 estructura final

### ¿Iniciar timesheet obligatorio la próxima semana?
**Necesario:** Para tener datos duros de clasificación
**Resistencia esperada:** Media (explicar como optimización, no amenaza)

**¿Ajustar algo del cronograma o criterios de clasificación antes de iniciar?**