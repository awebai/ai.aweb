#!/usr/bin/env python3
"""
Score the aweb UX surface inventory against persona priorities.

Reads personas.yaml + surfaces.yaml from this directory. For each
surface, computes:

  V(S) = sum_P [ W(P) * weight(role_for(S, P)) ]

Under both linear and exponential persona weighting schemes. Plus
produces per-persona action lists derived from the qualitative
role_for taxonomy:

  - essential / heavy / useful contribute to V(S) and to "kept"
    surface lists.
  - friction does NOT contribute to V(S). It produces a HIDE_FOR
    action: the surface should be hidden from the friction
    persona's view.
  - harmful also contributes 0 to V(S). It produces a REFRAME_FOR
    action: the surface's vocabulary / framing breaks the persona's
    mental model.
  - irrelevant: no signal (persona doesn't see this surface).

Output: ux-surface-report.md

Run from agents/sofia/ux/:
    uv run --with PyYAML python score.py
"""
from __future__ import annotations

from pathlib import Path
from collections import defaultdict
from typing import Any
import yaml

HERE = Path(__file__).parent
PERSONAS_FILE = HERE / "personas.yaml"
SURFACES_FILE = HERE / "surfaces.yaml"
REPORT_FILE = HERE / "ux-surface-report.md"

ROLE_VALUES = ["essential", "heavy", "useful", "irrelevant",
                "friction", "harmful"]
ROLE_VALUE_RANK = {v: i for i, v in enumerate(ROLE_VALUES)}

FOCUS_FRACTION = 0.6   # V(S) >= max * 0.6 -> FOCUS-band score
CUT_FRACTION   = 0.20  # V(S) <  max * 0.20 -> low-V


def load_data() -> tuple[dict[str, Any], dict[str, Any]]:
    with PERSONAS_FILE.open() as f:
        personas_doc = yaml.safe_load(f)
    with SURFACES_FILE.open() as f:
        surfaces_doc = yaml.safe_load(f)
    return personas_doc, surfaces_doc


def weights(personas_doc: dict[str, Any], field: str) -> dict[str, int]:
    return {p: meta[field] for p, meta in personas_doc["personas"].items()}


def role_weight_map(personas_doc: dict[str, Any]) -> dict[str, int]:
    return personas_doc["role_for_weights"]


def score(surface: dict[str, Any], w: dict[str, int],
          rw: dict[str, int]) -> int:
    role_for = surface.get("role_for") or {}
    return sum(w[p] * rw[role_for.get(p, "irrelevant")] for p in w)


def personas_with_role(surface: dict[str, Any], role: str) -> list[str]:
    role_for = surface.get("role_for") or {}
    return [p for p, v in role_for.items() if v == role]


def primary_persona(surface: dict[str, Any],
                     personas_doc: dict[str, Any]) -> str:
    role_for = surface.get("role_for") or {}
    if not role_for:
        return "—"
    # Find the persona(s) with the best (lowest rank) role value.
    # If multiple tie, pick the one with the highest priority.
    persona_priority = sorted(personas_doc["personas"].keys(),
                               key=lambda p: personas_doc["personas"][p]["priority"])
    best_rank = min(ROLE_VALUE_RANK[role_for.get(p, "irrelevant")]
                    for p in persona_priority)
    best_role = ROLE_VALUES[best_rank]
    # Skip "fake-best" values: irrelevant/friction/harmful aren't "primary use"
    if best_role in ("irrelevant", "friction", "harmful"):
        return "—"
    for p in persona_priority:
        if role_for.get(p) == best_role:
            return p
    return "—"


def recommend_action(surface: dict[str, Any],
                      priority_personas: list[str]) -> tuple[str, list[str]]:
    """Return (action_code, list_of_notes) for this surface.

    Action codes:
      DEPRECATED — explicit flag; cut.
      REDUNDANT — duplicates another surface; cut or merge.
      NEVER_CUT — essential for at least one persona.
      REFRAME_FOR — harmful for priority persona; vocabulary fix.
      HIDE_FOR — friction for priority persona; persona-aware hiding.
      FOCUS — heavy or essential for a priority persona.
      KEEP — heavy or essential for a non-priority persona only.
      USEFUL — useful for at least one persona; no friction/harm.
      CUT_CANDIDATE — no positive role for any persona.

    A surface can have multiple notes (e.g., FOCUS + HIDE_FOR).
    """
    notes: list[str] = []

    if surface.get("deprecated"):
        return "DEPRECATED", notes
    if surface.get("redundant_with"):
        return "REDUNDANT", [f"duplicates {surface['redundant_with']}"]

    role_for = surface.get("role_for") or {}
    essentials = personas_with_role(surface, "essential")
    heavies = personas_with_role(surface, "heavy")
    usefuls = personas_with_role(surface, "useful")
    frictions = personas_with_role(surface, "friction")
    harmfuls = personas_with_role(surface, "harmful")

    # Pick up overlay notes regardless of primary action
    priority_frictions = [p for p in frictions if p in priority_personas]
    priority_harmfuls = [p for p in harmfuls if p in priority_personas]
    if priority_frictions:
        notes.append(f"HIDE_FOR {','.join(priority_frictions)}")
    if priority_harmfuls:
        notes.append(f"REFRAME_FOR {','.join(priority_harmfuls)}")
    other_frictions = [p for p in frictions if p not in priority_personas]
    other_harmfuls = [p for p in harmfuls if p not in priority_personas]
    if other_frictions:
        notes.append(f"hide_for {','.join(other_frictions)}")
    if other_harmfuls:
        notes.append(f"reframe_for {','.join(other_harmfuls)}")

    # Required infrastructure pins
    required = surface.get("required_for") or []

    # Decide primary action
    priority_heavies = [p for p in heavies if p in priority_personas]

    if essentials:
        return "NEVER_CUT", notes
    if priority_heavies:
        return "FOCUS", notes
    if heavies:  # heavy for non-priority persona only
        return "KEEP", notes
    if priority_personas_with_any_use(role_for, priority_personas,
                                       {"useful"}):
        return "USEFUL_PRIORITY", notes
    if usefuls:
        return "USEFUL", notes
    if required:
        return "REQUIRED_INFRA", notes
    return "CUT_CANDIDATE", notes


def priority_personas_with_any_use(role_for: dict[str, str],
                                     priority: list[str],
                                     allowed: set[str]) -> bool:
    return any(role_for.get(p) in allowed for p in priority)


def render_md_table(rows: list[list[Any]], headers: list[str]) -> str:
    lines = ["| " + " | ".join(headers) + " |",
             "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def build_report(personas_doc: dict[str, Any],
                  surfaces: list[dict[str, Any]]) -> str:
    w_lin = weights(personas_doc, "weight_linear")
    w_exp = weights(personas_doc, "weight_exponential")
    rw = role_weight_map(personas_doc)

    persona_priority = sorted(personas_doc["personas"].keys(),
                               key=lambda p: personas_doc["personas"][p]["priority"])
    priority_personas = persona_priority[:2]  # top 2 = P1, P2

    for s in surfaces:
        s["V_lin"] = score(s, w_lin, rw)
        s["V_exp"] = score(s, w_exp, rw)
        s["primary"] = primary_persona(s, personas_doc)
        action, notes = recommend_action(s, priority_personas)
        s["action"] = action
        s["action_notes"] = notes

    v_lin_values: list[int] = [s["V_lin"] for s in surfaces]
    v_exp_values: list[int] = [s["V_exp"] for s in surfaces]
    max_lin: int = max(v_lin_values) if v_lin_values else 1
    max_exp: int = max(v_exp_values) if v_exp_values else 1

    out: list[str] = []
    out.append("# UX surface prioritization report")
    out.append("")
    out.append("Generated by `agents/sofia/ux/score.py` from "
               "`personas.yaml` + `surfaces.yaml`. Re-run after editing.")
    out.append("")
    out.append(f"- Total surfaces scored: **{len(surfaces)}**")
    out.append(f"- Max V(S) under linear weights: **{max_lin}**")
    out.append(f"- Max V(S) under exponential weights: **{max_exp}**")
    out.append(f"- Priority personas (P1 + P2): {', '.join(priority_personas)}")
    out.append("")

    # Persona weights table
    out.append("## Persona weights in use")
    out.append("")
    rows = []
    for p, meta in personas_doc["personas"].items():
        rows.append([p, meta["name"], meta["priority"],
                      meta["weight_linear"], meta["weight_exponential"]])
    out.append(render_md_table(rows,
        ["Persona", "Name", "Priority", "W_linear", "W_exponential"]))
    out.append("")

    out.append("## role_for taxonomy and weights")
    out.append("")
    rows = [[r, rw[r], _role_description(r)] for r in ROLE_VALUES]
    out.append(render_md_table(rows,
        ["role_for", "weight in V(S)", "meaning"]))
    out.append("")

    # Per-persona views — the actionable headline
    for p in persona_priority:
        meta = personas_doc["personas"][p]
        out.append(f"## Per-persona view: {p} ({meta['name']})")
        out.append("")

        essentials = sorted([s for s in surfaces
                              if (s.get('role_for') or {}).get(p) == 'essential'
                              and not s.get('deprecated')
                              and not s.get('redundant_with')],
                              key=lambda s: -s["V_lin"])
        heavies = sorted([s for s in surfaces
                           if (s.get('role_for') or {}).get(p) == 'heavy'
                           and not s.get('deprecated')
                           and not s.get('redundant_with')],
                           key=lambda s: -s["V_lin"])
        usefuls = sorted([s for s in surfaces
                           if (s.get('role_for') or {}).get(p) == 'useful'
                           and not s.get('deprecated')
                           and not s.get('redundant_with')],
                           key=lambda s: -s["V_lin"])
        frictions_p = [s for s in surfaces
                        if (s.get('role_for') or {}).get(p) == 'friction'
                        and not s.get('deprecated')
                        and not s.get('redundant_with')]
        harmfuls_p = [s for s in surfaces
                       if (s.get('role_for') or {}).get(p) == 'harmful'
                       and not s.get('deprecated')
                       and not s.get('redundant_with')]

        out.append(f"**Essential** — {p} cannot function without these "
                   f"({len(essentials)} surfaces):")
        out.append("")
        if essentials:
            out.append(_list_surfaces(essentials))
        else:
            out.append("_(none)_")
        out.append("")

        out.append(f"**Heavy** — used often in their daily workflow "
                   f"({len(heavies)} surfaces):")
        out.append("")
        if heavies:
            out.append(_list_surfaces(heavies))
        else:
            out.append("_(none)_")
        out.append("")

        out.append(f"**Friction** — visible but unused; "
                   f"**HIDE_FOR {p}** ({len(frictions_p)} surfaces):")
        out.append("")
        if frictions_p:
            out.append(_list_surfaces(frictions_p))
        else:
            out.append("_(none)_")
        out.append("")

        out.append(f"**Harmful** — breaks {p}'s mental model; "
                   f"**REFRAME_FOR {p}** ({len(harmfuls_p)} surfaces):")
        out.append("")
        if harmfuls_p:
            out.append(_list_surfaces(harmfuls_p))
        else:
            out.append("_(none)_")
        out.append("")

        # Show useful only as a tail summary, not full list
        out.append(f"_(useful: {len(usefuls)} surfaces — not listed; "
                   f"irrelevant: rest)_")
        out.append("")

    # Action recommendations across all surfaces
    out.append("## Recommended actions")
    out.append("")
    action_counts: dict[str, int] = defaultdict(int)
    for s in surfaces:
        action_counts[s["action"]] += 1
    rows = sorted(action_counts.items(),
                   key=lambda kv: -kv[1])
    out.append(render_md_table([[k, v, _action_description(k)] for k, v in rows],
        ["action", "count", "meaning"]))
    out.append("")

    # The actionable cut/hide/reframe lists
    out.append("### Cut candidates")
    out.append("")
    cuts = [s for s in surfaces if s["action"] in ("CUT_CANDIDATE", "REDUNDANT", "DEPRECATED")]
    if cuts:
        rows = [[s["id"], s["name"], s.get("location", ""), s["action"],
                 _short_notes(s)] for s in sorted(cuts, key=lambda s: (s["action"], s["id"]))]
        out.append(render_md_table(rows,
            ["id", "name", "location", "action", "notes"]))
    else:
        out.append("_(none)_")
    out.append("")

    out.append("### Hide-for actions (persona-aware visibility)")
    out.append("")
    hide_for = [s for s in surfaces
                if any(n.startswith("HIDE_FOR ") for n in s["action_notes"])]
    if hide_for:
        rows = [[s["id"], s["name"], s.get("location", ""), s["action"],
                 _short_notes(s)] for s in sorted(hide_for, key=lambda s: -s["V_lin"])]
        out.append(render_md_table(rows,
            ["id", "name", "location", "primary action", "hide notes"]))
    else:
        out.append("_(none)_")
    out.append("")

    out.append("### Reframe-for actions (vocabulary / mental-model fix)")
    out.append("")
    reframe_for = [s for s in surfaces
                    if any(n.startswith("REFRAME_FOR ") for n in s["action_notes"])]
    if reframe_for:
        rows = [[s["id"], s["name"], s.get("location", ""), s["action"],
                 _short_notes(s)] for s in sorted(reframe_for, key=lambda s: -s["V_lin"])]
        out.append(render_md_table(rows,
            ["id", "name", "location", "primary action", "reframe notes"]))
    else:
        out.append("_(none)_")
    out.append("")

    # Full table — every surface with its action and per-persona roles
    out.append("## Full scored inventory")
    out.append("")
    out.append("All surfaces with V(S), action recommendation, and "
               "per-persona role. Sorted by V_lin descending.")
    out.append("")
    surfaces_sorted = sorted(surfaces, key=lambda s: -s["V_lin"])
    rows = []
    for s in surfaces_sorted:
        role_for = s.get("role_for") or {}
        role_str = " / ".join(
            f"{p}:{_short_role(role_for.get(p, 'irrelevant'))}"
            for p in persona_priority)
        rows.append([s["id"], s["name"], s.get("location", ""),
                      role_str, s["V_lin"], s["V_exp"],
                      s["action"], " · ".join(s["action_notes"]) or "—"])
    out.append(render_md_table(rows,
        ["id", "name", "location",
         "role_for (P1/P2/P3/P4)",
         "V_lin", "V_exp", "action", "overlay notes"]))
    out.append("")

    out.append("---")
    out.append("")
    out.append("**Methodology limits**: role_for assignments are "
               "judgments from inventory + persona reasoning, grounded "
               "in Sofia's own dogfooding (P3-agent surfaces) + Juan's "
               "stated reads (P3-human anchors: init essential, "
               "workspace add-worktree heavy, roles friction). P1/P2 "
               "reads are hypothesis-shaped per their persona status. "
               "Treat as a structured prioritization aid; revise the "
               "YAML when reads turn out wrong.")

    return "\n".join(out) + "\n"


def _list_surfaces(surfaces: list[dict[str, Any]]) -> str:
    lines = []
    for s in surfaces:
        loc = s.get("location", "")
        lines.append(f"- `{s['id']}` — {s['name']} ({loc})")
    return "\n".join(lines)


def _role_description(role: str) -> str:
    return {
        "essential": "persona cannot function without it",
        "heavy": "core to daily workflow",
        "useful": "valued occasionally",
        "irrelevant": "persona does not see / use",
        "friction": "visible but unused; cognitive load (HIDE_FOR)",
        "harmful": "breaks mental model (REFRAME_FOR)",
    }[role]


def _action_description(action: str) -> str:
    return {
        "NEVER_CUT": "essential for ≥1 persona; preserve",
        "FOCUS": "heavy/essential for a priority persona; polish/promote",
        "KEEP": "heavy for a non-priority persona only; keep but don't promote",
        "USEFUL_PRIORITY": "useful for a priority persona",
        "USEFUL": "useful for a non-priority persona only",
        "REQUIRED_INFRA": "low value, no positive role, but required",
        "CUT_CANDIDATE": "no positive role for any persona; cut target",
        "REDUNDANT": "duplicates another surface",
        "DEPRECATED": "explicit flag; cut",
    }.get(action, "")


def _short_role(role: str) -> str:
    return {"essential": "ess", "heavy": "HVY", "useful": "use",
             "irrelevant": "—", "friction": "FRX", "harmful": "HRM"}.get(role, role)


def _short_notes(s: dict[str, Any]) -> str:
    return " · ".join(s["action_notes"]) or "—"


def main():
    personas_doc, surfaces_doc = load_data()
    surfaces = list(surfaces_doc["surfaces"])
    report = build_report(personas_doc, surfaces)
    REPORT_FILE.write_text(report)
    print(f"Wrote {REPORT_FILE}")
    print(f"Scored {len(surfaces)} surfaces.")


if __name__ == "__main__":
    main()
