#!/usr/bin/env python3
import sys
import time
import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, quote, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright
import payloads.xss as xss_payloads
import things.tolStp as ssti
import things.colorians as col

vers = "0.0.3#alpha"
session = requests.Session()


def ayo(symbol, message):
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    sym = col.get_symbol(symbol)
    print(f"{sym} {message} @ {time_str} /{date_str}/")

def test_payload_with_browser(url):
    alert_triggered = False
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            def handle_dialog(dialog):
                nonlocal alert_triggered
                alert_triggered = True
                dialog.dismiss()

            page.on("dialog", handle_dialog)
            page.goto(url, timeout=7000)
            page.wait_for_timeout(1500)
            browser.close()
    except Exception:
        pass
    return alert_triggered


def test_payload(parsed, param, params, payload):
    test_params = params.copy()
    test_params[param] = payload
    new_query = urlencode(test_params, doseq=True, quote_via=quote)
    test_url = urlunparse(parsed._replace(query=new_query))

    try:
        response = session.get(test_url, timeout=5)
        if payload in response.text or unquote(payload) in response.text:
            executed = test_payload_with_browser(test_url)
            if executed:
                return ("executed", param, payload)
            else:
                return ("reflected", param, payload)
        else:
            return (False, param, payload)
    except requests.RequestException as e:
        return (None, param, str(e))


def scanXSS(url, scan_type="all", threads=10):
    print()
    ayo("*", f"Starting scanning: {url}")
    print()

    if scan_type == "all":
        payloads = xss_payloads.XSS_PAYLOADS
    else:
        payloads = xss_payloads.XSS_BY_TYPE.get(scan_type)
        if not payloads:
            print()
            ayo("!", f"Type '{scan_type}' invalid. Try: {', '.join(xss_payloads.XSS_BY_TYPE.keys())}")
            print()
            return

    ayo("*", f"Type: {scan_type} | Payloads: {len(payloads)} | Threads: {threads}")
    print()

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if not params:
        ayo("!", "No parameter found in URL")
        print()
        return

    ayo("+", f"Parameter found: {', '.join(params.keys())}")
    print()

    vulnerable_executed = []
    vulnerable_reflected = []

    for param in params:
        ayo("*", f"Testing parameter: {param}")
        print()

        print(f'[+] Scanning ({len(payloads)} payloads)')
        print()
        found = False
        futures = {}

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for payload in payloads:
                future = executor.submit(test_payload, parsed, param, params, payload)
                futures[future] = payload 

            for future in as_completed(futures):
                result, p, payload_or_err = future.result()
                found = False
                futures = {}


                if result == "executed":
                    ayo("*", f"[EXE] Alert triggered! Payload: {payload_or_err}")
                    print()
                    vulnerable_executed.append((p, payload_or_err))
                    found = True

                elif result == "reflected":
                    ayo("!", f"[REF] Payload reflected but not executed: {payload_or_err}")
                    print()
                    vulnerable_reflected.append((p, payload_or_err))

                # elif result is None:
                #     ayo("!", f"Error on [{p}]: {payload_or_err}")

    print()
    print("------ github@0whynaru ------")
    print()

    if vulnerable_executed:
        ayo("VULN", f"{len(vulnerable_executed)} parameter EXECUTED (XSS confirmed):")
        print()
        for p, payload in vulnerable_executed:
            print(f"  [EXECUTED] {p} => {payload}")
        print()

    if vulnerable_reflected:
        ayo("WARN", f"{len(vulnerable_reflected)} parameter REFLECTED (not executed):")
        print()
        for p, payload in vulnerable_reflected:
            print(f"  [REFLECTED] {p} => {payload}")
        print()

    if not vulnerable_executed and not vulnerable_reflected:
        ayo("+", "There is no XSS found! nice try diddy:)")
        print()

def whatNew():
    print("""
a
""")
def title():
    print(r"""
     ___   ___   _ _    
  __| \ \ / / | | | |  {0.0.3#beta}
 / _` |\ V /| |_| | | 
 \__,_| \_/  \___/| |__
            > ... |____|
    """)


def ver():
    print("version:", vers)
    print()


def help():
    print("""
Usage: dvul [options] [target]

 Options:
  -h, --help            Show help message
  -sh, --shelp          Show scan help message
  -v, --version         Show version

  Scan:
    -sx, --scanx  <url>         Scan XSS on target URL
    --type      <type>          Payload type (default: all)
                                reflected, stored, dom, bypass,
                                filtered, dombased, polyglot,
                                blind, all
    --threads   <number>        Number of threads (default: 10)
    -st, --scanti <url>         Scan SSTI on target URL
    --engine    <engine>        Template engine (default: all)
                                jinja2, twig, freemarker, smarty,
                                mako, erb, velocity, thymeleaf,
                                tornado, nunjucks, polyglot, all
    -sq, --scansql              Scan SQL Injection on targets (coming soon)
""")


def shelp():
    print("""
    SSTI Scanner - Server-Side Template Injection
     Usage:
        dvul -st "http://target.com/page?id=1"
        dvul -st "http://target.com/page?id=1" --engine jinja2

    XSS Scanner  - Cross-Site Scripting
     Usage:
        dvul -sx "http://target.com/page?id=1"
        dvul -sx "http://target.com/page?id=1" --type reflected
        dvul -sx "http://target.com/page?id=1" --threads 20
""")


def disclaimer():
    print()
    print("[!] legal disclaimer: Usage of dVUL for attacking targets without prior mutual consent is illegal. "
          "It is the end user's responsibility to obey all applicable local, state and federal laws. "
          "Developers assume no liability and are not responsible for any misuse or damage caused by this program")
    print()


arguments = sys.argv[1:]

if len(arguments) == 0:
    title()
    help()
    sys.exit()

argument = arguments[0]

if argument in ('-h', '--help'):
    title()
    time.sleep(0.3)
    help()

elif argument in ('-sh', '--shelp'):
    shelp()

elif argument in ('-t', '--title'):
    title()

elif argument in ('-v', '--version'):
    ver()

elif argument in ('-sx', '--scanx'):
    if len(arguments) < 2:
        print()
        print("ERROR: Invalid target URL.")
        print("Make sure your command is correct: dvul -sx 'http://target.com/page?id=1'")
        print()
        sys.exit(1)

    target_url = arguments[1]

    scan_type = "all"
    if "--type" in arguments:
        type_index = arguments.index("--type")
        if type_index + 1 < len(arguments):
            scan_type = arguments[type_index + 1]

    threads = 10
    if "--threads" in arguments:
        thread_index = arguments.index("--threads")
        if thread_index + 1 < len(arguments):
            try:
                threads = int(arguments[thread_index + 1])
            except ValueError:
                ayo("!", "Invalid thread count, using default: 10")

    title()
    time.sleep(0.3)
    disclaimer()
    scanXSS(target_url, scan_type, threads)

elif argument in ('-st', '--scanti'):
    if len(arguments) < 2:
        print()
        print("ERROR: Invalid target URL.")
        print("Make sure your command is correct: dvul -st 'http://target.com/page?id=1'")
        print()
        sys.exit(1)

    target_url = arguments[1]

    engine = "all"
    if "--engine" in arguments:
        engine_index = arguments.index("--engine")
        if engine_index + 1 < len(arguments):
            engine = arguments[engine_index + 1]

    threads = 10
    if "--threads" in arguments:
        thread_index = arguments.index("--threads")
        if thread_index + 1 < len(arguments):
            try:
                threads = int(arguments[thread_index + 1])
            except ValueError:
                ayo("!", "Invalid thread count, using default: 10")

    title()
    time.sleep(0.3)
    disclaimer()
    ssti.scanSSTI(target_url, engine, threads)

else:
    title()
    help()
    sys.exit(1)
