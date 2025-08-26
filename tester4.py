#!/usr/bin/env python3
import random
import re
import asyncio
import aiohttp
import os

# --- Config ---
TARGET_REGISTERED = 20
HTTP_TIMEOUT = 5
NEGATIVE_REGEX = re.compile(r"Chat on WhatsApp", re.IGNORECASE)
PROFILE_PIC_REGEX = re.compile(r'https://pps\.whatsapp\.net/v/t[^\s"\']+', re.IGNORECASE)
# Regex to match all <h3> tags
H3_REGEX = re.compile(r'<h3[^>]*>([^<]+)</h3>', re.IGNORECASE | re.DOTALL)

MAX_CONCURRENT_REQUESTS = 10
BATCH_SIZE = 10

# Headers to avoid 403 errors
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://web.whatsapp.com/"
}

# --- Utils ---
def sample(arr, n):
    a = arr[:]
    random.shuffle(a)
    return a[:n]

def insert_at(lst, index, items):
    return lst[:index] + items + lst[index:]

def generate_number():
    code = str(300 + random.randint(0, 49))
    digits = list(range(10))
    uniq_five = sample(digits, 5)
    r1, r2 = sample(uniq_five, 2)
    base = [d for d in uniq_five if d != r1 and d != r2]
    subscriber = base[:]
    pos1 = random.randint(0, 5)
    pos2 = random.randint(0, 5)
    while pos2 == pos1:
        pos2 = random.randint(0, 5)
    subscriber = insert_at(subscriber, min(pos1, len(subscriber)), [r1, r1])
    if pos2 > pos1:
        pos2 += 1
    subscriber = insert_at(subscriber, min(pos2, len(subscriber)), [r2, r2])
    sub_str = ''.join(str(d) for d in subscriber)
    local = f"0{code}{sub_str}"
    wa_int = f"92{code}{sub_str}"
    wa_link = f"https://api.whatsapp.com/send/?phone={wa_int}&text&type=phone_number&app_absent=0"
    return {"local": local, "waInt": wa_int, "waLink": wa_link}

# sanitize a string to be filename-safe
def safe_filename_part(s):
    return re.sub(r'[^A-Za-z0-9_.-]', '_', s.strip())[:200]  # limit length for safety

# --- Async test ---
async def test_number(session, n):
    try:
        async with session.get(n["waLink"], timeout=HTTP_TIMEOUT, allow_redirects=False) as res:
            html = await res.text()
            if NEGATIVE_REGEX.search(html):
                return None, None, None

            # Extract profile picture URL if available
            profile_pic_match = PROFILE_PIC_REGEX.search(html)
            profile_pic_url = profile_pic_match.group(0) if profile_pic_match else None

            # Extract all <h3> tags
            h3_matches = H3_REGEX.findall(html)
            # Pick the middle one (second h3 if at least 2 exist)
            h3_text = h3_matches[1].strip() if len(h3_matches) >= 2 else (h3_matches[0].strip() if h3_matches else None)

            return n, profile_pic_url, h3_text
    except Exception as e:
        print(f"Error testing number {n['waInt']}: {str(e)}")
        return None, None, None

async def download_profile_picture(session, url, filename):
    """Download profile picture with proper headers to avoid 403 errors"""
    try:
        # Make sure URL is properly formatted (replace &amp; with &)
        clean_url = url.replace("&amp;", "&")
        async with session.get(clean_url, timeout=HTTP_TIMEOUT, headers=HEADERS) as pic_res:
            if pic_res.status == 200:
                with open(filename, 'wb') as f:
                    f.write(await pic_res.read())
                return True
            else:
                print(f"  Failed to download profile picture (status: {pic_res.status})")
                return False
    except Exception as e:
        print(f"  Error downloading profile picture: {e}")
        return False

async def main():
    registered = []
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession(connector=connector, headers=HEADERS) as session:
        while len(registered) < TARGET_REGISTERED:
            batch = [generate_number() for _ in range(BATCH_SIZE)]
            tasks = [test_number(session, n) for n in batch]
            results = await asyncio.gather(*tasks)

            for n, profile_pic_url, h3_text in results:
                if n is not None and len(registered) < TARGET_REGISTERED:
                    registered.append(n)
                    # Print as clickable link
                    print(f"{len(registered):02}. Local: {n['local']} | waLink: {n['waLink']}")

                    # Print extracted h3 info if available
                    if h3_text:
                        print(f"  Display name (h3): {h3_text}")

                    # Download profile picture if available
                    if profile_pic_url:
                        # sanitize display name to include in filename
                        name_part = safe_filename_part(h3_text) if h3_text else "no_name"
                        filename = f"{n['waInt']}_{name_part}.jpg"

                        print(f"  Attempting to download profile picture as {filename} ...")
                        success = await download_profile_picture(session, profile_pic_url, filename)
                        if success:
                            print(f"  Profile picture saved as {filename}")
                        else:
                            print("  Profile picture download failed.")

            # small safeguard to avoid tight loop in case of anomalies
            await asyncio.sleep(0.1)

    print("\n✅ Found target registered numbers!")

if __name__ == "__main__":
    asyncio.run(main())
