#!/usr/bin/env node
/**
 * Odoo CxP Report Generator
 * Pulls pending payables and generates dashboard HTML
 * Usage: node odoo-cxp-report.js [output-path]
 * 
 * Saves weekly snapshots to reportes/cxp_snapshot_YYYY-MM-DD.json for trend comparison
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const ODOO_URL = 'condugas-sa.odoo.com';
const ODOO_DB = 'siendoconsulting-condugas-main-27941080';
const ODOO_KEY = process.env.ODOO_API_KEY || 'ca4174ee968614204dfc083de14add7039e74e6e';
const ODOO_UID = 19;

function rpc(model, method, args, kwargs = {}) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      jsonrpc: '2.0', method: 'call',
      params: { service: 'object', method: 'execute_kw', args: [ODOO_DB, ODOO_UID, ODOO_KEY, model, method, ...args, kwargs] }
    });
    const req = https.request({ hostname: ODOO_URL, path: '/jsonrpc', method: 'POST', headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) } }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => { try { const j = JSON.parse(data); j.error ? reject(j.error) : resolve(j.result); } catch(e) { reject(e); } });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

async function main() {
  console.log('Fetching payables...');
  const payables = await rpc('account.move.line', 'search_read', [[[['account_type','=','liability_payable'],['parent_state','=','posted'],['amount_residual','!=',0]]]], { fields: ['partner_id','date','date_maturity','amount_residual','ref','move_name','move_id','journal_id'], limit: 1000, order: 'date_maturity asc' });
  
  console.log(`Found ${payables.length} pending payables`);
  
  // Get analytics mapping
  const alines = await rpc('account.move.line', 'search_read', [[[['parent_state','=','posted'],['analytic_distribution','!=',false],['journal_id','=',2],['account_type','!=','liability_payable']]]], { fields: ['move_id','analytic_distribution'], limit: 2000 });
  
  const contractMap = { '1':'Boyacá','2':'Bucaramanga','3':'Floridablanca','4':'Jericó','6':'O&M Z2','7':'OZZLO','8':'Pérdidas','9':'Valle','10':'Admin Central','18':'Asociados','17':'Externas','12':'Ger. Técnica','16':'Internas','11':'Nuevos Negocios' };
  const moveContract = {};
  for (const l of alines) {
    const mid = l.move_id[0];
    if (!moveContract[mid] && l.analytic_distribution) {
      moveContract[mid] = Object.keys(l.analytic_distribution).map(k => contractMap[k] || `ID-${k}`).join(', ');
    }
  }
  
  // Save snapshot
  const today = new Date().toISOString().split('T')[0];
  const snapshot = { date: today, total: 0, overdue: 0, count: payables.length, by_contract: {}, by_aging: {} };
  
  for (const r of payables) {
    const amt = Math.abs(r.amount_residual);
    snapshot.total += amt;
    const dm = r.date_maturity || r.date;
    const days = dm ? Math.floor((Date.now() - new Date(dm)) / 86400000) : 0;
    if (days > 0) snapshot.overdue += amt;
    
    const mid = r.move_id ? r.move_id[0] : 0;
    const contract = moveContract[mid] || 'Sin asignar';
    if (!snapshot.by_contract[contract]) snapshot.by_contract[contract] = { total: 0, overdue: 0 };
    snapshot.by_contract[contract].total += amt;
    if (days > 0) snapshot.by_contract[contract].overdue += amt;
  }
  
  const snapshotDir = path.join(__dirname, '..', 'reportes');
  fs.mkdirSync(snapshotDir, { recursive: true });
  fs.writeFileSync(path.join(snapshotDir, `cxp_snapshot_${today}.json`), JSON.stringify(snapshot, null, 2));
  console.log(`Snapshot saved: cxp_snapshot_${today}.json`);
  console.log(`Total CxP: $${(snapshot.total/1e6).toFixed(0)}M | Overdue: $${(snapshot.overdue/1e6).toFixed(0)}M | Health: ${((1-snapshot.overdue/snapshot.total)*100).toFixed(1)}%`);
}

main().catch(e => { console.error(e); process.exit(1); });
