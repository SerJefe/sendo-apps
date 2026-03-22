#!/usr/bin/env node

const fetch = require('node-fetch');
const fs = require('fs');

const WHOOP_TOKEN = 'SZzZ8ACnQ99x_xNe2j1lnBLKkXpjPc5FpiBUsfHUiAI.tOER53JLRwSHJWoZ7A2MGk908fEEaL8AOuVEcuBYylE';
const API_BASE = 'https://api.prod.whoop.com/developer/v1';

async function fetchWhoopData() {
    const headers = {
        'Authorization': `Bearer ${WHOOP_TOKEN}`,
        'Accept': 'application/json'
    };

    try {
        console.log('🔄 Testing Whoop API endpoints...');

        // Try different endpoints
        const endpoints = [
            '/user/profile/basic',
            '/cycle',
            '/recovery',
            '/sleep',
            '/workout'
        ];

        for (const endpoint of endpoints) {
            try {
                const response = await fetch(`${API_BASE}${endpoint}?limit=1`, { headers });
                console.log(`📍 ${endpoint}: ${response.status}`);
                
                if (response.ok) {
                    const data = await response.json();
                    console.log(`✅ ${endpoint} SUCCESS:`, JSON.stringify(data, null, 2));
                    
                    // Save successful data
                    fs.writeFileSync(`/tmp/whoop-${endpoint.replace('/', '')}.json`, JSON.stringify(data, null, 2));
                } else {
                    const error = await response.text();
                    console.log(`❌ ${endpoint} ERROR:`, error);
                }
            } catch (err) {
                console.log(`🚫 ${endpoint} FAILED:`, err.message);
            }
        }
    } catch (error) {
        console.error('💥 Whoop API Error:', error);
    }
}

fetchWhoopData();