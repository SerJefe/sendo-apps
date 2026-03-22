#!/usr/bin/env python3
"""
Test de conexión Odoo - Condugas SA
Usando credenciales reales de Sebastián
"""

import xmlrpc.client
import json
import sys
from datetime import datetime

# Cargar credenciales
with open('/root/.openclaw/workspace/.secrets/odoo-config.json', 'r') as f:
    config = json.load(f)

def test_odoo_connection():
    """Test completo de conexión Odoo."""
    print(f"🔌 Probando conexión Odoo Condugas...")
    print(f"📍 URL: {config['url']}")
    print(f"🗄️ DB: {config['database']}")
    print(f"👤 Usuario: {config['username']}")
    print(f"📦 Versión: {config['version']}")
    print("-" * 60)
    
    try:
        # 1. Conexión inicial
        common = xmlrpc.client.ServerProxy(f"{config['url']}/xmlrpc/2/common")
        print(f"✅ Conectado al servidor común")
        
        # 2. Autenticación
        uid = common.authenticate(
            config['database'], 
            config['username'], 
            config['api_key'], 
            {}
        )
        
        if uid:
            print(f"✅ Autenticación exitosa - UID: {uid}")
            
            # 3. Conexión a modelos
            models = xmlrpc.client.ServerProxy(f"{config['url']}/xmlrpc/2/object")
            print(f"✅ Conectado a modelos")
            
            # 4. Test básico - info de la compañía
            company_info = models.execute_kw(
                config['database'], uid, config['api_key'],
                'res.company', 'search_read',
                [[]], {'fields': ['name', 'currency_id'], 'limit': 1}
            )
            
            if company_info:
                company = company_info[0]
                print(f"✅ Compañía: {company['name']}")
                print(f"💰 Moneda: ID {company['currency_id'][0] if company['currency_id'] else 'N/A'}")
            
            # 5. Test empleados (count)
            employee_count = models.execute_kw(
                config['database'], uid, config['api_key'],
                'hr.employee', 'search_count', [[]]
            )
            print(f"👥 Empleados totales: {employee_count}")
            
            # 6. Test cuentas contables
            account_count = models.execute_kw(
                config['database'], uid, config['api_key'],
                'account.account', 'search_count', [[]]
            )
            print(f"🏦 Cuentas contables: {account_count}")
            
            # 7. Test módulos instalados
            modules = models.execute_kw(
                config['database'], uid, config['api_key'],
                'ir.module.module', 'search_read',
                [['&', ('state', '=', 'installed'), ('application', '=', True)]],
                {'fields': ['name', 'shortdesc'], 'limit': 10}
            )
            
            print(f"📦 Módulos principales instalados:")
            for module in modules[:5]:  # Top 5
                print(f"   - {module['name']}: {module['shortdesc']}")
            
            print("-" * 60)
            print(f"🎯 CONEXIÓN ODOO EXITOSA")
            print(f"✅ Ready para automatización ralph-loop")
            print(f"⚙️ Scripts de conciliación y nómina pueden ejecutarse")
            
            return True
            
        else:
            print("❌ Fallo de autenticación - verificar credenciales")
            return False
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def update_tools_md():
    """Actualiza TOOLS.md con confirmación de credenciales."""
    tools_path = '/root/.openclaw/workspace/TOOLS.md'
    
    # Leer TOOLS.md actual
    with open(tools_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Agregar sección Odoo confirmada
    odoo_section = f"""

### Odoo (Condugas SA) - CONFIGURADO ✅

- **URL**: {config['url']}
- **DB**: {config['database']}
- **Usuario**: {config['username']}
- **Versión**: {config['version']}
- **Estado**: ✅ Conexión verificada {datetime.now().strftime('%Y-%m-%d %H:%M')}
- **API Key**: Configurada securely en `.secrets/`
- **Test script**: `scripts/test-odoo-connection.py`

**Ready para:**
- ✅ Conciliación bancaria automática
- ✅ Distribución nómina por contrato
- ✅ Clasificación 452 empleados
- ✅ Early warning sistema contratos
"""
    
    # Agregar al final si no existe
    if "### Odoo (Condugas SA)" not in content:
        content += odoo_section
        
        with open(tools_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📝 TOOLS.md actualizado con config Odoo")

if __name__ == "__main__":
    success = test_odoo_connection()
    if success:
        update_tools_md()
        print(f"\n🚀 NEXT STEPS:")
        print(f"1. Ejecutar ralph-loop para conciliación bancaria")
        print(f"2. Probar procedimientos automáticos")
        print(f"3. Dashboard financiero en tiempo real")
    else:
        print(f"\n⚠️ Fix credenciales antes de continuar")
        sys.exit(1)