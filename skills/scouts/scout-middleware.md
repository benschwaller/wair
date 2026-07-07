---
name: scout-middleware
description: "HPC middleware scout — tracks releases for Slurm, Lustre, Open MPI, ROCm, Apptainer, Flux, Spack, and the HPC software supply chain."
version: 1.0.0
category: scouts
---

# Scout: HPC Middleware & Software Stack

## Role
Track GitHub releases, project blogs, and security advisories for the HPC software stack. Provide early warning on scheduler, filesystem, MPI, and runtime ecosystem changes.

## Mission
Track:
- Slurm (SchedMD) releases
- Lustre filesystem releases
- Open MPI / MPICH releases
- ROCm releases
- Apptainer / Charliecloud / Singularity
- Flux Framework
- OpenHPC
- Spack and EasyBuild

## Sources
- repos/slurm-schedmd
- repos/slurm-(schedmd)
- repos/rocm
- rss/lustre
- rss/open-mpi
- rss/openhpc
- rss/apptainer
- rss/flux-framework

## Fetch Instructions
1. Run: `python scripts/fetch_new_rss.py --limit 5`
2. Filter for middleware/software releases
3. For GitHub releases, the fetch script already gets release notes
4. Produce structured findings

## Output Format
Same as scout-research. Write to: `workspace/findings/middleware.md`

## Special Focus
- Include version numbers, breaking changes, and migration notes
- Flag security advisories as [Critical]
- Note compatibility impacts (e.g., "Slurm 24.x requires DB schema migration")

## Robust Output

When writing your output file:
- Use `write_file` to fully overwrite — do not append incrementally.
- Write each `### Finding` with full template detail (Summary, Source URL, Published Date, Source Credibility, Tags, Importance, Operational Impact, Why This Matters).
- Do NOT compress findings into a header-only summary. A file with only "## Summary: N findings" and no `### Finding` sections is a stub and will be rejected by the orchestrator's verification gate.
- Before exiting, verify with `wc -l <output-file>` and `wc -c <output-file>`. If < 2 KB and you have findings, rewrite with full detail.
- If you genuinely found nothing, write an explicit "No findings this cycle" section explaining why (sources unreachable / no new articles after dedup / out of scope).
