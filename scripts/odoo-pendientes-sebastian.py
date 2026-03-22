#!/usr/bin/env python3
"""
Script para revisar pendientes de Sebastián en Odoo Condugas
"""

import xmlrpc.client
import sys
from datetime import datetime, timedelta

# Configuración Odoo
URL = "https://condugas-sa.odoo.com"
DB = "siendoconsulting-condugas-main-27941080"
USERNAME = "s.sanchez@condugas.com.co"
API_KEY = "ca4174ee968614204dfc083de14add7039e74e6e"
USER_ID = 19
PARTNER_ID = 865

def connect_odoo():
    """Conectar a Odoo y autenticar"""
    try:
        common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common')
        uid = common.authenticate(DB, USERNAME, API_KEY, {})
        if not uid:
            print("❌ Error de autenticación")
            return None, None
        
        models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object')
        return models, uid
        
    except Exception as e:
        print(f"❌ Error conectando a Odoo: {e}")
        return None, None

def revisar_pagos_draft(models, uid):
    """Revisar pagos en estado draft asignados a Sebastián"""
    try:
        payments = models.execute_kw(DB, uid, API_KEY, 'account.payment', 'search_read',
            [[('state', '=', 'draft'), ('partner_id', '=', PARTNER_ID)]],
            {'fields': ['name', 'amount', 'date', 'payment_type', 'partner_id']})
        return payments
    except Exception as e:
        print(f"Error revisando pagos: {e}")
        return []

def revisar_mensajes_recientes(models, uid):
    """Revisar mensajes recientes donde mencionan a Sebastián"""
    try:
        # Mensajes de los últimos 7 días
        fecha_limite = datetime.now() - timedelta(days=7)
        fecha_str = fecha_limite.strftime('%Y-%m-%d %H:%M:%S')
        
        messages = models.execute_kw(DB, uid, API_KEY, 'mail.message', 'search_read',
            [[('create_date', '>=', fecha_str), 
              ('partner_ids', 'in', [PARTNER_ID])]], 
            {'fields': ['subject', 'body', 'date', 'author_id', 'model', 'res_id'], 
             'limit': 10, 'order': 'date desc'})
        return messages
    except Exception as e:
        print(f"Error revisando mensajes: {e}")
        return []

def revisar_actividades_pendientes(models, uid):
    """Revisar actividades pendientes asignadas a Sebastián"""
    try:
        activities = models.execute_kw(DB, uid, API_KEY, 'mail.activity', 'search_read',
            [[('user_id', '=', USER_ID), ('date_deadline', '<=', datetime.now().date().strftime('%Y-%m-%d'))]],
            {'fields': ['summary', 'activity_type_id', 'date_deadline', 'res_model', 'res_id', 'res_name']})
        return activities
    except Exception as e:
        print(f"Error revisando actividades: {e}")
        return []

def main():
    models, uid = connect_odoo()
    if not models:
        return
    
    pendientes = []
    
    # 1. Pagos en draft
    pagos = revisar_pagos_draft(models, uid)
    if pagos:
        pendientes.append("📄 **PAGOS PENDIENTES:**")
        for pago in pagos:
            pendientes.append(f"• {pago['name']} - ${pago['amount']:,.0f} ({pago['date']})")
    
    # 2. Mensajes recientes
    mensajes = revisar_mensajes_recientes(models, uid)
    if mensajes:
        # Solo incluir si hay mensajes realmente relevantes (no automáticos)
        mensajes_relevantes = [m for m in mensajes if m.get('subject') and 'automatico' not in m.get('subject', '').lower()]
        if mensajes_relevantes:
            pendientes.append("\n💬 **MENSAJES RECIENTES:**")
            for msg in mensajes_relevantes[:3]:  # Máximo 3
                subject = msg.get('subject', 'Sin asunto')[:50]
                author = msg.get('author_id', [None, 'Desconocido'])[1] if msg.get('author_id') else 'Desconocido'
                pendientes.append(f"• {subject} - {author}")
    
    # 3. Actividades vencidas
    actividades = revisar_actividades_pendientes(models, uid)
    if actividades:
        pendientes.append("\n⚠️ **ACTIVIDADES VENCIDAS:**")
        for act in actividades:
            summary = act.get('summary', 'Sin descripción')
            deadline = act.get('date_deadline')
            pendientes.append(f"• {summary} (vence: {deadline})")
    
    # Resultado final
    if pendientes:
        resultado = "\n".join(pendientes)
        print(resultado)
    else:
        print("✅ No hay pendientes en Odoo")

if __name__ == "__main__":
    main()