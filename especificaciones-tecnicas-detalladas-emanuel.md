# 🛠️ ESPECIFICACIONES TÉCNICAS DETALLADAS - CONDUGAS SA

**Implementación Sistema Vivo Empresarial - Detalles completos para Emanuel**

---

## 🏗️ ARQUITECTURA TÉCNICA DETALLADA

### **🖥️ INFRAESTRUCTURA BASE:**
```yaml
SERVIDOR PRODUCCIÓN:
  CPU: 16 cores mínimo (Intel Xeon o AMD EPYC)
  RAM: 64GB mínimo, 128GB recomendado
  Storage: 2TB SSD NVMe (database) + 4TB HDD (archivos)
  Network: 1Gbps mínimo uplink
  OS: Ubuntu 22.04 LTS Server
  
SERVIDOR STAGING:
  CPU: 8 cores
  RAM: 32GB
  Storage: 1TB SSD
  Network: 100Mbps
  OS: Ubuntu 22.04 LTS Server

BACKUP SERVIDOR:
  Location: AWS S3 + local NAS Synology
  Frequency: Daily incremental, weekly full
  Retention: 1 año online, 7 años archive
```

### **📊 DATABASE ARCHITECTURE:**
```sql
-- PostgreSQL 15+ específico
CREATE DATABASE condugas_production;
CREATE DATABASE condugas_staging;

-- Configuración performance
shared_buffers = 16GB
effective_cache_size = 48GB  
work_mem = 256MB
maintenance_work_mem = 2GB
checkpoint_completion_target = 0.9
wal_buffers = 64MB
max_connections = 200

-- Índices específicos performance
CREATE INDEX CONCURRENTLY idx_hr_employee_contract_id ON hr_employee(x_contract_id);
CREATE INDEX CONCURRENTLY idx_account_move_analytic ON account_move_line(analytic_account_id, date);
CREATE INDEX CONCURRENTLY idx_timesheet_employee_date ON account_analytic_line(employee_id, date);
```

---

## 🧠 SISTEMA NERVIOSO CENTRAL - ODOO CORE

### **📋 MÓDULOS ODOO ESPECÍFICOS:**
```python
# requirements.txt específico
MODULOS_CORE = [
    'base',
    'web',
    'account',              # v19.0.1.2.3+
    'account_accountant',   # Enterprise
    'analytic',            # Cuentas analíticas contratos
    'hr',                  # RRHH 452 empleados
    'hr_timesheet',        # Control horas
    'hr_payroll',          # Nómina por contrato
    'hr_expense',          # Gastos empleados
    'project',             # Proyectos = contratos
    'stock',               # Inventario materiales
    'purchase',            # Órdenes compra
    'sale',                # Facturación clientes
    'account_reports',     # Reportes contables
    'spreadsheet_dashboard', # Dashboard custom
    'account_bank_statement_import', # Bancos automático
    'l10n_co',            # Localización Colombia
]

# Módulos custom desarrollar
MODULOS_CUSTOM = [
    'condugas_voice_interface',    # Interface voz operarios
    'condugas_alert_system',       # Alertas automáticas
    'condugas_dashboard_executive', # Dashboard Sebastián
    'condugas_employee_classification', # 4D + A/B/C
    'condugas_tender_intelligence', # Licitaciones automático
    'condugas_client_integration',  # APIs EPM + otros
]
```

### **🗃️ ESTRUCTURA DATABASE CUSTOM:**

#### **EMPLEADOS 4D - CAMPOS CUSTOM:**
```xml
<!-- hr.employee fields custom -->
<record id="view_employee_form_condugas" model="ir.ui.view">
    <field name="name">employee.form.condugas</field>
    <field name="model">hr.employee</field>
    <field name="inherit_id" ref="hr.view_employee_form"/>
    <field name="arch" type="xml">
        <xpath expr="//group[@name='active_group']" position="after">
            <group name="condugas_classification" string="Clasificación Condugas">
                <!-- DIMENSIÓN 1: PROYECTO -->
                <field name="x_proyecto_principal" 
                       widget="selection"
                       options="{'no_create': True}"
                       required="True"/>
                <field name="x_proyectos_secundarios" 
                       widget="many2many_tags"/>
                
                <!-- DIMENSIÓN 2: PROCESO -->
                <field name="x_proceso_tipo" 
                       widget="radio"
                       required="True"/>
                <field name="x_proceso_especialidad"/>
                
                <!-- DIMENSIÓN 3: JERÁRQUICO (ya existe en Odoo) -->
                <!-- parent_id field -->
                
                <!-- DIMENSIÓN 4: DISTRIBUCIÓN -->
                <field name="x_distribucion_tipo"
                       widget="selection"
                       required="True"/>
                <field name="x_nivel_operativo"
                       widget="selection"
                       required="True"/>
                
                <!-- CLASIFICACIÓN A/B/C AUTOMÁTICA -->
                <field name="x_clasificacion_automatica"
                       readonly="True"
                       widget="badge"/>
                <field name="x_score_productividad"
                       readonly="True"/>
                <field name="x_score_multifuncionalidad"
                       readonly="True"/>
                <field name="x_score_especialization"
                       readonly="True"/>
                <field name="x_score_total"
                       readonly="True"/>
            </group>
        </xpath>
    </field>
</record>
```

#### **CAMPOS ESPECÍFICOS PYTHON:**
```python
class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    
    # DIMENSIÓN 1: PROYECTO
    x_proyecto_principal = fields.Many2one(
        'account.analytic.account',
        string='Proyecto Principal',
        domain="[('company_id', '=', company_id)]",
        required=True,
        help="Contrato donde empleado dedica >50% tiempo"
    )
    x_proyectos_secundarios = fields.Many2many(
        'account.analytic.account',
        string='Proyectos Secundarios',
        help="Contratos donde empleado participa ocasionalmente"
    )
    
    # DIMENSIÓN 2: PROCESO  
    x_proceso_tipo = fields.Selection([
        ('administrativo', 'Administrativo'),
        ('tecnico', 'Técnico'),
        ('logistico', 'Logístico'), 
        ('financiero', 'Financiero'),
        ('estrategico', 'Estratégico'),
        ('legal', 'Legal'),
        ('hse', 'HSE'),
        ('comercial', 'Comercial')
    ], string='Tipo Proceso', required=True)
    
    x_proceso_especialidad = fields.Char(
        string='Especialidad',
        help="Ej: Soldadura, Excavación, Contabilidad, etc."
    )
    
    # DIMENSIÓN 4: DISTRIBUCIÓN
    x_distribucion_tipo = fields.Selection([
        ('operativo', 'Operativo - Ejecuta obra directa'),
        ('indirecto', 'Indirecto - Apoya obra sin ejecutar'),
        ('central', 'Central - Puede manejar múltiples contratos'),
        ('administrativo', 'Administrativo - Tareas contratos específicos'),
        ('estrategico', 'Estratégico - Administración central')
    ], string='Distribución', required=True)
    
    x_nivel_operativo = fields.Selection([
        ('operativo', 'Operativo'),
        ('tactico', 'Táctico'), 
        ('estrategico', 'Estratégico')
    ], string='Nivel Operativo', required=True)
    
    # CLASIFICACIÓN AUTOMÁTICA A/B/C
    x_clasificacion_automatica = fields.Selection([
        ('A_conservar', 'A - CONSERVAR'),
        ('B_optimizar', 'B - OPTIMIZAR'),
        ('C_automatizar', 'C - AUTOMATIZAR/ELIMINAR')
    ], string='Clasificación A/B/C', 
       compute='_compute_clasificacion_automatica',
       store=True)
       
    x_score_productividad = fields.Float(
        string='Score Productividad',
        compute='_compute_scores_clasificacion',
        store=True,
        help="0-100 basado en timesheet effectiveness"
    )
    
    x_score_multifuncionalidad = fields.Float(
        string='Score Multifuncionalidad', 
        compute='_compute_scores_clasificacion',
        store=True,
        help="0-100 basado en # proyectos maneja"
    )
    
    x_score_especialization = fields.Float(
        string='Score Especialización',
        compute='_compute_scores_clasificacion', 
        store=True,
        help="0-100 basado en uniqueness skills"
    )
    
    x_score_total = fields.Float(
        string='Score Total',
        compute='_compute_clasificacion_automatica',
        store=True
    )
    
    @api.depends('x_score_productividad', 'x_score_multifuncionalidad', 'x_score_especialization')
    def _compute_clasificacion_automatica(self):
        for employee in self:
            # Algoritmo scoring específico
            total_score = (
                employee.x_score_productividad * 0.4 +
                employee.x_score_multifuncionalidad * 0.3 + 
                employee.x_score_especialization * 0.3
            )
            employee.x_score_total = total_score
            
            # Clasificación automática
            if total_score >= 70:
                employee.x_clasificacion_automatica = 'A_conservar'
            elif total_score >= 40:
                employee.x_clasificacion_automatica = 'B_optimizar'
            else:
                employee.x_clasificacion_automatica = 'C_automatizar'
    
    def _compute_scores_clasificacion(self):
        for employee in self:
            # PRODUCTIVIDAD: horas efectivas vs disponibles
            timesheet_lines = self.env['account.analytic.line'].search([
                ('employee_id', '=', employee.id),
                ('date', '>=', fields.Date.today() - timedelta(days=90))
            ])
            
            horas_registradas = sum(timesheet_lines.mapped('unit_amount'))
            horas_disponibles = 90 * 8  # 90 días x 8 horas
            productividad = min(100, (horas_registradas / horas_disponibles) * 100)
            employee.x_score_productividad = productividad
            
            # MULTIFUNCIONALIDAD: # proyectos activos
            proyectos_count = len(employee.x_proyectos_secundarios) + (1 if employee.x_proyecto_principal else 0)
            multifuncionalidad = min(100, proyectos_count * 20)
            employee.x_score_multifuncionalidad = multifuncionalidad
            
            # ESPECIALIZACIÓN: rareness skills
            empleados_misma_especialidad = self.env['hr.employee'].search_count([
                ('x_proceso_especialidad', '=', employee.x_proceso_especialidad),
                ('id', '!=', employee.id),
                ('active', '=', True)
            ])
            
            if empleados_misma_especialidad == 0:
                especializacion = 100  # Único en la empresa
            elif empleados_misma_especialidad <= 2:
                especializacion = 80   # Muy especializado
            elif empleados_misma_especialidad <= 5:
                especializacion = 60   # Especializado
            else:
                especializacion = 20   # Común
                
            employee.x_score_especialization = especializacion
```

---

## 🚨 SISTEMA ALERTAS AUTOMÁTICAS

### **⚡ ARQUITECTURA ALERTAS:**
```python
class CodugasAlertSystem(models.Model):
    _name = 'condugas.alert.system'
    _description = 'Sistema Alertas Automático Condugas'
    _order = 'priority desc, create_date desc'
    
    name = fields.Char('Alert Name', required=True)
    alert_type = fields.Selection([
        ('supervivencia_roja', 'SUPERVIVENCIA - Crítico'),
        ('control_amarilla', 'CONTROL - Atención'), 
        ('desarrollo_verde', 'DESARROLLO - Oportunidad')
    ], required=True)
    
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'), 
        ('2', 'High'),
        ('3', 'Critical Emergency')
    ], default='1')
    
    trigger_condition = fields.Text('Trigger SQL Condition')
    notification_channels = fields.Selection([
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('dashboard', 'Dashboard Only'),
        ('whatsapp', 'WhatsApp'),
        ('all', 'Todos los canales')
    ])
    
    recipients = fields.Many2many('res.users', string='Recipients')
    is_active = fields.Boolean('Active', default=True)
    last_triggered = fields.Datetime('Last Triggered')
    trigger_count = fields.Integer('Trigger Count', default=0)
    
    def check_alert_conditions(self):
        """Cron job cada 15 minutos check todas alertas activas"""
        active_alerts = self.search([('is_active', '=', True)])
        
        for alert in active_alerts:
            try:
                # Ejecutar SQL condition
                self.env.cr.execute(alert.trigger_condition)
                result = self.env.cr.fetchall()
                
                if result:  # Condition met
                    alert._trigger_alert(result)
                    
            except Exception as e:
                _logger.error(f"Error checking alert {alert.name}: {e}")
    
    def _trigger_alert(self, trigger_data):
        """Ejecutar alerta específica"""
        self.last_triggered = fields.Datetime.now()
        self.trigger_count += 1
        
        # Generar mensaje personalizado
        message = self._generate_alert_message(trigger_data)
        
        # Enviar según canales configurados
        if self.notification_channels in ['email', 'all']:
            self._send_email_alert(message)
        if self.notification_channels in ['sms', 'all']:
            self._send_sms_alert(message)
        if self.notification_channels in ['whatsapp', 'all']:
            self._send_whatsapp_alert(message)
            
        # Dashboard notification
        self._create_dashboard_notification(message)
    
    def _generate_alert_message(self, trigger_data):
        """Generate personalized alert message"""
        base_message = f"🚨 ALERTA {self.alert_type.upper()}: {self.name}\n"
        
        if self.alert_type == 'supervivencia_roja':
            base_message += "⚠️ ACCIÓN INMEDIATA REQUERIDA\n"
        elif self.alert_type == 'control_amarilla':  
            base_message += "📊 MONITOREO INTENSIVO ACTIVADO\n"
        else:
            base_message += "🎯 OPORTUNIDAD DETECTADA\n"
            
        base_message += f"Datos: {trigger_data}\n"
        base_message += f"Timestamp: {fields.Datetime.now()}"
        
        return base_message

# Configuración alertas específicas Condugas
ALERTAS_PREDEFINIDAS = [
    {
        'name': 'Margen Negativo Crítico',
        'alert_type': 'supervivencia_roja',
        'priority': '3',
        'trigger_condition': '''
            SELECT 
                aa.name as contrato,
                ROUND(((SUM(aml.debit) - SUM(aml.credit)) / SUM(aml.debit)) * 100, 2) as margen
            FROM account_analytic_account aa
            JOIN account_move_line aml ON aml.analytic_account_id = aa.id
            WHERE aa.active = true
            GROUP BY aa.id, aa.name
            HAVING ((SUM(aml.debit) - SUM(aml.credit)) / SUM(aml.debit)) * 100 < -15
        ''',
        'notification_channels': 'all',
        'recipients': ['sebastián', 'andrea']
    },
    {
        'name': 'Cash Flow Negativo 30 días',
        'alert_type': 'supervivencia_roja', 
        'priority': '3',
        'trigger_condition': '''
            SELECT 
                SUM(CASE 
                    WHEN am.move_type = 'in_invoice' AND am.invoice_date <= CURRENT_DATE + INTERVAL '30 days'
                    THEN am.amount_total 
                    ELSE 0 
                END) as egresos_30d,
                SUM(CASE
                    WHEN am.move_type = 'out_invoice' AND am.invoice_date <= CURRENT_DATE + INTERVAL '30 days'
                    THEN am.amount_total
                    ELSE 0
                END) as ingresos_30d
            FROM account_move am
            WHERE am.state = 'posted'
            HAVING (ingresos_30d - egresos_30d) < 0
        ''',
        'notification_channels': 'all',
        'recipients': ['sebastián', 'andrea']
    },
    {
        'name': 'Timeline Atrasado +30%',
        'alert_type': 'control_amarilla',
        'priority': '2', 
        'trigger_condition': '''
            SELECT 
                p.name as proyecto,
                p.date_start,
                p.date as fecha_fin_planeada,
                CURRENT_DATE,
                ROUND(((CURRENT_DATE - p.date_start)::numeric / (p.date - p.date_start)::numeric) * 100, 2) as progreso_tiempo,
                (SELECT COUNT(*) FROM project_task pt WHERE pt.project_id = p.id AND pt.stage_id IN (SELECT id FROM project_task_type WHERE fold = true)) as tareas_completadas,
                (SELECT COUNT(*) FROM project_task pt WHERE pt.project_id = p.id) as total_tareas
            FROM project_project p
            WHERE p.active = true
            AND p.date > CURRENT_DATE
            HAVING (((CURRENT_DATE - p.date_start)::numeric / (p.date - p.date_start)::numeric) * 100) > 130
        ''',
        'notification_channels': 'email',
        'recipients': ['camilo', 'sebastián']
    },
    {
        'name': 'Licitación Alta Probabilidad',
        'alert_type': 'desarrollo_verde',
        'priority': '1',
        'trigger_condition': '''
            SELECT 
                cl.name as licitacion,
                cl.scoring_probabilidad,
                cl.valor_estimado,
                cl.fecha_cierre
            FROM condugas_licitacion cl
            WHERE cl.scoring_probabilidad >= 85
            AND cl.fecha_cierre >= CURRENT_DATE
            AND cl.estado = 'detectada'
        ''',
        'notification_channels': 'email',
        'recipients': ['carlos', 'sebastián']
    }
]
```

---

## 🎤 INTERFACE VOZ OPERARIOS

### **🗣️ ARQUITECTURA VOZ:**
```python
# condugas_voice_interface/models/voice_interface.py
import speech_recognition as sr
import pyttsx3
import openai
from datetime import datetime
import logging

class CodugasVoiceInterface(models.Model):
    _name = 'condugas.voice.interface'
    _description = 'Interface Voz Operarios Condugas'
    
    session_id = fields.Char('Session ID', required=True)
    employee_id = fields.Many2one('hr.employee', 'Operario', required=True)
    command_text = fields.Text('Comando Original')
    parsed_command = fields.Text('Comando Procesado') 
    action_taken = fields.Selection([
        ('material_consumed', 'Material Consumido'),
        ('timesheet_update', 'Actualización Timesheet'),
        ('problem_report', 'Reporte Problema'),
        ('query_inventory', 'Consulta Inventario'),
        ('error', 'Error Procesamiento')
    ])
    
    result_message = fields.Text('Mensaje Resultado')
    audio_file_path = fields.Char('Audio File Path')
    processing_time = fields.Float('Processing Time (seconds)')
    confidence_score = fields.Float('Confidence Score')
    
    @api.model
    def process_voice_command(self, audio_file_path, employee_id):
        """Procesar comando voz operario"""
        start_time = datetime.now()
        
        try:
            # 1. Speech to text
            recognizer = sr.Recognizer()
            with sr.AudioFile(audio_file_path) as source:
                audio = recognizer.record(source)
                
            # Usar Google Speech API optimizado español colombiano
            command_text = recognizer.recognize_google(
                audio, 
                language='es-CO',
                show_all=False
            )
            
            # 2. Parse command usando OpenAI/Claude
            parsed_command = self._parse_construction_command(command_text)
            
            # 3. Execute action
            action_result = self._execute_parsed_command(parsed_command, employee_id)
            
            # 4. Generate response
            response_audio = self._generate_voice_response(action_result)
            
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # 5. Log interaction
            voice_log = self.create({
                'session_id': f"{employee_id}_{int(datetime.now().timestamp())}",
                'employee_id': employee_id,
                'command_text': command_text,
                'parsed_command': str(parsed_command),
                'action_taken': action_result.get('action_type'),
                'result_message': action_result.get('message'),
                'audio_file_path': audio_file_path,
                'processing_time': processing_time,
                'confidence_score': action_result.get('confidence', 0.9)
            })
            
            return {
                'success': True,
                'action_taken': action_result,
                'response_audio': response_audio,
                'log_id': voice_log.id
            }
            
        except Exception as e:
            _logger.error(f"Error processing voice command: {e}")
            return {
                'success': False,
                'error': str(e),
                'response_audio': self._generate_error_response()
            }
    
    def _parse_construction_command(self, command_text):
        """Parse comando construcción usando NLP"""
        
        # Diccionario jerga construcción colombiana
        CONSTRUCCION_DICT = {
            'materiales': {
                'tuberia': ['tubería', 'tubo', 'tuberias'],
                'pvc': ['pvc', 'policloruro'],
                'cemento': ['cemento', 'bulto cemento'],
                'arena': ['arena', 'arena lavada'],
                'grava': ['grava', 'gravilla', 'material granular'],
                'hierro': ['hierro', 'varilla', 'acero']
            },
            'actividades': {
                'soldadura': ['soldadura', 'soldar', 'soldando'],
                'excavacion': ['excavación', 'excavar', 'excavando'],
                'relleno': ['relleno', 'rellenando', 'bacheo'],
                'compactacion': ['compactación', 'compactar', 'compactando']
            },
            'contratos': {
                'boyaca': ['boyacá', 'boyaca'],
                'valle': ['valle', 'valle del cauca'],
                'oyma': ['oyma', 'oymz2', 'oyma r1'],
                'floridablanca': ['floridablanca', 'florida'],
                'jerico': ['jericó', 'jerico']
            },
            'unidades': {
                'metros': ['metros', 'metro', 'm', 'mts'],
                'bultos': ['bultos', 'bulto', 'sacos'],
                'kilos': ['kilos', 'kilogramos', 'kg']
            }
        }
        
        # Patterns específicos comandos construcción
        import re
        
        patterns = {
            'material_consumption': re.compile(
                r'(consumí|consumi|use|gaste)\s+(\d+)\s+(\w+)\s+(.*?)\s+(proyecto|contrato)\s+(\w+)',
                re.IGNORECASE
            ),
            'timesheet_update': re.compile(
                r'(terminé|termine|acabé|complete)\s+(.*?)\s+(empiezo|inicio|comienzo)\s+(.*)',
                re.IGNORECASE
            ),
            'problem_report': re.compile(
                r'(problema|error|falla|inconveniente)\s+(.*?)\s+(necesito|requiero)\s+(.*)',
                re.IGNORECASE
            ),
            'inventory_query': re.compile(
                r'(cuánto|cuanto|que cantidad)\s+(.*?)\s+(me queda|queda|hay)',
                re.IGNORECASE
            )
        }
        
        # Match patterns
        for pattern_name, pattern in patterns.items():
            match = pattern.search(command_text)
            if match:
                return {
                    'command_type': pattern_name,
                    'groups': match.groups(),
                    'full_text': command_text,
                    'confidence': 0.85
                }
        
        # Si no match, usar OpenAI para parse complejo
        openai_parsed = self._openai_parse_fallback(command_text)
        return openai_parsed
    
    def _execute_parsed_command(self, parsed_command, employee_id):
        """Ejecutar comando parseado"""
        
        command_type = parsed_command.get('command_type')
        
        if command_type == 'material_consumption':
            return self._handle_material_consumption(parsed_command, employee_id)
        elif command_type == 'timesheet_update':
            return self._handle_timesheet_update(parsed_command, employee_id)
        elif command_type == 'problem_report':
            return self._handle_problem_report(parsed_command, employee_id)
        elif command_type == 'inventory_query':
            return self._handle_inventory_query(parsed_command, employee_id)
        else:
            return {
                'action_type': 'error',
                'message': 'No pude entender el comando. Por favor repite.',
                'confidence': 0.1
            }
    
    def _handle_material_consumption(self, parsed_command, employee_id):
        """Manejar consumo materiales"""
        try:
            groups = parsed_command['groups']
            cantidad = int(groups[1])
            material = groups[2].lower()
            proyecto = groups[5].lower()
            
            # Buscar empleado y proyecto
            employee = self.env['hr.employee'].browse(employee_id)
            analytic_account = self.env['account.analytic.account'].search([
                ('name', 'ilike', proyecto)
            ], limit=1)
            
            if not analytic_account:
                return {
                    'action_type': 'error',
                    'message': f'No encontré el proyecto {proyecto}. Verifica el nombre.',
                    'confidence': 0.3
                }
            
            # Buscar producto material
            product = self.env['product.product'].search([
                ('name', 'ilike', material)
            ], limit=1)
            
            if not product:
                return {
                    'action_type': 'error', 
                    'message': f'No encontré el material {material} en inventario.',
                    'confidence': 0.3
                }
            
            # Validar stock disponible
            stock_quant = self.env['stock.quant'].search([
                ('product_id', '=', product.id),
                ('location_id.usage', '=', 'internal')
            ])
            
            available_qty = sum(stock_quant.mapped('quantity'))
            
            if cantidad > available_qty:
                return {
                    'action_type': 'error',
                    'message': f'Solo hay {available_qty} {product.uom_id.name} disponibles. No puedo registrar {cantidad}.',
                    'confidence': 0.9
                }
            
            # Crear movimiento inventario (consumo)
            stock_move = self.env['stock.move'].create({
                'name': f'Consumo {product.name} - {employee.name}',
                'product_id': product.id,
                'product_uom_qty': cantidad,
                'product_uom': product.uom_id.id,
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.stock_location_production').id,
                'analytic_account_id': analytic_account.id,
                'origin': f'Voz-{employee.name}-{datetime.now().strftime("%Y%m%d%H%M")}'
            })
            stock_move._action_confirm()
            stock_move._action_assign()
            stock_move._action_done()
            
            # Calcular stock restante
            remaining_stock = available_qty - cantidad
            
            return {
                'action_type': 'material_consumed',
                'message': f'Registrado: {cantidad} {product.uom_id.name} de {product.name} en proyecto {analytic_account.name}. Te quedan {remaining_stock} {product.uom_id.name}.',
                'confidence': 0.95,
                'data': {
                    'product_id': product.id,
                    'quantity': cantidad,
                    'project_id': analytic_account.id,
                    'remaining_stock': remaining_stock
                }
            }
            
        except Exception as e:
            return {
                'action_type': 'error',
                'message': f'Error procesando consumo material: {str(e)}',
                'confidence': 0.1
            }
```

---

## 📊 DASHBOARD SEBASTIÁN TIEMPO REAL

### **🖥️ ARQUITECTURA DASHBOARD:**
```html
<!-- Dashboard HTML estructura -->
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard Ejecutivo Condugas</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <!-- CSS Framework optimizado TDAH -->
    <style>
        :root {
            --condugas-azul-oscuro: #292D63;
            --condugas-amarillo: #F8B133;  
            --condugas-azul-claro: #1D70B7;
            --rojo-alerta: #e74c3c;
            --verde-ok: #27ae60;
            --amarillo-atencion: #f39c12;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            overflow-x: hidden;
        }
        
        /* Header flotante SIEMPRE visible */
        .header-flotante {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 80px;
            background: var(--condugas-azul-oscuro);
            color: white;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        }
        
        .header-left {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .logo-empresa {
            font-size: 24px;
            font-weight: bold;
            color: var(--condugas-amarillo);
        }
        
        .semaforo-empresa {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            font-weight: bold;
            animation: pulse 2s infinite;
            cursor: pointer;
        }
        
        .semaforo-verde { background: var(--verde-ok); }
        .semaforo-amarillo { background: var(--amarillo-atencion); }
        .semaforo-rojo { background: var(--rojo-alerta); }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        .header-center {
            display: flex;
            gap: 30px;
        }
        
        .header-metric {
            text-align: center;
        }
        
        .header-metric-value {
            font-size: 18px;
            font-weight: bold;
            color: var(--condugas-amarillo);
        }
        
        .header-metric-label {
            font-size: 12px;
            opacity: 0.8;
        }
        
        .header-right {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .alertas-count {
            background: var(--rojo-alerta);
            color: white;
            border-radius: 20px;
            padding: 8px 15px;
            font-weight: bold;
            animation: blink 1s infinite;
        }
        
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0.3; }
        }
        
        /* Contenido principal */
        .dashboard-main {
            margin-top: 80px;
            padding: 20px;
            min-height: calc(100vh - 80px);
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 20px;
            height: calc(100vh - 120px);
        }
        
        /* Panel contratos */
        .contratos-panel {
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            padding: 20px;
            overflow-y: auto;
        }
        
        .panel-title {
            font-size: 20px;
            font-weight: bold;
            color: var(--condugas-azul-oscuro);
            margin-bottom: 15px;
            border-bottom: 3px solid var(--condugas-amarillo);
            padding-bottom: 10px;
        }
        
        .contratos-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }
        
        .contrato-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            padding: 20px;
            cursor: pointer;
            transition: transform 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .contrato-card:hover {
            transform: translateY(-5px);
        }
        
        .contrato-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 5px;
            height: 100%;
        }
        
        .contrato-verde::before { background: var(--verde-ok); }
        .contrato-amarillo::before { background: var(--amarillo-atencion); }
        .contrato-rojo::before { background: var(--rojo-alerta); }
        
        .contrato-nombre {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .contrato-metricas {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }
        
        .metrica {
            text-align: center;
        }
        
        .metrica-valor {
            font-size: 16px;
            font-weight: bold;
        }
        
        .metrica-label {
            font-size: 12px;
            opacity: 0.9;
        }
        
        /* Panel lateral */
        .panel-lateral {
            display: grid;
            grid-template-rows: 1fr 1fr;
            gap: 20px;
        }
        
        .empleados-panel, .alertas-panel {
            background: white;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            padding: 20px;
        }
        
        .empleados-progress {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 15px;
        }
        
        .empleado-categoria {
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            color: white;
            font-weight: bold;
        }
        
        .categoria-a { background: var(--verde-ok); }
        .categoria-b { background: var(--amarillo-atencion); }
        .categoria-c { background: var(--rojo-alerta); }
        
        .alertas-lista {
            max-height: 200px;
            overflow-y: auto;
        }
        
        .alerta-item {
            padding: 10px;
            border-left: 4px solid;
            margin-bottom: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .alerta-critica {
            background: #ffebee;
            border-color: var(--rojo-alerta);
        }
        
        .alerta-atencion {
            background: #fff8e1;
            border-color: var(--amarillo-atencion);
        }
        
        /* Responsive */
        @media (max-width: 1200px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
                grid-template-rows: auto auto;
            }
            
            .panel-lateral {
                grid-template-rows: none;
                grid-template-columns: 1fr 1fr;
            }
        }
        
        @media (max-width: 768px) {
            .header-flotante {
                flex-direction: column;
                height: auto;
                padding: 10px;
            }
            
            .dashboard-main {
                margin-top: 140px;
            }
            
            .panel-lateral {
                grid-template-columns: 1fr;
                grid-template-rows: auto auto;
            }
        }
    </style>
</head>
<body>
    <!-- Header flotante -->
    <div class="header-flotante">
        <div class="header-left">
            <div class="logo-empresa">CONDUGAS SA</div>
            <div class="semaforo-empresa semaforo-verde" id="semaforoGeneral">✓</div>
        </div>
        
        <div class="header-center">
            <div class="header-metric">
                <div class="header-metric-value" id="cashFlow">+$450M</div>
                <div class="header-metric-label">Cash Flow 30d</div>
            </div>
            <div class="header-metric">
                <div class="header-metric-value" id="contratosCriticos">2/8</div>
                <div class="header-metric-label">Contratos Críticos</div>
            </div>
            <div class="header-metric">
                <div class="header-metric-value" id="empleadosProgress">65%</div>
                <div class="header-metric-label">Progress 452→250</div>
            </div>
        </div>
        
        <div class="header-right">
            <div class="alertas-count" id="alertasCount">2 ALERTAS</div>
            <div style="font-size: 12px;" id="lastUpdate">Actualizado: hace 2 min</div>
        </div>
    </div>
    
    <!-- Contenido principal -->
    <div class="dashboard-main">
        <div class="dashboard-grid">
            <!-- Panel contratos -->
            <div class="contratos-panel">
                <div class="panel-title">📊 ESTADO CONTRATOS</div>
                
                <div class="contratos-grid" id="contratosGrid">
                    <!-- Contratos se cargan dinámicamente via JavaScript -->
                </div>
            </div>
            
            <!-- Panel lateral -->
            <div class="panel-lateral">
                <!-- Empleados -->
                <div class="empleados-panel">
                    <div class="panel-title">👥 OPTIMIZACIÓN EMPLEADOS</div>
                    
                    <div class="empleados-progress">
                        <div class="empleado-categoria categoria-a">
                            <div style="font-size: 24px;" id="empleadosA">70</div>
                            <div>A - CONSERVAR</div>
                        </div>
                        <div class="empleado-categoria categoria-b">
                            <div style="font-size: 24px;" id="empleadosB">120</div>
                            <div>B - OPTIMIZAR</div>
                        </div>
                        <div class="empleado-categoria categoria-c">
                            <div style="font-size: 24px;" id="empleadosC">60</div>
                            <div>C - ELIMINAR</div>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 15px; font-weight: bold; color: var(--verde-ok);">
                        AHORRO PROYECTADO: $350M COP/año
                    </div>
                </div>
                
                <!-- Alertas -->
                <div class="alertas-panel">
                    <div class="panel-title">🚨 ALERTAS ACTIVAS</div>
                    
                    <div class="alertas-lista" id="alertasLista">
                        <!-- Alertas se cargan dinámicamente -->
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- JavaScript tiempo real -->
    <script>
        // WebSocket connection para datos tiempo real
        const DASHBOARD_CONFIG = {
            websocket_url: 'ws://localhost:8069/websocket',
            refresh_interval: 30000, // 30 segundos
            alert_sound_enabled: true
        };
        
        class DashboardConductor {
            constructor() {
                this.websocket = null;
                this.lastData = null;
                this.alertSoundEnabled = DASHBOARD_CONFIG.alert_sound_enabled;
                
                this.initWebSocket();
                this.startPeriodicRefresh();
                this.bindEvents();
            }
            
            initWebSocket() {
                try {
                    this.websocket = new WebSocket(DASHBOARD_CONFIG.websocket_url);
                    
                    this.websocket.onopen = () => {
                        console.log('Dashboard WebSocket conectado');
                        this.subscribeToUpdates();
                    };
                    
                    this.websocket.onmessage = (event) => {
                        const data = JSON.parse(event.data);
                        this.updateDashboard(data);
                    };
                    
                    this.websocket.onclose = () => {
                        console.log('Dashboard WebSocket desconectado, reconectando...');
                        setTimeout(() => this.initWebSocket(), 5000);
                    };
                    
                } catch (error) {
                    console.error('Error WebSocket:', error);
                    this.fallbackToPolling();
                }
            }
            
            subscribeToUpdates() {
                // Suscribir a updates específicos
                this.websocket.send(JSON.stringify({
                    type: 'subscribe',
                    channels: [
                        'dashboard.executive',
                        'alerts.critical',
                        'contracts.status',
                        'employees.classification'
                    ]
                }));
            }
            
            fallbackToPolling() {
                // Fallback a polling HTTP si WebSocket falla
                setInterval(() => {
                    fetch('/dashboard/executive/data')
                        .then(response => response.json())
                        .then(data => this.updateDashboard(data))
                        .catch(error => console.error('Error polling:', error));
                }, DASHBOARD_CONFIG.refresh_interval);
            }
            
            updateDashboard(data) {
                this.updateHeader(data.header);
                this.updateContratos(data.contratos);
                this.updateEmpleados(data.empleados);
                this.updateAlertas(data.alertas);
                
                this.lastData = data;
                document.getElementById('lastUpdate').textContent = 
                    `Actualizado: ${new Date().toLocaleTimeString()}`;
            }
            
            updateHeader(header) {
                // Semáforo general
                const semaforo = document.getElementById('semaforoGeneral');
                semaforo.className = `semaforo-empresa semaforo-${header.semaforo_color}`;
                semaforo.textContent = header.semaforo_icon;
                
                // Métricas header
                document.getElementById('cashFlow').textContent = header.cash_flow;
                document.getElementById('contratosCriticos').textContent = 
                    `${header.contratos_criticos}/${header.total_contratos}`;
                document.getElementById('empleadosProgress').textContent = header.empleados_progress;
                
                // Alertas count
                const alertasCount = document.getElementById('alertasCount');
                if (header.alertas_count > 0) {
                    alertasCount.textContent = `${header.alertas_count} ALERTAS`;
                    alertasCount.style.display = 'block';
                    
                    // Sound alert si hay nuevas alertas críticas
                    if (this.alertSoundEnabled && header.alertas_nuevas > 0) {
                        this.playAlertSound();
                    }
                } else {
                    alertasCount.style.display = 'none';
                }
            }
            
            updateContratos(contratos) {
                const grid = document.getElementById('contratosGrid');
                grid.innerHTML = '';
                
                contratos.forEach(contrato => {
                    const card = document.createElement('div');
                    card.className = `contrato-card contrato-${contrato.semaforo}`;
                    card.onclick = () => this.openContratoDetail(contrato.id);
                    
                    card.innerHTML = `
                        <div class="contrato-nombre">${contrato.nombre}</div>
                        <div style="font-size: 14px; opacity: 0.9;">${contrato.descripcion}</div>
                        
                        <div class="contrato-metricas">
                            <div class="metrica">
                                <div class="metrica-valor">${contrato.margen}%</div>
                                <div class="metrica-label">Margen</div>
                            </div>
                            <div class="metrica">
                                <div class="metrica-valor">${contrato.timeline}%</div>
                                <div class="metrica-label">Avance</div>
                            </div>
                            <div class="metrica">
                                <div class="metrica-valor">${contrato.empleados}</div>
                                <div class="metrica-label">Empleados</div>
                            </div>
                            <div class="metrica">
                                <div class="metrica-valor">$${contrato.valor_ejecutado}</div>
                                <div class="metrica-label">Ejecutado</div>
                            </div>
                        </div>
                        
                        ${contrato.alertas_activas > 0 ? 
                            `<div style="position: absolute; top: 10px; right: 10px; background: var(--rojo-alerta); color: white; border-radius: 15px; padding: 5px 10px; font-size: 12px;">
                                ${contrato.alertas_activas} alertas
                            </div>` : ''}
                    `;
                    
                    grid.appendChild(card);
                });
            }
            
            updateEmpleados(empleados) {
                document.getElementById('empleadosA').textContent = empleados.categoria_a;
                document.getElementById('empleadosB').textContent = empleados.categoria_b;
                document.getElementById('empleadosC').textContent = empleados.categoria_c;
            }
            
            updateAlertas(alertas) {
                const lista = document.getElementById('alertasLista');
                lista.innerHTML = '';
                
                if (alertas.length === 0) {
                    lista.innerHTML = '<div style="text-align: center; color: var(--verde-ok); font-weight: bold;">✓ Todo funcionando correctamente</div>';
                    return;
                }
                
                alertas.forEach(alerta => {
                    const item = document.createElement('div');
                    item.className = `alerta-item ${alerta.tipo === 'critica' ? 'alerta-critica' : 'alerta-atencion'}`;
                    
                    item.innerHTML = `
                        <div style="font-weight: bold; margin-bottom: 5px;">
                            ${alerta.tipo === 'critica' ? '🚨' : '⚠️'} ${alerta.titulo}
                        </div>
                        <div style="font-size: 12px; opacity: 0.8;">
                            ${alerta.descripcion}
                        </div>
                        <div style="font-size: 10px; margin-top: 5px; text-align: right;">
                            ${alerta.timestamp}
                        </div>
                    `;
                    
                    item.onclick = () => this.openAlertaDetail(alerta.id);
                    lista.appendChild(item);
                });
            }
            
            playAlertSound() {
                // Audio alert para alertas críticas
                const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjZ92cNtJAUvnMP1yl8rCBgaaL7s3KNNDAxOpePxtGMcBj992cNwJAUuzMPy0WkkCBFotuHcpUwMDFWq5Pc0NAIKJhI=');
                audio.volume = 0.3;
                audio.play().catch(e => console.log('Audio no disponible'));
            }
            
            bindEvents() {
                // Click semáforo general → mostrar resumen
                document.getElementById('semaforoGeneral').onclick = () => {
                    this.showGeneralSummary();
                };
                
                // Teclado shortcuts
                document.addEventListener('keydown', (e) => {
                    if (e.ctrlKey && e.key === 'r') {
                        e.preventDefault();
                        this.forceRefresh();
                    }
                    if (e.key === 'Escape') {
                        this.closeAllModals();
                    }
                });
                
                // Auto-hide mouse cursor after inactivity
                let mouseTimer;
                document.addEventListener('mousemove', () => {
                    document.body.style.cursor = 'auto';
                    clearTimeout(mouseTimer);
                    mouseTimer = setTimeout(() => {
                        document.body.style.cursor = 'none';
                    }, 10000);
                });
            }
            
            openContratoDetail(contratoId) {
                // Modal detalle contrato
                window.open(`/dashboard/contrato/${contratoId}`, '_blank');
            }
            
            openAlertaDetail(alertaId) {
                // Modal detalle alerta
                window.open(`/dashboard/alerta/${alertaId}`, '_blank');
            }
            
            showGeneralSummary() {
                // Modal resumen general empresa
                const modal = document.createElement('div');
                modal.innerHTML = `
                    <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 10000; display: flex; align-items: center; justify-content: center;">
                        <div style="background: white; border-radius: 15px; padding: 30px; max-width: 600px; width: 90%;">
                            <h2>📊 Resumen Ejecutivo Condugas SA</h2>
                            <div style="margin: 20px 0;">
                                <!-- Contenido summary se carga dinámicamente -->
                                <div id="summaryContent">Cargando...</div>
                            </div>
                            <button onclick="this.closest('div').parentNode.remove()" 
                                    style="background: var(--condugas-azul-oscuro); color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                                Cerrar
                            </button>
                        </div>
                    </div>
                `;
                document.body.appendChild(modal);
                
                // Load summary data
                fetch('/dashboard/executive/summary')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('summaryContent').innerHTML = data.html;
                    });
            }
            
            forceRefresh() {
                fetch('/dashboard/executive/data?force=true')
                    .then(response => response.json())
                    .then(data => this.updateDashboard(data));
            }
            
            closeAllModals() {
                document.querySelectorAll('div[style*="position: fixed"]').forEach(modal => {
                    modal.remove();
                });
            }
        }
        
        // Inicializar dashboard cuando DOM esté listo
        document.addEventListener('DOMContentLoaded', () => {
            window.dashboardConductor = new DashboardConductor();
        });
    </script>
</body>
</html>
```

---

## 🏦 INTEGRACIÓN BANCARIA DETALLADA

### **💳 CONFIGURACIÓN BANCOS ESPECÍFICA:**
```python
# condugas_banking/models/bank_integration.py

BANKS_CONFIGURATION = {
    'bancolombia': {
        'bank_code': '007',
        'api_endpoint': 'https://api.grupobancolombia.com/v1/statements',
        'auth_method': 'oauth2',
        'supported_formats': ['csv', 'excel', 'api'],
        'accounts': {
            'BNK2': {
                'account_number': '****1016',
                'account_type': 'checking',
                'currency': 'COP',
                'description': 'Cuenta principal operaciones',
                'auto_import': True,
                'import_frequency': 'daily_4am'
            },
            'BNK7': {
                'account_number': '****0235',
                'account_type': 'savings',
                'currency': 'COP',
                'description': 'Cuenta secundaria',
                'auto_import': True,
                'import_frequency': 'daily_6am'
            },
            'BNK9': {
                'account_number': '****2179',
                'account_type': 'checking',
                'currency': 'COP',
                'description': 'Cuenta proyectos específicos',
                'auto_import': True,
                'import_frequency': 'daily_6am'
            },
            'BNK10': {
                'account_number': '****8289',
                'account_type': 'checking',
                'currency': 'COP',
                'description': 'Cuenta proveedores',
                'auto_import': True,
                'import_frequency': 'daily_8am'
            },
            'BNK11': {
                'account_number': '****9169',
                'account_type': 'checking',
                'currency': 'COP',
                'description': 'Cuenta específica OYMA R1',
                'auto_import': True,
                'import_frequency': 'daily_4am',
                'special_handling': 'oyma_project'
            },
            'BNK12': {
                'account_number': '****8721',
                'account_type': 'savings',
                'currency': 'COP',
                'description': 'Cuenta reserva',
                'auto_import': True,
                'import_frequency': 'daily_10am'
            }
        }
    },
    'davivienda': {
        'bank_code': '051',
        'api_endpoint': 'https://conecta.davivienda.com/public/v1/statements',
        'auth_method': 'basic',
        'supported_formats': ['ofx', 'csv'],
        'accounts': {
            'BNK3': {
                'account_number': '****nomina1',
                'account_type': 'payroll',
                'currency': 'COP',
                'description': 'Nómina empleados',
                'auto_import': True,
                'import_frequency': 'daily_5am'
            },
            'BNK8': {
                'account_number': '****nomina2',
                'account_type': 'payroll',
                'currency': 'COP',
                'description': 'Nómina directivos',
                'auto_import': True,
                'import_frequency': 'daily_5am'
            }
        }
    },
    'banco_bogota': {
        'bank_code': '001',
        'api_endpoint': 'https://www.bancodebogota.com/wps/portal/banco-de-bogota/bogota-empresas',
        'auth_method': 'scraping',  # No tiene API, usar RPA
        'supported_formats': ['excel', 'pdf'],
        'accounts': {
            'BNK4': {
                'account_number': '****epm',
                'account_type': 'checking',
                'currency': 'COP',
                'description': 'Pagos EPM + clientes principales',
                'auto_import': True,
                'import_frequency': 'daily_7am'
            }
        }
    },
    'av_villas': {
        'bank_code': '052',
        'api_endpoint': None,  # No API disponible
        'auth_method': 'scraping',
        'supported_formats': ['csv', 'excel'],
        'accounts': {
            'BNK5': {
                'account_number': '****4070',
                'account_type': 'checking', 
                'currency': 'COP',
                'description': 'Proveedores específicos',
                'auto_import': True,
                'import_frequency': 'daily_9am'
            }
        }
    },
    'banco_occidente': {
        'bank_code': '023',
        'api_endpoint': None,
        'auth_method': 'file_upload',
        'supported_formats': ['excel', 'csv'],
        'accounts': {
            'BNK6': {
                'account_number': '****occidente',
                'account_type': 'checking',
                'currency': 'COP', 
                'description': 'Operaciones regionales',
                'auto_import': False,  # Manual upload
                'import_frequency': 'weekly'
            }
        }
    }
}

class CodugasBankImporter(models.Model):
    _name = 'condugas.bank.importer'
    _description = 'Importador Automático Bancos Condugas'
    
    @api.model
    def import_all_banks_scheduled(self):
        """Cron job que ejecuta diariamente importación automática"""
        current_hour = datetime.now().hour
        
        for bank_code, bank_config in BANKS_CONFIGURATION.items():
            for account_code, account_config in bank_config['accounts'].items():
                if not account_config.get('auto_import', False):
                    continue
                    
                import_time = self._parse_import_frequency(account_config['import_frequency'])
                
                if current_hour == import_time:
                    try:
                        self._import_bank_account(bank_code, account_code, bank_config, account_config)
                    except Exception as e:
                        _logger.error(f"Error importing {bank_code}-{account_code}: {e}")
                        self._notify_import_error(bank_code, account_code, str(e))
    
    def _parse_import_frequency(self, frequency):
        """Parse frequency string to hour"""
        if 'daily_' in frequency:
            hour_str = frequency.split('daily_')[1].replace('am', '').replace('pm', '')
            hour = int(hour_str)
            return hour if 'am' in frequency else hour + 12
        return 6  # Default 6am
    
    def _import_bank_account(self, bank_code, account_code, bank_config, account_config):
        """Import específico por banco + cuenta"""
        
        journal = self.env['account.journal'].search([
            ('code', '=', account_code),
            ('type', '=', 'bank')
        ], limit=1)
        
        if not journal:
            raise Exception(f"Journal {account_code} not found")
        
        auth_method = bank_config['auth_method']
        
        if auth_method == 'oauth2':
            statements = self._import_via_oauth2(bank_config, account_config)
        elif auth_method == 'basic':
            statements = self._import_via_basic_auth(bank_config, account_config)
        elif auth_method == 'scraping':
            statements = self._import_via_scraping(bank_config, account_config)
        elif auth_method == 'file_upload':
            statements = self._import_via_file_upload(bank_config, account_config)
        else:
            raise Exception(f"Auth method {auth_method} not supported")
        
        # Procesar statements importados
        for statement_data in statements:
            self._process_bank_statement(journal, statement_data, account_config)
    
    def _import_via_oauth2(self, bank_config, account_config):
        """Import via OAuth2 API (Bancolombia)"""
        import requests
        
        # OAuth2 token
        token = self._get_oauth2_token(bank_config)
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'Condugas-Odoo-Integration/1.0'
        }
        
        # Request últimos 7 días movimientos
        from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        to_date = datetime.now().strftime('%Y-%m-%d')
        
        params = {
            'account': account_config['account_number'],
            'from_date': from_date,
            'to_date': to_date,
            'format': 'json'
        }
        
        response = requests.get(bank_config['api_endpoint'], headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json().get('statements', [])
        else:
            raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    def _import_via_basic_auth(self, bank_config, account_config):
        """Import via Basic Auth (Davivienda)"""
        import requests
        from base64 import b64encode
        
        # Credenciales desde ir.config_parameter
        username = self.env['ir.config_parameter'].sudo().get_param(f'banking.{bank_config["bank_code"]}.username')
        password = self.env['ir.config_parameter'].sudo().get_param(f'banking.{bank_config["bank_code"]}.password')
        
        credentials = b64encode(f"{username}:{password}".encode()).decode()
        
        headers = {
            'Authorization': f'Basic {credentials}',
            'Accept': 'application/json'
        }
        
        from_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        to_date = datetime.now().strftime('%Y-%m-%d')
        
        params = {
            'cuenta': account_config['account_number'],
            'fechaInicio': from_date,
            'fechaFin': to_date
        }
        
        response = requests.get(bank_config['api_endpoint'], headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json().get('movimientos', [])
        else:
            raise Exception(f"Basic Auth Error: {response.status_code}")
    
    def _import_via_scraping(self, bank_config, account_config):
        """Import via web scraping (Banco Bogotá, AV Villas)"""
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        
        # Chrome headless
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            if 'bogota' in bank_config['api_endpoint']:
                return self._scrape_banco_bogota(driver, account_config)
            elif 'villas' in bank_config.get('name', ''):
                return self._scrape_av_villas(driver, account_config)
        finally:
            driver.quit()
    
    def _scrape_banco_bogota(self, driver, account_config):
        """Scraping específico Banco Bogotá"""
        # Credenciales
        username = self.env['ir.config_parameter'].sudo().get_param('banking.001.username')
        password = self.env['ir.config_parameter'].sudo().get_param('banking.001.password')
        
        # Login
        driver.get('https://www.bancodebogota.com/wps/portal/banco-de-bogota/bogota-empresas')
        
        # Wait for login form
        driver.implicitly_wait(10)
        
        username_field = driver.find_element(By.ID, 'userId')
        password_field = driver.find_element(By.ID, 'password')
        
        username_field.send_keys(username)
        password_field.send_keys(password)
        
        login_button = driver.find_element(By.ID, 'loginButton')
        login_button.click()
        
        # Navigate to statements
        driver.implicitly_wait(15)
        
        # Click extractos
        extractos_link = driver.find_element(By.LINK_TEXT, 'Extractos')
        extractos_link.click()
        
        # Select account
        account_select = driver.find_element(By.ID, 'accountSelect')
        account_select.send_keys(account_config['account_number'][-4:])  # Últimos 4 dígitos
        
        # Select date range (últimos 7 días)
        from_date = (datetime.now() - timedelta(days=7)).strftime('%d/%m/%Y')
        to_date = datetime.now().strftime('%d/%m/%Y')
        
        from_date_field = driver.find_element(By.ID, 'fromDate')
        to_date_field = driver.find_element(By.ID, 'toDate')
        
        from_date_field.clear()
        from_date_field.send_keys(from_date)
        
        to_date_field.clear()
        to_date_field.send_keys(to_date)
        
        # Submit
        submit_button = driver.find_element(By.ID, 'consultarButton')
        submit_button.click()
        
        # Wait for results
        driver.implicitly_wait(10)
        
        # Parse table movimientos
        movements_table = driver.find_element(By.ID, 'movementsTable')
        rows = movements_table.find_elements(By.TAG_NAME, 'tr')
        
        statements = []
        for row in rows[1:]:  # Skip header
            cols = row.find_elements(By.TAG_NAME, 'td')
            if len(cols) >= 5:
                statements.append({
                    'date': cols[0].text,
                    'description': cols[1].text,
                    'reference': cols[2].text,
                    'debit': self._parse_amount(cols[3].text),
                    'credit': self._parse_amount(cols[4].text),
                    'balance': self._parse_amount(cols[5].text)
                })
        
        return statements
    
    def _process_bank_statement(self, journal, statement_data, account_config):
        """Procesar statement importado + auto-reconciliación"""
        
        # Crear/encontrar statement
        statement_name = f"{journal.code}-{datetime.now().strftime('%Y%m%d')}"
        
        existing_statement = self.env['account.bank.statement'].search([
            ('name', '=', statement_name),
            ('journal_id', '=', journal.id)
        ], limit=1)
        
        if existing_statement:
            statement = existing_statement
        else:
            statement = self.env['account.bank.statement'].create({
                'name': statement_name,
                'journal_id': journal.id,
                'date': fields.Date.today(),
                'balance_start': 0,  # Se calculará
                'balance_end_real': 0  # Se calculará
            })
        
        # Procesar cada línea
        for line_data in statement_data:
            self._create_statement_line(statement, line_data, account_config)
        
        # Auto-reconciliación
        self._auto_reconcile_statement(statement)
        
        # Notificar Andrea si hay líneas no reconciliadas
        unreconciled_lines = statement.line_ids.filtered(lambda l: not l.is_reconciled)
        if unreconciled_lines:
            self._notify_manual_reconciliation_needed(statement, unreconciled_lines)
    
    def _create_statement_line(self, statement, line_data, account_config):
        """Crear línea statement desde data importada"""
        
        amount = line_data.get('credit', 0) - line_data.get('debit', 0)
        
        # Parse date
        date_str = line_data.get('date', '')
        if '/' in date_str:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
        else:
            date_obj = fields.Date.today()
        
        # Clean description
        description = line_data.get('description', '').strip()
        reference = line_data.get('reference', '').strip()
        
        # Check if line already exists
        existing_line = self.env['account.bank.statement.line'].search([
            ('statement_id', '=', statement.id),
            ('date', '=', date_obj),
            ('amount', '=', amount),
            ('payment_ref', '=', reference)
        ], limit=1)
        
        if existing_line:
            return existing_line  # Skip duplicate
        
        # Create new line
        line = self.env['account.bank.statement.line'].create({
            'statement_id': statement.id,
            'date': date_obj,
            'payment_ref': reference,
            'narration': description,
            'amount': amount,
            'partner_id': self._identify_partner_from_description(description)
        })
        
        return line
    
    def _auto_reconcile_statement(self, statement):
        """Auto-reconciliación inteligente statement"""
        
        for line in statement.line_ids.filtered(lambda l: not l.is_reconciled):
            
            # Buscar facturas matching
            matching_moves = self._find_matching_account_moves(line)
            
            if len(matching_moves) == 1:
                # Perfect match → auto-reconcile
                self._reconcile_line_with_move(line, matching_moves[0])
            elif len(matching_moves) > 1:
                # Multiple matches → flag for manual review
                line.write({
                    'narration': f"{line.narration} [MÚLTIPLES MATCHES: {len(matching_moves)}]"
                })
            else:
                # No matches → try fuzzy matching
                fuzzy_matches = self._find_fuzzy_matches(line)
                if fuzzy_matches:
                    best_match = max(fuzzy_matches, key=lambda m: m['confidence'])
                    if best_match['confidence'] > 0.85:
                        self._reconcile_line_with_move(line, best_match['move'])
    
    def _find_matching_account_moves(self, line):
        """Encontrar movimientos contables matching exacto"""
        
        # Buscar por monto + fecha ±3 días
        date_from = line.date - timedelta(days=3)
        date_to = line.date + timedelta(days=3)
        
        domain = [
            ('amount_total', '=', abs(line.amount)),
            ('date', '>=', date_from),
            ('date', '<=', date_to),
            ('state', '=', 'posted')
        ]
        
        if line.amount > 0:  # Credit (payment received)
            domain.append(('move_type', 'in', ['out_invoice', 'out_receipt']))
        else:  # Debit (payment made)
            domain.append(('move_type', 'in', ['in_invoice', 'in_receipt']))
        
        return self.env['account.move'].search(domain)
    
    def _find_fuzzy_matches(self, line):
        """Encontrar matches aproximados usando similaridad texto"""
        import difflib
        
        # Buscar facturas en rango fecha amplio
        date_from = line.date - timedelta(days=10) 
        date_to = line.date + timedelta(days=10)
        
        candidate_moves = self.env['account.move'].search([
            ('date', '>=', date_from),
            ('date', '<=', date_to),
            ('state', '=', 'posted'),
            ('amount_total', '>', abs(line.amount) * 0.8),  # ±20% amount
            ('amount_total', '<', abs(line.amount) * 1.2)
        ])
        
        matches = []
        line_description = line.narration.lower()
        
        for move in candidate_moves:
            # Compare description similarity
            move_ref = (move.ref or '').lower()
            move_name = (move.name or '').lower()
            partner_name = (move.partner_id.name or '').lower()
            
            similarities = [
                difflib.SequenceMatcher(None, line_description, move_ref).ratio(),
                difflib.SequenceMatcher(None, line_description, move_name).ratio(),
                difflib.SequenceMatcher(None, line_description, partner_name).ratio()
            ]
            
            max_similarity = max(similarities)
            
            # Amount similarity
            amount_diff = abs(abs(line.amount) - move.amount_total) / move.amount_total
            amount_similarity = 1 - amount_diff
            
            # Date similarity
            date_diff = abs((line.date - move.date).days)
            date_similarity = max(0, 1 - (date_diff / 10))
            
            # Combined confidence
            confidence = (max_similarity * 0.5 + 
                         amount_similarity * 0.3 + 
                         date_similarity * 0.2)
            
            if confidence > 0.6:  # Minimum threshold
                matches.append({
                    'move': move,
                    'confidence': confidence,
                    'similarity_details': {
                        'text': max_similarity,
                        'amount': amount_similarity,
                        'date': date_similarity
                    }
                })
        
        return sorted(matches, key=lambda m: m['confidence'], reverse=True)
    
    def _reconcile_line_with_move(self, line, move):
        """Reconciliar línea bancaria con movimiento contable"""
        
        # Encontrar línea a reconciliar
        receivable_line = move.line_ids.filtered(
            lambda l: l.account_id.account_type in ['asset_receivable', 'liability_payable']
        )
        
        if receivable_line:
            # Create payment
            payment_vals = {
                'payment_type': 'inbound' if line.amount > 0 else 'outbound',
                'partner_id': move.partner_id.id,
                'amount': abs(line.amount),
                'currency_id': line.statement_id.currency_id.id,
                'date': line.date,
                'ref': line.payment_ref,
                'journal_id': line.statement_id.journal_id.id
            }
            
            payment = self.env['account.payment'].create(payment_vals)
            payment.action_post()
            
            # Reconcile
            lines_to_reconcile = receivable_line + payment.line_ids.filtered(
                lambda l: l.account_id == receivable_line.account_id
            )
            
            lines_to_reconcile.reconcile()
            
            # Mark statement line as reconciled
            line.write({
                'is_reconciled': True,
                'narration': f"{line.narration} [AUTO-RECONCILIADO: {move.name}]"
            })
    
    def _notify_manual_reconciliation_needed(self, statement, unreconciled_lines):
        """Notificar Andrea líneas que necesitan reconciliación manual"""
        
        andrea = self.env.ref('base.user_admin')  # O buscar por email
        
        message = f"""
        🏦 CONCILIACIÓN BANCARIA - REVISIÓN MANUAL REQUERIDA
        
        Banco: {statement.journal_id.name}
        Statement: {statement.name}
        Fecha: {statement.date}
        
        Líneas sin conciliar: {len(unreconciled_lines)}
        
        Detalle líneas:
        """
        
        for line in unreconciled_lines:
            message += f"\n• ${line.amount:,.0f} - {line.narration} - {line.date}"
        
        message += f"\n\nPor favor revisa en: /web#action=account.action_bank_statement_tree&model=account.bank.statement&id={statement.id}"
        
        # Enviar email + notificación dashboard
        andrea.notify_info(message)
        
        # También enviar WhatsApp si configurado
        if self.env['ir.config_parameter'].sudo().get_param('banking.whatsapp.enabled'):
            self._send_whatsapp_notification(message)
    
    def _parse_amount(self, amount_str):
        """Parse amount string to float"""
        if not amount_str:
            return 0.0
            
        # Remove currency symbols and formatting
        clean_amount = amount_str.replace('$', '').replace(',', '').replace('.', '')
        
        # Handle Colombian format (dots as thousands, comma as decimal)
        if ',' in amount_str:
            parts = clean_amount.split(',')
            if len(parts) == 2 and len(parts[1]) <= 2:
                # Comma as decimal separator
                clean_amount = parts[0] + '.' + parts[1]
        
        try:
            return float(clean_amount)
        except:
            return 0.0
    
    def _identify_partner_from_description(self, description):
        """Identificar partner desde descripción bancaria"""
        if not description:
            return False
            
        # Buscar partners por nombre en descripción
        partners = self.env['res.partner'].search([('active', '=', True)])
        
        description_lower = description.lower()
        
        for partner in partners:
            partner_name = partner.name.lower()
            if partner_name in description_lower or description_lower in partner_name:
                if len(partner_name) > 3:  # Avoid false positives
                    return partner.id
        
        # Buscar por VAT number en descripción  
        import re
        vat_pattern = re.search(r'\d{8,12}', description)
        if vat_pattern:
            vat_number = vat_pattern.group()
            partner_by_vat = self.env['res.partner'].search([('vat', 'like', vat_number)], limit=1)
            if partner_by_vat:
                return partner_by_vat.id
        
        return False
```

---

## 🎯 CRONOGRAMA DETALLADO + ENTREGABLES

### **📅 CRONOGRAMA SEMANAL ESPECÍFICO:**

#### **ABRIL SEMANA 1 (1-7 abril):**
```
LUNES 1 ABRIL:
□ Setup servidor producción Ubuntu 22.04
□ Instalación PostgreSQL 15 + configuración performance
□ Instalación Odoo 19 Enterprise + módulos base
□ Migración 452 empleados desde sistema actual
□ Testing conexión + performance básico

MARTES 2 ABRIL:
□ Creación 17 cuentas analíticas = contratos
□ Configuración 13 journals bancarios
□ Setup 5 campos custom employees (4D classification)
□ Importación estructura departamental actual
□ Testing separación financiera básica

MIÉRCOLES 3 ABRIL:
□ Configuración timesheet employees centrales
□ Setup workflow aprobaciones básico
□ Creación usuarios + permisos base directors
□ Testing timesheet input + validation
□ Setup backup automático + restore testing

JUEVES 4 ABRIL:
□ Dashboard básico Sebastián (HTML + CSS)
□ Conexión dashboard → Odoo data via API
□ Testing responsivo + TDAH-friendly design  
□ Setup alertas básicas (email only)
□ Training directores: navigation + basic inputs

VIERNES 5 ABRIL:
□ Go-live ambiente staging complete
□ UAT con Sebastián + Andrea + Camilo
□ Fixes issues encontrados UAT
□ Preparación deployment production
□ Documentation + troubleshooting guide

WEEKEND:
□ Deployment production supervised
□ Monitoring 24/7 primeros días
□ Rollback plan tested + ready
```

#### **ABRIL SEMANA 2 (8-14 abril):**
```
LUNES 8 ABRIL:
□ Importación automática extractos 3 bancos priority
□ Configuración conciliación automática basic
□ Testing API Bancolombia OAuth2 integration
□ Setup Davivienda basic auth connection
□ Testing importación + validation data

MARTES 9 ABRIL:
□ Separación financiera automática por contrato
□ Configuración nómina marzo separada por proyecto
□ Testing P&L automático por contrato
□ Setup reportes automáticos Andrea
□ Validation accuracy financial separation

MIÉRCOLES 10 ABRIL:
□ Dashboard Sebastián version 2.0 (más métricas)
□ Setup WebSocket tiempo real updates
□ Testing dashboard performance + responsiveness
□ Configuración notificaciones push básicas
□ Mobile optimization básico

JUEVES 11 ABRIL:
□ Training masivo employees (básico navigation)
□ Setup timesheet compliance monitoring
□ Configuración validation rules anti-errores
□ Testing workflow aprobaciones by role
□ Documentation user guides por rol

VIERNES 12 ABRIL:
□ Sistema clasificación A/B/C employees basic
□ Algoritmo scoring básico productividad
□ Dashboard classification progress visual
□ Testing accuracy clasificación vs manual
□ Preparación datos presentation week 3
```

#### **ABRIL SEMANA 3 (15-21 abril):**
```
LUNES 15 ABRIL:
□ Sistema alertas automáticas core funcionando
□ Configuración 15 alertas predefinidas críticas
□ Testing triggers automáticos + notifications
□ Setup escalation matrix by alert type
□ Training team alertas + response procedures

MARTES 16 ABRIL:
□ Interface voz operarios development start
□ Setup OpenClaw + Claude integration básico
□ Testing speech recognition español Colombian
□ Desarrollo diccionario jerga construcción
□ Testing audio quality + transcription accuracy

MIÉRCOLES 17 ABRIL:
□ Algoritmos clasificación empleados refinados
□ Scoring multifuncionalidad + especialización
□ Dashboard empleados real-time updates
□ Testing accuracy clasificación automated
□ Validation manual vs automated results

JUEVES 18 ABRIL:
□ Reportes automáticos clients basic setup
□ Integration APIs EPM preparación básica
□ Testing data export formats clients
□ Setup automated client communications
□ Documentation client integration procedures

VIERNES 19 ABRIL:
□ UAT completo system integration
□ Testing all modules working together
□ Performance optimization + bottlenecks fix
□ Security testing + penetration test básico
□ Final validation + go/no-go decision
```

#### **ABRIL SEMANA 4 (22-28 abril):**
```
LUNES 22 ABRIL:
□ Go-live production complete system
□ All employees using system (no fallback)
□ Monitoring intensive 24/7
□ Support on-site + remote available
□ Issue tracking + resolution tiempo real

MARTES 23 ABRIL:
□ Nómina marzo separated automática por contrato
□ Validation accuracy nómina vs manual process
□ Testing payroll integration + bank payments
□ Documentation payroll procedures automated
□ Training HR team new payroll workflow

MIÉRCOLES 24 ABRIL:
□ Classification empleados A/B/C finalizada
□ Dashboard classification results accurate
□ Legal preparation documentación terminaciones
□ Plan transition 452→250 detailed ready
□ Validation legal compliance + procedures

JUEVES 25 ABRIL:
□ System stable + performance optimized
□ All integrations working without manual intervention
□ Backup + restore procedures validated production
□ User adoption >90% all roles
□ Documentation complete + knowledge transfer

VIERNES 26 ABRIL:
□ Métricas before/after documented
□ ROI calculation with real data
□ Client presentation + demo recording
□ Success metrics validation
□ Preparation next phase (Mayo)

WEEKEND:
□ System monitoring + health checks
□ Performance optimization based usage real
□ Planning Mayo advanced features
```

---

## 🎯 PREGUNTAS TÉCNICAS ESPECÍFICAS EMANUEL

### **🛠️ DESARROLLO + IMPLEMENTACIÓN:**

1. **¿Puedes desarrollar módulos custom Odoo** con la complejidad mostrada arriba (Python + XML + JavaScript + CSS)?

2. **¿Tienes experiencia específica PostgreSQL optimization** para databases 450+ usuarios concurrent?

3. **¿Puedes implementar WebSockets** para dashboard tiempo real sin performance issues?

4. **¿Tienes experiencia integración OpenClaw + Claude** para voice recognition español técnico?

5. **¿Puedes desarrollar algoritmos machine learning** para clasificación empleados automática?

### **🏦 INTEGRACIONES BANCARIAS:**

6. **¿Has implementado antes OAuth2 + Basic Auth + Web Scraping** para múltiples bancos simultaneously?

7. **¿Experiencia específica Selenium** para scraping banking websites Colombia?

8. **¿Puedes manejar different data formats** (CSV, Excel, OFX, PDF, API JSON) en single workflow?

9. **¿Algoritmos reconciliación automática** con fuzzy matching + machine learning has implementado?

10. **¿Rate limiting + error handling** para APIs bancarios has manejado production?

### **📊 DASHBOARD + UX:**

11. **¿Experiencia específica designing for TDAH** users with minimal navigation?

12. **¿Puedes implementar dashboard responsive** que funcione tablets + phones + desktop perfectly?

13. **¿WebSockets + Server-Sent Events** para push notifications tiempo real has usado?

14. **¿JavaScript frameworks** modern (React, Vue, Angular) o prefieres vanilla JS?

15. **¿CSS animations + transitions** para maintain user attention without being distracting?

### **🎤 INTERFACE VOZ + MOBILE:**

16. **¿Has integrado antes speech recognition** con sistemas ERP enterprise?

17. **¿Experiencia specific OpenClaw API** + Claude integration para voice workflows?

18. **¿Tablet deployment** industrial environments con 4G connectivity has manejado?

19. **¿Natural Language Processing** para parsing comandos técnicos construcción has desarrollado?

20. **¿Offline capability** cuando tablets pierden connectivity 4G temporal?

### **⚡ PERFORMANCE + SCALE:**

21. **¿Sistema que manejas currently** cuántos usuarios concurrent maximum?

22. **¿Database optimization** PostgreSQL para queries complex con analytical data?

23. **¿Caching strategies** (Redis, Memcached) para dashboard performance has implementado?

24. **¿Load balancing + clustering** Odoo multiple servers has configurado?

25. **¿Monitoring tools** (Grafana, Prometheus) para production systems usas?

### **💰 PRESUPUESTO + TIMELINE:**

26. **Tu presupuesto total** para desarrollar todo esto ¿cuánto sería exactly?

27. **¿Timeline realista** para cada fase: abril base, mayo advanced, junio optimization?

28. **¿Team additional** necesitas o puedes hacer solo todo development?

29. **¿Support post-implementation** cuántos horas/semana budgetear?

30. **¿Garantía específica** ROI $920M COP/año puedes dar con métricas documentadas?

---

## 🚨 RED FLAGS A DETECTAR EMANUEL

### **❌ RESPUESTAS PROBLEMÁTICAS:**
- *"Sí, todo se puede hacer"* sin detalles técnicos específicos
- *"Odoo standard tiene todo"* ignorando 40% custom development required  
- *"Timeline no es problema"* sin breakdown realistic tasks
- *"No necesito ayuda additional"* para scope este tamaño
- *"Presupuesto después definimos"* sin estimate serious

### **✅ RESPUESTAS ESPERADAS:**
- *"He hecho X similar, pero Y componente necesitaría research additional Z días"*
- *"Odoo standard cubre 60%, necesito develop custom modules para 40% restante"*
- *"Timeline realista sería X para base, Y para advanced, contingency Z días"*
- *"Para voice integration necesitaría specialist additional o 3 semanas extra research"*
- *"Presupuesto estimate $X breakdown: development Y, infrastructure Z, contingency W"*

---

## 🎯 RESULTADO ESPERADO

**Emanuel debe demostrar:**
1. **Comprensión técnica específica** cada componente
2. **Experiencia real** sistemas similar complexity
3. **Timeline realistic** con contingencies
4. **Presupuesto detailed** breakdown justified  
5. **Plan específico** cómo logra cada objetivo técnicamente

**Sebastián puede decidir:**
- ✅ **Proceder con Emanuel** si demonstrates competency real
- 🤝 **Emanuel + specialist additional** para components complex
- ❌ **Buscar developer different** si gaps críticos detected

**🎯 ESTE ES EL BRIEFING MÁS DETALLADO POSIBLE. EMANUEL DEBE RESPONDER CON MISMO NIVEL DETAIL O ADMITIR QUE NECESITA APOYO SPECIFIC.**