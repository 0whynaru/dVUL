import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from playwright.sync_api import sync_playwright
import payloads.ssti as ssti_payloads
import things.colorians as col

session = requests.Session()


def ayo(symbol, message):
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    sym = col.get_symbol(symbol)
    print(f"{sym} {message} @ {time_str} /{date_str}/")


def confirm_ssti_with_browser(url, expected):
    """
    Konfirmasi via Playwright — cek inner_text() bukan content()
    biar ga false positive dari HTML tags.
    """
    confirmed = False
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=7000)
            page.wait_for_timeout(1500)
    
            text = page.inner_text("body")
            if expected in text:
                confirmed = True
            browser.close()
    except Exception:
        pass
    return confirmed


def test_ssti_payload(parsed, param, params, payload_tuple):
    payload, expected, engine = payload_tuple
    test_params = params.copy()
    test_params[param] = payload
    new_query = urlencode(test_params, doseq=True, quote_via=quote)
    test_url = urlunparse(parsed._replace(query=new_query))

    try:
        response = session.get(test_url, timeout=5)
        if expected in response.text:
            confirmed = confirm_ssti_with_browser(test_url, expected)
            if confirmed:
                return ("vuln", param, payload, engine)
            else:
                return ("reflected", param, payload, engine)
        else:
            return (False, param, payload, engine)
    except requests.RequestException as e:
        return (None, param, str(e), engine)


def scanSSTI(url, engine="all", threads=10):
    print()
    ayo("*", f"Starting SSTI scan: {url}")
    print()

    payloads = ssti_payloads.SSTI_BY_ENGINE.get(engine)
    if not payloads:
        ayo("!", f"Engine '{engine}' invalid. Try: {', '.join(ssti_payloads.SSTI_BY_ENGINE.keys())}")
        print()
        return

    ayo("*", f"Engine: {engine} | Payloads: {len(payloads)} | Threads: {threads}")
    print()

    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if not params:
        ayo("!", "No parameter found in URL")
        print()
        return

    ayo("+", f"Parameter found: {', '.join(params.keys())}")
    print()

    vulnerable = []
    reflected = []

    for param in params:
        ayo("*", f"Testing parameter: {param}")
        print()
        print(f'[+] Scanning ({len(payloads)} payloads)')
        print()

        futures = {}

        with ThreadPoolExecutor(max_workers=threads) as executor:
            for payload_tuple in payloads:
                future = executor.submit(test_ssti_payload, parsed, param, params, payload_tuple)
                futures[future] = payload_tuple

            for future in as_completed(futures):
                result, p, payload_or_err, engine_name = future.result()

                if result == "vuln":
                    ayo("VULN", f"[CONFIRMED] '{p}' VULNERABLE! Engine: {engine_name} | Payload: {payload_or_err}")
                    print()
                    vulnerable.append((p, payload_or_err, engine_name))

                elif result == "reflected":
                    ayo("!", f"[REFLECTED] '{p}' - Found in response but browser not confirmed: {payload_or_err}")
                    print()
                    reflected.append((p, payload_or_err, engine_name))

                elif result is None:
                    ayo("!", f"Error on [{p}]: {payload_or_err}")

    print()
    print("--- github@0whynaru ---")
    print()

    if vulnerable:
        ayo("VULN", f"{len(vulnerable)} parameter CONFIRMED SSTI:")
        print()
        for p, payload, eng in vulnerable:
            print(f"  [VULN] => {payload} ({eng})")
        print()

    if reflected:
        ayo("WARN", f"{len(reflected)} parameter REFLECTED (not confirmed):")
        print()
        for p, payload, eng in reflected:
            print(f"  [REF] => {payload} ({eng})")
        print()

    if not vulnerable and not reflected:
        ayo("+", "No SSTI found!")
        print()