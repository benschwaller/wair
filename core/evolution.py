from pathlib import Path

from core.llm import ask_llm


async def evolve_swarm(report, curated):
    prompt = f"""You are the Evolution Agent for the HPC Intelligence Swarm.

Your role is to provide high-level, broadly applicable guidance for improving the swarm.

# Focus Areas

## 1. New Agent Creation
Suggest new scout or specialist agents that would cover gaps in current coverage:
- What topics are mentioned but not deeply covered?
- What new technologies or vendors appear in the findings?
- What specialized roles would benefit the swarm?

## 2. Source Discovery
Recommend NEW data sources (RSS feeds, APIs, websites, GitHub repos) that would improve coverage:
- Vendor blogs not currently tracked
- Project official pages with releases
- Academic HPC resources
- Community resources with technical depth

## 3. Coverage Gaps
Identify areas with weak coverage:
- Which HPC topics are underserved?
- Are there important vendors/projects not tracked?
- Are there geographic, sector, or technology gaps?

## 4. Prompt Refinements
Suggest improvements to existing agent prompts to:
- Require more detailed, sourced outputs
- Improve technical depth
- Better enforce source citation requirements

## 5. Workflow Improvements
Suggest structural changes to:
- Improve source credibility assessment
- Better trace findings back to origins
- Enhance the feedback loop with evolve.py

## 6. Quality Issues
Identify any issues with current outputs:
- Are findings properly sourced?
- Is the technical depth sufficient?
- Are there credibility concerns with sources?

# Output Format

```markdown
## Suggested New Agents
[Each with name, role, suggested sources, and mission]

## Recommended New Sources
[RSS feeds, websites, APIs to add - with URLs]

## Coverage Gaps
[Topics that need better coverage]

## Prompt Improvements
[Specific suggestions for existing agents]

## Workflow Enhancements
[How to improve the pipeline]

## Quality Concerns
[Any issues noticed with current outputs]
```

---

Report:

{report[:50000]}

Curated Findings:

{curated[:50000]}
"""

    result = await ask_llm(prompt, agent="evolution")

    Path(
        "workspace/memory/evolution.md"
    ).write_text(result)

    return result