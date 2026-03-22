# Odoo API Guide — Condugas SA

## Conexión y Autenticación

```python
import xmlrpc.client

# Configuración Condugas
url = 'https://condugas-sa.odoo.com'
db = 'siendoconsulting-condugas-main-27941080'
username = 'user@condugas.com.co'  # Tu usuario
password = 'your_api_key'  # API key generado en Odoo

# Conexión
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if uid:
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    print(f"✅ Conectado como user ID: {uid}")
else:
    print("❌ Error de autenticación")
```

## Operaciones CRUD Básicas

### 1. Lectura de Datos (READ)

```python
# Buscar registros
def search_records(model, domain=[], fields=[], limit=None):
    record_ids = models.execute_kw(
        db, uid, password, model, 'search', 
        [domain], {'limit': limit} if limit else {}
    )
    
    if fields and record_ids:
        return models.execute_kw(
            db, uid, password, model, 'read', 
            [record_ids], {'fields': fields}
        )
    return record_ids

# Ejemplos específicos Condugas
# Empleados activos
empleados = search_records('hr.employee', 
    [('active', '=', True)], 
    ['name', 'department_id', 'job_id', 'parent_id']
)

# Facturas no conciliadas
facturas_pendientes = search_records('account.move',
    [('state', '=', 'posted'), ('payment_state', '!=', 'paid')],
    ['name', 'partner_id', 'amount_total', 'invoice_date']
)

# Productos con stock bajo
productos_stock = search_records('product.product',
    [('qty_available', '<', 10), ('active', '=', True)],
    ['name', 'qty_available', 'virtual_available', 'categ_id']
)
```

### 2. Creación de Registros (CREATE)

```python
# Crear empleado
nuevo_empleado = models.execute_kw(db, uid, password, 'hr.employee', 'create', [{
    'name': 'Juan Pérez',
    'work_email': 'juan.perez@condugas.com.co',
    'department_id': 5,  # ID del departamento
    'job_id': 12,  # ID del cargo
    'work_phone': '+57 300 123 4567',
    'address_home_id': False,  # Opcional
}])

# Crear asiento contable
asiento = models.execute_kw(db, uid, password, 'account.move', 'create', [{
    'move_type': 'entry',
    'date': '2026-03-20',
    'ref': 'Conciliación bancaria automática',
    'line_ids': [
        (0, 0, {  # Línea débito
            'name': 'Transferencia banco',
            'account_id': 123,  # ID cuenta bancaria
            'debit': 1000000,
            'credit': 0,
        }),
        (0, 0, {  # Línea crédito
            'name': 'Contrapartida',
            'account_id': 456,  # ID cuenta contrapartida
            'debit': 0,
            'credit': 1000000,
        })
    ]
}])
```

### 3. Actualización (UPDATE)

```python
# Actualizar empleado
models.execute_kw(db, uid, password, 'hr.employee', 'write', 
    [[empleado_id], {'department_id': nuevo_departamento_id}])

# Confirmar nóminas en borrador
nominas_borrador = search_records('hr.payslip', [('state', '=', 'draft')])
if nominas_borrador:
    models.execute_kw(db, uid, password, 'hr.payslip', 'write',
        [nominas_borrador, {'state': 'done'}])
```

### 4. Eliminación (DELETE)

```python
# CUIDADO: Eliminar es irreversible
# models.execute_kw(db, uid, password, 'model.name', 'unlink', [[record_ids]])

# Mejor: desactivar
models.execute_kw(db, uid, password, 'hr.employee', 'write', 
    [[empleado_id], {'active': False}])
```

## Modelos Clave Condugas

### Contabilidad (account.*)
```python
# Cuentas contables
cuentas = search_records('account.account', 
    [('company_id', '=', 1)], 
    ['code', 'name', 'account_type', 'reconcile'])

# Asientos contables
asientos = search_records('account.move',
    [('date', '>=', '2026-03-01'), ('state', '=', 'posted')],
    ['name', 'date', 'amount_total', 'state', 'line_ids'])

# Líneas de asientos
lineas = search_records('account.move.line',
    [('move_id', 'in', [move_id])],
    ['name', 'account_id', 'debit', 'credit', 'reconciled'])
```

### RRHH (hr.*)
```python
# Empleados por departamento
empleados_proyectos = search_records('hr.employee',
    [('department_id.name', 'ilike', 'proyecto')],
    ['name', 'job_id', 'parent_id', 'work_email'])

# Nóminas del mes
nominas_marzo = search_records('hr.payslip',
    [('date_from', '>=', '2026-03-01'), ('date_to', '<=', '2026-03-31')],
    ['employee_id', 'name', 'state', 'net_wage', 'gross_wage'])

# Contratos activos
contratos = search_records('hr.contract',
    [('state', '=', 'open')],
    ['employee_id', 'name', 'wage', 'date_start', 'analytic_account_id'])
```

### Proyectos/Contratos (project.*, account.analytic.*)
```python
# Proyectos activos
proyectos = search_records('project.project',
    [('active', '=', True)],
    ['name', 'partner_id', 'analytic_account_id', 'date_start', 'user_id'])

# Cuentas analíticas (contratos)
cuentas_analiticas = search_records('account.analytic.account',
    [('company_id', '=', 1)],
    ['name', 'code', 'partner_id', 'project_ids'])
```

## Casos de Uso Específicos

### Conciliación Bancaria Automática
```python
def conciliar_banco(banco_id, fecha_desde, fecha_hasta):
    # 1. Obtener extracto bancario
    extractos = search_records('account.bank.statement',
        [('journal_id', '=', banco_id), 
         ('date', '>=', fecha_desde), 
         ('date', '<=', fecha_hasta)],
        ['name', 'balance_start', 'balance_end_real', 'line_ids'])
    
    # 2. Obtener líneas no conciliadas
    lineas_pendientes = search_records('account.move.line',
        [('account_id.account_type', '=', 'asset_cash'),
         ('reconciled', '=', False),
         ('journal_id', '=', banco_id)],
        ['name', 'debit', 'credit', 'date', 'ref'])
    
    # 3. Algoritmo de matching por monto + fecha ±2 días
    # 4. Crear reconciliación automática
    
    return f"✅ Conciliadas {len(matches)} transacciones"
```

### Nómina por Contrato
```python
def distribuir_nomina_por_contrato():
    # 1. Obtener empleados con contrato analítico
    empleados = search_records('hr.employee',
        [('contract_id.analytic_account_id', '!=', False)],
        ['name', 'contract_id', 'department_id'])
    
    # 2. Por cada nómina confirmada, crear distribución analítica
    for emp in empleados:
        contract = search_records('hr.contract', 
            [('id', '=', emp['contract_id'][0])],
            ['analytic_account_id', 'wage'])
        
        # 3. Crear línea analítica en asiento nómina
        # account.analytic.line con account_id = contract.analytic_account_id
    
    return "✅ Nóminas distribuidas por contrato"
```

## Manejo de Errores y Límites

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(60 / calls_per_minute)  # Throttling simple
            try:
                return func(*args, **kwargs)
            except xmlrpc.client.Fault as e:
                if 'limit' in str(e).lower():
                    print(f"⚠️  Rate limit hit, esperando 30s...")
                    time.sleep(30)
                    return func(*args, **kwargs)
                else:
                    print(f"❌ Error Odoo: {e}")
                    return None
        return wrapper
    return decorator

@rate_limit(30)  # 30 calls per minute máximo
def safe_search(model, domain, fields):
    return search_records(model, domain, fields, limit=100)
```

## Configuración Condugas Específica

```python
# IDs importantes Condugas (verificar en tu instancia)
CONDUGAS_CONFIG = {
    'company_id': 1,  # Condugas S.A BIC
    'currency_id': 6,  # COP
    'banks': {
        'bancolombia_corriente': 123,
        'bancolombia_ahorros': 124,
        'davivienda': 125,
        # ... resto de 12 bancos
    },
    'departamentos': {
        'proyectos': 5,
        'administracion': 6,
        'financiero': 7,
        # ... completar con IDs reales
    },
    'cuentas_principales': {
        'efectivo': '1105',
        'bancos': '111005',
        'proveedores': '2205',
        'nomina': '2505',
    }
}
```

## Next Steps

1. **Verificar IDs reales** en tu instancia Odoo
2. **Generar API key** en Odoo > Configuración > Usuarios > Tu usuario > Claves API
3. **Testear conexión** con datos no críticos primero
4. **Implementar logging** para auditoría de cambios automáticos

**⚠️ IMPORTANTE:** Siempre testear en ambiente de desarrollo antes de producción. Los cambios en Odoo son inmediatos y pueden afectar contabilidad en vivo.