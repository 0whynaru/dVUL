import sys
import time
import requests
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import payloads.xss as xss_payloads

vers = "0.0.1#stable"


def ayo(symbol, message):
    now = datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    print(f"[{symbol}] {message} @ {time_str} /{date_str}/")


def scanSSTI():
    ayo("*", "Memulai scan SSTI...")
    print()
    print("[!] Fungsi scan belum diimplementasi.")
    print()


def scanXSS(url, scan_type="all"):
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

    ayo("*", f"Type: {scan_type} [!] Payloads: {len(payloads)}")
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
        for payload in payloads:
            test_params = params.copy()
            test_params[param] = payload
            new_query = urlencode(test_params, doseq=True)
            test_url = urlunparse(parsed._replace(query=new_query))

            try:
                response = requests.get(test_url, timeout=5)
                if payload in response.text:
                    ayo("VULN", f"Parameter '{param}' VULNERABLE! Payload: {payload}")
                    print()
                    vulnerable.append((param, payload))
                    break
                else:
                    ayo("-", f"[{param}] Not vulnerable: {payload[:40]}...")
            except requests.RequestException as e:
                ayo("!", f"Error: {e}")

    print()
    print("--- github@0owhynaru ---")
    print()
    if vulnerable:
        ayo("VULN", f"{len(vulnerable)} parameter vulnerable:")
        print()
        for param, payload in vulnerable:
            print(f"  {param} => {payload}")
            print()
    else:
        ayo("+", "There is no XSS found!")
        print()


def title():
    print(r"""
     ___   ___   _ _    
  __| \ \ / / | | | |  {0.0.1#stable}
 / _` |\ V /| |_| | | 
 \__,_| \_/  \___/| |__
            > ... |____|
    """)


def ver():
    print()
    print("version:", vers)
    print()


def help():
    print("""
          
Usage: python main.py [options] [target]

 Options:
  -h, --help            Show help message
  -v, --version         Show version

  Scan:
    -sh, --shelp                give how to use.
    -s, --scan  <url>           Scan XSS on target URL
    --type      <type>          Payload type (default: all)
                                reflected, stored, dom, bypass,
                                filtered, dombased, polyglot, all
""")

def shelp():
     print("""
     Usage:
    python dVUL -s "http://localhost/page?id=1"
    python dVUL -s "http://localhost/page?id=1" --type reflected
    python dVUL -s "http://localhost/page?id=1" --type bypass""")
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

elif argument in ('-t', '--title'):
    title()

elif argument in ('-v', '--version'):
    ver()

elif argument in ('--shelp', '-sh'):
    shelp()

# XSS NYA COKKKK
elif argument in ('-sx', '--scanx'):
    if len(arguments) < 2:
        print()
        print("ERROR: Invalid target URL.")
        print("Make sure your command is correct: python main.py -s 'http://localhost/page?id=1'")
        print()
        sys.exit(1)
# XSS NYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    target_url = arguments[1]

    scan_type = "all"
    if "--type" in arguments:
        type_index = arguments.index("--type")
        if type_index + 1 < len(arguments):
            scan_type = arguments[type_index + 1]

    title()
    time.sleep(0.3)
    disclaimer()
    scanXSS(target_url, scan_type)
# INI SSTIIIIIII
elif argument in ('--scans', '-ss'):
    print('commming')

else:
    title()
    help()
    sys.exit(1)