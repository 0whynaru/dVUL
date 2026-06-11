
JINJA2 = [
    ("{{7*'dvul'}}", "dvuldvuldvuldvuldvuldvuldvul", "Jinja2"),
    ("{{'dvul'*7}}", "dvuldvuldvuldvuldvuldvuldvul", "Jinja2"),
    ("{%if 7*7==49%}DVULCONFIRMED{%endif%}", "DVULCONFIRMED", "Jinja2"),
    ("{{7*7}}", "49", "Jinja2"),
    ("{{-7*-7}}", "49", "Jinja2"),
    ("{{range(9)|list}}", "[0, 1, 2, 3, 4, 5, 6, 7, 8]", "Jinja2"),
    ("{{lipsum.__globals__}}", "os", "Jinja2"),
    ("{{''.__class__}}", "<class 'str'>", "Jinja2"),
    ("{{[].__class__}}", "<class 'list'>", "Jinja2"),
    ("{{().__class__.__bases__}}", "object", "Jinja2"),
    ("{{(7).__class__}}", "<class 'int'>", "Jinja2"),
    ("{{7|string}}", "7", "Jinja2"),
    ("{{7|float}}", "7.0", "Jinja2"),
    ("{%set x=7*7%}{{x}}", "49", "Jinja2"),
    ("{{dict(a=1)}}", "{'a': 1}", "Jinja2"),
    ("{{config}}", "Config", "Jinja2"),
    ("{{request}}", "Request", "Jinja2"),
    ("{{self}}", "TemplateReference", "Jinja2"),
    ("{{lipsum}}", "Lorem", "Jinja2"),
    ("{{cycler}}", "cycler", "Jinja2"),
    ("{{joiner}}", "joiner", "Jinja2"),
    ("{{namespace}}", "namespace", "Jinja2"),
    ("{{''.__class__.__mro__}}", "mro", "Jinja2"),
    ("{{config.items()}}", "items", "Jinja2"),
]

TWIG = [
    ("{{'dvul'~'confirm'}}", "dvulconfirm", "Twig"),
    ("{%if 7*7==49%}DVULCONFIRMED{%endif%}", "DVULCONFIRMED", "Twig"),
    ("{% if 7*7==49 %}DVULCONFIRMED{% endif %}", "DVULCONFIRMED", "Twig"),
    ("{{7*7}}", "49", "Twig"),
    ("{{7*'7'}}", "49", "Twig"),
    ("{{7|abs}}", "7", "Twig"),
    ("{{_self}}", "Template", "Twig"),
    ("{{_self.env}}", "env", "Twig"),
    ("{{constant('PHP_VERSION')}}", ".", "Twig"),
    ("{{constant('PHP_OS')}}", "Linux", "Twig"),
    ("{{dump(7*7)}}", "49", "Twig"),
    ("{{'hello'|upper}}", "HELLO", "Twig"),
    ("{{'hello'|length}}", "5", "Twig"),
    ("{{[1,2,3]|length}}", "3", "Twig"),
    ("{{date('Y')}}", "202", "Twig"),
    ("{%- set x = 7*7 -%}{{x}}", "49", "Twig"),
    ("{% for i in 1..3 %}{{i}}{% endfor %}", "123", "Twig"),
]


FREEMARKER = [
    ("<#if 7*7==49>DVULCONFIRMED</#if>", "DVULCONFIRMED", "Freemarker"),
    ("<#assign x='dvulconfirm'>${x}", "dvulconfirm", "Freemarker"),
    ("${\"dvul\"?upper_case}", "DVUL", "Freemarker"),
    ("${7*7}DVUL", "49DVUL", "Freemarker"),
    ("${7*7}", "49", "Freemarker"),
    ("<#assign x=7*7>${x}", "49", "Freemarker"),
    ("<#list 1..3 as x>${x}</#list>", "123", "Freemarker"),
    ("${.version}", ".", "Freemarker"),
    ("<#assign x='freemarker'>${x?upper_case}", "FREEMARKER", "Freemarker"),
    ("${\"hello\"?upper_case}", "HELLO", "Freemarker"),
    ("<#if 7*7==49>1</#if>", "1", "Freemarker"),
    ("${\"freemarker\"?length}", "10", "Freemarker"),
    ("${\"abc\"?replace(\"a\",\"x\")}", "xbc", "Freemarker"),
    ("<#attempt>${7*7}<#recover>err</#attempt>", "49", "Freemarker"),
    ("<#macro m>test</#macro><@m/>", "test", "Freemarker"),
]

SMARTY = [
    ("{if 7*7==49}DVULCONFIRMED{/if}", "DVULCONFIRMED", "Smarty"),
    ("{assign var='x' value='dvulconfirm'}{$x}", "dvulconfirm", "Smarty"),
    ("{\"dvul\"|upper}", "DVUL", "Smarty"),
    ("{7*7}", "49", "Smarty"),
    ("{math equation='7*7'}", "49", "Smarty"),
    ("{'dvul'}", "dvul", "Smarty"),
    ("{$smarty.version}", ".", "Smarty"),
    ("{'hello'|upper}", "HELLO", "Smarty"),
    ("{section name=s loop=3}{$smarty.section.s.index}{/section}", "012", "Smarty"),
    ("{foreach from=[1,2,3] item=i}{$i}{/foreach}", "123", "Smarty"),
    ("{'hello'|capitalize}", "Hello", "Smarty"),
    ("{'hello world'|replace:'world':'earth'}", "hello earth", "Smarty"),
    ("{function name='f'}test{/function}{f}", "test", "Smarty"),
]
MAKO = [
    ("<%def name='x()'>DVULCONFIRMED</%def>${x()}", "DVULCONFIRMED", "Mako"),
    ("${'dvulconfirm'}", "dvulconfirm", "Mako"),
    ("${','.join(['d','v','u','l'])}", "d,v,u,l", "Mako"),
    ("${7*7}DVUL", "49DVUL", "Mako"),
    ("${7*7}", "49", "Mako"),
    ("<% x=7*7 %>${x}", "49", "Mako"),
    ("<% x='hello' %>${x.upper()}", "HELLO", "Mako"),
    ("<% x=[1,2,3] %>${len(x)}", "3", "Mako"),
    ("${str(7*7)}", "49", "Mako"),
    ("${','.join(['a','b','c'])}", "a,b,c", "Mako"),
]

ERB = [
    ("<%= 'dvulconfirm' %>", "dvulconfirm", "ERB"),
    ("<%= 'dvul'.upcase %>", "DVUL", "ERB"),
    ("<%= [1,2,3].join('-') %>", "1-2-3", "ERB"),
    ("<%= 7*7 %>DVUL", "49DVUL", "ERB"),
    ("<%= 7*7 %>", "49", "ERB"),
    ("<%= 'a'*7 %>", "aaaaaaa", "ERB"),
    ("<% x=7*7 %><%= x %>", "49", "ERB"),
    ("<%= [1,2,3].length %>", "3", "ERB"),
    ("<%= 'hello'.upcase %>", "HELLO", "ERB"),
    ("<%= 'hello'.reverse %>", "olleh", "ERB"),
    ("<% (1..3).each do |i| %><%= i %><% end %>", "123", "ERB"),
    ("<%= RUBY_VERSION %>", ".", "ERB"),
]

VELOCITY = [
    ("#if(7*7==49)DVULCONFIRMED#end", "DVULCONFIRMED", "Velocity"),
    ("#set($x='dvulconfirm')${x}", "dvulconfirm", "Velocity"),
    ("#set($x=7*7)#if($x==49)DVULCONFIRMED#end", "DVULCONFIRMED", "Velocity"),
    ("#set($x=7*7)${x}", "49", "Velocity"),
    ("#set($s='hello')${s.toUpperCase()}", "HELLO", "Velocity"),
    ("#foreach($i in [1,2,3])${i}#end", "123", "Velocity"),
    ("#set($a=[1,2,3])${a.size()}", "3", "Velocity"),
    ("#set($s='hello')${s.length()}", "5", "Velocity"),
    ("#set($s='hello world')${s.replace('world','earth')}", "hello earth", "Velocity"),
    ("#set($x=7*7)#set($y=$x+1)${y}", "50", "Velocity"),
    ("#macro(m)test#end#m()", "test", "Velocity"),
]


THYMELEAF = [
    ("[[${'dvulconfirm'}]]", "dvulconfirm", "Thymeleaf"),
    ("[[${#strings.toUpperCase('dvul')}]]", "DVUL", "Thymeleaf"),
    ("[[${T(java.lang.Runtime)}]]", "java.lang.Runtime", "Thymeleaf"),
    ("[[${7*7}]]DVUL", "49DVUL", "Thymeleaf"),
    ("[[${7*7}]]", "49", "Thymeleaf"),
    ("[(${7*7})]", "49", "Thymeleaf"),
    ("[[${#lists.size({1,2,3})}]]", "3", "Thymeleaf"),
    ("[[${#numbers.formatInteger(7*7,1)}]]", "49", "Thymeleaf"),
    ("[[${#bools.isTrue(true)}]]", "true", "Thymeleaf"),
]

TORNADO = [
    ("{%if 7*7==49%}DVULCONFIRMED{%end%}", "DVULCONFIRMED", "Tornado"),
    ("{{'dvul'+'confirm'}}", "dvulconfirm", "Tornado"),
    ("{{len('dvulconfirm')}}", "11", "Tornado"),
    ("{{7*7}}", "49", "Tornado"),
    ("{% if 7*7==49 %}DVULCONFIRMED{% end %}", "DVULCONFIRMED", "Tornado"),
    ("{{handler.settings}}", "settings", "Tornado"),
]

NUNJUCKS = [
    ("{%if 7*7==49%}DVULCONFIRMED{%endif%}", "DVULCONFIRMED", "Nunjucks"),
    ("{{'dvul'+'confirm'}}", "dvulconfirm", "Nunjucks"),
    ("{{'dvul'|upper}}", "DVUL", "Nunjucks"),
    ("{{7*7}}", "49", "Nunjucks"),
    ("{%set x=7*7%}{{x}}", "49", "Nunjucks"),
    ("{{\"hello\"|upper}}", "HELLO", "Nunjucks"),
    ("{{\"hello\"|reverse}}", "olleh", "Nunjucks"),
    ("{{[1,2,3]|length}}", "3", "Nunjucks"),
    ("{{\"hello\"|replace(\"l\",\"r\")}}", "herro", "Nunjucks"),
    ("{%for i in [1,2,3]%}{{i}}{%endfor%}", "123", "Nunjucks"),
]

PEBBLE = [
    ("{% if 7*7 == 49 %}DVULCONFIRMED{% endif %}", "DVULCONFIRMED", "Pebble"),
    ("{{'dvul'|upper}}", "DVUL", "Pebble"),
    ("{{7*7}}", "49", "Pebble"),
    ("{{ 'hello' | upper }}", "HELLO", "Pebble"),
    ("{{ 'hello' | length }}", "5", "Pebble"),
    ("{% set x = 7*7 %}{{ x }}", "49", "Pebble"),
    ("{% for i in [1,2,3] %}{{ i }}{% endfor %}", "123", "Pebble"),
]

HANDLEBARS = [
    ("{{#if true}}DVULCONFIRMED{{/if}}", "DVULCONFIRMED", "Handlebars"),
    ("{{#unless false}}DVULCONFIRMED{{/unless}}", "DVULCONFIRMED", "Handlebars"),
    ("{{#with '7'}}{{this}}{{/with}}", "7", "Handlebars"),
    ("{{#each [1,2,3]}}{{this}}{{/each}}", "123", "Handlebars"),
]

OGNL = [
    ("%{'dvul'+'confirm'}", "dvulconfirm", "OGNL/Struts2"),
    ("%{7*7}DVUL", "49DVUL", "OGNL/Struts2"),
    ("%{7*7}", "49", "OGNL/Struts2"),
    ("${7*7}", "49", "OGNL"),
    ("%{'hello'.toUpperCase()}", "HELLO", "OGNL/Struts2"),
    ("%{[1,2,3].size()}", "3", "OGNL/Struts2"),
    ("%{@java.lang.Runtime@getRuntime()}", "Runtime", "OGNL/Struts2"),
]


GROOVY = [
    ("${\"hello\".toUpperCase()}", "HELLO", "Groovy"),
    ("${[1,2,3].size()}", "3", "Groovy"),
    ("${(1..3).sum()}", "6", "Groovy"),
    ("${'hello'.reverse()}", "olleh", "Groovy"),
    ("${7*7}", "49", "Groovy"),
]

SPEL = [
    ("#{T(java.lang.Runtime).getRuntime()}", "Runtime", "Spring EL"),
    ("#{7*7}", "49", "Spring EL"),
    ("${7*7}", "49", "Spring EL"),
    ("#{T(java.lang.Math).random()}", "0.", "Spring EL"),
    ("#{new java.util.Date()}", "202", "Spring EL"),
]

RAZOR = [
    ("@(7*7)", "49", "Razor"),
    ("{#7*7}", "49", "Razor"),
    ("@{7*7}", "49", "Razor"),
]


JSP = [
    ("<c:out value=\"${7*7}\"/>", "49", "JSP EL"),
    ("${7*7}", "49", "JSP EL"),
    ("${pageContext}", "pageContext", "JSP EL"),
    ("${requestScope}", "requestScope", "JSP EL"),
    ("${sessionScope}", "sessionScope", "JSP EL"),
]

POLYGLOT = [
    ("{{7*'dvul'}}", "dvuldvuldvuldvuldvuldvuldvul", "Polyglot"),
    ("{%if 7*7==49%}DVULCONFIRMED{%endif%}", "DVULCONFIRMED", "Polyglot"),
    ("<#if 7*7==49>DVULCONFIRMED</#if>", "DVULCONFIRMED", "Polyglot"),
    ("{{7*7}}", "49", "Polyglot"),
    ("${7*7}", "49", "Polyglot"),
    ("{7*7}", "49", "Polyglot"),
    ("<%= 7*7 %>", "49", "Polyglot"),
    ("#set($x=7*7)${x}", "49", "Polyglot"),
    ("[[${7*7}]]", "49", "Polyglot"),
    ("%{7*7}", "49", "Polyglot"),
]

SSTI_ALL = (
    JINJA2 + TWIG + FREEMARKER + SMARTY + MAKO +
    ERB + VELOCITY + THYMELEAF + TORNADO + NUNJUCKS +
    PEBBLE + HANDLEBARS + OGNL + GROOVY + SPEL +
    RAZOR + JSP + POLYGLOT
)

SSTI_BY_ENGINE = {
    "jinja2":     JINJA2,
    "twig":       TWIG,
    "freemarker": FREEMARKER,
    "smarty":     SMARTY,
    "mako":       MAKO,
    "erb":        ERB,
    "velocity":   VELOCITY,
    "thymeleaf":  THYMELEAF,
    "tornado":    TORNADO,
    "nunjucks":   NUNJUCKS,
    "pebble":     PEBBLE,
    "handlebars": HANDLEBARS,
    "ognl":       OGNL,
    "groovy":     GROOVY,
    "spel":       SPEL,
    "razor":      RAZOR,
    "jsp":        JSP,
    "polyglot":   POLYGLOT,
    "all":        SSTI_ALL,
}