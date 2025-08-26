#!/usr/bin/env node
const axios = require("axios");

// --- Config ---
const NUM_COUNT = 50;
const HTTP_TIMEOUT = 5000;
const NEGATIVE_REGEX = /Chat on WhatsApp/i; // text indicating invalid/unregistered number

// --- Utils ---
function sample(arr, n) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a.slice(0, n);
}

function insertAt(arr, index, items) {
  return arr.slice(0, index).concat(items, arr.slice(index));
}

function generateNumber() {
  const code = (300 + Math.floor(Math.random() * 50)).toString();
  const digits = [...Array(10).keys()];
  const uniqFive = sample(digits, 5);

  const [r1, r2] = sample(uniqFive, 2);
  const base = uniqFive.filter(d => d !== r1 && d !== r2);

  let subscriber = base.slice();
  let pos1 = Math.floor(Math.random() * 6);
  let pos2 = Math.floor(Math.random() * 6);
  while (pos2 === pos1) pos2 = Math.floor(Math.random() * 6);

  subscriber = insertAt(subscriber, Math.min(pos1, subscriber.length), [r1, r1]);
  if (pos2 > pos1) pos2 += 1;
  subscriber = insertAt(subscriber, Math.min(pos2, subscriber.length), [r2, r2]);

  const subStr = subscriber.join('');
  const local = `0${code}${subStr}`;
  const waInt = `92${code}${subStr}`;
  const waLink = `https://api.whatsapp.com/send/?phone=${waInt}&text&type=phone_number&app_absent=0`;

  return { local, waInt, waLink };
}

// --- Test wa.me / api.whatsapp.com link ---
async function testNumber(waLink) {
  try {
    const res = await axios.get(waLink, {
      maxRedirects: 0,
      validateStatus: null,
      timeout: HTTP_TIMEOUT
    });

    const html = res.data || "";
    if (NEGATIVE_REGEX.test(html)) return false; // "Chat on WhatsApp" = invalid
    return true; // likely registered
  } catch (err) {
    return false;
  }
}

// --- Main ---
(async () => {
  const numbers = [];
  for (let i = 0; i < NUM_COUNT; i++) numbers.push(generateNumber());

  console.log(`\nTesting ${numbers.length} numbers...\n`);

  for (let i = 0; i < numbers.length; i++) {
    const n = numbers[i];
    const valid = await testNumber(n.waLink);
    console.log(
      `${String(i + 1).padStart(2, '0')}. Local: ${n.local} | waLink: ${n.waLink} -> ${valid ? "✅ Registered" : "❌ Not Registered"}`
    );
  }
})();
