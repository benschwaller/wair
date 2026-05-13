import os
from pathlib import Path
from datetime import datetime
from openai import AsyncOpenAI
import asyncio

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

PROMPTS_DIR = Path("prompts")


async def ask_llm(prompt, model="openrouter/free", agent="unknown", max_retries=3):
    last_error = None

    for attempt in range(max_retries):
        try:
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

            if response is None:
                last_error = "Response is None"
                await asyncio.sleep(1)
                continue

            if not hasattr(response, 'choices') or not response.choices:
                last_error = "Response has no choices"
                await asyncio.sleep(1)
                continue

            choice = response.choices[0]
            if not hasattr(choice, 'message') or choice.message is None:
                last_error = "Choice message is None"
                await asyncio.sleep(1)
                continue

            result = choice.message.content
            if result is None:
                last_error = "Message content is None"
                await asyncio.sleep(1)
                continue

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

        except Exception as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)
            continue

    print(f"WARNING: LLM call failed after {max_retries} attempts: {last_error}")
    return f"[Error: Could not get response from LLM - {last_error}]"