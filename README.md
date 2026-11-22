# Em Dash Bridge

基于 **CJK Punct Bridge ?! `v1.3.5`** 提取的极简连续破折号桥接 / 回退字体。

## 功能说明

Em Dash Bridge 仅公开破折号排版所需的 4 个 Unicode 字符：

- `U+2014` `—`：一字破折号
- `U+2015` `―`：水平线
- `U+2E3A` `⸺`：二字破折号
- `U+2E3B` `⸻`：三字破折号

其 OpenType 排版逻辑保持通用且语言无关：

- `——` → 映射至与 `⸺` 相同的连续二字破折号字形
- `———` → 映射至与 `⸻` 相同的连续三字破折号字形
- `――` → 保留原来的二连字 HORIZONTAL BAR 连续字形
- `―――` → 保留原来的三连字 HORIZONTAL BAR 连续字形

上述替换全部通过 OpenType `DFLT` 脚本下的 `ccmp` 特性实现，不包含 `locl` 表，也不区分中文、日文、韩文或西文语言：所有语言环境均适用同一套规则。

直接映射的 `U+2E3A` 与 `U+2E3B` 复用作为 `U+2014` 二连字与三连字输出的目标字形，因此不会增加额外轮廓。

## 有意移除的内容

- 除 `U+2014`、`U+2015`、`U+2E3A`、`U+2E3B` 之外的所有标点符号
- 这 4 个码位以外的其他破折号与连字符
- `locl` 表及所有语言 / 地区专属排版分支
- 其他无关的 `GSUB` / `GPOS` 行为

每款构建出的字体仅包含 7 个字形（含 `.notdef`）：4 个直接映射字符的字形，加上保留的 2 个 `U+2015` 连字输出字形，其中 `U+2E3A` / `U+2E3B` 同时兼作 `U+2014` 的连字输出目标。

## 构建说明

构建会生成正体与斜体可变字体，以及每种姿态各 9 个静态字重，均同时提供 `TTF` 与 `WOFF2` 格式。

从解压后的 `CJKPunctBridgeInterrobang-v1.3.5.zip` 目录重新构建：

```bash
pip install -r requirements.txt
python scripts/build.py /path/to/extracted/source dist
```

本次构建使用的源压缩包为 `CJKPunctBridgeInterrobang-v1.3.5.zip`，其 SHA-256 为：

`5554f37832a6cff1ecf4c0815216be73c40176a6c781b9b3df87b0083129afce`

## 许可证

Em Dash Bridge 属于修改衍生字体，依据 **SIL Open Font License 1.1** 分发，详见 [OFL.txt](OFL.txt) 与 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
