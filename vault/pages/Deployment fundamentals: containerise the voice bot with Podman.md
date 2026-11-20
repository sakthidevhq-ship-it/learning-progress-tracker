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

## Learnings
- 2026-11-18 · An ALB listener checks its rules first, lowest priority number first, and the first match wins; the default action has no conditions and applies only when no rule matched. Our canary split lives in the voicebot-lb :443 default action as a weighted forward (prod/canary 95/5, then 90/10, now 100/0), while testingprod is a separate host-header rule at priority 6 that is managed in the console, not Terraform.
- 2026-11-20 · Python wheels can depend on OS libraries that pip and uv never install: LightGBM needs libgomp.so.1 (Ubuntu's libgomp1), so two servers booted from a new image without it couldn't load the smart LLM router and silently fell back to premium-only. The image bake has to install a package's system dependencies, and a fallback that hides the failure should still raise an alert.
- 2026-11-20 · An ASG is attached to a target group from the ASG side (Integrations → Load balancing); the target group's Register targets screen only takes single instances or IPs. Once attached, the ASG registers and deregisters its instances itself, so hand-registered instances leave dead targets behind. Target type, protocol, port and VPC are fixed when a target group is created; only health checks can be edited.
