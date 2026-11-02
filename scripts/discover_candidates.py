#!/usr/bin/env python3
"""Discover, merge, rank, and export literature-matrix candidate papers.

The fixture path is dependency-free for offline tests. Live adapters are
best-effort public HTTP calls and record failures in the search ledger.
"""

from __future__ import annotations

import argparse
import csv
import html as html_lib
import json
import math
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from existing_notes import match_existing_notes

CANDIDATE_FIELDS = [
    "id", "title", "year", "venue", "sources", "source_status", "layer",
    "overall_score", "relevance_score", "venue_score", "citation_score",
    "recency_score", "novelty_risk_score", "citation_count", "graph_relation",
    "doi", "arxiv_id", "openreview_id", "acl_id", "pmlr_url", "cvf_url",
    "semantic_scholar_id", "openalex_id", "official_url", "pdf_url",
    "code_url", "data_url", "why_relevant", "why_core", "query", "abstract",
]

DIRECT_TERMS = {
    "activation", "patching", "causal", "tracing", "mechanism",
    "mechanistic", "steering", "probing", "representation", "neuron",
    "circuit", "rag", "retrieval", "evidence", "knowledge", "commonsense",
    "common", "sense", "long", "tail", "low", "frequency", "fact",
    "facts", "factual", "reasoning", "trajectory", "trajectories",
    "composition", "compose", "rule", "rules", "entity", "entities",
    "benchmark",
}

STOPWORDS = {
    "the", "and", "for", "with", "from", "into", "onto", "that", "this",
    "these", "those", "via", "using", "used", "use", "based", "towards",
    "toward", "between", "among", "over", "under", "within", "without",
    "paper", "study", "survey", "approach", "method", "model", "models",
}
def unique(values: Iterable[str]) -> list[str]:
    seen, out = set(), []
    for value in values:
        value = str(value or "").strip()
        if value and value not in seen:
            seen.add(value)
            out.append(value)
    return out



def split_semicolon_values(*values: str) -> list[str]:
    return unique(part.strip() for value in values for part in str(value or "").split(";"))

def normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", title.lower())).strip()


def tokens(text: str) -> set[str]:
    return {tok for tok in re.findall(r"[a-z0-9]+", text.lower()) if len(tok) > 2 and tok not in STOPWORDS}


def first(*values: Any) -> str:
    for value in values:
        if value is not None and str(value).strip():
            return str(value).strip()
    return ""


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@dataclass
class Candidate:
    title: str
    year: int = 0
    venue: str = ""
    abstract: str = ""
    doi: str = ""
    arxiv_id: str = ""
    openreview_id: str = ""
    acl_id: str = ""
    pmlr_url: str = ""
    cvf_url: str = ""
    semantic_scholar_id: str = ""
    openalex_id: str = ""
    official_url: str = ""
    pdf_url: str = ""
    code_url: str = ""
    data_url: str = ""
    query: str = ""
    graph_relation: str = "query_hit"
    citation_count: int = 0
    has_code: bool = False
    sources: list[str] = field(default_factory=list)
    source_status: str = "metadata-only"
    layer: str = "matrix-only"
    overall_score: float = 0.0
    relevance_score: float = 0.0
    venue_score: float = 0.0
    citation_score: float = 0.0
    recency_score: float = 0.0
    novelty_risk_score: float = 0.0
    why_relevant: str = ""
    why_core: str = ""

    @classmethod
    def from_raw(cls, raw: dict[str, Any], gap: str = "") -> "Candidate":
        source = first(raw.get("source"), raw.get("provider"), "manual")
        openreview_id = first(raw.get("openreview_id"))
        acl_id = first(raw.get("acl_id"))
        pmlr_url = first(raw.get("pmlr_url"))
        cvf_url = first(raw.get("cvf_url"))
        official_url = first(raw.get("official_url"), pmlr_url, cvf_url)
        if acl_id and not official_url:
            official_url = f"https://aclanthology.org/{acl_id}/"
        if openreview_id and not official_url:
            official_url = f"https://openreview.net/forum?id={openreview_id}"
        candidate = cls(
            title=first(raw.get("title"), raw.get("name")),
            year=to_int(raw.get("year")),
            venue=first(raw.get("venue"), raw.get("venue_name")),
            abstract=first(raw.get("abstract"), raw.get("summary"), raw.get("tldr")),
            doi=first(raw.get("doi")),
            arxiv_id=first(raw.get("arxiv_id"), raw.get("arxivId")),
            openreview_id=openreview_id,
            acl_id=acl_id,
            pmlr_url=pmlr_url,
            cvf_url=cvf_url,
            semantic_scholar_id=first(raw.get("semantic_scholar_id"), raw.get("paperId"), raw.get("corpusId")),
            openalex_id=first(raw.get("openalex_id"), raw.get("id") if source == "openalex" else ""),
            official_url=official_url,
            pdf_url=first(raw.get("pdf_url"), raw.get("pdf")),
            code_url=first(raw.get("code_url"), raw.get("github_url"), raw.get("repository")),
            data_url=first(raw.get("data_url"), raw.get("dataset_url")),
            query=first(raw.get("query"), gap),
            graph_relation=first(raw.get("graph_relation"), "query_hit"),
            citation_count=to_int(raw.get("citation_count"), to_int(raw.get("citationCount"))),
            has_code=bool(raw.get("has_code") or raw.get("code_url") or raw.get("github_url")),
            sources=[source],
        )
        candidate.source_status = infer_source_status(candidate)
        return candidate

    @property
    def normalized_title(self) -> str:
        return normalize_title(self.title)

    def merge(self, other: "Candidate") -> "Candidate":
        self.sources = unique([*self.sources, *other.sources])
        for attr in [
            "doi", "arxiv_id", "openreview_id", "acl_id", "pmlr_url",
            "cvf_url", "semantic_scholar_id", "openalex_id", "official_url",
            "pdf_url", "code_url", "data_url",
        ]:
            if not getattr(self, attr) and getattr(other, attr):
                setattr(self, attr, getattr(other, attr))
        self.venue = self.venue or other.venue
        self.abstract = self.abstract or other.abstract
        self.year = self.year or other.year
        self.citation_count = max(self.citation_count, other.citation_count)
        self.has_code = self.has_code or other.has_code
        self.graph_relation = ";".join(split_semicolon_values(self.graph_relation, other.graph_relation))
        self.query = "; ".join(split_semicolon_values(self.query, other.query))
        self.source_status = infer_source_status(self)
        return self

    def to_row(self, row_id: int) -> dict[str, str]:
        values = {field: getattr(self, field, "") for field in CANDIDATE_FIELDS}
        values["id"] = f"C{row_id:04d}"
        values["sources"] = ";".join(self.sources)
        for field in ["overall_score", "relevance_score", "venue_score", "citation_score", "recency_score", "novelty_risk_score"]:
            values[field] = f"{getattr(self, field):.3f}"
        values["year"] = str(self.year or "")
        values["citation_count"] = str(self.citation_count)
        return {field: str(values.get(field, "")) for field in CANDIDATE_FIELDS}


def infer_source_status(c: Candidate) -> str:
    text = f"{c.venue} {c.official_url} {c.pmlr_url} {c.cvf_url} {c.acl_id} {c.openreview_id}".lower()
    if c.pmlr_url or "proceedings.mlr.press" in text:
        return "official:icml-pmlr"
    if c.acl_id or "aclanthology.org" in text:
        return "official:acl-anthology"
    if c.cvf_url or "openaccess.thecvf.com" in text:
        return "official:cvf"
    if c.openreview_id or "openreview.net" in text:
        return "official:openreview"
    if c.arxiv_id or "arxiv" in c.venue.lower() or "arxiv" in c.official_url.lower():
        return "arxiv-only"
    if c.code_url or c.data_url:
        return "project/code-only"
    return "metadata-only"


def merge_key(c: Candidate) -> tuple[str, str]:
    for field in ["doi", "arxiv_id", "openreview_id"]:
        value = getattr(c, field)
        if value:
            return field, value.lower()
    if c.official_url:
        return "official_url", c.official_url.lower().rstrip("/")
    return "title", c.normalized_title


def merge_candidates(candidates: list[Candidate]) -> list[Candidate]:
    merged: dict[tuple[str, str], Candidate] = {}
    titles: dict[str, tuple[str, str]] = {}
    for candidate in candidates:
        key = merge_key(candidate)
        title_key = candidate.normalized_title
        existing = key if key in merged else titles.get(title_key)
        if existing in merged:
            merged[existing].merge(candidate)
        else:
            merged[key] = candidate
            if title_key:
                titles[title_key] = key
    return list(merged.values())


def relevance(c: Candidate, gap: str) -> float:
    gap_terms = tokens(gap) | DIRECT_TERMS
    title_query = tokens(f"{c.title} {c.query}")
    abstract = tokens(c.abstract)
    tq = len(title_query & gap_terms) / min(max(len(gap_terms), 1), 28)
    ab = len(abstract & gap_terms) / min(max(len(gap_terms), 1), 28)
    text = f"{c.title} {c.query} {c.abstract}".lower()
    bonus = 0.0
    for phrase in ["low-frequency", "long-tail", "activation patching", "causal tracing", "commonsense reasoning", "factual recall", "knowledge graph"]:
        if phrase in text:
            bonus += 0.07
    if any(rel in c.graph_relation for rel in ["seed", "cited_by_seed", "cites_seed", "shared_reference", "semantic_related"]):
        bonus += 0.10
    return min(1.0, 0.58 * min(tq, 1.0) + 0.22 * min(ab, 1.0) + bonus)


def venue_score(c: Candidate) -> float:
    if c.source_status.startswith("official"):
        return 0.95
    if c.source_status == "arxiv-only":
        return 0.58
    if c.source_status == "project/code-only":
        return 0.35
    return 0.2


def citation_score(count: int) -> float:
    return 0.0 if count <= 0 else min(1.0, math.log10(count + 1) / 3.0)


def recency_score(year: int, current_year: int) -> float:
    return 0.0 if not year else max(0.0, min(1.0, 1.0 - ((current_year - year) / 8.0)))


def novelty_score(c: Candidate) -> float:
    rel_bonus = 0.35 if any(rel in c.graph_relation for rel in ["cited_by_seed", "cites_seed", "shared_reference", "semantic_related"]) else 0.0
    direct = min(0.45, len(tokens(f"{c.title} {c.abstract}") & DIRECT_TERMS) / 18.0)
    arxiv = 0.15 if c.source_status == "arxiv-only" and c.year >= 2024 else 0.0
    return min(1.0, rel_bonus + direct + arxiv)


def explain(c: Candidate) -> str:
    if c.relevance_score < 0.22:
        return "weak topical overlap only; keep matrix-only unless manually promoted with stronger evidence"
    text = f"{c.title} {c.abstract} {c.query}".lower()
    signals = []
    if any(term in text for term in ["long-tail", "low-frequency", "factual", "fact"]):
        signals.append("factual/long-tail signal")
    if any(term in text for term in ["commonsense", "common sense", "knowledge graph", "entity"]):
        signals.append("entity or commonsense signal")
    if any(term in text for term in ["activation", "causal", "patching", "tracing", "steering", "probe"]):
        signals.append("mechanism/intervention signal")
    return "; ".join(signals or ["weak topical overlap only"])


def assign_layer(c: Candidate) -> None:
    if c.relevance_score >= 0.55 and (c.venue_score >= 0.7 or c.has_code or c.novelty_risk_score >= 0.45):
        c.layer = "core"
    elif c.relevance_score >= 0.42 or (c.relevance_score >= 0.35 and c.venue_score >= 0.7):
        c.layer = "bridge"
    elif c.relevance_score >= 0.22 or c.novelty_risk_score >= 0.4:
        c.layer = "supplemental"
    else:
        c.layer = "matrix-only"
    c.why_relevant = explain(c)
    if c.layer in {"core", "bridge"}:
        if c.source_status == "arxiv-only":
            c.why_core = "High relevance to the gap despite arXiv-only status; keep source_status conservative and verify before deep-card claims."
        elif c.layer == "core":
            c.why_core = "Directly supports a work package through method, benchmark, mechanism, or closest-prior evidence."
        else:
            c.why_core = "Connects two required areas for the matrix and should be read before synthesis."


def rank_candidates(candidates: list[Candidate], gap: str, current_year: int | None = None) -> list[Candidate]:
    current_year = current_year or datetime.now(timezone.utc).year
    for c in candidates:
        c.source_status = infer_source_status(c)
        c.relevance_score = relevance(c, gap)
        c.venue_score = venue_score(c)
        c.citation_score = citation_score(c.citation_count)
        c.recency_score = recency_score(c.year, current_year)
        c.novelty_risk_score = novelty_score(c)
        c.overall_score = round(0.45*c.relevance_score + 0.25*c.venue_score + 0.15*c.novelty_risk_score + 0.10*c.recency_score + 0.05*c.citation_score, 6)
        assign_layer(c)
    return sorted(candidates, key=lambda c: (c.overall_score, c.relevance_score, c.venue_score), reverse=True)


def http_text(url: str, failed: list[dict[str, str]], adapter: str, timeout: int = 20) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "literature-matrix-research/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="replace")
    except Exception as exc:
        failed.append({"adapter": adapter, "url": url, "error": str(exc)})
        return ""


def http_json(url: str, failed: list[dict[str, str]], adapter: str) -> Any:
    text = http_text(url, failed, adapter)
    return json.loads(text) if text else {}


def inverted_abstract(index: dict[str, list[int]]) -> str:
    positions = {}
    for word, locs in index.items():
        for loc in locs:
            positions[int(loc)] = word
    return " ".join(positions[i] for i in sorted(positions))


def search_arxiv(query: str, limit: int, failed: list[dict[str, str]]) -> list[dict[str, Any]]:
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode({"search_query": f"all:{query}", "start": 0, "max_results": limit})
    text = http_text(url, failed, "arxiv")
    if not text:
        return []
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    root = ET.fromstring(text)
    records = []
    for entry in root.findall("atom:entry", ns):
        arxiv_url = entry.findtext("atom:id", default="", namespaces=ns)
        records.append({
            "source": "arxiv",
            "title": " ".join((entry.findtext("atom:title", default="", namespaces=ns) or "").split()),
            "abstract": " ".join((entry.findtext("atom:summary", default="", namespaces=ns) or "").split()),
            "year": to_int((entry.findtext("atom:published", default="", namespaces=ns) or "")[:4]),
            "venue": "arXiv",
            "arxiv_id": arxiv_url.rstrip("/").split("/")[-1],
            "official_url": arxiv_url,
            "pdf_url": arxiv_url.replace("/abs/", "/pdf/"),
            "query": query,
        })
    return records


def search_semantic_scholar(query: str, limit: int, failed: list[dict[str, str]]) -> list[dict[str, Any]]:
    fields = "title,year,venue,abstract,citationCount,externalIds,openAccessPdf,url"
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + urllib.parse.urlencode({"query": query, "limit": limit, "fields": fields})
    data = http_json(url, failed, "semantic_scholar")
    out = []
    for item in data.get("data", []):
        external = item.get("externalIds") or {}
        pdf = item.get("openAccessPdf") or {}
        out.append({"source": "semantic_scholar", "title": item.get("title"), "year": item.get("year"), "venue": item.get("venue"), "abstract": item.get("abstract"), "citation_count": item.get("citationCount"), "semantic_scholar_id": item.get("paperId"), "doi": external.get("DOI"), "arxiv_id": external.get("ArXiv"), "official_url": item.get("url"), "pdf_url": pdf.get("url"), "query": query})
    return out


def search_openalex(query: str, limit: int, failed: list[dict[str, str]]) -> list[dict[str, Any]]:
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode({"search": query, "per-page": limit})
    data = http_json(url, failed, "openalex")
    out = []
    for item in data.get("results", []):
        primary = item.get("primary_location") or {}
        source = primary.get("source") or {}
        out.append({"source": "openalex", "title": item.get("title"), "year": item.get("publication_year"), "venue": source.get("display_name"), "abstract": inverted_abstract(item.get("abstract_inverted_index") or {}), "citation_count": item.get("cited_by_count"), "doi": str(item.get("doi") or "").replace("https://doi.org/", ""), "openalex_id": item.get("id"), "official_url": primary.get("landing_page_url"), "pdf_url": primary.get("pdf_url"), "query": query})
    return out


def search_openreview(query: str, limit: int, failed: list[dict[str, str]]) -> list[dict[str, Any]]:
    url = "https://api2.openreview.net/notes/search?" + urllib.parse.urlencode({"term": query, "limit": limit})
    data = http_json(url, failed, "openreview")
    out = []
    for item in data.get("notes", []):
        content = item.get("content") or {}
        title = content.get("title")
        abstract = content.get("abstract")
        title = title.get("value") if isinstance(title, dict) else title
        abstract = abstract.get("value") if isinstance(abstract, dict) else abstract
        oid = item.get("forum") or item.get("id")
        out.append({"source": "openreview", "title": title, "abstract": abstract, "venue": "OpenReview", "openreview_id": oid, "official_url": f"https://openreview.net/forum?id={oid}", "query": query})
    return out


def search_acl(query: str, limit: int, failed: list[dict[str, str]]) -> list[dict[str, Any]]:
    html = http_text("https://aclanthology.org/search/?" + urllib.parse.urlencode({"q": query}), failed, "acl")
    out = []
    for match in re.finditer(r'href="/(?P<id>\d{4}\.[^"]+?)/"[^>]*>\s*(?P<title>[^<]+)', html):
        acl_id = match.group("id")
        out.append({"source": "acl", "title": re.sub(r"\s+", " ", match.group("title")).strip(), "year": to_int(acl_id[:4]), "venue": "ACL Anthology", "acl_id": acl_id, "official_url": f"https://aclanthology.org/{acl_id}/", "pdf_url": f"https://aclanthology.org/{acl_id}.pdf", "query": query})
        if len(out) >= limit:
            break
    return out


def html_plain(text: str) -> str:
    return " ".join(html_lib.unescape(re.sub(r"<[^>]+>", " ", text)).split())


def conference_year_window(year_from: int = 0, year_to: int = 0) -> tuple[int, int]:
    """Use three calendar years when a lower bound is not supplied."""
    upper = year_to or max(year_from, datetime.now(timezone.utc).year)
    return year_from or upper - 2, upper


def proceedings_indexes(html: str, adapter: str) -> list[dict[str, Any]]:
    entries = []
    if adapter == "pmlr":
        for item in re.findall(r"<li\b[^>]*>(.*?)</li>", html, re.S | re.I):
            link = re.search(r'''href=["'](?:https://proceedings\.mlr\.press/|/)?([vr]\d+)/?["']''', item, re.I)
            if not link:
                continue
            label = re.sub(r"^Volume\s+R?\d+\s*", "", html_plain(item), flags=re.I)
            years = set(re.findall(r"\b(?:19|20)\d{2}\b", label))
            entries.append({"url": f"https://proceedings.mlr.press/{link.group(1)}/",
                            "label": label, "year": int(next(iter(years))) if len(years) == 1 else 0})
    else:
        for name, year, suffix in re.findall(r'''href=["'](?:https://openaccess\.thecvf\.com/|/)?([A-Za-z]+)(\d{4})(\.py)?/?["']''', html):
            url = f"https://openaccess.thecvf.com/{name}{year}{suffix}?day=all"
            if not any(row["url"] == url for row in entries):
                entries.append({"url": url, "label": name, "year": int(year)})
    return entries


def proceedings_papers(html: str, adapter: str, url: str) -> list[tuple[str, str]]:
    papers = []
    if adapter == "pmlr":
        for block in re.split(r'''<div\b[^>]*class=["']paper["'][^>]*>''', html, flags=re.I)[1:]:
            title = re.search(r'''<p\b[^>]*class=["']title["'][^>]*>(.*?)</p>''', block, re.S | re.I)
            link = re.search(r'''href=["']([^"']+\.html)["']''', block, re.I)
            if title and link:
                papers.append((html_plain(title.group(1)), urllib.parse.urljoin(url, link.group(1))))
    else:
        for block in re.findall(r'''<dt\b[^>]*class=["']ptitle["'][^>]*>(.*?)</dt>''', html, re.S | re.I):
            link = re.search(r'''<a\b[^>]*href=["']([^"']+)["'][^>]*>(.*?)</a>''', block, re.S | re.I)
            if link:
                papers.append((html_plain(link.group(2)), urllib.parse.urljoin(url, link.group(1))))
    return papers


def search_proceedings(query: str, limit: int, failed: list[dict[str, str]], adapter: str,
                       year_from: int, year_to: int, venues: list[str] | None,
                       coverage: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    lower, upper = conference_year_window(year_from, year_to)
    venues = unique(venues or [])
    index_url = "https://proceedings.mlr.press/" if adapter == "pmlr" else "https://openaccess.thecvf.com/menu"
    html = http_text(index_url, failed, adapter)
    entries = proceedings_indexes(html, adapter)
    report = {"adapter": adapter, "query": query, "index_url": index_url,
              "year_from": lower, "year_to": upper, "venues": venues,
              "search_scope": ("indexed volume labels with explicit year; title matching only" if adapter == "pmlr"
                               else "main-conference indexes; title matching only"),
              "index_status": "retrieved" if html else "failed", "status": "failed",
              "unknown_year_indexes": [{"url": row["url"], "label": row["label"]} for row in entries if not row["year"]],
              "missing_indexes": [], "proceedings": [], "returned_records": 0}
    if coverage is not None:
        coverage.append(report)
    if not html:
        return []
    if not entries:
        report["status"] = "unparsed-index"
        return []

    def venue_matches(label: str, venue: str) -> bool:
        return f" {normalize_title(venue)} " in f" {normalize_title(label)} "

    selected = [row for row in entries if lower <= row["year"] <= upper
                and (not venues or any(venue_matches(row["label"], venue) for venue in venues))]
    selected.sort(key=lambda row: row["year"], reverse=True)
    report["missing_indexes"] = [{"year": year, "venue": venue} for year in range(lower, upper + 1)
                                 for venue in venues or ["*"]
                                 if not any(row["year"] == year and (venue == "*" or venue_matches(row["label"], venue))
                                            for row in selected)]
    out, query_tokens = [], tokens(query)
    for entry in selected:
        state = {**entry, "status": "not-fetched-limit", "papers_parsed": 0, "title_matches": 0, "returned_records": 0}
        report["proceedings"].append(state)
        if len(out) >= limit:
            continue
        html = http_text(entry["url"], failed, adapter)
        papers = proceedings_papers(html, adapter, entry["url"])
        matches = [(title, url) for title, url in papers if not query_tokens
                   or len(tokens(title) & query_tokens) >= (2 if len(query_tokens) >= 3 else 1)]
        returned = matches[:max(0, limit - len(out))]
        state.update(status=("failed" if not html else "unparsed" if not papers else
                             "truncated" if len(returned) < len(matches) else "retrieved"),
                     papers_parsed=len(papers), title_matches=len(matches), returned_records=len(returned))
        for title, url in returned:
            out.append({"source": adapter, "title": title, "year": entry["year"],
                        "venue": entry["label"], f"{adapter}_url": url,
                        "official_url": url, "query": query})
    states = [row["status"] for row in report["proceedings"]]
    report["returned_records"] = len(out)
    report["status"] = ("no-index" if not selected else "truncated" if any(state in {"truncated", "not-fetched-limit"} for state in states)
                        else "partial" if report["missing_indexes"] or any(state != "retrieved" for state in states) else "retrieved")
    return out


def search_pmlr(query: str, limit: int, failed: list[dict[str, str]], year_from: int = 0,
                year_to: int = 0, venues: list[str] | None = None,
                coverage: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    return search_proceedings(query, limit, failed, "pmlr", year_from, year_to, venues, coverage)


def search_cvf(query: str, limit: int, failed: list[dict[str, str]], year_from: int = 0,
               year_to: int = 0, venues: list[str] | None = None,
               coverage: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    return search_proceedings(query, limit, failed, "cvf", year_from, year_to, venues, coverage)


def build_queries(args: argparse.Namespace) -> list[str]:
    vals = unique([args.query, args.seed_title, args.gap])
    if args.query and args.gap:
        vals.append(f"{args.query} {args.gap}")
    return unique(vals)


def live_search(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, str]]]:
    failed, raw, coverage = [], [], []
    adapters = [search_arxiv, search_semantic_scholar, search_openalex, search_openreview, search_acl, search_pmlr, search_cvf]
    queries = build_queries(args)
    for query in queries:
        for adapter in adapters:
            if adapter in {search_pmlr, search_cvf}:
                raw.extend(adapter(query, args.limit, failed, args.year_from, args.year_to,
                                   getattr(args, "proceedings_venue", []), coverage))
            else:
                raw.extend(adapter(query, args.limit, failed))
            if args.sleep:
                time.sleep(args.sleep)
    return raw, {"created_at": datetime.now(timezone.utc).isoformat(), "queries": queries, "adapters": [fn.__name__ for fn in adapters], "record_count": len(raw), "seed_url": args.seed_url, "source_coverage": coverage}, failed


def load_fixture(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any], list[dict[str, str]], str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("records", []), {"fixture": str(path), "queries": [data.get("gap", "")]}, [], data.get("gap", "")


def write_outputs(candidates: list[Candidate], out_dir: Path, search_log: dict[str, Any], failed_queries: list[dict[str, str]]) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = [c.to_row(i + 1) for i, c in enumerate(candidates)]
    with (out_dir / "candidate_table.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=CANDIDATE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    with (out_dir / "candidate_table.jsonl").open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    (out_dir / "search_log.json").write_text(json.dumps(search_log, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# Failed Queries", ""]
    if failed_queries:
        for item in failed_queries:
            lines.append(f"- `{item.get('adapter')}`: {item.get('url')} :: {item.get('error')}")
    else:
        lines.append("No failed queries recorded.")
    (out_dir / "failed_queries.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="")
    parser.add_argument("--seed-title", default="")
    parser.add_argument("--seed-url", default="")
    parser.add_argument("--gap", default="")
    parser.add_argument("--year-from", type=int, default=0)
    parser.add_argument("--year-to", type=int, default=0)
    parser.add_argument("--proceedings-venue", action="append", default=[],
                        help="Repeatable PMLR index-label/CVF main-conference filter, e.g. ICML or CVPR; omitted means all indexed venues in the year window")
    parser.add_argument("--notes-root", type=Path,
                        help="Read-only existing Markdown note lookup; writes a separate match ledger")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--fixture", type=Path, default=None)
    parser.add_argument("--limit", type=int, default=8)
    parser.add_argument("--sleep", type=float, default=0.0)
    args = parser.parse_args(argv)
    if args.year_from and args.year_to and args.year_from > args.year_to:
        parser.error("--year-from must not exceed --year-to")
    if args.notes_root is not None and not args.notes_root.is_dir():
        parser.error("--notes-root must be an existing directory")
    if args.fixture:
        raw, log, failed, fixture_gap = load_fixture(args.fixture)
        gap = args.gap or fixture_gap
    else:
        raw, log, failed = live_search(args)
        gap = args.gap or args.query or args.seed_title
    candidates = [Candidate.from_raw(row, gap=gap) for row in raw if first(row.get("title"))]
    if args.year_from:
        candidates = [c for c in candidates if not c.year or c.year >= args.year_from]
    if args.year_to:
        candidates = [c for c in candidates if not c.year or c.year <= args.year_to]
    ranked = rank_candidates(merge_candidates(candidates), gap=gap)
    note_matches = (match_existing_notes([candidate.to_row(i + 1) for i, candidate in enumerate(ranked)],
                                        args.notes_root) if args.notes_root is not None else None)
    write_outputs(ranked, args.out_dir, log, failed)
    match_ledger = args.out_dir / "existing_note_matches.jsonl"
    if note_matches is not None:
        match_ledger.write_text(
            "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in note_matches), encoding="utf-8")
    elif match_ledger.exists():
        match_ledger.unlink()
    print(f"candidates={len(ranked)} out_dir={args.out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
