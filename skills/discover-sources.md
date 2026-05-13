# Skill: discover-sources

When discovering new sources for HPC intelligence:

## Source Types to Discover

### RSS Feeds
- HPC vendor blogs (Dell, HPE, NVIDIA, AMD, Intel)
- Project release feeds (Slurm, PBS, Lustre, GPFS)
- Technology news aggregators covering HPC
- University research group blogs

### API Sources
- GitHub APIs for HPC projects
- Package repository APIs (PyPI, conda)
- Cloud provider API documentation

### Web Sources
- Official documentation sites
- Academic institution pages
- Conference proceedings pages

## Discovery Process

1. **Analyze gaps**: What topics are mentioned but poorly covered?
2. **Trace upstream**: If a vendor is mentioned, find their official blog/RSS
3. **Follow citations**: Academic papers cite project pages
4. **Check aggregators**: Phoronix, HPCwire often link to primary sources
5. **Search GitHub**: Find active HPC-related repositories

## Source Quality Criteria

For each potential source, verify:
- **Relevance**: Does it cover HPC, cluster computing, or AI infrastructure?
- **Quality**: Is content technical and detailed?
- **Freshness**: Is it actively maintained?
- **Accessibility**: Is it available via RSS/API/public website?

## Output Format

For each discovered source, provide:

```
## Discovered Source

**Name**: [source name]
**URL**: [URL]
**Type**: [rss/api/web]
**Topics Covered**: [topic1, topic2, ...]
**Credibility Estimate**: [High/Medium/Low]
**Why Useful**: [1-2 sentences on relevance to HPC]
**Suggested Agent**: [which agent should use this source]
```

## Coverage Analysis

Identify gaps in current coverage:
- Which HPC topics are underserved?
- Are there important vendors/projects not being tracked?
- Are there geographic or sector-specific gaps?

Return a list of suggested new sources ranked by potential value.