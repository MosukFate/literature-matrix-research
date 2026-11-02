# Evidence Navigation and Context Regression Cases

Baseline: the frozen same-paper VCD comparison exposed these concrete gaps before this update. Keep its initial cards unchanged; use an isolated repaired copy for application checks. This is a small regression set, not a workflow benchmark.

| Observed baseline failure | Required behavior after update | Verification |
|---|---|---|
| Correct maximum F1 gain attributed to the abstract, where it does not occur | Bind headline numbers to the actual source object/page and check attribution wording | VCD GQA-Popular Qwen-VL: Table 1, main PDF p.6; +7.39 pp from reported means; introduction/§4.2, not abstract |
| A combined Table 1/2 link opens only Table 1 | Each referenced source object has its own correct page locator | Table 1 p.6, Table 2 p.7; verify original pages, not just URL syntax |
| Main and ablation defaults have different reported scores | Retain separate experiment contexts and flag unresolved differences before combining increments | VCD main LLaVA MME 604.66 vs supplement default 591.67; do not invent an explanation |
| Application initially assigned a chapter-wide default to a specific table despite a conflicting general setting | Distinguish the defaults stated in each section from confirmed table-specific run settings | Supplement §A POPE T999 vs §B default500; Tables7/8 omit actual T, so record it as unconfirmed |
| Referenced 7B/13B VCD rows repeat every mean and SD without warning | Flag source duplication beside the affected scope claim while preserving the reported values and distinct results | Compare main Table 1 and supplement Table 8; do not infer misconduct or invalidate all 13B results |
| Original figure checks exist, but render pointers fail after copying the card | Validate links and provenance paths from the final export root | Original six paths exist; relocated bundle must report missing/outside paths or use portable source-page locators |
| Long source-anchored tables trigger a warning on each middle row | Inherit the adjacent source anchor for that table only | Numeric rows of an anchored long table should not warn; a following unanchored table should warn |
| Negated overclaim warnings and an already explained β example obscure actionable cues | Recognize local explanations/negation while retaining genuine unsupported-claim warnings | Paired positive/negative tests; do not claim semantic or scientific verification |

Protected regression expectations: the formal 0–10 card schema, layered how/why/effect methods, embedded examples, original-result-table plus immediate interpretation, conservative source status, and novice repair gate remain unchanged.

Application check: give a fresh-context evaluator the revised skill and a small source packet, ask for a result paragraph with an original figure and evidence record, and inspect the actual output. Do not supply this table or its expected answer as the task prompt.
