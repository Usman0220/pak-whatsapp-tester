#!/usr/bin/env python3
import random
import re
import requests

# --- Config ---
NUM_COUNT = 15
HTTP_TIMEOUT = 5
NEGATIVE_REGEX = re.compile(r"Chat on WhatsApp", re.IGNORECASE)

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

# --- Test wa.me / api.whatsapp.com link ---
def test_number(wa_link):
    try:
        res = requests.get(wa_link, allow_redirects=False, timeout=HTTP_TIMEOUT)
        html = res.text or ""
        if NEGATIVE_REGEX.search(html):
            return False  # Invalid / Not registered
        return True  # Likely registered
    except:
        return False

# --- Main ---
if __name__ == "__main__":
    numbers = [generate_number() for _ in range(NUM_COUNT)]

    print(f"\nTesting {len(numbers)} numbers...\n")

    for i, n in enumerate(numbers, start=1):
        valid = test_number(n["waLink"])
        print(f"{i:02}. Local: {n['local']} | waLink: {n['waLink']} -> {'✅ Registered' if valid else '❌ Not Registered'}")
