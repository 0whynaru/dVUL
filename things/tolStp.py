import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, quote
from concurrent.futures import ThreadPoolExecutor, as_completed
import payloads.ssti as ssti_payloads

session = requests.Session()


def ayo(symbol, message):
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    print(f"[{symbol}] {message} @ {time_str} /{date_str}/")


def test_ssti_payload(parsed, param, params, payload_tuple):
    payload, expected, engine = payload_tuple
    test_params = params.copy()
    test_params[param] = payload
    new_query = urlencode(test_params, doseq=True, quote_via=quote)
    test_url = urlunparse(parsed._replace(query=new_query))

    try:
        response = session.get(test_url, timeout=5)
        if expected in response.text:
            return ("vuln", param, payload, engine)
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
                    ayo("VULN", f"[SSTI] Parameter '{p}' VULNERABLE! Engine: {engine_name} | Payload: {payload_or_err}")
                    print()
                    vulnerable.append((p, payload_or_err, engine_name))

                elif result is False:
                    ayo("-", f"[{p}] Not vulnerable: {payload_or_err[:40]}...")

                elif result is None:
                    ayo("!", f"Error on [{p}]: {payload_or_err}")

    print()
    print("--- github@0whynaru ---")
    print()

    if vulnerable:
        ayo("VULN", f"{len(vulnerable)} parameter VULNERABLE to SSTI:")
        print()
        for p, payload, eng in vulnerable:
            print(f"  [SSTI] {p} => {payload} ({eng})")
        print()
    else:
        ayo("+", "No SSTI found!")
        print()
