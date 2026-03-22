#!/usr/bin/env node
/**
 * GoodNotes Google Drive reader
 * Lists recently modified files or downloads specific PDFs
 * Usage:
 *   node gdrive-goodnotes.js recent [days]     — list files modified in last N days (default 7)
 *   node gdrive-goodnotes.js download <fileId> <outputPath>
 *   node gdrive-goodnotes.js tree               — full folder tree
 */

const { google } = require('googleapis');
const fs = require('fs');
const path = require('path');

const KEY_PATH = path.join(__dirname, '..', '.secrets', 'gdrive-service-account.json');
const ROOT_FOLDER = '1SLKkJ6eiW2g1QPv5bA7BDHI6_wJBEI7w';

async function getAuth() {
  return new google.auth.GoogleAuth({
    keyFile: KEY_PATH,
    scopes: ['https://www.googleapis.com/auth/drive.readonly']
  });
}

async function listRecent(days = 7) {
  const auth = await getAuth();
  const drive = google.drive({ version: 'v3', auth });
  const since = new Date(Date.now() - days * 86400000).toISOString();

  const res = await drive.files.list({
    q: `modifiedTime > '${since}' and mimeType = 'application/pdf'`,
    fields: 'files(id,name,modifiedTime,parents)',
    orderBy: 'modifiedTime desc',
    pageSize: 50
  });

  console.log(`Files modified in last ${days} days:`);
  for (const f of res.data.files) {
    console.log(`  ${f.modifiedTime} | ${f.name} | ${f.id}`);
  }
  return res.data.files;
}

async function downloadFile(fileId, outputPath) {
  const auth = await getAuth();
  const drive = google.drive({ version: 'v3', auth });
  const dest = fs.createWriteStream(outputPath);
  const res = await drive.files.get({ fileId, alt: 'media' }, { responseType: 'stream' });
  await new Promise((resolve, reject) => {
    res.data.pipe(dest);
    res.data.on('end', resolve);
    res.data.on('error', reject);
  });
  console.log(`Downloaded: ${outputPath}`);
}

async function listTree(folderId = ROOT_FOLDER, indent = '') {
  const auth = await getAuth();
  const drive = google.drive({ version: 'v3', auth });

  const res = await drive.files.list({
    q: `'${folderId}' in parents`,
    fields: 'files(id,name,mimeType,modifiedTime)',
    orderBy: 'name',
    pageSize: 100
  });

  for (const f of res.data.files) {
    const isFolder = f.mimeType === 'application/vnd.google-apps.folder';
    console.log(`${indent}${isFolder ? '📁' : '📄'} ${f.name} | ${f.modifiedTime}${isFolder ? '' : ' | ' + f.id}`);
    if (isFolder) {
      await listTree(f.id, indent + '  ');
    }
  }
}

const [cmd, ...args] = process.argv.slice(2);

(async () => {
  switch (cmd) {
    case 'recent':
      await listRecent(parseInt(args[0]) || 7);
      break;
    case 'download':
      if (args.length < 2) { console.error('Usage: download <fileId> <outputPath>'); process.exit(1); }
      await downloadFile(args[0], args[1]);
      break;
    case 'tree':
      await listTree();
      break;
    default:
      console.log('Usage: node gdrive-goodnotes.js <recent|download|tree> [args]');
  }
})().catch(e => { console.error(e.message); process.exit(1); });
