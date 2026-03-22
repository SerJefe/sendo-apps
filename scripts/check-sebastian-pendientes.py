#!/usr/bin/env python3

import xmlrpc.client
from datetime import datetime, timedelta
import os

# Configuración Odoo
url = 'https://condugas-sa.odoo.com'
db = 'siendoconsulting-condugas-main-27941080'
username = 's.sanchez@condugas.com.co'
api_key = 'ca4174ee968614204dfc083de14add7039e74e6e'

# IDs de Sebastián
sebastian_user_id = 19
sebastian_partner_id = 865

def connect_odoo():
    common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
    models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # Autenticar
    uid = common.authenticate(db, username, api_key, {})
    if not uid:
        raise Exception("Error de autenticación")
    
    return models, uid

def check_pending_payments(models, uid):
    """Revisar pagos en estado draft asignados a Sebastián"""
    try:
        payment_ids = models.execute_kw(db, uid, api_key, 'account.payment', 'search', [
            [('state', '=', 'draft'), ('partner_id', '=', sebastian_partner_id)]
        ])
        
        if not payment_ids:
            return []
            
        payments = models.execute_kw(db, uid, api_key, 'account.payment', 'read', [payment_ids], 
                                   {'fields': ['name', 'amount', 'date', 'partner_id', 'payment_type']})
        
        results = []
        for payment in payments:
            results.append(f"💰 Pago draft: {payment['name']} - ${payment['amount']:,.0f} ({payment['payment_type']})")
        
        return results
    except Exception as e:
        return [f"❌ Error revisando pagos: {e}"]

def check_recent_mentions(models, uid):
    """Revisar mensajes recientes donde mencionan a Sebastián"""
    try:
        # Buscar mensajes de los últimos 7 días
        date_limit = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
        
        message_ids = models.execute_kw(db, uid, api_key, 'mail.message', 'search', [
            [
                ('create_date', '>', date_limit),
                '|',
                ('partner_ids', 'in', [sebastian_partner_id]),
                ('body', 'ilike', 'sebastián')
            ]
        ], {'limit': 10})
        
        if not message_ids:
            return []
            
        messages = models.execute_kw(db, uid, api_key, 'mail.message', 'read', [message_ids],
                                   {'fields': ['subject', 'body', 'date', 'author_id', 'model', 'res_id']})
        
        results = []
        for msg in messages[-5:]:  # Solo los 5 más recientes
            author = msg['author_id'][1] if msg['author_id'] else 'Sistema'
            subject = msg['subject'] or 'Sin asunto'
            model = msg['model'] or ''
            
            results.append(f"💬 {author}: {subject} ({model})")
        
        return results
    except Exception as e:
        return [f"❌ Error revisando mensajes: {e}"]

def check_pending_activities(models, uid):
    """Revisar actividades pendientes asignadas a Sebastián"""
    try:
        activity_ids = models.execute_kw(db, uid, api_key, 'mail.activity', 'search', [
            [('user_id', '=', sebastian_user_id), ('date_deadline', '<=', datetime.now().strftime('%Y-%m-%d'))]
        ])
        
        if not activity_ids:
            return []
            
        activities = models.execute_kw(db, uid, api_key, 'mail.activity', 'read', [activity_ids],
                                     {'fields': ['summary', 'date_deadline', 'activity_type_id', 'res_model', 'res_name']})
        
        results = []
        for activity in activities:
            summary = activity['summary'] or 'Sin descripción'
            deadline = activity['date_deadline']
            resource = activity['res_name'] or activity['res_model']
            
            results.append(f"⚡ {summary} - Vence: {deadline} ({resource})")
        
        return results
    except Exception as e:
        return [f"❌ Error revisando actividades: {e}"]

def main():
    try:
        models, uid = connect_odoo()
        
        # Revisar cada categoría
        payments = check_pending_payments(models, uid)
        mentions = check_recent_mentions(models, uid)
        activities = check_pending_activities(models, uid)
        
        # Compilar resultados
        all_results = []
        
        if payments:
            all_results.extend(payments)
        
        if activities:
            all_results.extend(activities)
            
        if mentions:
            all_results.extend(mentions)
        
        if all_results:
            print("📋 Pendientes Odoo - Sebastián:")
            for item in all_results[:10]:  # Máximo 10 items
                print(item)
        else:
            # Si no hay nada pendiente, no imprimir nada
            pass
            
    except Exception as e:
        print(f"❌ Error conectando a Odoo: {e}")

if __name__ == "__main__":
    main()