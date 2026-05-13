from pathlib import Path
import yaml
import frontmatter

from core.models import Agent

CONFIG_PATH = Path('config/models.yaml')


def load_model_overrides():
    if not CONFIG_PATH.is_file():
        return {}
    with CONFIG_PATH.open() as f:
        cfg = yaml.safe_load(f)
    return cfg.get('agents', {})


def load_markdown(path):
    post = frontmatter.load(path)
    return {
        "metadata": post.metadata,
        "content": post.content,
    }


def load_agents(directory):
    agents = []
    overrides = load_model_overrides()

    for path in Path(directory).glob("*.md"):
        if path.name == "agents.md":
            continue

        data = load_markdown(path)
        meta = data["metadata"]

        model = overrides.get(path.stem, meta.get("model", "openrouter/free"))

        agent = Agent(
            name=meta.get("name", path.stem),
            role=meta.get("role", "unknown"),
            model=model,
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