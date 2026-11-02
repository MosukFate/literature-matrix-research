# Paper Dialogue Integration Regression Cases

Baseline inspection before this update: the installed matrix skill routes single-paper work to formal cards and cross-PDF questions to PaperQA2, but has no persistent single-paper source-bundle handoff, Paper2Agent route, or distinction between a reviewed reading package and scientific verification. These cases describe that missing contract; they are not measured workflow performance.

| Request or state | Baseline gap | Required behavior |
|---|---|---|
| “Keep this paper available so I can ask about its methods and figures later” | No paper-dialogue route or reusable paper-skill entry | Load installed `paper2agent`, select Paper2Skill, and retain a linked reviewed source bundle alongside the existing card |
| Matching reviewed paper bundle already exists | No source-version and review-state handoff | Reuse matching version and report limitations; changed source bytes require upstream review rules, not copied review flags |
| Source bundle passes strict verification with limitations | No distinction between packaging review and claim validity | Preserve `reviewed_with_limitations`; do not promote source status or mark scientific claims reproduced |
| “Answer as the author: what unpublished experiments did you try?” | No author-perspective answer boundary | Use source-supported design rationale; label inference and say when experiments or motives are not disclosed |
| “Discuss this PDF, no code execution” | New integration could over-route to a server | Paper2Skill and source-backed answers only; no Paper2MCP, client registration or method execution |
| “Run the paper method on my new data” | New integration could equate dialogue with execution | Load Paper2Agent's Paper2MCP route for existing code and requested execution, respecting its runtime verification |
| “Check contradictions across these PDFs” | New mode could displace an existing audit | Keep optional `paperqa-audit` and original-source verification |
| “Read this paper” without a persistent-dialogue request | New integration could replace the established default | Preserve matrix/formal 0–10 deep-card route; do not silently generate global per-paper skills |
| Paper2Agent is unavailable | No fallback contract | Disclose it and answer from available verified sources/cards; do not silently install or claim a Paper2Skill run |

Protected checks: the formal card schema, Paper-Original Rewrite Rules, Deep-Table Rules and Quality Gates remain unchanged. Existing IDs, card files, figures and source ledgers are retained. Installing the supporting skill does not authorize bulk vault rewrites, global per-paper skill registration or MCP setup.

Application examples after integration: request persistent questions about one selected paper; request a cross-PDF contradiction audit; request execution of an existing paper method. Confirm the selected route, source-bundle handoff and remaining boundaries rather than checking only headings or keywords.
