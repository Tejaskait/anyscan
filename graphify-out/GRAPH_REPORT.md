# Graph Report - anyscan  (2026-10-31)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 93 nodes · 134 edges · 14 communities (10 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13

## God Nodes (most connected - your core abstractions)
1. `steps` - 6 edges
2. `process_video()` - 6 edges
3. `main()` - 6 edges
4. `main()` - 6 edges
5. `AGENTS.md - read this first` - 6 edges
6. `AnyScan` - 6 edges
7. `main()` - 5 edges
8. `sync_progress()` - 5 edges
9. `User profile and goal (context for any AI agent)` - 5 edges
10. `classes` - 4 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `argparse`  [EXTRACTED]
  scripts/extract_frames.py →   _Bridges community 1 → community 0_
- `main()` --calls--> `argparse`  [EXTRACTED]
  scripts/steps.py →   _Bridges community 2 → community 0_

## Import Cycles
- None detected.

## Communities (14 total, 4 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.21
Nodes (5): main(), main(), main(), main(), main()

### Community 1 - "Community 1"
Cohesion: 0.36
Nodes (3): dhash(), main(), process_video()

### Community 2 - "Community 2"
Cohesion: 0.46
Nodes (4): current(), main(), render(), sync_progress()

### Community 3 - "Community 3"
Cohesion: 0.25
Nodes (7): project, steps, id, note, status, title, where

### Community 4 - "Community 4"
Cohesion: 0.29
Nodes (6): AGENTS.md - read this first, Conventions, Hard rules, Orientation order (do this before anything else), Project, Resuming work

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (6): AnyScan, Handing off to an AI agent, Rules that protect the results, Setup, Steps (details in STEPS.yaml), Where am I?

### Community 6 - "Community 6"
Cohesion: 0.33
Nodes (5): Goal, The project: AnyScan, User preferences, User profile and goal (context for any AI agent), Who the user is

### Community 7 - "Community 7"
Cohesion: 0.40
Nodes (4): classes, coco, name, prompts

### Community 8 - "Community 8"
Cohesion: 0.40
Nodes (4): Decisions (see docs/context/01_decisions.md for the full list), Log, Open questions, PROGRESS

### Community 9 - "Community 9"
Cohesion: 0.50
Nodes (3): Failure patterns, Limitations, Results (only measured values)

## Knowledge Gaps
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `main()` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.008) - this node is a cross-community bridge._