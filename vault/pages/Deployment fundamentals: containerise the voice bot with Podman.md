title:: Deployment fundamentals: containerise the voice bot with Podman
type:: practice
state:: collected
ingested:: [[2026-11-18]]
note:: Came up while building the case for image-based deploys to my lead. I am an application developer and want to understand what makes a deployment setup good, using our own deploy (git reset + uv sync on live boxes) as the worked example.
domain:: [[Systems]]
topic:: [[Software Engineering]]
complexity:: intermediate
size:: deep-dive
concepts:: [[Build Artifacts]], [[Immutable Infrastructure]], [[Containers]], [[Zero-Downtime Deploys]], [[Dev-Prod Parity]], [[Infrastructure as Code]]
prerequisites:: [[Linux Basics]], [[Twelve-Factor App]]

## Summary
Learn what makes a deployment setup good by judging our own against seven questions: what is the artifact, can a server be recreated, is config separate from code, does a rollout stay safe, how do I roll back, does staging match prod, and can I tell what runs where. Then build a container image of the voice bot and run it locally under Podman to meet the host assumptions first-hand (log paths, the recordings directory, the git commit lookup, host networking).

## Key Takeaways
- Containers answer the artifact, recreate-a-server, rollback and staging-parity questions; they do nothing for draining or config
- Our deploy ships a git commit and builds on each prod box; an image moves that build to CI once
- Podman runs each container as a child of systemd, so the existing gunicorn@ units can stay

## Checklist
- [ ] Read run_deploy.py end to end and write down what one prod deploy does, step by step
- [ ] Score our deploy against the seven questions (artifact, recreate, config, rollout, rollback, parity, what runs where)
- [ ] Write a Containerfile for the bot and build it locally
- [ ] Run one gunicorn worker from the image under Podman with host networking and take a test call
- [ ] List every host assumption that broke (logs, /storage/recordings, /storage/models, git commit lookup)
- [ ] Run it as a systemd unit with Quadlet and compare with gunicorn@.service
- [ ] Time a rollback: switch to the previous image tag and restart
