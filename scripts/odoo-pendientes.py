#!/usr/bin/env python3
import xmlrpc.client
import sys
from datetime import datetime, timedelta

# Configuración Odoo
url = 'https://condugas-sa.odoo.com'
db = 'siendoconsulting-condugas-main-27941080'
username = 's.sanchez@condugas.com.co'
api_key = 'ca4174ee968614204dfc083de14add7039e74e6e'
user_id = 19
partner_id = 865

def connect_odoo():
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    uid = common.authenticate(db, username, api_key, {})
    if not uid:
        print("Error: No se pudo autenticar")
        return None, None
    
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    return uid, models

def check_draft_payments(uid, models):
    """Revisa pagos en estado draft asignados a Sebastián"""
    try:
        payments = models.execute_kw(db, uid, api_key, 'account.payment', 'search_read', 
            [[('state', '=', 'draft'), ('partner_id', '=', partner_id)]], 
            {'fields': ['name', 'amount', 'payment_date', 'partner_id']})
        return payments
    except Exception as e:
        print(f"Error consultando pagos: {e}")
        return []

def check_recent_messages(uid, models):
    """Revisa mensajes recientes donde mencionan a Sebastián"""
    try:
        # Buscar mensajes de los últimos 7 días
        date_limit = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        messages = models.execute_kw(db, uid, api_key, 'mail.message', 'search_read', 
            [['|', ('partner_ids', 'in', [partner_id]), ('author_id', '=', partner_id),
              ('date', '>=', date_limit), ('message_type', '!=', 'notification')]], 
            {'fields': ['subject', 'body', 'date', 'author_id'], 'limit': 10, 'order': 'date desc'})
        return messages
    except Exception as e:
        print(f"Error consultando mensajes: {e}")
        return []

def check_pending_activities(uid, models):
    """Revisa actividades pendientes asignadas a Sebastián"""
    try:
        activities = models.execute_kw(db, uid, api_key, 'mail.activity', 'search_read', 
            [[('user_id', '=', user_id), ('date_deadline', '<=', datetime.now().strftime('%Y-%m-%d'))]], 
            {'fields': ['summary', 'note', 'date_deadline', 'res_name', 'activity_type_id']})
        return activities
    except Exception as e:
        print(f"Error consultando actividades: {e}")
        return []

def main():
    uid, models = connect_odoo()
    if not uid:
        return
    
    pendientes = []
    
    # 1. Pagos en draft
    draft_payments = check_draft_payments(uid, models)
    if draft_payments:
        pendientes.append(f"💰 Pagos pendientes ({len(draft_payments)}):")
        for payment in draft_payments[:3]:  # Máximo 3
            pendientes.append(f"  • ${payment['amount']:,.0f} - {payment['name']}")
    
    # 2. Mensajes recientes
    recent_messages = check_recent_messages(uid, models)
    unread_count = len([m for m in recent_messages if m.get('author_id') and m['author_id'][0] != partner_id])
    if unread_count > 0:
        pendientes.append(f"💬 Mensajes recientes ({unread_count})")
    
    # 3. Actividades pendientes
    pending_activities = check_pending_activities(uid, models)
    if pending_activities:
        pendientes.append(f"📋 Actividades pendientes ({len(pending_activities)}):")
        for activity in pending_activities[:3]:  # Máximo 3
            deadline = activity['date_deadline']
            pendientes.append(f"  • {activity['summary']} - {activity['res_name']} (vence: {deadline})")
    
    if pendientes:
        print("🎯 **Pendientes Odoo Condugas:**")
        print("\n".join(pendientes))
        print(f"\n📊 Revisado: {datetime.now().strftime('%H:%M %d/%m/%Y')}")
    else:
        print("")  # No hay pendientes, no enviar nada

if __name__ == "__main__":
    main()