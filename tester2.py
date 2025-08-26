#!/usr/bin/env python3
import random
import re
import asyncio
import aiohttp

# --- Config ---
TARGET_REGISTERED = 5
HTTP_TIMEOUT = 5
NEGATIVE_REGEX = re.compile(r"Chat on WhatsApp", re.IGNORECASE)
MAX_CONCURRENT_REQUESTS = 10
BATCH_SIZE = 10

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

# --- Async test ---
async def test_number(session, n):
    try:
        async with session.get(n["waLink"], timeout=HTTP_TIMEOUT, allow_redirects=False) as res:
            html = await res.text()
            if NEGATIVE_REGEX.search(html):
                return None
            return n
    except:
        return None

async def main():
    registered = []
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT_REQUESTS)
    async with aiohttp.ClientSession(connector=connector) as session:
        while len(registered) < TARGET_REGISTERED:
            batch = [generate_number() for _ in range(BATCH_SIZE)]
            tasks = [test_number(session, n) for n in batch]
            results = await asyncio.gather(*tasks)
            for n in results:
                if n is not None and len(registered) < TARGET_REGISTERED:
                    registered.append(n)
                    # Print as clickable link
                    print(f"{len(registered):02}. Local: {n['local']} | waLink: {n['waLink']}")
    
    print("\n✅ Found target registered numbers!")

if __name__ == "__main__":
    asyncio.run(main())
