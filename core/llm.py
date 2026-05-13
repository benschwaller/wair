import os
from pathlib import Path
from datetime import datetime
from openai import AsyncOpenAI

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

PROMPTS_DIR = Path("prompts")

async def ask_llm(prompt, model="openrouter/free", agent="unknown"):
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an HPC intelligence analyst.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.4,
    )

    result = response.choices[0].message.content

    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
    prompt_file = PROMPTS_DIR / f"{timestamp}_{agent}.md"
    
    prompt_file.write_text(f"""---
agent: {agent}
model: {model}
timestamp: {datetime.utcnow().isoformat()}
---

# Prompt

{prompt}

# Response

{result}
""")

    return result