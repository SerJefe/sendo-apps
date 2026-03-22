# 🎯 Guía Skills Avanzados — Condugas & Siendo

## 🔍 Code Review Agents
**19.2M instalaciones | Automatiza PR reviews con 4 agentes especializados**

### **¿Para qué sirve?**
- **Review automático del código** que Ema crea para automatización Condugas
- **4 agentes paralelos** analizan compliance, bugs, blame/history, calidad
- **Scoring 0-100** filtra falsos positivos (threshold configurable)
- **Output como comentario PR** o terminal

### **¿Cuándo usarlo?**
✅ **SÍ usar cuando:**
- Ema sube código Python para Odoo (conciliación, nómina, etc.)
- Pull requests de automatización crítica (banking, payroll)
- Scripts que tocan datos financieros sensibles
- Cualquier código que impacte 452 empleados

❌ **NO usar para:**
- Cambios menores en documentación
- Configs simples o ajustes de estilo
- Prototipos exploratorios

### **¿Cómo activarlo?**
```bash
/code-review [--comment]
```

### **Ejemplos prácticos Condugas:**

#### **Scenario 1: Review script conciliación bancaria**
```bash
# Ema sube bank_reconciliation.py
/code-review --comment

# Output esperado:
# 🔍 Agent #1: CLAUDE.md compliance ✅ (95/100)
# 🐛 Agent #2: No obvious bugs found ✅ (88/100) 
# 📊 Agent #3: Git history clean ✅ (92/100)
# ⚡ Agent #4: Code quality excellent ✅ (91/100)
# 
# 💬 PR Comment: "Automated review complete. 
# High confidence approval (91.5/100 avg score)"
```

#### **Scenario 2: Review script clasificación empleados**
```bash
# Script que clasifica 452 empleados A/B/C
/code-review

# Output esperado con issues:
# ⚠️ Agent #2: Potential silent failure in line 45 (72/100)
# ⚠️ Agent #4: Complex nested logic, suggest simplification (78/100)
# 
# FILTERED OUT (below 80 threshold):
# - Agent #1 found minor style issues (75/100)
```

### **Configuración Condugas:**
```python
# En el código que Ema sube, incluir:
# CLAUDE.md compliance guidelines:
# - Error handling para API Odoo
# - Logging obligatorio para cambios DB
# - Rollback automático en failures
# - Validación antes de commits masivos
```

### **Tips & trucos:**
- **Threshold 85+** para código financiero crítico
- **Threshold 75+** para scripts generales
- **--comment** flag para integración GitHub
- **Review antes de merge** a branch principal

---

## 🧠 Claude-Mem 
**19.2M instalaciones | Memoria persistente across sessions**

### **¿Para qué sirve?**
- **Memoria long-term** de todos tus proyectos Condugas/Siendo
- **No reexplicar contexto** cada nueva conversación
- **Preferencias persistentes** (paletas, métodos, decisiones)
- **Historial de decisiones** y reasoning behind ellas

### **¿Cuándo usarlo?**
✅ **SÍ usar cuando:**
- Trabajás regularmente con el mismo assistant
- Proyectos multi-sesión (automatización abril)
- Necesitás continuidad en decisiones estratégicas
- Contexto complejo (modelo Ser Siendo, Alletagia, etc.)

❌ **NO necesario para:**
- Tasks one-shot simples
- Información ya documentada elsewhere
- Conversaciones que no requieren follow-up

### **¿Cómo activarlo?**
```bash
# Instalar localmente
npm install -g claude-mem

# Setup inicial
claude-mem init --project="condugas-automation"

# En conversaciones
claude-mem store "Sebastián prefiere paleta #292D63, #F8B133, #1D70B7"
claude-mem store "OYMA R1 en crisis: -$280M enero, carta suspensión enviada"
claude-mem recall "automatización condugas"
```

### **Ejemplos prácticos para Sebastián:**

#### **Setup inicial (una vez):**
```bash
# Store context crítico
claude-mem store "Sebastián Sánchez: Gerente Condugas + Fundador Siendo + Docente EAFIT"
claude-mem store "Modelo filosófico: Ser Siendo, framework Alletagia, nunca usar 'liderazgo'"
claude-mem store "Equipo Condugas: Cami(Proy), Juan(Estrat), Carlos(NvosNeg), Andre(Fin), Ema(Dev)"
claude-mem store "Tech stack: Odoo 19, n8n, Claude, Limitless, 452 empleados"
claude-mem store "Paleta marca: Condugas #292D63/#F8B133, Siendo #003f5c/#3A86FF"
```

#### **Durante proyecto automatización:**
```bash
# Store decisiones importantes
claude-mem store "Roadmap abril: 452→250 personas, ROI $350M/mes, ralph-loop implementation"
claude-mem store "Procedimientos priorizados: 1)Bancaria 2)Nómina 3)Clasificación 4)EarlyWarning"
claude-mem store "Lina = patrocinio (energía expansiva), Andrea = responsabilidad (intensiva)"

# Recall en nuevas sesiones
claude-mem recall "roadmap abril"
claude-mem recall "procedimientos"
claude-mem recall "desarrollo humano"
```

#### **Para briefings diarios:**
```bash
# Al start del día
claude-mem recall "tareas críticas" "OYMA crisis" "limitless ayer"

# Durante el día
claude-mem store "EPM respondió carta suspensión: [resultado]"
claude-mem store "Datos febrero recibidos: [análisis]"
claude-mem store "Reunión Lina-Ema observada: [insights]"
```

### **Configuración Sebastián:**
```javascript
// ~/.claude-mem/config.json
{
  "projects": {
    "condugas": {
      "context_limit": 10000,
      "auto_store": ["decisiones", "crisis", "roadmap"],
      "priority_tags": ["crítico", "EPM", "automatización", "equipo"]
    },
    "siendo": {
      "context_limit": 5000, 
      "auto_store": ["desarrollo_humano", "framework", "clientes"],
      "priority_tags": ["letagogía", "coherencia", "consulting"]
    }
  },
  "spanish_mode": true,
  "timezone": "America/Bogota"
}
```

### **Tips & trucos:**
- **Tag everything** con categorías (crítico, equipo, decisión, etc.)
- **Weekly cleanup** de memories irrelevantes
- **Backup memory** to GitHub para no perder contexto
- **Cross-reference** con MEMORY.md del workspace

---

## 🔄 Workflow Combinado: Code Review + Memory

### **Flujo ideal para automatización Condugas:**

```bash
# 1. Ema desarrolla script
vim implementations/bank_reconciliation.py

# 2. Memory store del context
claude-mem store "Ema implementó conciliación bancaria v1.0, integración Odoo API"

# 3. Automated code review
/code-review --comment

# 4. Memory store del review result
claude-mem store "bank_reconciliation.py: review score 89/100, listo para testing"

# 5. En siguiente sesión
claude-mem recall "conciliación bancaria"
# Output: "Ema implementó v1.0, score 89/100, testing pending"
```

### **ROI de ambos skills:**
- **Code review:** Evita bugs en producción ($$$)
- **Memory:** Reduce reexplicación contexto (tiempo)
- **Combinados:** Continuidad projects + calidad code
- **For Sebastián:** Focus en decisiones, no en repetir context

---

## 🎯 Next Steps

### **Implementar code-review-agents:**
1. **Setup GitHub integration** para repos Condugas
2. **Configure thresholds:** 85+ financial, 75+ general
3. **Train Ema** en CLAUDE.md compliance guidelines

### **Implementar claude-mem:**
1. **One-time setup** de todo el contexto Sebastián
2. **Daily habit** de store decisiones importantes
3. **Weekly review** y cleanup de memories

**Ambos skills se complementan perfecto para tu workflow de automatización masiva** 🚀