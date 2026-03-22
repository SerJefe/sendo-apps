#!/usr/bin/env python3
"""
Revisar pendientes de Sebastián en Odoo Condugas
Partner ID: 865, User ID: 19
"""

import xmlrpc.client
import json
from datetime import datetime, timedelta

# Cargar credenciales
with open('/root/.openclaw/workspace/.secrets/odoo-config.json', 'r') as f:
    config = json.load(f)

def check_pendientes():
    """Revisar todos los pendientes de Sebastián."""
    pendientes = []
    
    try:
        # Conectar
        common = xmlrpc.client.ServerProxy(f"{config['url']}/xmlrpc/2/common")
        uid = common.authenticate(config['database'], config['username'], config['api_key'], {})
        
        if not uid:
            return ["❌ Error de autenticación"]
        
        models = xmlrpc.client.ServerProxy(f"{config['url']}/xmlrpc/2/object")
        
        # 1. Pagos en borrador asignados a Sebastián (partner_id 865)
        draft_payments = models.execute_kw(
            config['database'], uid, config['api_key'],
            'account.payment', 'search_read',
            [['&', ('state', '=', 'draft'), ('partner_id', '=', 865)]],
            {'fields': ['name', 'amount', 'currency_id', 'date', 'partner_id'], 'limit': 10}
        )
        
        if draft_payments:
            pendientes.append(f"💰 **Pagos pendientes ({len(draft_payments)}):**")
            for payment in draft_payments:
                amount = payment['amount']
                currency = payment['currency_id'][1] if payment['currency_id'] else 'COP'
                date = payment['date'] or 'Sin fecha'
                pendientes.append(f"   • {payment['name']}: {amount:,.0f} {currency} - {date}")
        
        # 2. Mensajes recientes donde lo mencionan (últimos 3 días)
        fecha_limite = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S')
        
        recent_messages = models.execute_kw(
            config['database'], uid, config['api_key'],
            'mail.message', 'search_read',
            [['&', 
              ('create_date', '>=', fecha_limite),
              '|', ('partner_ids', 'in', [865]), ('author_id', '=', 865)
            ]],
            {'fields': ['subject', 'body', 'create_date', 'author_id', 'model', 'res_id'], 'limit': 5}
        )
        
        if recent_messages:
            pendientes.append(f"\n📧 **Mensajes recientes ({len(recent_messages)}):**")
            for msg in recent_messages:
                subject = msg['subject'] or 'Sin asunto'
                author = msg['author_id'][1] if msg['author_id'] else 'Sistema'
                model = msg['model'] or 'General'
                date = msg['create_date'][:10] if msg['create_date'] else 'Sin fecha'
                pendientes.append(f"   • {subject} - {author} ({model}) - {date}")
        
        # 3. Actividades pendientes asignadas a user_id 19
        pending_activities = models.execute_kw(
            config['database'], uid, config['api_key'],
            'mail.activity', 'search_read',
            [[('user_id', '=', 19)]],
            {'fields': ['summary', 'date_deadline', 'res_model', 'res_name'], 'limit': 10}
        )
        
        if pending_activities:
            pendientes.append(f"\n📋 **Actividades pendientes ({len(pending_activities)}):**")
            for activity in pending_activities:
                summary = activity['summary'] or 'Sin descripción'
                deadline = activity['date_deadline'] or 'Sin fecha'
                model = activity['res_model'] or ''
                res_name = activity['res_name'] or ''
                
                # Determinar estado por fecha
                if deadline != 'Sin fecha':
                    deadline_date = datetime.strptime(deadline, '%Y-%m-%d').date()
                    today = datetime.now().date()
                    if deadline_date < today:
                        estado_emoji = '🔴'  # Vencido
                    elif deadline_date == today:
                        estado_emoji = '🟡'  # Hoy
                    else:
                        estado_emoji = '🟢'  # Futuro
                else:
                    estado_emoji = '⚪'
                    
                pendientes.append(f"   • {estado_emoji} {summary} - {deadline} ({res_name})")
        
        return pendientes
        
    except Exception as e:
        return [f"❌ Error: {e}"]

if __name__ == "__main__":
    pendientes = check_pendientes()
    
    if not pendientes:
        print("✅ Sin pendientes")
    else:
        for item in pendientes:
            print(item)