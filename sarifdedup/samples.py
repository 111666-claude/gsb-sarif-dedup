"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def res(rule, uri, line, level, message):
    return {"ruleId": rule, "uri": uri, "line": line, "level": level, "message": message}


def run(name):
    if name == "fingerprint":
        raws = [res("R1", "a.c", 10, "warning", "x"), res("R1", "a.c", 20, "warning", "y")]
        _line({"results": len(core.dedup(raws, set(), set(), core.Counter()).results)})
        return 0
    if name == "severity":
        raws = [res("R1", "a.c", 10, "note", "x"), res("R1", "a.c", 10, "error", "y")]
        report = core.dedup(raws, set(), set(), core.Counter())
        _line({"level": report.results[0].level if report.results else ""})
        return 0
    if name == "overlay":
        raws = [res("R1", "a.c", 10, "error", "x")]
        fp = "R1|a.c"
        report = core.dedup(raws, {fp}, {"R1"}, core.Counter())
        _line({"suppressed": len(report.suppressed)})
        return 0
    if name == "noloc":
        raws = [{"ruleId": "R1", "level": "warning", "message": "x",
                 "partialFingerprints": {"primary": "P1"}}]
        _line({"results": len(core.dedup(raws, set(), set(), core.Counter()).results)})
        return 0
    if name == "work":
        raws = [res("R%04d" % i, "a.c", i, "warning", "m") for i in range(800)]
        report = core.dedup(raws, set(), set(), core.Counter())
        counter = core.Counter()
        for i in range(800):
            core.lookup(report, "R%04d|a.c" % i, counter)
        _line({"results": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
