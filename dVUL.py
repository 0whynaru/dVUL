import time
import sys
import argparse
import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, quote, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
from playwright.sync_api import sync_playwright
import payloads.xss as xss_payloads
import things.tolStp as ssti
import things.colorians as col
from fake_useragent import UserAgent

# ANSI colors
BOLDSA      = "\033[1m"
YELLOWSA    = "\033[33m"
B_YELLOWSA  = BOLDSA + YELLOWSA
B_YELLOWSAA = "\033[41m"
RESETSA     = "\033[0m"
CYANSA      = "\033[36m"
GREYSA      = "\033[90m"
WHITESA     = "\033[37m"
B_CYANSA    = BOLDSA + CYANSA
BLUESA      = "\033[34m"
RED         = "\033[31m"
BLS         = "\033[0m"
BL          = RED + BOLDSA
GREEN       = "\033[32m"
B_GREEN     = BOLDSA + GREEN
Ws          = BOLDSA + WHITESA
eds         = "{F4LL3vN}"
vers        = "0.0.4#bug"
versti      = f"{WHITESA}{'{' + B_YELLOWSA}{vers}{WHITESA + '}' + B_YELLOWSA}"

ua = UserAgent(fallback="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
session = requests.Session()

def get_randomHeader():
    return {
        "User-Agent": ua.random,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
    }

LEGACY_ALIASES = {
    "-sx": "scanx",
    "--scanx": "scanx",
    "-st": "scanti",
    "--scanti": "scanti",
    "-sq": "scansql",
    "--scansql": "scansql",
}

def normalize_legacy_flags(argv):
    if len(argv) > 1 and argv[1] in LEGACY_ALIASES:
        argv[1] = LEGACY_ALIASES[argv[1]]
    return argv

def ayo(symbol, message):
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    sym = col.get_symbol(symbol)
    print(f"{sym} {message} @ {time_str} /{date_str}/")

def ayok(symbol, message):
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    sym = col.get_symbol(symbol)
    print(f"[{BLUESA}{time_str}{RESETSA}] [{sym}] {message}")

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
            page.goto(url, timeout=7000, wait_until="networkidle")
            page.wait_for_timeout(1500)
            browser.close()
    except Exception:
        pass
    return alert_triggered

def get_baseline(parsed, param, params, timeout=8):
    baseline_params = params.copy()
    baseline_params[param] = "dvulishere"
    new_query = urlencode(baseline_params, doseq=True, quote_via=quote)
    baseline_url = urlunparse(parsed._replace(query=new_query))
    try:
        response = session.get(baseline_url, headers=get_randomHeader(), timeout=timeout)
        return response.text, response.status_code
    except requests.RequestException:
        return "", None

def is_meaningfully_reflected(response_text, baseline_text, payload):
    candidates = {payload, unquote(payload)}
    neutralised_markers = ["&lt;", "&gt;", "&quot;", "&#x3c;", "&#x3e;", "&#60;", "&#62;"]
    dangerous_markers = ["<", "javascript:", "onerror", "onload", "onclick", "onmouseover", "svg", "script"]

    for candidate in candidates:
        if not candidate or candidate not in response_text:
            continue
        if candidate in baseline_text:
            continue
        is_dangerous = "<" in candidate or any(m in candidate.lower() for m in dangerous_markers)
        if not is_dangerous:
            continue
        start = response_text.find(candidate)
        window = response_text[max(0, start - 25):start + len(candidate) + 25]
        if "<" not in candidate and any(marker in window for marker in neutralised_markers):
            continue
        return True
    return False

def test_payload(parsed, param, params, payload, baseline_text, timeout=8):
    test_params = params.copy()
    test_params[param] = payload
    new_query = urlencode(test_params, doseq=True, quote_via=quote)
    test_url = urlunparse(parsed._replace(query=new_query))
    try:
        response = session.get(test_url, headers=get_randomHeader(), timeout=timeout)
    except requests.RequestException as e:
        return (None, param, str(e))
    if not is_meaningfully_reflected(response.text, baseline_text, payload):
        return (False, param, payload)
    executed = test_payload_with_browser(test_url)
    if executed:
        return ("executed", param, payload)
    return ("reflected", param, payload)

def scanXSS(url, scan_type="all", threads=10, timeout=8, no_ref=False, progress_bar=False):
    print()
    ayok("INFO", f"Starting scanning: {url}")
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

    ayok(f"{B_GREEN}INFO", f"Type: {scan_type} ~ {len(payloads)}/{threads}")
    print()

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if not params:
        ayok("!", "No parameter found in URL")
        print()
        return

    ayok("INFO", f"{Ws}Parameter found: {', '.join(params.keys())}{RESETSA}")
    print()

    vulnerable_executed = []
    vulnerable_reflected = []
    errors = []

    for param in params:
        ayok("INFO", f"Testing parameter: {param}")
        print()

        baseline_text, baseline_status = get_baseline(parsed, param, params, timeout)
        if baseline_status is None:
            ayok("!", f"Could not fetch baseline for '{param}', accuracy may be reduced")
            print()
        if progress_bar:
            total = len(payloads)
            completed = 0
            lock = Lock()
            dot_index = 0

            def update_progress():
                nonlocal completed, dot_index
                with lock:
                    completed += 1
                    dot_index = (dot_index % 3) + 1
                    dots = "." * dot_index
                    percent = int(completed / total * 100)
                    filled = int(percent / 2)
                    bar = f"{WHITESA}{'█' * filled}{GREYSA}{'░' * (50 - filled)}{RESETSA}"
                    print(f"\rPayload progress{dots:<4} [{bar}] {WHITESA}{percent}%{RESETSA}  ", end="", flush=True)
                    if completed == total:
                        print()

        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = {
                executor.submit(test_payload, parsed, param, params, payload, baseline_text, timeout): payload
                for payload in payloads
            }

            for future in as_completed(futures):
                result, p, payload_or_err = future.result()

                if progress_bar:
                    update_progress()

                if result == "executed":
                    if not progress_bar:
                        ayok("*", f"{BL}[EXE]{RESETSA} {Ws}Alert triggered! {payload_or_err}{RESETSA}")
                    vulnerable_executed.append((p, payload_or_err))
                elif result == "reflected":
                    if not no_ref:
                        if not progress_bar:
                            ayok("!", f"{B_YELLOWSA}[REF]{RESETSA} Reflected, not executed {payload_or_err}{RESETSA}")
                        vulnerable_reflected.append((p, payload_or_err))
                elif result is None:
                    errors.append((p, payload_or_err))

        if progress_bar:
            print()
        print()

    print()
    print("ARIGATOU GOZAIMASU! >_<")
    print("------( github@0whynaru )------")
    print()

    if vulnerable_executed:
        seen = set()
        ayo("VULN", f"{len(vulnerable_executed)} parameter EXECUTED (XSS confirmed):")
        print()
        for p, payload in vulnerable_executed:
            key = (p, payload)
            if key in seen:
                continue
            seen.add(key)
            print(f"  {BL}[EXEC]{RESETSA} {payload}")
        print()

    if vulnerable_reflected:
        ayo("WARN", f"{len(vulnerable_reflected)} parameter REFLECTED (not executed):")
        print()
        for p, payload in vulnerable_reflected:
            print(f"  {B_YELLOWSA}[REF]{RESETSA} {payload}")
        print()

    if errors:
        ayo("!", f"{len(errors)} requests failed (timeouts/connection errors) - results may be incomplete")
        print()

    if not vulnerable_executed and not vulnerable_reflected:
        ayo("+", "There is no XSS found! nice try diddy:)")
        print()

def whatNew():
    print(f"""
dVUL version is {vers}.
+ Fixed legacy -sx/-st/-sq flags being misread as invalid by argparse
+ Added -nr/--no-ref to hide REFLECTED (non-executed) results
+ Baseline-diff reflection check (fewer false positives)
+ Fixed thread-pool bug that could drop/duplicate results
+ Fixed SSTI Scan
+ Added optional progress bar (-p/--progress) during scanning

This tools is only mini-project for beginner programmer like me
""")

def title():
    print(rf"""{B_YELLOWSA}
         
        {BL} |{B_YELLOWSA}
        {BL} |{B_YELLOWSA}
      {BL}___H___{B_YELLOWSA}
   ___  {BL}|{B_YELLOWSAA}{B_YELLOWSA}|{BLS}{BL}|{B_YELLOWSA}  ___   _ _    
  __| \ {BL}|{B_YELLOWSAA}{B_YELLOWSA}|{BLS}{BL}|{B_YELLOWSA}/ / | | | |   {versti}
 / _` | V V /| |_| | |     {eds}
 \__,_| \_/   \____/ |__ 
        {BL}\{B_YELLOWSAA}{B_YELLOWSA}|{BLS}{BL}/{B_YELLOWSA}        |____|    
         {BL}V
{RESETSA}""")

def disclaimer():
    print()
    print("[!] legal disclaimer: Usage of dVUL for attacking targets without prior mutual consent is illegal. "
          "It is the end user's responsibility to obey all applicable local, state and federal laws. "
          "Developers assume no liability and are not responsible for any misuse or damage caused by this program")
    print()

def build_parser():
    parser = argparse.ArgumentParser(
        prog="dvul",
        description="dVUL - small web vulnerability scanner",
        add_help=False,
    )
    parser.add_argument("-h", "--help", action="store_true")
    parser.add_argument("-sh", "--shelp", action="store_true")
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-t", "--title", action="store_true")
    parser.add_argument("-w", "--whatsnew", action="store_true")

    sub = parser.add_subparsers(dest="command")

    sx = sub.add_parser("scanx", add_help=False)
    sx.add_argument("target")
    sx.add_argument("--type", default="all")
    sx.add_argument("--threads", type=int, default=10)
    sx.add_argument("--timeout", type=int, default=8)
    sx.add_argument("-nr", "--no-ref", dest="no_ref", action="store_true")
    sx.add_argument("-p", "--progress", action="store_true",
                    help="Show progress bar instead of real-time findings")

    st = sub.add_parser("scanti", add_help=False)
    st.add_argument("target")
    st.add_argument("--engine", default="all")
    st.add_argument("--threads", type=int, default=10)

    sub.add_parser("scansql", add_help=False)

    return parser

def help_text():
    print("""
Usage: dvul [options] [command]

 Options:
  -h, --help            Show help message
  -sh, --shelp          Show scan help message
  -v, --version         Show version
  -w, --whatsnew        Show changelog

 Commands:
  scanx <url>            Scan XSS on target URL
    --type    <type>     Payload type (default: all)
                          reflected, stored, dom, bypass,
                          filtered, dombased, polyglot,
                          blind, all
    --threads <number>   Number of threads (default: 10)
    --timeout <seconds>  Per-request timeout (default: 8)
    -nr, --no-ref        Hide REFLECTED (non-executed) results
    -p, --progress       Use progress bar (findings shown at end)

  scanti <url>            Scan SSTI on target URL
    --engine  <engine>   Template engine (default: all)
                          jinja2, twig, freemarker, smarty,
                          mako, erb, velocity, thymeleaf,
                          tornado, nunjucks, polyglot, all
    --threads <number>   Number of threads (default: 10)

  scansql                 Scan SQL Injection on targets (coming soon)

 (legacy flags -sx/-st/-sq still work as aliases for scanx/scanti/scansql)
""")

def shelp_text():
    print("""
    SSTI Scanner - Server-Side Template Injection
     Usage:
        dvul scanti "http://target.com/page?id=1"
        dvul scanti "http://target.com/page?id=1" --engine jinja2

    XSS Scanner  - Cross-Site Scripting
     Usage:
        dvul scanx "http://target.com/page?id=1"
        dvul scanx "http://target.com/page?id=1" --type reflected
        dvul scanx "http://target.com/page?id=1" --threads 20
        dvul scanx "http://target.com/page?id=1" -nr
        dvul scanx "http://target.com/page?id=1" -p   # progress bar mode
""")

def main():
    sys.argv = normalize_legacy_flags(sys.argv)
    parser = build_parser()

    if len(sys.argv) == 1:
        title()
        help_text()
        sys.exit()

    args, unknown = parser.parse_known_args()

    if args.help:
        title()
        time.sleep(0.3)
        help_text()
        return

    if args.shelp:
        shelp_text()
        return

    if args.version:
        print("version:", vers)
        print()
        return

    if args.title:
        title()
        return

    if args.whatsnew:
        whatNew()
        return

    if args.command == "scanx":
        title()
        time.sleep(0.3)
        disclaimer()
        scanXSS(args.target, args.type, args.threads, args.timeout, args.no_ref, args.progress)
        return

    if args.command == "scanti":
        title()
        time.sleep(0.3)
        disclaimer()
        ssti.scanSSTI(args.target, args.engine, args.threads)
        return

    if args.command == "scansql":
        ayo("!", "SQLi scan is not implemented yet")
        return

    title()
    help_text()
    sys.exit(1)

if __name__ == "__main__":
    main()