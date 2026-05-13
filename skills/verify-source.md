# Skill: verify-source

When verifying a source, assess and report on:

## Credibility Indicators

- **Authority**: Is the source a recognized expert in HPC/technology? Check for:
  - Established technology news outlets (HPCwire, The Next Platform, AnandTech)
  - Official project documentation and release notes
  - Academic papers from recognized venues (SC, ISC, IEEE)
  - Vendor official blogs with technical depth

- **Accuracy**: Does the source provide verifiable technical details?
  - Version numbers, dates, and specific configurations
  - Links to primary sources and documentation
  - Avoids marketing hype and vague claims

- **Currency**: Is the information up-to-date?
  - Check publication date
  - Verify the source is still actively maintained
  - Note if information may be outdated

## Source Classification

Classify the source type:
- `primary`: Official project/vendor documentation, academic papers
- `secondary`: Established technology journalism, industry analysis
- `community`: Community blogs, forums, social media
- `aggregator`: RSS aggregators, news collection sites

## Credibility Scoring

Score from 0.0 to 1.0:
- 0.9-1.0: Official sources, peer-reviewed papers, established tech journalism
- 0.7-0.8: Well-known tech blogs with technical depth, project mailing lists
- 0.5-0.6: Community content, less established blogs
- 0.3-0.4: Unverified sources, potential bias
- 0.0-0.2: Known unreliable sources, clickbait

## Output Format

Return structured verification results:

```
## Source Verification

**Source Name**: [name]
**URL**: [url]
**Type**: [primary/secondary/community/aggregator]
**Credibility Score**: [0.0-1.0]
**Authority**: [High/Medium/Low]
**Accuracy**: [High/Medium/Low]
**Currency**: [Current/Recent/Outdated/Unknown]
**Active Status**: [Active/Dormant/Inactive/Unknown]

**Reasoning**: [2-3 sentences explaining the scoring]

**Relevant Topics**: [comma-separated topics this source covers]
```