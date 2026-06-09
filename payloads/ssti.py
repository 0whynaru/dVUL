SSTI_DETECT_PAYLOADS = [
    # Jinja2 / Twig
    ("{{7*7}}", "49", "Jinja2/Twig"),
    ("{{7*'7'}}", "7777777", "Jinja2"),
    ("{{'7'*7}}", "7777777", "Jinja2"),

    # Twig spesifik
    ("{{7*'7'}}", "49", "Twig"),

    # Freemarker
    ("${7*7}", "49", "Freemarker"),
    ("<#assign x=7*7>${x}", "49", "Freemarker"),

    # Smarty
    ("{7*7}", "49", "Smarty"),
    ("{math equation='7*7'}", "49", "Smarty"),

    # Mako
    ("${7*7}", "49", "Mako"),
    ("<%=7*7%>", "49", "Mako/ERB"),

    # ERB (Ruby)
    ("<%= 7*7 %>", "49", "ERB (Ruby)"),
    ("<%= 7*7 %>", "49", "ERB"),

    # Pebble
    ("{{7*7}}", "49", "Pebble"),

    # Velocity
    ("#set($x=7*7)${x}", "49", "Velocity"),
    ("$x = 7 * 7; $x", "49", "Velocity"),

    # Tornado
    ("{{7*7}}", "49", "Tornado"),

    # Nunjucks
    ("{{7*7}}", "49", "Nunjucks"),

    # Handlebars (biasanya ga evaluate math, tapi bisa error-based)
    ("{{#with '7'}}{{this}}{{/with}}", "7", "Handlebars"),

    # Thymeleaf (Java)
    ("[[${7*7}]]", "49", "Thymeleaf"),
    ("[(${7*7})]", "49", "Thymeleaf"),

    # OGNL (Java/Struts)
    ("%{7*7}", "49", "OGNL/Struts2"),
    ("${7*7}", "49", "OGNL"),

    # Groovy
    ("${7*7}", "49", "Groovy"),

    # Polyglot - bisa kena banyak engine
    ("{{7*7}}${7*7}<%=7*7%>[=7*7]#{7*7}", "49", "Polyglot"),
]

# Group by engine untuk targeted scan
SSTI_BY_ENGINE = {
    "jinja2":     [p for p in SSTI_DETECT_PAYLOADS if "Jinja2" in p[2]],
    "twig":       [p for p in SSTI_DETECT_PAYLOADS if "Twig" in p[2]],
    "freemarker": [p for p in SSTI_DETECT_PAYLOADS if "Freemarker" in p[2]],
    "smarty":     [p for p in SSTI_DETECT_PAYLOADS if "Smarty" in p[2]],
    "mako":       [p for p in SSTI_DETECT_PAYLOADS if "Mako" in p[2]],
    "erb":        [p for p in SSTI_DETECT_PAYLOADS if "ERB" in p[2]],
    "velocity":   [p for p in SSTI_DETECT_PAYLOADS if "Velocity" in p[2]],
    "thymeleaf":  [p for p in SSTI_DETECT_PAYLOADS if "Thymeleaf" in p[2]],
    "tornado":    [p for p in SSTI_DETECT_PAYLOADS if "Tornado" in p[2]],
    "nunjucks":   [p for p in SSTI_DETECT_PAYLOADS if "Nunjucks" in p[2]],
    "polyglot":   [p for p in SSTI_DETECT_PAYLOADS if "Polyglot" in p[2]],
    "all":        SSTI_DETECT_PAYLOADS,
}