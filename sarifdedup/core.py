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
        self.suppressed = False


class Report:
    def __init__(self):
        self.results = []
        self.suppressed = []
        self._index = {}


def fingerprint_of(raw, counter):
    counter.scanned += 1
    partial = raw.get("partialFingerprints") or {}
    if partial.get("primary"):
        return partial["primary"]
    return "%s|%s|%s" % (raw.get("ruleId", ""), raw.get("uri", ""), raw.get("line", 0))


def dedup(raws, baseline, always_report, counter):
    report = Report()
    for raw in raws:
        counter.scanned += 1
        fp = fingerprint_of(raw, counter)
        found = report._index.get(fp)
        if found is None:
            found = Result(fp, raw.get("ruleId", ""), raw.get("level", "note"),
                           raw.get("message", ""), raw.get("uri", ""), raw.get("line", 0))
            if fp in baseline and found.rule_id not in always_report:
                found.suppressed = True
                report.suppressed.append(found)
            else:
                report.results.append(found)
            report._index[fp] = found
        else:
            if RANK.get(raw.get("level", "note"), 0) > RANK.get(found.level, 0):
                found.level = raw.get("level", "note")
            found.message = raw.get("message", "")
            found.line = raw.get("line", 0)
    return report


def lookup(report, fp, counter):
    counter.scanned += 1
    item = report._index.get(fp)
    if item is None or item.suppressed:
        return None
    return item
