# Consolidation plan — one canonical Velvet Knowledge Hub

- Author: CaptainQ (Q-Submarine), for the Commander
- Date: 2026-07-13
- Status: approved in direction (periscope review passed, "proceed with amendments")
- Purpose: a self-contained plan that can be executed later and still run well. Anyone picking this up cold — including a future session with no memory of this conversation — should be able to act from this document alone.

---

## 0. One-line decision

Make **`knowledge-hub`** the single canonical site. Harvest the best assets out of the other two repos first, then archive them (archive, never delete).

---

## 1. Why we are here (read this first)

Three repositories were built for the same goal, each a different architectural bet:

| Repo | Last worked | Architecture | State | Character |
|---|---|---|---|---|
| `wkdjk/Deer-velvet-knowledge-hub` | 2026-07-06 | Google Sheets + Apps Script + Looker Studio (no-code) | Sheet installed, real data flowing, dashboard being built | Best thinking. Strongest data model and operating discipline. Looker gives poor visual control |
| `wkdjk/velvet-knowledge-hub` | 2026-07-11 | Python build + sqlite + Google Sheets + Naver news + AI classification + 79 tests | Deployed, most features | Heaviest and most complex. Not maintainable by a non-developer. This is the complexity the v1 requirements told us to strip |
| `wkdjk/knowledge-hub` | 2026-07-12 (newest) | Plain HTML + inline SVG charts (no libraries) + CSV files + GitHub Pages | **Deployed, 6/6 builds green, real data, 5 screens complete** | Simplest, the only one that works, and the only one that matches the written v1 requirements |

**The real problem was never a missing feature. It was fragmentation.** Each restart chased "the best possible outcome" by adopting a *different architecture*, so effort scattered across three incompatible bets instead of compounding on one. Three ships each sailed half a route; none reached port.

**The fix is not to build more. It is to commit to one line and remove the optionality.**

---

## 2. Guiding principles (the anti-relapse rules)

These exist because the failure mode was a habit, not a repo. Changing the repo without changing the habit lets it recur.

1. **Single canonical line.** `knowledge-hub` is the only site. No new repository, no new architecture, is started for this project. If a fourth idea appears, it becomes a note in this plan — not a new repo.
2. **Features ride on top of CSV, never underneath it.** The site's contract is "a non-developer updates it by replacing CSV files." Any new capability must preserve that. If a feature needs a build system, sqlite, or a service the Commander cannot personally operate, it is Phase 2+ and stays *off the critical path*.
3. **Done means seen, not deployed.** A green GitHub Pages build is not completion. Completion is the deployed URL inspected top-to-bottom, on desktop and phone, with no blank screen and no broken chart.
4. **Archive, never delete.** The other two repos hold tested code and hard-won thinking. They are set to archived/read-only, not removed.
5. **Simplicity is the deliverable.** When in doubt, remove. The v1 requirements doc (in `knowledge-hub/CLAUDE.md`) is the source of truth for scope; re-read it before any work.

---

## 3. What we keep, archive, and harvest

### Keep (the flagship)
`wkdjk/knowledge-hub` — as-is. It already has the five screens the requirements ask for:
1. Summary + three stat cards
2. Yearly import-volume chart (single country filter, SVG, trend line)
3. News highlights (last 90 days)
4. Quarterly report archive
5. Sources & references

### Harvest BEFORE archiving (this is a required step, not optional)

The periscope review's top failure mode was archiving the other repos *before* extracting their value, then rebuilding it from scratch months later. To close that, the harvest below must be done, or explicitly logged as "consciously skipped", before either repo is archived.

**From `Deer-velvet-knowledge-hub` (the thinking):**
- [ ] `docs/VKH-design.md` — the fullest design document (data schemas, operating routine, phased build path). Copy into `knowledge-hub/docs/`.
- [ ] `docs/STATUS.md` — the cross-version comparison and the "escape cost / failure modes" analysis.
- [ ] The **39-company Korean↔English name-alias table** (seeded in `apps-script/setup.gs` / `seedCompanies`). This is real curated data that would be expensive to rebuild. Extract to a CSV under `knowledge-hub/data/` (e.g. `companies.csv`) even if unused yet.
- [ ] The **long-format `stats_raw` data model** (source / period / hs_code / metric / value / unit / src_file / country) and the **news copyright rule** (title + link + own summary only; never store or transmit article full text). Record both as short notes in `knowledge-hub/docs/`.

**From `velvet-knowledge-hub` (the machinery, for Phase 2):**
- [ ] The Naver news collection + AI classification logic (`scripts/collect_naver.py`, `scripts/classify_articles.py`) — kept as a reference for Phase 2 automation. Do **not** wire it into the flagship now.
- [ ] `OPERATOR_GUIDE.md` — mine it for any non-developer instructions worth folding into `knowledge-hub/data/README.md`.
- [ ] The QIA / Stats NZ converter logic (`scripts/convert_*.py` already exist in knowledge-hub too — reconcile, keep the simpler one).

### Archive (after harvest)
- [ ] Set `wkdjk/Deer-velvet-knowledge-hub` to archived (read-only) on GitHub.
- [ ] Set `wkdjk/velvet-knowledge-hub` to archived (read-only) on GitHub.
- [ ] Add a one-line note to each repo's README: "Archived 2026-__. Superseded by wkdjk/knowledge-hub. See its docs/consolidation-plan.md." (Add the README note in a final commit *before* flipping the archive switch, since archived repos are read-only.)

---

## 4. Phased plan

Mirrors the staging already written into the v1 requirements. Each phase has an acceptance gate that must pass before the next begins.

### Phase 1 — stabilise and trust the flagship (do this first)
Goal: the site is correct, complete, and visibly solid on the real URL.

1. **Eye-inspection gate.** Open the deployed site (`https://wkdjk.github.io/knowledge-hub/`). Scroll top to bottom on desktop and on a phone-width screen. Confirm: no blank screen, no broken/half-drawn chart, no table clipped off-screen. Record the result. *This is the definition of done for the whole phase.*
2. **Close the data gap.** The latest commit reflected QIA (annual-only) and Stats NZ, and its own message flagged that monthly Korean import data needs the separate per-year archive. Decide the honest position for each stat card and chart: show the freshest reliable number, and label its period plainly. No stale or empty core numbers on the first screen.
3. **Harvest step from section 3** (at least the Deer-velvet thinking + company table), so nothing is lost before archiving.
4. **Non-developer update path.** Confirm `data/README.md` genuinely lets the Commander swap a CSV and see the change. Fix it if not.

**Phase 1 gate:** deployed URL passes the eye-inspection on desktop + phone, core numbers are current and correctly labelled, and the Commander can update a CSV unaided.

### Phase 2 — news automation only (after Phase 1 is stable)
- Bring across *only* the news auto-collection, as a separate optional job that writes into the existing `data/news.csv` shape. It must fail safe: if the automation breaks, the site still renders from the last CSV. Reference implementation: `velvet-knowledge-hub/scripts/collect_naver.py`.
- Keep it off the critical path — a broken collector must never blank the site.

### Phase 3 — statistics auto-refresh (last)
- Only after Phase 2 has run reliably for a full cycle. Automate the import/export CSV refresh, same fail-safe rule: automation feeds the CSV; the site only ever reads the CSV.

---

## 5. Open decisions for the Commander (decide before/at execution)

1. **Custom domain?** Stay on `wkdjk.github.io/knowledge-hub/`, or point a real domain at it? (Affects how the site is shared with DINZ / partners.)
2. **Archive timing.** Archive the other two repos as part of Phase 1, or leave them dormant-but-live until Phase 2 proves the news pipeline can be lifted out? (Recommended: archive after the harvest checklist is done, which can be within Phase 1.)
3. **Data honesty line.** For the monthly-Korean-import gap: prefer an older-but-real number with a clear "as of" label, or omit that card until fresh data exists? (Recommended: show real + labelled; never show empty on the first screen.)

---

## 6. How to resume this later (cold-start instructions)

If you are picking this up with no prior context:
1. Read `knowledge-hub/CLAUDE.md` — the v1 requirements. That is the scope contract.
2. Read this file top to bottom.
3. Start at Phase 1, step 1 (the eye-inspection). Do not start building features.
4. Honour the section 2 principles, especially: no new repo, features ride on CSV, done means seen.

The single most important sentence in this plan: **the problem was fragmentation, and the cure is to keep exactly one line alive and let work compound on it.**
