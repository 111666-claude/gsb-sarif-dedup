"""按指纹合并结果并按基线抑制。"""

RANK = {"note": 0, "warning": 1, "error": 2}


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


class Result:
    def __init__(self, fingerprint, rule_id, level, message, uri, line):
        self.fingerprint = fingerprint
        self.rule_id = rule_id
        self.level = level
        self.message = message
        self.uri = uri
        self.line = line


class Report:
    def __init__(self):
        self.results = []
        self.suppressed = []


def fingerprint_of(raw, counter):
    counter.scanned += 1
    return raw.get("ruleId", "") + "|" + raw.get("uri", "")


def dedup(raws, baseline, always_report, counter):
    report = Report()
    for raw in raws:
        counter.scanned += 1
        uri = raw.get("uri", "")
        if not uri:
            continue
        fp = fingerprint_of(raw, counter)
        found = None
        for item in report.results:
            counter.scanned += 1
            if item.fingerprint == fp:
                found = item
        if found is None:
            found = Result(fp, raw.get("ruleId", ""), raw.get("level", "note"),
                           raw.get("message", ""), uri, raw.get("line", 0))
            if fp in baseline:
                report.suppressed.append(found)
            else:
                report.results.append(found)
        else:
            if RANK.get(found.level, 0) >= RANK.get(raw.get("level", "note"), 0):
                found.level = raw.get("level", "note")
            found.message = raw.get("message", "")
        found.line = raw.get("line", 0)
    return report


def lookup(report, fp, counter):
    for item in report.results:
        counter.scanned += 1
        if item.fingerprint == fp:
            return item
    return None
