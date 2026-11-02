# Literature Matrix Research

一个面向 Codex 等支持 Agent Skills 的宿主的文献研究技能：从研究主题、种子论文或已有论文库，构建有来源依据的文献矩阵、Obsidian 阅读系统和逐篇深读卡，并支持围绕单篇论文持续问答。

它负责组织研究流程和约束证据质量。检索脚本产生候选，原文核查决定结论，深读卡解释方法；需要长期追问时，可通过可选的 Paper2Agent 保存可检索的论文资料层。

## 选择任务路线

| 目标 | 路线 | 主要产物 |
|---|---|---|
| 找论文、扩展种子、基础调查（search-only candidate table） | `search-only` | 候选 CSV/JSONL、检索日志、失败查询、来源状态 |
| 精读一篇论文（single-paper deep card） | 默认正式深读卡 | 方法流程、公式映射、原始证据、实验口径、局限与复现路径 |
| 比较一批论文（matrix plus core deep cards） | `matrix` | 快览矩阵、核心/桥接/补充层、基准与失败面比较 |
| 建立完整 Obsidian 阅读系统 | `obsidian-package` | START、Dashboard、分阶段索引、卡片、矩阵和审计资料 |
| 补原图、原表或修正浅层卡片 | `deep-table-enrichment` / `paper-original-rewrite` / `card-polish` | 保留身份与笔记的修订卡、证据台账、修订记录 |
| 以后反复追问某一篇论文 | `paper-dialogue` | 可复用来源包、精确引用的回答、已核对发现与未解问题 |
| 对多个本地 PDF 做问答或矛盾候选核查 | 可选 `paperqa-audit` | 候选证据与回原文验证队列 |
| 用论文方法处理新数据 | 按需交给 Paper2Agent 的 `Paper2MCP` | 绑定原代码、经过测试的工具及其实际运行结果 |

说“精读这篇”“read this paper”或“做深度卡”时，默认进入正式深读路线。只有明确要求找论文、基础调查、`candidate_table` 或 `search-only`，才止步于候选池。

## 安装与更新

需要一个能加载技能、读取文件并执行本地命令的宿主。网络检索另需网络访问；多代理复核能力取决于宿主。

下面使用个人技能目录 `~/.codex/skills` 作为示例。若宿主或 `CODEX_HOME` 使用其他位置，请替换为它实际配置的技能目录。

### 首次安装：Windows PowerShell

```powershell
$skillsRoot = Join-Path $env:USERPROFILE '.codex\skills'
$skillRoot = Join-Path $skillsRoot 'literature-matrix-research'
if (Test-Path -LiteralPath $skillRoot) { throw '目录已存在，请按更新说明处理，不要覆盖。' }
New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null
git clone https://github.com/MosukFate/literature-matrix-research.git "$skillRoot"
```

### 首次安装：macOS / Linux

```bash
skills_root="${CODEX_HOME:-$HOME/.codex}/skills"
skill_root="$skills_root/literature-matrix-research"
test ! -e "$skill_root" || { echo '目录已存在，请先检查现有安装。'; exit 1; }
mkdir -p "$skills_root"
git clone https://github.com/MosukFate/literature-matrix-research.git "$skill_root"
```

也可以完整复制此仓库的技能文件到宿主目录。保留 `SKILL.md`、`agents/`、`references/` 和 `scripts/`；测试文件便于后续验证。安装后在新的对话轮次调用 `$literature-matrix-research`，或按宿主要求重新加载技能。

### 已有安装

若目录是 Git checkout，先检查本地改动，再进行仅允许快进的更新：

```powershell
git -C "$skillRoot" status --short
git -C "$skillRoot" diff
# 工作区干净，或你已妥善保留本地修改后：
git -C "$skillRoot" pull --ff-only
```

若原来通过复制安装、目录没有 Git 历史，请在另一位置取得新版并比较差异，再合并需要的文件。不要直接删除、重置或覆盖自己的规则与改动。

## 依赖按任务准备

| 阶段 | 所需能力 |
|---|---|
| 本仓库候选检索、旧笔记匹配、验证和打包脚本 | Python 标准库；建议 Python 3.11+。本地回归使用 `unittest`，无需 pytest |
| 在线发现论文 | 公共 HTTP 来源可达；失败、限流和超时写入日志 |
| PDF、原图和表格核查 | 宿主可用的 PDF 阅读/渲染工具；按需使用 PyMuPDF、pypdf、pdfplumber、MarkItDown 等，不强制全部安装 |
| 单篇持续问答资料层 | 可选安装 `paper2agent`，使用其内部 Paper2Skill；依赖见下文 |
| 跨 PDF 语义核查 | 可选 `paperqa2-audit` 技能及其运行环境、模型提供方配置 |
| 执行论文算法 | Paper2MCP 与该论文实际需要的代码、数据、模型、R/CLI/API/GPU 等 |

检索、写卡和纯论文问答不要求先配置一组固定 MCP，也不要求安装全部可选科研工具。实际使用哪些支持技能，以及缺少什么，应在该阶段说明。完整衔接见 [Skill Integration](references/skill_integration.md)。

## 可以直接使用的请求

**单篇深读**

```text
用 literature-matrix-research 精读这篇论文。
从 PDF 和补充材料建立正式深读卡，解释输入到输出的流程、公式与代码映射，
保留原图和相关原表，给出实验设置、证据边界、复现缺口和小白细节自检。
```

**先找论文**

```text
Search-only：查找 2024–2026 年与视觉语言模型对象幻觉有关的论文。
输出 candidate_table、检索日志和失败查询；先不写深读卡，区分正式会议与预印本。
```

**矩阵与阅读顺序**

```text
围绕这个研究问题建立文献矩阵，分清核心、桥接、补充与 matrix-only。
先说明每篇为什么相关，再为核心论文写正式深读卡；输出 Obsidian 阅读顺序与来源审计。
```

**复用旧笔记**

```text
为这批论文更新阅读矩阵，先在指定 vault 中查找已有笔记。
复用能够明确匹配的 ID 和文件路径，保留我的批注、问题、图片与手工证据。
```

**持续问答**

```text
用 paper-dialogue 为这篇论文建立或复用来源包，保留现有深读卡。
以后回答都回查正文、补充、图表；以作者视角解释设计时，区分原文陈述、推导和未知。
现在只讨论论文，不运行模型。
```

## 正式深读卡的契约

正式 `type: paper-card` 使用 0–10 结构：

| 节 | 内容 |
|---|---|
| 0 | 总览摘要 |
| 1 | 论文定位与核心痛点 |
| 2 | 核心思想与逻辑链 |
| 3 | 方法/模型/训练/推理拆解 |
| 4 | 数学公式、推导与算法映射 |
| 5 | 创新点与 baseline 本质差异 |
| 6 | 实验、消融、效率与可信度 |
| 7 | 优缺点、局限与过度宣传风险 |
| 8 | 复现路径与落地适用性 |
| 9 | 阅读建议与相关工作 |
| 10 | 最终总结 |

方法部分先给输入到输出的流程，再分层解释 **怎么做、为什么做、产生什么效果**。关键公式须解释变量、目标、假设与实现对应；例子嵌入相关分析。相关原始结果表应保留或经原文校正，紧接 `结果解析 / Result interpretation`。

只有元数据、摘要、旧综述或尚未核对的全文/表格时，应使用 `paper-stub` / `matrix-stub`，不把它计作完成的深读卡。每张正式卡有 `小白细节自检 / Novice detail check`；细节不足时进行一次来源支持的修补，仍不足则保持 stub，而不是堆字数。

完整字段和要求见 [深读卡 Schema](references/ai_paper_deep_read_card_schema.md)。

## 候选检索与旧笔记复用

以下命令从仓库根目录运行。在线示例会访问外部来源：

```powershell
python -X utf8 scripts/discover_candidates.py `
  --query "visual language model object hallucination" `
  --year-from 2024 --year-to 2026 `
  --proceedings-venue ICML --proceedings-venue CVPR `
  --notes-root 'path/to/reading-package-or-vault' `
  --out-dir 'path/to/discovery-output'

python -X utf8 scripts/validate_candidate_table.py 'path/to/discovery-output/candidate_table.jsonl'
```

`--notes-root` 可省略；它只读扫描 Markdown，匹配结果另存为 `existing_note_matches.jsonl`，不会修改 vault。唯一且无冲突的匹配可复用笔记身份；歧义、冲突及不支持的元数据格式需要人工确认。旧笔记存在不等于来源已经核验，stub 也不会因此自动升级。

离线检查候选处理流程：

```powershell
python -X utf8 scripts/discover_candidates.py `
  --fixture tests/fixtures/discovery_minimal.json `
  --out-dir 'path/to/offline-discovery'
python -X utf8 scripts/validate_candidate_table.py 'path/to/offline-discovery/candidate_table.jsonl'
```

每次检索保留 `candidate_table.csv`、`candidate_table.jsonl`、`search_log.json` 和 `failed_queries.md`。会议年份检索使用官方索引；不指定年份时，proceedings 适配器采用当前年及前两年。`--proceedings-venue` 只收窄相应会议适配器，不会过滤所有聚合来源，也不自动保证 main track 身份。

同时查看日志中的 `source_coverage` 和失败记录：有限结果、缺失索引或请求失败，不是“没有相关论文”的证明。候选排名是筛选辅助，不是论文质量或新颖性的证明。详见 [Discovery Pipeline](references/discovery_pipeline.md)。

## 原图、原表与结论定位

- 优先匹配正式 HTML/源资产；不完整时渲染 PDF 原页再裁切。PDF 内嵌对象序号不能当作原图号。
- 保留面板、标签、坐标轴、图例与完整图注访问。图旁给原图号、可点击原页、原尺寸入口，以及它支持什么、不能支持什么。
- 关键数值绑定版本、表/图/页、模型、数据划分、指标和设置；区分最大/平均、百分点/相对百分比、子集/总体、作者报告/计算推导。
- 对实际引用的关键结果检查正文与消融口径、可相加的分项与总分、跨模型重复行。无法解释的差异保留原值与两处来源；不擅改原表，也不推定未披露的实际运行参数。
- 原图资产、表格转录、成功解析和来源包的存在，都不会自行提升 `source_status`。机制和因果主张仍要有相应证据。

见 [原图与提取流程](references/pdf_source_extraction.md) 和 [证据规则](references/evidence_and_source_rules.md)。

## 可选：Paper2Agent 持续问答

Paper2Agent 是单独安装的上游技能，本仓库只维护衔接规则和必要的小补丁，不复制其论文资料或运行环境。

| 组件 | 分工 |
|---|---|
| 本技能的深读卡 | 方法解释、实验口径、证据边界和项目关联 |
| Paper2Skill | 正文、补充、图表和表格组成的可复用原文资料层 |
| Paper2MCP | 用户要求实际运行方法时，将已有研究代码封装为经过测试的工具 |

### 安装上游技能

可以要求宿主的技能安装器安装以下固定来源，并保留整个文件夹：

```text
仓库：jmiao24/Paper2Agent
路径：skills/paper2agent
提交：8c2d059165ef8cdcb70dbea76655b9c2b55b38e6
```

也可以在 Windows 手动安装到尚不存在的技能目录：

```powershell
$skillsRoot = Join-Path $env:USERPROFILE '.codex\skills'
$skillRoot = Join-Path $skillsRoot 'literature-matrix-research'
$paperSkillRoot = Join-Path $skillsRoot 'paper2agent'
if (Test-Path -LiteralPath $paperSkillRoot) { throw 'Paper2Agent 已存在，请先核对版本和本地修改。' }
New-Item -ItemType Directory -Path $skillsRoot -Force | Out-Null
$paperSource = Join-Path $env:TEMP ('paper2agent-source-' + [guid]::NewGuid().ToString('N'))
git clone https://github.com/jmiao24/Paper2Agent.git "$paperSource"
if ($LASTEXITCODE -ne 0) { throw '下载失败，请检查网络后重试。' }
git -C "$paperSource" checkout --detach 8c2d059165ef8cdcb70dbea76655b9c2b55b38e6
if ($LASTEXITCODE -ne 0) { throw '未能检出指定版本，停止安装。' }
Copy-Item -LiteralPath (Join-Path $paperSource 'skills\paper2agent') -Destination $paperSkillRoot -Recurse
```

保留内部子目录与脚本；只复制 `SKILL.md` 或少量转换脚本会缺失依赖文件。

### 此固定版本的 Windows 路径补丁

在该上游提交的 Windows 实测中，正常生成的目录被 POSIX 模板规则误判。仓库提供 [3 行路径兼容补丁](patches/paper2agent-windows-paths.patch)，统一包内 layout/manifest 的相对路径。只针对上述已测试提交，不保证适用于其他版本。

```powershell
$patch = Join-Path $skillRoot 'patches\paper2agent-windows-paths.patch'
git -C "$paperSkillRoot" apply --check "$patch"
if ($LASTEXITCODE -ne 0) { throw '补丁不适用或已应用，请先检查，不要强行覆盖。' }
git -C "$paperSkillRoot" apply "$patch"
```

### 可选独立 PDF 环境

Paper2Skill 要求 Python ≥3.11。其 `uv run` 入口可按脚本元数据准备依赖；也可以使用已安装匹配依赖的独立 Python 直接运行。以下是上述固定提交的 Windows 环境示例，不更改全局 PATH：

```powershell
$paperRuntime = Join-Path $env:USERPROFILE '.codex\runtimes\paper2agent'
if (Test-Path -LiteralPath $paperRuntime) { throw '运行环境已存在，请先核对依赖，不要覆盖。' }
python -m venv "$paperRuntime"
$paperPython = Join-Path $paperRuntime 'Scripts\python.exe'
& $paperPython -m pip install uv 'pymupdf==1.28.2' 'pymupdf4llm==1.28.2' 'pypdf==6.18.1' 'pillow==12.2.0'
& $paperPython -m pip check
& $paperPython -X utf8 (Join-Path $paperSkillRoot 'paper2skill\scripts\paper_bundle.py') --help
& $paperPython -X utf8 (Join-Path $paperSkillRoot 'paper2skill\scripts\test_paper_bundle.py')
```

当前固定版本的补丁与本地环境已通过 27 项上游合成文档测试。这不等于验证任意真实论文的提取结果；升级上游后须重新核对依赖和运行测试。扫描 PDF 的 OCR 还需 Tesseract 数据；无法识别时保留图像和限制，不能宣称已读出文本。

### 问答怎样保持可追溯

`paper-dialogue` 创建或复用匹配版本的 Paper2Skill 资料包，记录包入口、论文版本、严格验证状态、限制与未解问题。问答时读取相关原文完整段落、表头和图注；以作者视角解释时，区分公开陈述、分析推断和未知。

旧审阅决定只按 Paper2Skill 的同源字节规则复用；同名论文或已有深读卡不代表新来源包已逐页审阅。`reviewed_with_limitations` 的限制须保留，也不代表科学结论或复现实验已通过。未完成审阅的包不能冒称正式完成。

仅保存值得复用的已核对发现和开放问题；后续对话重新加载这些资料，不承诺未保存的聊天记忆或后台常驻。不会自动把每篇论文注册成全局技能、启动 MCP 或批量转换整个 vault。详细契约见 [Persistent Paper Dialogue](references/paper_dialogue.md)。

## 输出示意

实际目录随任务范围调整；单篇深读无需强行建立完整文献库。完整阅读包通常类似：

```text
reading-package/
├── 00_START_HERE.md
├── 00_综述与索引/                 # Dashboard、矩阵、阶段入口
├── 01_核心论文/
│   └── <paper-id>.md             # 正式卡或明确标注的 stub
├── 02_桥接论文/
├── 07_补充证据池_<说明>/
└── 99_审计与来源/
    └── <paper-id>/
        ├── claim_ledger.md
        ├── figure_ledger.md
        ├── figures/
        └── <paper-id>-paper/      # 可选 Paper2Skill 阅读包
            ├── SKILL.md
            ├── references/
            └── assets/
```

上游转换快照、逐页审阅与验证报告应保留在阅读包外的审阅目录；交付时记录真实位置和状态。主线、补充、matrix-only 与完成的深读卡数量分别统计。目录与索引约定见 [Matrix and Reading Order](references/matrix_and_reading_order.md)。

## 验证与打包

在仓库根目录运行本仓库全部回归测试：

```powershell
python -X utf8 tests/run_all.py
```

当前套件包含 **63 项测试**，覆盖候选归一化/排序、会议年份检索、只读旧笔记匹配、路由、README、内容风险提示和证据路径检查。它使用标准库；不联网，不运行论文算法，不依赖 pytest。上文 Paper2Skill 的 27 项测试属于外部工具套件，单独运行和报告。

检查实际产物：

```powershell
python -X utf8 scripts/validate_candidate_table.py 'path/to/discovery-output/candidate_table.jsonl'
python -X utf8 scripts/validate_structure.py 'path/to/reading-package' --require-beginner
python -X utf8 scripts/validate_content_risks.py 'path/to/reading-package'
python -X utf8 scripts/validate_evidence_links.py 'path/to/final-export'
```

- 结构检查针对卡片契约，不能证明原文事实正确。
- 内容风险扫描是人工核对队列；保留真实告警、处置和退出码，不靠加模板文字追求零提示。
- 链接检查覆盖标准 Markdown 本地链接/图像与台账路径，报告缺失或越出交付根目录的目标；不联网验证 HTTP，也不判断图号、页码是否语义正确。
- 源包审阅、工具测试、科学复现和因果证据是不同验证范围，必须分别说明。

打包本技能：

```powershell
python -X utf8 scripts/package_skill.py . --output 'path/to/literature-matrix-research.zip'
```

若宿主提供 skill-format validator，可另行检查技能元数据。它不是输出论文包验证的替代品。

## 仓库与参考资料

```text
SKILL.md          模式、路由与核心约束
agents/           宿主展示信息
references/       深读、来源、图表、问答与工作流契约
scripts/          候选检索、旧笔记匹配、验证和打包
tests/            本地回归与最小候选 fixture
patches/          明确版本适用的上游兼容补丁
```

本公开仓库保留可复用的技能、参考、脚本和测试。论文 PDF、全文语料、Obsidian vault、模型权重、本地运行环境、私密配置和个人机器路径不随技能发布。

本技能的外部衔接包括 [Paper2Agent](https://github.com/jmiao24/Paper2Agent)、[Academic Research Skills](https://github.com/Imbad0202/academic-research-skills) 及按需安装的 PaperQA2、论文检索、PDF/MarkItDown、Obsidian 工具。它们各自的安装、许可和验证范围由对应项目维护；本仓库没有将这些项目整套打包。

本仓库采用 [MIT License](LICENSE)。
