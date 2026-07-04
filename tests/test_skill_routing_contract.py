import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
INTEGRATION = (ROOT / "references" / "skill_integration.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")


def test_mode_router_is_explicit_and_progressive():
    assert "## Mode Router" in SKILL
    assert "search-only" in SKILL and "scripts/discover_candidates.py" in SKILL
    assert "candidate_table" in SKILL and "failed_queries.md" in SKILL
    assert "Do not create `paper-card`" in SKILL

def test_default_route_prefers_matrix_and_deep_cards():
    assert "Default route" in SKILL
    assert "matrix + formal deep cards" in SKILL
    assert "Single-paper close reading" in SKILL
    assert "explicitly asks for `search-only`" in SKILL
    assert "basic survey" in SKILL
def test_usage_examples_cover_default_and_search_only():
    assert "## Usage Examples" in SKILL
    assert "single-paper deep card" in SKILL
    assert "matrix plus core deep cards" in SKILL
    assert "search-only candidate table" in SKILL
    assert "基础调查" in SKILL

def test_skill_chaining_names_supporting_skills_without_force_loading():
    assert "paper-lookup" in SKILL
    assert "superpowers:test-driven-development" in SKILL
    assert "Do not force-load other skills" in SKILL
    assert not re.search(r"@[^`\s]+/(SKILL\.md|references|scripts)", SKILL)


def test_no_mojibake_in_routing_labels():
    bad_tokens = ["鏂", "鎬", "缁", "閺", "鐠", "\ue1f0", "\ue219", "\ue74e", "\ue100"]
    for token in bad_tokens:
        assert token not in SKILL, token
    assert "怎么做" in SKILL
    assert "为什么这么做" in SKILL
    assert "这么做的效果是什么" in SKILL
    assert "结果解析 / Result interpretation" in SKILL

def test_readme_usage_examples_match_default_routes():
    assert "single-paper deep card" in README
    assert "matrix plus core deep cards" in README
    assert "search-only candidate table" in README
    assert "candidate_table.csv" in README
    assert "基础调查" in README

def test_integration_search_only_points_to_discovery_first():
    section_start = INTEGRATION.index("### `search-only`")
    section = INTEGRATION[section_start:INTEGRATION.index("### `matrix`", section_start)]
    assert "scripts/discover_candidates.py" in section
    assert "candidate_table.csv" in section
    assert "paper-lookup" in section


if __name__ == "__main__":
    test_mode_router_is_explicit_and_progressive()
    test_default_route_prefers_matrix_and_deep_cards()
    test_usage_examples_cover_default_and_search_only()
    test_skill_chaining_names_supporting_skills_without_force_loading()
    test_no_mojibake_in_routing_labels()
    test_readme_usage_examples_match_default_routes()
    test_integration_search_only_points_to_discovery_first()
    print("test_skill_routing_contract.py passed")