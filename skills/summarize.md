# Skill: summarize

When summarizing HPC content:

## Requirements

- **ALWAYS include source URL** in format: `[Source Name](URL)`
- **Include publication date** when available
- **Include credibility indicator**: [High Credibility], [Medium Credibility], or [Low Credibility]
- **Focus on operational impact**: What does this mean for HPC administrators?
- **Avoid marketing language**: Use technical, precise language
- **Identify breaking changes**: Flag any changes that require action

## Output Structure

```markdown
## [Article Title]

**Source**: [Source Name](URL) | **Date**: [Date] | **Credibility**: [High/Medium/Low]

**Summary**:
[2-3 paragraphs covering the key technical details, not just headlines]

**Operational Impact**:
[What this means for HPC administrators - specific actions or considerations]

**Key Technical Details**:
- [specific version numbers, configurations, metrics]
- [specific timeline or dates mentioned]
- [specific tools or software mentioned]

**Tags**: [scheduler] [orchestration] [GPU] [networking] [etc.]
```

## Quality Standards

1. Never leave a finding unsourced - if no URL available, mark as `[Unverified]`
2. Never just rehash headlines - include technical depth
3. Always explain WHY HPC admins should care
4. Flag any claims that need further verification with `[Verify]`