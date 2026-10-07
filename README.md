# sarif-dedup

合并静态分析结果：按指纹去重、按严重度取最高、按基线抑制，并有"始终上报"的覆盖层。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m sarifdedup --sample=fingerprint
python3 -m sarifdedup --sample=severity
python3 -m sarifdedup --sample=overlay
python3 -m sarifdedup --sample=noloc
python3 -m sarifdedup --sample=work
```

## 口径

- **指纹**：结果带 `partialFingerprints.primary` 时用它；否则由 `规则|文件|行号` 拼成。
- **去重**：同一指纹只留一条，等级取最高的那次（error > warning > note > 其它），消息取最后一次出现的。
- **基线**：指纹在基线里的结果进"已抑制"列表，不计入结果；规则在"始终上报"集合里时不受基线影响。
- **无位置**：带指纹但没有文件位置的结果照常保留。
- **查找**：按指纹走索引，不逐条比较。

## 不变量

- 结果列表里每个指纹只有一条，且等级不低于同一指纹出现过的任何一次。
- 已抑制结果不进结果列表。
- `scanned` 不随结果数乘查询次数放大：八百条结果查八百次的 `scanned` 不超过 6000。

## 输出契约

场景打印一行 JSON，键随场景而定。`--sample=work` 打印 `{"results": N, "scanned": N}`。
