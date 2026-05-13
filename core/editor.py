from datetime import datetime

from core.llm import ask_llm


async def generate_report(curated, discoveries):
    today = datetime.utcnow().strftime("%Y-%m-%d")

    prompt = f"""
You are the Editor Agent.

Generate a polished HPC intelligence report.

Structure:

# HPC Weekly Report

Date: {today}

## Major Themes

## Important Updates

## Emerging Topics

## Suggested New Agents

Use concise language.
Focus on operational relevance.
Avoid marketing tone.

Curated Findings:

{curated[:100000]}

Discoveries:

{discoveries[:50000]}
"""

    return await ask_llm(prompt)