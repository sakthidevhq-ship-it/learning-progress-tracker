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
