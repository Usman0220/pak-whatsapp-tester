#!/usr/bin/env python3
import random
import re
import asyncio
import aiohttp
import os
import time
from concurrent.futures import ThreadPoolExecutor

# --- Enhanced Config for Maximum Speed ---
TARGET_REGISTERED = 20
HTTP_TIMEOUT = 3  # Reduced timeout for faster failures
NEGATIVE_REGEX = re.compile(r"Chat on WhatsApp", re.IGNORECASE)
PROFILE_PIC_REGEX = re.compile(r'https://pps\.whatsapp\.net/v/t[^\s"\']+', re.IGNORECASE)
# Regex to match all <h3> tags
H3_REGEX = re.compile(r'<h3[^>]*>([^<]+)</h3>', re.IGNORECASE | re.DOTALL)

# Directory for saving profile images
IMAGES_DIR = "profile_images"

# 🚀 SPEED OPTIMIZATIONS
MAX_CONCURRENT_REQUESTS = 50  # Increased from 10 to 50
BATCH_SIZE = 50               # Increased from 10 to 50
CONNECTION_POOL_SIZE = 100    # Large connection pool
KEEPALIVE_TIMEOUT = 30       # Keep connections alive longer

# Headers optimized for speed
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
    "Referer": "https://web.whatsapp.com/"
}

# --- Optimized Utils ---
def sample(arr, n):
    """Faster sampling using random.sample"""
    return random.sample(arr, min(n, len(arr)))

def insert_at(lst, index, items):
    return lst[:index] + items + lst[index:]

# Pre-compiled number generation for speed
AREA_CODES = [str(300 + i) for i in range(50)]  # Pre-generate area codes
DIGITS = list(range(10))

def generate_number():
    """Optimized number generation"""
    code = random.choice(AREA_CODES)  # Faster than randint + str
    uniq_five = sample(DIGITS, 5)
    r1, r2 = sample(uniq_five, 2)
    base = [d for d in uniq_five if d != r1 and d != r2]
    subscriber = base[:]
    
    # Optimized position selection
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

# Optimized filename sanitization
UNSAFE_CHARS = re.compile(r'[^A-Za-z0-9_.-]')
def safe_filename_part(s):
    return UNSAFE_CHARS.sub('_', s.strip())[:200] if s else "no_name"

# --- Enhanced Async Functions ---
async def test_number(session, n, semaphore):
    """Enhanced test function with semaphore for better concurrency control"""
    async with semaphore:
        try:
            async with session.get(
                n["waLink"], 
                timeout=aiohttp.ClientTimeout(total=HTTP_TIMEOUT),
                allow_redirects=False
            ) as res:
                # Quick status check first
                if res.status != 200:
                    return None, None, None
                
                html = await res.text()
                
                # Quick negative check
                if NEGATIVE_REGEX.search(html):
                    return None, None, None

                # Extract profile picture URL if available
                profile_pic_match = PROFILE_PIC_REGEX.search(html)
                profile_pic_url = profile_pic_match.group(0) if profile_pic_match else None

                # Extract all <h3> tags
                h3_matches = H3_REGEX.findall(html)
                h3_text = h3_matches[1].strip() if len(h3_matches) >= 2 else (h3_matches[0].strip() if h3_matches else None)

                return n, profile_pic_url, h3_text
        except asyncio.TimeoutError:
            return None, None, None
        except Exception:
            # Silent failure for speed - no printing during tests
            return None, None, None

async def download_profile_picture(session, url, filename):
    """Optimized download function"""
    try:
        clean_url = url.replace("&amp;", "&")
        async with session.get(
            clean_url, 
            timeout=aiohttp.ClientTimeout(total=HTTP_TIMEOUT),
            headers=HEADERS
        ) as pic_res:
            if pic_res.status == 200:
                # Use thread executor for file I/O to avoid blocking
                content = await pic_res.read()
                loop = asyncio.get_event_loop()
                with ThreadPoolExecutor() as executor:
                    await loop.run_in_executor(executor, _write_file, filename, content)
                return True
            return False
    except Exception:
        return False

def _write_file(filename, content):
    """Helper function for threaded file writing"""
    with open(filename, 'wb') as f:
        f.write(content)

async def process_batch_results(results, registered, session):
    """Process batch results concurrently"""
    download_tasks = []
    
    for n, profile_pic_url, h3_text in results:
        if n is not None and len(registered) < TARGET_REGISTERED:
            registered.append(n)
            
            # Print results immediately
            print(f"{len(registered):02}. Local: {n['local']} | waLink: {n['waLink']}")
            
            if h3_text:
                highlight = f"\033[1;33m{h3_text}\033[0m"
                print(f"  Display name (h3): {highlight}")
            
            # Queue download task instead of waiting for it
            if profile_pic_url:
                name_part = safe_filename_part(h3_text)
                filename = os.path.join(IMAGES_DIR, f"{n['waInt']}_{name_part}.jpg")
                download_task = download_profile_picture(session, profile_pic_url, filename)
                download_tasks.append((download_task, filename))
    
    # Process all downloads concurrently
    if download_tasks:
        download_results = await asyncio.gather(
            *[task for task, _ in download_tasks], 
            return_exceptions=True
        )
        
        for (_, filename), result in zip(download_tasks, download_results):
            if result is True:
                print(f"  ✅ Profile picture saved as {filename}")
            elif result is not True and not isinstance(result, Exception):
                print(f"  ❌ Profile picture download failed for {filename}")

async def main():
    """Optimized main function with performance monitoring"""
    start_time = time.time()
    
    # Create images directory if it doesn't exist
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
        print(f"📁 Created directory: {IMAGES_DIR}")
    
    print(f"🚀 Starting SPEED-OPTIMIZED tester (Target: {TARGET_REGISTERED} numbers)")
    print(f"⚡ Config: {MAX_CONCURRENT_REQUESTS} concurrent, {BATCH_SIZE} batch size, {HTTP_TIMEOUT}s timeout")
    print("-" * 80)
    
    registered = []
    
    # Optimized connector with larger connection pool
    connector = aiohttp.TCPConnector(
        limit=CONNECTION_POOL_SIZE,
        limit_per_host=MAX_CONCURRENT_REQUESTS,
        keepalive_timeout=KEEPALIVE_TIMEOUT,
        enable_cleanup_closed=True
    )
    
    # Semaphore for controlling concurrent requests
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    
    timeout = aiohttp.ClientTimeout(total=HTTP_TIMEOUT, connect=2)
    
    async with aiohttp.ClientSession(
        connector=connector, 
        headers=HEADERS,
        timeout=timeout
    ) as session:
        batch_count = 0
        
        while len(registered) < TARGET_REGISTERED:
            batch_count += 1
            batch_start = time.time()
            
            # Generate larger batches for efficiency
            batch = [generate_number() for _ in range(BATCH_SIZE)]
            
            # Create all test tasks
            tasks = [test_number(session, n, semaphore) for n in batch]
            
            # Execute all tests concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out exceptions and None results
            valid_results = [r for r in results if r is not None and not isinstance(r, Exception)]
            
            # Process results concurrently
            await process_batch_results(valid_results, registered, session)
            
            batch_time = time.time() - batch_start
            found_in_batch = len([r for r in valid_results if r[0] is not None])
            
            print(f"📊 Batch {batch_count}: {found_in_batch}/{BATCH_SIZE} found in {batch_time:.2f}s | Total: {len(registered)}/{TARGET_REGISTERED}")
            
            # Minimal delay to avoid overwhelming servers
            if len(registered) < TARGET_REGISTERED:
                await asyncio.sleep(0.05)  # Reduced from 0.1 to 0.05
    
    total_time = time.time() - start_time
    print("-" * 80)
    print(f"✅ COMPLETED! Found {len(registered)} registered numbers in {total_time:.2f} seconds")
    print(f"⚡ Average speed: {len(registered)/total_time:.2f} numbers/second")
    print(f"🎯 Success rate: {len(registered)}/{batch_count * BATCH_SIZE} = {(len(registered)/(batch_count * BATCH_SIZE))*100:.1f}%")

if __name__ == "__main__":
    # Set optimal event loop policy for Windows
    if os.name == 'nt':  # Windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())
