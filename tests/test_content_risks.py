import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_content_risks.py"
SPEC = importlib.util.spec_from_file_location("content_risks", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def scan(body):
    root = Path.cwd()
    text = "---\ntype: paper-card\nsource_status: full paper verified\n---\n"
    text += body + "\n### 小白细节自检\n输入输出均已说明。\n"
    output = io.StringIO()
    with patch.object(sys, "argv", [str(SCRIPT), str(root)]), \
            patch.object(MODULE, "markdown_files", return_value=[root / "card.md"]), \
            patch.object(MODULE, "read_text", return_value=text), \
            contextlib.redirect_stdout(output):
        MODULE.main()
    return json.loads(output.getvalue())["issues"]


def issues_for(body, kind):
    return [issue for issue in scan(body) if issue["issue"] == kind]


class ContentRiskContextTests(unittest.TestCase):
    def test_long_table_inherits_its_immediate_source(self):
        body = "原 Table 1，PDF p.6，按原文核对。\n\n| Model | Score |\n|---|---:|\n"
        body += "\n".join(f"| Model {i} | {70+i}.0 |" for i in range(12))
        self.assertEqual([], issues_for(body, "numeric_table_line_without_obvious_anchor"))

    def test_unanchored_table_does_not_inherit_previous_table_source(self):
        body = "Table 1, PDF p.6\n\n| Model | Score |\n|---|---:|\n| A | 71 |\n\n"
        body += "另一个尚未找到来源的实验。\n\n| Model | Score |\n|---|---:|\n"
        body += "\n".join(f"| Other {i} | {80+i} |" for i in range(8))
        issues = issues_for(body, "numeric_table_line_without_obvious_anchor")
        self.assertTrue(any("Other 7" in issue["text"] for issue in issues))

    def test_remote_source_paragraph_does_not_anchor_later_table(self):
        body = "Table 1, PDF p.6\n\n" + "\n\n".join(["无关背景。"] * 4)
        body += "\n\n| Model | Score |\n|---|---:|\n| A | 71 |\n"
        self.assertTrue(issues_for(body, "numeric_table_line_without_obvious_anchor"))

    def test_frontmatter_source_status_is_not_a_table_source(self):
        body = "| Model | Score |\n|---|---:|\n| A | 71 |\n"
        self.assertTrue(issues_for(body, "numeric_table_line_without_obvious_anchor"))

    def test_negated_proof_does_not_trigger_strong_claim(self):
        self.assertEqual([], issues_for("这些结果并未直接证明机制正确。", "strong_claim_word"))

    def test_negated_claim_followed_by_positive_overclaim_is_kept(self):
        self.assertTrue(issues_for("结果未证明机制，但该方法完全消除幻觉。", "strong_claim_word"))

    def test_positive_claim_is_still_reviewed(self):
        self.assertTrue(issues_for("该方法证明了机制，并且是唯一最优方案。", "strong_claim_word"))

    def test_negated_universality_is_not_flagged(self):
        self.assertEqual([], issues_for("该结果不能视为普遍 best，也不一定可推广。", "strong_claim_word"))

    def test_vcd_threshold_example_has_nearby_explanation(self):
        body = "只允许原图概率至少为原图最大概率 $\\beta$ 倍的词进入候选集合。\n\n"
        body += "例如原图最可能词概率为 0.6，$\\beta=0.1$，候选最低概率为 0.06。这个数值例子仅为解释规则。"
        self.assertEqual([], issues_for(body, "formula_without_nearby_symbol_explanation"))

    def test_formula_without_explanation_still_fails(self):
        self.assertTrue(issues_for("只有 $q=0.7$。", "formula_without_nearby_symbol_explanation"))

    def test_distant_explanation_does_not_hide_bare_formula(self):
        body = "符号解释：q 是归一化分数。\n" + "背景。\n" * 12 + "$q=0.7$"
        self.assertTrue(issues_for(body, "formula_without_nearby_symbol_explanation"))


if __name__ == "__main__":
    unittest.main()
