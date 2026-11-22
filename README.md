# Em Dash Bridge

**从 CJK Punct Bridge ?! 提取的极简连续破折号桥接字体。** 当你只需要让连续破折号不断开、而不希望接管其他任何标点时，把本字体放在字体栈最前方即可。

当前版本为 **`v1.0.2`**，可在 [GitHub Releases](https://github.com/Speechlessmanbilibili/Em-Dash-Bridge/releases/latest) 下载。

## 它做什么？

每款字体仅包含 **7 个字形**（含 `.notdef`），公开 `cmap` 仅覆盖 4 个破折号相关码位，其余所有字符全部直接透传给后续字体：

| 码位 / 序列 | 角色与连字行为 |
| --- | --- |
| `U+2014` `—` | 一字破折号；连续 2 个 `——` 连字至 `⸺`，连续 3 个 `———` 连字至 `⸻` |
| `U+2015` `―` | 水平线；保留原有二连字 `――` 与三连字 `―――` 连续字形 |
| `U+2E3A` `⸺` | 二字破折号；直接映射并复用 `——` 的连字目标轮廓 |
| `U+2E3B` `⸻` | 三字破折号；直接映射并复用 `———` 的连字目标轮廓 |

所有连字规则均写在 OpenType `DFLT` 脚本的 `ccmp` 特性中：

- **通用且语言无关**：无 `locl` 表，不区分简中、繁中、日文、韩文或西文语言标记，任何环境下行为完全一致。
- **零多余干扰**：已移除上述 4 个码位之外的所有标点、连字符及其他 `GSUB` / `GPOS` 特性。

## 网页与桌面使用

字体提供 **正体 / 斜体单轴可变字体（`wght` `100～900`）** 以及 **正斜体各 9 个静态字重（Thin 100 ～ Black 900）**，同时包含 `TTF` 与 `WOFF2` 格式。在 CSS 中置于正文字体栈最前端即可生效：

```css
@font-face {
  font-family: "Em Dash Bridge";
  src: url("./EmDashBridge-Variable.woff2") format("woff2-variations");
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
}
@font-face {
  font-family: "Em Dash Bridge";
  src: url("./EmDashBridge-Italic-Variable.woff2") format("woff2-variations");
  font-style: italic;
  font-weight: 100 900;
  font-display: swap;
}

body {
  font-family:
    "Em Dash Bridge",
    "Inter",
    "Noto Sans SC",
    sans-serif;
}
```

## 本地构建

本仓库基于 **`CJKPunctBridgeInterrobang-v1.3.5.zip`** 提取子集并重构 OpenType 特性，源压缩包 SHA-256 为：

`5554f37832a6cff1ecf4c0815216be73c40176a6c781b9b3df87b0083129afce`

将压缩包解压至任意目录后执行：

```bash
pip install -r requirements.txt
python scripts/build.py /path/to/extracted/source dist
```

## 许可证

Em Dash Bridge 属于修改衍生字体，依据 [SIL Open Font License 1.1](OFL.txt) 分发；上游字体版权归属详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
