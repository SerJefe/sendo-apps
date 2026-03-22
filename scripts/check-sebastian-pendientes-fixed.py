#!/usr/bin/env python3
"""
Revisión de pendientes de Sebastián en Odoo Condugas (versión corregida)
- Pagos en borrador (account.payment)
- Mensajes recientes donde lo mencionan
- Actividades pendientes (mail.activity)
"""

import xmlrpc.client
import json
from datetime import datetime, timedelta

# Cargar credenciales
with open('/root/.openclaw/workspace/.secrets/odoo-config.json', 'r') as f:
    config = json.load(f)

def check_sebastian_pendientes():
    """Revisa pendientes específicos de Sebastián."""
    try:
        # Conectar
        common = xmlrpc.client.ServerProxy(f"{config['url']}/xmlrpc/2/common")
        uid = common.authenticate(config['database'], config['username'], config['api_key'], {})
        models = xmlrpc.client.ServerProxy(f"{config['url']}/xmlrpc/2/object")
        
        pendientes = []
        
        # 1. Pagos en estado draft asignados a Sebastián (partner_id 865)
        print("🔍 Revisando pagos en borrador...")
        try:
            draft_payments = models.execute_kw(
                config['database'], uid, config['api_key'],
                'account.payment', 'search_read',
                [['&', ('state', '=', 'draft'), ('partner_id', '=', 865)]],
                {'fields': ['name', 'amount', 'currency_id', 'date', 'ref'], 'limit': 10}
            )
            
            if draft_payments:
                pendientes.append("💰 **Pagos en borrador:**")
                for payment in draft_payments:
                    amount = f"${payment['amount']:,.0f}"
                    currency = payment['currency_id'][1] if payment['currency_id'] else ""
                    ref = payment['ref'] or payment['name']
                    pendientes.append(f"   • {ref}: {amount} {currency}")
        except Exception as e:
            print(f"⚠️ Error en pagos: {e}")
        
        # 2. Mensajes recientes donde mencionan a Sebastián
        print("📧 Revisando mensajes recientes...")
        try:
            week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
            
            recent_messages = models.execute_kw(
                config['database'], uid, config['api_key'],
                'mail.message', 'search_read',
                [['&', ('date', '>=', week_ago), ('partner_ids', 'in', [865])]],
                {'fields': ['subject', 'body', 'author_id', 'date', 'model', 'res_id'], 'limit': 5, 'order': 'date desc'}
            )
            
            if recent_messages:
                # Filtrar mensajes relevantes (no automáticos)
                relevant_messages = []
                for msg in recent_messages:
                    subject = msg['subject'] or ""
                    if subject and not any(skip in subject.lower() 
                        for skip in ['automatic', 'notification', 'system', 'logged', 'created']):
                        relevant_messages.append(msg)
                
                if relevant_messages:
                    pendientes.append("\n📧 **Mensajes recientes:**")
                    for msg in relevant_messages[:3]:  # Top 3
                        author = msg['author_id'][1] if msg['author_id'] else "Sistema"
                        date_str = datetime.strptime(msg['date'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m')
                        subject = msg['subject'] or "Sin asunto"
                        pendientes.append(f"   • {date_str} - {author}: {subject}")
        except Exception as e:
            print(f"⚠️ Error en mensajes: {e}")
        
        # 3. Actividades pendientes asignadas a Sebastián (user_id 19)
        print("📋 Revisando actividades pendientes...")
        try:
            # Actividades vencidas
            pending_activities = models.execute_kw(
                config['database'], uid, config['api_key'],
                'mail.activity', 'search_read',
                [['&', ('user_id', '=', 19), ('date_deadline', '<=', datetime.now().strftime('%Y-%m-%d'))]],
                {'fields': ['summary', 'date_deadline', 'activity_type_id', 'res_model', 'res_name'], 'limit': 10, 'order': 'date_deadline asc'}
            )
            
            if pending_activities:
                pendientes.append("\n📋 **Actividades vencidas:**")
                for activity in pending_activities:
                    deadline = datetime.strptime(activity['date_deadline'], '%Y-%m-%d').strftime('%d/%m')
                    summary = activity['summary'] or "Sin resumen"
                    model_name = activity['res_name'] or activity['res_model']
                    pendientes.append(f"   • {deadline}: {summary} ({model_name})")
            
            # Actividades próximas (próximos 3 días)
            future_date = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')
            upcoming_activities = models.execute_kw(
                config['database'], uid, config['api_key'],
                'mail.activity', 'search_read',
                [['&', '&', ('user_id', '=', 19), ('date_deadline', '>', datetime.now().strftime('%Y-%m-%d')), ('date_deadline', '<=', future_date)]],
                {'fields': ['summary', 'date_deadline', 'res_name'], 'limit': 5, 'order': 'date_deadline asc'}
            )
            
            if upcoming_activities:
                pendientes.append("\n📅 **Próximas actividades:**")
                for activity in upcoming_activities:
                    deadline = datetime.strptime(activity['date_deadline'], '%Y-%m-%d').strftime('%d/%m')
                    summary = activity['summary'] or "Sin resumen"
                    model_name = activity['res_name'] or ""
                    pendientes.append(f"   • {deadline}: {summary} {model_name}")
        except Exception as e:
            print(f"⚠️ Error en actividades: {e}")
        
        return pendientes
        
    except Exception as e:
        return [f"❌ Error general al revisar Odoo: {e}"]

if __name__ == "__main__":
    pendientes = check_sebastian_pendientes()
    
    if pendientes:
        print("\n" + "="*50)
        print("🎯 PENDIENTES SEBASTIÁN - ODOO CONDUGAS")
        print("="*50)
        for item in pendientes:
            print(item)
        print("")
    else:
        print("✅ No hay pendientes en Odoo para Sebastián")