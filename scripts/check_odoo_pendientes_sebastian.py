#!/usr/bin/env python3
import xmlrpc.client
import sys
from datetime import datetime, timedelta

# Configuración Odoo
url = 'https://condugas-sa.odoo.com'
db = 'siendoconsulting-condugas-main-27941080'
username = 's.sanchez@condugas.com.co'
password = 'ca4174ee968614204dfc083de14add7039e74e6e'
sebastian_partner_id = 865
sebastian_user_id = 19

try:
    # Conexión a Odoo
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, password, {})
    
    if not uid:
        print("Error de autenticación")
        sys.exit(1)
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    pendientes = []
    
    # 1. Pagos en draft asignados a Sebastián
    payments = models.execute_kw(db, uid, password, 'account.payment', 'search_read',
        [[('state', '=', 'draft'), ('partner_id', '=', sebastian_partner_id)]],
        {'fields': ['name', 'amount', 'currency_id', 'date', 'payment_type']})
    
    if payments:
        pendientes.append(f"💰 Pagos en borrador ({len(payments)}):")
        for p in payments:
            currency = p['currency_id'][1] if p['currency_id'] else 'COP'
            tipo = p['payment_type']
            pendientes.append(f"  • {p['name']}: ${p['amount']:,.0f} {currency} ({tipo})")
    
    # 2. Mensajes recientes donde mencionan a Sebastián (últimos 7 días)
    fecha_limite = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    
    messages = models.execute_kw(db, uid, password, 'mail.message', 'search_read',
        [['|', 
          ('partner_ids', 'in', [sebastian_partner_id]),
          ('body', 'ilike', 'sebastian'),
          ('create_date', '>=', fecha_limite)]],
        {'fields': ['subject', 'body', 'author_id', 'create_date', 'model', 'res_id'],
         'limit': 5, 'order': 'create_date desc'})
    
    mensajes_relevantes = []
    for msg in messages:
        if msg['author_id'] and msg['author_id'][0] != sebastian_partner_id:  # Excluir sus propios mensajes
            body_clean = msg['body'].replace('<p>', '').replace('</p>', '').replace('\n', ' ')[:100] if msg['body'] else ''
            if body_clean:
                mensajes_relevantes.append({
                    'autor': msg['author_id'][1],
                    'fecha': msg['create_date'],
                    'contenido': body_clean
                })
    
    if mensajes_relevantes:
        pendientes.append(f"💬 Mensajes recientes ({len(mensajes_relevantes)}):")
        for m in mensajes_relevantes[:3]:  # Solo los 3 más recientes
            pendientes.append(f"  • {m['autor']}: {m['contenido']}...")
    
    # 3. Actividades pendientes asignadas a Sebastián
    activities = models.execute_kw(db, uid, password, 'mail.activity', 'search_read',
        [[('user_id', '=', sebastian_user_id), ('date_deadline', '>=', datetime.now().strftime('%Y-%m-%d'))]],
        {'fields': ['activity_type_id', 'summary', 'date_deadline', 'res_name', 'res_model'],
         'order': 'date_deadline asc'})
    
    if activities:
        pendientes.append(f"📋 Actividades pendientes ({len(activities)}):")
        for a in activities[:5]:  # Solo las 5 más próximas
            tipo = a['activity_type_id'][1] if a['activity_type_id'] else 'Actividad'
            fecha = a['date_deadline']
            resumen = a['summary'] or a['res_name'] or 'Sin descripción'
            pendientes.append(f"  • {tipo}: {resumen} - Vence: {fecha}")
    
    # Resultado final
    if pendientes:
        print("🎯 Pendientes Sebastián - Odoo Condugas")
        print("\n".join(pendientes))
    else:
        # Si no hay pendientes, no imprimir nada (según instrucciones)
        pass

except Exception as e:
    print(f"Error conectando a Odoo: {e}")
    sys.exit(1)