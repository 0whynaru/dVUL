# colorians.py — terminal color helper
# inspired by sqlmap's output style

RESET   = "\033[0m"
BOLD    = "\033[1m"

# Foreground colors
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
GREY    = "\033[90m"

# Bold variants (sqlmap style)
B_RED     = BOLD + RED
B_GREEN   = BOLD + GREEN
B_YELLOW  = BOLD + YELLOW
B_BLUE    = BOLD + BLUE
B_MAGENTA = BOLD + MAGENTA
B_CYAN    = BOLD + CYAN
B_WHITE   = BOLD + WHITE


def colorize(text, color):
    return f"{color}{text}{RESET}"


# ─── Symbol styles (sqlmap-like) ─────────────────────────────────────────────
#
#  sqlmap uses:
#   [INFO]    → bold white
#   [WARNING] → bold yellow
#   [ERROR]   → bold red
#   [CRITICAL]→ bold red
#   [SUCCESS] → bold green
#   [*]       → bold blue  (generic info)
#   [+]       → bold green (found/good)
#   [-]       → grey       (not found)
#   [!]       → bold yellow (warning)

SYMBOLS = {
    "*":    colorize("[*]", B_BLUE),
    "+":    colorize("[+]", B_GREEN),
    "-":    colorize("[-]", GREY),
    "!":    colorize("[!]", B_YELLOW),
    "VULN": colorize("[VULN]", B_RED),
    "WARN": colorize("[WARN]", B_YELLOW),
    "INFO": colorize("[INFO]", B_WHITE),
    "EXE":  colorize("[EXE]", B_RED),
    "REF":  colorize("[REF]", B_MAGENTA),
    "SSTI": colorize("[SSTI]", B_RED),
    "ERR":  colorize("[ERR]", RED),
}


def get_symbol(symbol):
    return SYMBOLS.get(symbol, colorize(f"[{symbol}]", WHITE))