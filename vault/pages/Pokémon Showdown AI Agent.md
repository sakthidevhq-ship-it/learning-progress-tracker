title:: Pokémon Showdown AI Agent
type:: project
state:: collected
ingested:: [[2026-10-03]]
note:: A fun one: an agent that does everything before and during a battle, plus posts on what I learn building it.
domain:: [[Game AI]]
topic:: [[Imperfect Information Games]]
complexity:: advanced
size:: deep-dive
concepts:: [[Opponent Modeling]], [[Game State Representation]], [[Action Space Design]], [[Game Theory Basics]], [[Reinforcement Learning Basics]], [[Agent Architecture]]
prerequisites:: [[Python]], [[Game Theory Basics]]

## Summary
Build an agent that plays Pokémon Showdown end to end. Before the game: read the current meta, build a team around coverage and a strategy (ability and move synergy, IV/EV spreads). During the game: track what's known about the opponent's team and pick moves under uncertainty. Write posts on the learnings and implementation along the way.

## Checklist
- [ ] Before the game: figure out the current meta and the strategies people run (usage stats, sample teams)
- [ ] Team building: coverage plus a game plan
- [ ] Team building: ability synergy and move synergy
- [ ] Team building: IV/EV spreads
- [ ] Connect a bot to Showdown and play full battles
- [ ] During the game: track known info about the opponent (revealed mons, moves, items, likely sets)
- [ ] During the game: pick moves from current known info (damage calcs, switch predictions, search)
- [ ] Post: learnings on meta and team building
- [ ] Post: implementation details of the battle agent

## Notes
Everything before and during a game.

Before: figure out the current meta and the strategies people run. Build a team around coverage and strategy: ability synergy, move synergy, IV/EV distribution.

During: which move to pick based on the info known so far.

Write posts and blogs on the learnings and implementation details.

Related in the library: Pokemon TCG Agent (LLM agentic approach); Pluribus, Suphx and Noam Brown's talks for imperfect-information play.
