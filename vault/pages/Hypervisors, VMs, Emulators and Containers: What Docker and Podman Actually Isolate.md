title:: Hypervisors, VMs, Emulators and Containers: What Docker and Podman Actually Isolate
type:: article
state:: collected
ingested:: [[2026-10-25]]
note:: Referesh on core topics
domain:: [[Systems]]
topic:: [[Operating Systems]]
complexity:: intermediate
size:: medium
concepts:: [[Virtualization]], [[Hypervisors]], [[Emulation]], [[Linux Namespaces]], [[cgroups]], [[Containers]]
prerequisites:: [[Linux Basics]], [[Virtual Memory]]

## Summary
A refresher topic on the isolation spectrum. Emulators (e.g. QEMU's TCG) translate one instruction set to another in software; type-1 (Xen, ESXi) and hosted (KVM+QEMU, VirtualBox) hypervisors run guest kernels directly on the CPU using hardware virtualization (VT-x/AMD-V, nested page tables), so each VM has its own kernel. Containers (Docker, Podman) share the host kernel and isolate only what kernel namespaces (pid, net, mount, uts, ipc, user, cgroup) and cgroups (CPU/memory/IO limits) present to a process, hardened with seccomp and capabilities; Podman differs mainly in being daemonless and rootless by default.

## Key Takeaways
- Emulation translates instructions; virtualization runs them natively with hardware help
- A VM isolates a whole kernel; a container is a normal process with a restricted view of one shared kernel
- Namespaces control what a process can see, cgroups control how much it can use
- A kernel exploit escapes a container but not a VM, which is why gVisor and Firecracker microVMs exist

## Learnings
- 2026-11-15 · Good deployment starts with the artifact: build it once, test that exact thing, run it everywhere. Our deploy ships a git commit and each prod box rebuilds it (git reset, then an unfrozen uv sync needing GitHub, CodeArtifact, PyPI and S3 mid-deploy), so twelve boxes do twelve untested builds; the 1.15 canary's daily-python crash was a bad host build, not bad code. A container image moves that build to CI once, and Podman keeps our systemd units.
- 2026-11-15 · Pets vs cattle: immutable infrastructure means never changing a running server, only replacing it from a written definition. Our ASG boxes are replaced, not edited, but their AMI is snapshotted off the live primary box, so it carries every manual change ever made there. Config (secrets, URLs, flags) should be the only thing that differs between staging and prod.
- 2026-11-16 · An ASG instance refresh with skip matching on replaces only instances that differ from the launch template version; when the code commit is fetched by user data at boot it isn't part of the template, so the refresh replaces nothing and still reports success. For a code-only rollout turn skip matching off; launch-before-terminate needs max healthy above 100%, and instance warmup must cover the whole boot.
