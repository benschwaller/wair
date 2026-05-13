from pathlib import Path
import frontmatter

from core.models import Agent


def load_markdown(path):
    post = frontmatter.load(path)
    return {
        "metadata": post.metadata,
        "content": post.content,
    }


def load_agents(directory):
    agents = []

    for path in Path(directory).glob("*.md"):
        if path.name == "agents.md":
            continue

        data = load_markdown(path)
        meta = data["metadata"]

        agent = Agent(
            name=meta.get("name", path.stem),
            role=meta.get("role", "unknown"),
            model=meta.get("model", "openrouter/free"),
            mission=data["content"],
            skills=meta.get("skills", []),
            sources=meta.get("sources", []),
            output=meta.get("output", ""),
        )

        agents.append(agent)

    return agents


def load_skills(directory):
    skills = {}

    for path in Path(directory).glob("*.md"):
        skills[path.stem] = path.read_text()

    return skills


def load_sources(directory):
    sources = {}

    for path in Path(directory).glob("*.md"):
        sources[path.stem] = path.read_text()

    return sources