# A minimal, self-contained subset of logic from tester6.py that is safe to run on-device
# (avoids heavy network dependencies like aiohttp). Used only for the in-app demo.

import random

TARGET_REGISTERED = 20

def sample(arr, n):
    return random.sample(arr, min(n, len(arr)))

def insert_at(lst, index, items):
    return lst[:index] + items + lst[index:]

AREA_CODES = [str(300 + i) for i in range(50)]
DIGITS = list(range(10))

def generate_number():
    code = random.choice(AREA_CODES)
    uniq_five = sample(DIGITS, 5)
    r1, r2 = sample(uniq_five, 2)
    base = [d for d in uniq_five if d != r1 and d != r2]
    subscriber = base[:]

    pos1, pos2 = sample(range(6), 2)
    pos1, pos2 = min(pos1, pos2), max(pos1, pos2)

    subscriber = insert_at(subscriber, min(pos1, len(subscriber)), [r1, r1])
    pos2 += 1 if pos2 > pos1 else 0
    subscriber = insert_at(subscriber, min(pos2, len(subscriber)), [r2, r2])

    sub_str = ''.join(str(d) for d in subscriber)
    local = f"0{code}{sub_str}"
    wa_int = f"92{code}{sub_str}"
    wa_link = f"https://api.whatsapp.com/send/?phone={wa_int}&text&type=phone_number&app_absent=0"
    return {"local": local, "waInt": wa_int, "waLink": wa_link}