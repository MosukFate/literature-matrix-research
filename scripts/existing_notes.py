"""Read-only exact identity lookup in existing Markdown paper notes.

Only opening frontmatter's top-level, single-line scalar fields are read.
This supports the skill's local card format without treating body citations,
aliases, nested mappings, lists, or multiline YAML as primary paper identity.
A match locates a note; its declared type is copied without validating it.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit


IDENTIFIER_FIELDS = {
    "doi": ("doi", "doi_url"),
    "arxiv_id": ("arxiv_id", "arxiv", "arxiv_url"),
    "openreview_id": ("openreview_id", "openreview", "openreview_url"),
}
URL_FIELDS = ("official_url", "pdf_url", "paper_url", "source_url")
METADATA_FIELDS = {"title", "type", "paper_type", *URL_FIELDS,
                   *(field for fields in IDENTIFIER_FIELDS.values() for field in fields)}


def _scalar(value: str) -> str:
    """Read plain, single-quoted, or JSON-compatible double-quoted scalars."""
    value = value.strip()
    if value.startswith('"'):
        try:
            scalar, end = json.JSONDecoder().raw_decode(value)
        except ValueError:
            return ""
        tail = value[end:].strip()
        return scalar if isinstance(scalar, str) and (not tail or tail.startswith("#")) else ""
    if value.startswith("'"):
        match = re.fullmatch(r"'((?:[^']|'')*)'\s*(?:#.*)?", value)
        return match[1].replace("''", "'") if match else ""
    value = re.split(r"\s+#", value, maxsplit=1)[0].strip()
    if not value or value.casefold() in {"null", "~"} or value[0] in "[{}|>&*!":
        return ""
    return value


def _metadata(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    metadata = {}
    for line in lines[1:]:
        if line.strip() in {"---", "..."}:
            return metadata
        match = re.match(r"^([A-Za-z_][A-Za-z_0-9-]*):\s*(.*)$", line)
        if match and match[1].casefold() in METADATA_FIELDS:
            metadata[match[1].casefold()] = _scalar(match[2])
    return {}


def _doi(value: str) -> str:
    value = value.strip()
    if "://" in value:
        url = urlsplit(value)
        if (url.hostname or "").casefold() not in {"doi.org", "dx.doi.org"}:
            return ""
        value = unquote(url.path).lstrip("/")
    value = re.sub(r"^doi:\s*", "", value, flags=re.IGNORECASE)
    return value.casefold() if re.fullmatch(r"10\.\d{4,9}/\S+", value) else ""


def _arxiv(value: str) -> str:
    value = value.strip()
    if "://" in value:
        url = urlsplit(value)
        if (url.hostname or "").casefold() not in {"arxiv.org", "www.arxiv.org", "export.arxiv.org"}:
            return ""
        value = re.sub(r"^/(?:abs|pdf|html)/", "", unquote(url.path), flags=re.IGNORECASE)
    value = re.sub(r"^arxiv:\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\.pdf$", "", value, flags=re.IGNORECASE)
    if not re.fullmatch(r"(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[a-z]{2})?/\d{7})(?:v\d+)?", value, re.IGNORECASE):
        return ""
    return re.sub(r"v\d+$", "", value, flags=re.IGNORECASE).casefold()


def _openreview(value: str) -> str:
    value = value.strip()
    if "://" in value:
        url = urlsplit(value)
        if (url.hostname or "").casefold() not in {"openreview.net", "www.openreview.net"}:
            return ""
        value = parse_qs(url.query).get("id", [""])[0]
    value = re.sub(r"^openreview:\s*", "", value, flags=re.IGNORECASE)
    return value if re.fullmatch(r"[A-Za-z0-9_-]+", value) else ""


NORMALIZERS = {"doi": _doi, "arxiv_id": _arxiv, "openreview_id": _openreview}


def _identities(metadata: dict) -> dict[str, set[str]]:
    identities = {}
    for family, fields in IDENTIFIER_FIELDS.items():
        normalize = NORMALIZERS[family]
        values = [metadata.get(field, "") for field in fields]
        values.extend(metadata.get(field, "") for field in URL_FIELDS
                      if "://" in str(metadata.get(field, "")))
        identities[family] = {identity for value in values if isinstance(value, str)
                              and (identity := normalize(value))}
    return identities


def _title(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join("".join(char if char.isalnum() or unicodedata.category(char).startswith("M")
                            else " " for char in value).split())


def match_existing_notes(candidates: list[dict], notes_root: Path) -> list[dict]:
    """Return one match/ambiguity/no-match row per candidate without writes.

    Matching identifiers take precedence over normalized exact titles. Any
    disagreement in an identifier family shared by candidate and note blocks
    that note, including a title fallback. Duplicate matches remain ambiguous.
    Paths are absolute; note types are declarations, not verified card quality.
    """
    notes = []
    for path in sorted(Path(notes_root).rglob("*.md")):
        metadata = _metadata(path)
        if metadata:
            notes.append((str(path.resolve()), metadata.get("type") or metadata.get("paper_type", ""),
                          _title(metadata.get("title", "")), _identities(metadata)))

    rows = []
    for candidate in candidates:
        row = {"candidate_id": candidate.get("candidate_id") or candidate.get("id", ""),
               "title": candidate.get("title", "")}
        title = _title(str(row["title"] or ""))
        identities = _identities(candidate)
        id_matches, title_matches, conflicts = [], [], False
        for path, note_type, note_title, note_ids in notes:
            matched_ids = [family for family in IDENTIFIER_FIELDS if identities[family] & note_ids[family]]
            disagreement = any(len(identities[family]) > 1 or len(note_ids[family]) > 1
                               or (identities[family] and note_ids[family]
                                   and identities[family] != note_ids[family]) for family in IDENTIFIER_FIELDS)
            same_title = bool(title and title == note_title)
            if disagreement:
                conflicts = conflicts or same_title or bool(matched_ids)
            elif matched_ids:
                id_matches.append((path, note_type, matched_ids))
            elif same_title:
                title_matches.append((path, note_type, ["title"]))
        matches = id_matches or title_matches
        if not matches:
            row.update(status="no_match", match_reason="conflicting_identifiers" if conflicts else "no_exact_match")
        else:
            reasons = {reason for _, _, reasons in matches for reason in reasons}
            row.update(status="matched" if len(matches) == 1 else "ambiguous",
                       match_reason=";".join(reason for reason in (*IDENTIFIER_FIELDS, "title") if reason in reasons))
            if len(matches) == 1:
                row.update(existing_note_path=matches[0][0], existing_note_type=matches[0][1])
            else:
                row.update(existing_note_paths=[match[0] for match in matches],
                           existing_note_types=[match[1] for match in matches])
        rows.append(row)
    return rows
