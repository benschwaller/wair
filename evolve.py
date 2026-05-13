#!/usr/bin/env python3
"""
evolve.py - HPC Swarm Evolution Processor

Processes evolution.md suggestions and applies changes to agents, skills, and sources.
Supports interactive and auto modes with full preview before changes.
"""

import re
import sys
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

try:
    import questionary
    QUESTIONARY_AVAILABLE = True
except ImportError:
    QUESTIONARY_AVAILABLE = False

try:
    import frontmatter
    FRONTMATTER_AVAILABLE = True
except ImportError:
    FRONTMATTER_AVAILABLE = False

EVOLUTION_PATH = Path("workspace/memory/evolution.md")
AGENTS_DIR = Path("agents")
SKILLS_DIR = Path("skills")
SOURCES_DIR = Path("sources")
BACKUP_DIR = AGENTS_DIR / ".backups"
CONFIRMATION_THRESHOLD = 0.5


@dataclass
class AgentSuggestion:
    name: str
    functionality: str
    rationale: str
    confidence: float = 0.0
    suggested_skills: List[str] = field(default_factory=list)
    suggested_sources: List[str] = field(default_factory=list)
    match_path: Optional[Path] = None


@dataclass
class SourceSuggestion:
    title: str
    url: str
    description: str
    source_type: str  # rss, api, repo
    already_exists: bool = False


@dataclass
class SkillSuggestion:
    name: str
    description: str
    already_exists: bool = False


@dataclass
class GapSuggestion:
    name: str
    description: str
    suggested_agent: Optional[str] = None


@dataclass
class WorkflowSuggestion:
    title: str
    description: str


@dataclass
class EvolutionSections:
    agents: List[AgentSuggestion] = field(default_factory=list)
    sources: List[SourceSuggestion] = field(default_factory=list)
    skills: List[SkillSuggestion] = field(default_factory=list)
    gaps: List[GapSuggestion] = field(default_factory=list)
    workflows: List[WorkflowSuggestion] = field(default_factory=list)
    prompts: List[Dict[str, str]] = field(default_factory=list)


class EvolutionParser:
    """Parse evolution.md with flexible section detection."""

    SECTION_PATTERNS = {
        "agents": [r"##\s*(?:New\s+)?Agents?", r"##\s*New\s+Agent", r"##\s*Suggested\s+New\s+Agents?"],
        "prompts": [r"##\s*Prompt\s+(?:Ideas?|Templates?)"],
        "sources": [r"##\s*(?:Source\s+Additions?|Recommended\s+New\s+Sources?)", r"##\s*New\s+Sources"],
        "gaps": [r"##\s*Coverage\s+Gaps?"],
        "workflows": [r"##\s*Workflow\s+Improvements?"],
    }

    def parse(self, content: str) -> EvolutionSections:
        lines = content.split('\n')
        sections = EvolutionSections()

        current_section = None
        section_lines = []
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            for sec_name, patterns in self.SECTION_PATTERNS.items():
                for pattern in patterns:
                    if re.match(pattern, line, re.IGNORECASE):
                        if current_section and section_lines:
                            self._process_section(current_section, section_lines, sections)
                        current_section = sec_name
                        section_lines = []
                        break
                else:
                    continue
                break
            else:
                if current_section:
                    section_lines.append(line)

            i += 1

        if current_section and section_lines:
            self._process_section(current_section, section_lines, sections)

        return sections

    def _process_section(self, section_type: str, lines: List[str], sections: EvolutionSections):
        if section_type == "agents":
            self._parse_agents(lines, sections)
        elif section_type == "sources":
            self._parse_sources(lines, sections)
        elif section_type == "gaps":
            self._parse_gaps(lines, sections)
        elif section_type == "workflows":
            self._parse_workflows(lines, sections)
        elif section_type == "prompts":
            self._parse_prompts(lines, sections)

    def _parse_agents(self, lines: List[str], sections: EvolutionSections):
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            name_match = re.search(r'-\s*\*\*([^*]+)\*\*', line)
            if name_match:
                name = name_match.group(1).strip()
                functionality = ""
                rationale = ""

                j = i + 1
                while j < len(lines) and j < i + 15:
                    next_line = lines[j].strip()

                    if not next_line:
                        j += 1
                        continue

                    if next_line.startswith("- Mission:"):
                        parts = next_line.split(":", 1)
                        if len(parts) > 1:
                            rationale = parts[1].strip().rstrip(".")
                        j += 1
                        continue

                    if next_line.startswith("- ") and not next_line.startswith("- **"):
                        if not functionality:
                            functionality = next_line[2:].strip().rstrip(".")
                        j += 1
                        continue

                    if next_line.startswith("#"):
                        break

                    if next_line and not next_line.startswith("-") and not next_line.startswith("*"):
                        break

                    j += 1

                if name and (functionality or rationale):
                    sections.agents.append(AgentSuggestion(
                        name=name,
                        functionality=functionality or "Not specified",
                        rationale=rationale or "Not specified"
                    ))
            elif line.startswith("|") and "**" in line:
                table_row_match = re.search(r'\|\s*\*\*([^\|]+)\*\*', line)
                if table_row_match:
                    name = table_row_match.group(1).strip()
                    cells = [c.strip() for c in line.split("|")]
                    if len(cells) >= 3:
                        functionality = cells[2].strip()
                    if len(cells) >= 4:
                        rationale = cells[3].strip() if len(cells) > 3 else ""
                    if name:
                        sections.agents.append(AgentSuggestion(
                            name=name,
                            functionality=functionality or "Not specified",
                            rationale=rationale or "Not specified"
                        ))

            i += 1

    def _parse_sources(self, lines: List[str], sections: EvolutionSections):
        current_sub = None
        current_category = None
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if re.match(r'^###?\s+', line):
                i += 1
                continue

            if line.startswith("|"):
                cells = [c.strip() for c in line.split("|")]
                if len(cells) >= 3:
                    first_cell = cells[1].strip() if len(cells) > 1 else ""
                    second_cell = cells[2].strip() if len(cells) > 2 else ""
                    third_cell = cells[3].strip() if len(cells) > 3 else ""

                    if first_cell.startswith("**"):
                        current_category = first_cell.strip("**")
                        i += 1
                        continue

                    if first_cell == "" and second_cell:
                        title = second_cell
                        url = third_cell if third_cell.startswith("http") else ""
                        desc = third_cell if not third_cell.startswith("http") else (cells[4].strip() if len(cells) > 4 else "")
                        sections.sources.append(SourceSuggestion(
                            title=title,
                            url=url,
                            description=desc,
                            source_type=current_sub or "rss"
                        ))
                    i += 1
                    continue

            if "RSS" in line.upper():
                current_sub = "rss"
            elif "API" in line.upper():
                current_sub = "api"
            elif "REPO" in line.upper():
                current_sub = "repo"
            elif line.startswith("- **") and not current_sub:
                current_sub = "api"

            if line.startswith("- ["):
                link_match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', line)
                if link_match:
                    title = link_match.group(1).strip()
                    url = link_match.group(2).strip()
                    desc = ""
                    if ") -" in line:
                        desc = line.split(") -", 1)[1].strip()
                    elif ")—" in line:
                        desc = line.split(")—", 1)[1].strip()
                    elif "]" in line:
                        rest = line.split("]", 1)[1]
                        if rest.startswith("("):
                            rest = rest.split(")", 1)[1].strip()
                        if rest.startswith("-"):
                            desc = rest[1:].strip()
                        elif rest:
                            desc = rest.strip()

                    sections.sources.append(SourceSuggestion(
                        title=title,
                        url=url,
                        description=desc,
                        source_type=current_sub or "api"
                    ))
            elif line.startswith("- **"):
                title_match = re.search(r'\*\*([^*]+)\*\*', line)
                if title_match:
                    title = title_match.group(1).strip()
                    desc = ""
                    if " -" in line:
                        desc = line.split(" -", 1)[1].strip()
                    elif "(" in line and ")" in line:
                        start = line.find("(")
                        end = line.find(")")
                        if start < end:
                            desc = line[start+1:end].strip()

                    sections.sources.append(SourceSuggestion(
                        title=title,
                        url="",
                        description=desc,
                        source_type=current_sub or "api"
                    ))

            i += 1

    def _parse_gaps(self, lines: List[str], sections: EvolutionSections):
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            gap_match = re.search(r'-\s*\*\*([^*]+):\*\*\s*(.+)', line)
            if gap_match:
                name = gap_match.group(1).strip()
                description = gap_match.group(2).strip()
                sections.gaps.append(GapSuggestion(
                    name=name,
                    description=description
                ))
            elif line.startswith("- **"):
                name_match = re.search(r'\*\*([^*]+)\*\*', line)
                if name_match:
                    name = name_match.group(1).strip()
                    desc = line.split("**", 2)[-1].strip() if "**" in line else ""
                    if desc.startswith(":"):
                        desc = desc[1:].strip()
                    sections.gaps.append(GapSuggestion(
                        name=name,
                        description=desc
                    ))
            elif line.startswith("|") and "|" in line and not re.match(r'\|[\s\-:]+\|', line):
                cells = [c.strip() for c in line.split("|")]
                if len(cells) >= 2 and cells[1] and cells[1] != "Gap":
                    first_cell_lower = cells[1].lower()
                    if first_cell_lower in ("enhancement", "issue", "recommendation"):
                        continue
                    if first_cell_lower.startswith("---"):
                        continue
                    name = cells[1]
                    desc = ""
                    if len(cells) >= 3 and cells[2]:
                        desc = cells[2].strip()
                    if name and name != "Gap":
                        sections.gaps.append(GapSuggestion(
                            name=name,
                            description=desc
                        ))

    def _parse_workflows(self, lines: List[str], sections: EvolutionSections):
        current_title = None
        current_desc = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            title_match = re.search(r'-\s*\*\*([^*]+)\*\*', line)
            if title_match:
                if current_title:
                    sections.workflows.append(WorkflowSuggestion(
                        title=current_title,
                        description=" ".join(current_desc).strip()
                    ))
                current_title = title_match.group(1).strip()
                current_desc = []
                rest = line.split("**", 2)[-1].strip() if "**" in line else ""
                if rest.startswith("-"):
                    rest = rest[1:].strip()
                if rest:
                    current_desc.append(rest)
            elif current_title and line:
                if line.startswith("- "):
                    line = line[2:].strip()
                if line:
                    current_desc.append(line)

        if current_title:
            sections.workflows.append(WorkflowSuggestion(
                title=current_title,
                description=" ".join(current_desc).strip()
            ))

    def _parse_prompts(self, lines: List[str], sections: EvolutionSections):
        current_name = None
        current_template = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            name_match = re.search(r'-\s*\*\*([^*]+)\*\*', line)
            if name_match:
                if current_name:
                    sections.prompts.append({
                        "name": current_name,
                        "template": "\n".join(current_template).strip()
                    })
                current_name = name_match.group(1).strip()
                current_template = []
            elif current_name and ("Template:" in line or '"' in line):
                if "Template:" in line:
                    template = line.split("Template:", 1)[1].strip()
                    if template.startswith('"'):
                        template = template.strip('"')
                    current_template.append(template)
                elif '"' in line:
                    current_template.append(line)

        if current_name:
            sections.prompts.append({
                "name": current_name,
                "template": "\n".join(current_template).strip()
            })


class AgentAnalyzer:
    """Analyze and match agents for evolution suggestions."""

    def __init__(self, agents_dir: Path):
        self.agents_dir = agents_dir

    def load_existing_agents(self) -> List[Dict[str, Any]]:
        agents = []
        for path in self.agents_dir.glob("*.md"):
            if path.name in ("agents.md", "evolution.md"):
                continue
            try:
                post = frontmatter.load(path)
                agents.append({
                    "path": path,
                    "name": post.metadata.get("name", path.stem),
                    "role": post.metadata.get("role", ""),
                    "skills": post.metadata.get("skills", []),
                    "sources": post.metadata.get("sources", []),
                    "content": post.content
                })
            except Exception:
                continue
        return agents

    def find_matching_agent(self, suggestion: AgentSuggestion) -> Optional[Path]:
        agents = self.load_existing_agents()
        if not agents:
            return None

        best_match = None
        best_score = 0

        suggestion_text = (
            suggestion.name + " " +
            suggestion.functionality + " " +
            suggestion.rationale
        ).lower()

        suggestion_words = set(re.findall(r'\w+', suggestion_text))

        for agent in agents:
            agent_text = (
                agent["name"] + " " +
                agent["role"] + " " +
                " ".join(agent["skills"]) + " " +
                agent["content"]
            ).lower()

            agent_words = set(re.findall(r'\w+', agent_text))

            overlap = suggestion_words & agent_words
            score = len(overlap)

            for skill in suggestion.suggested_skills:
                if skill.lower() in " ".join(agent["skills"]).lower():
                    score += 3
                if skill.lower().replace("-", " ") in agent_text:
                    score += 1

            if score > best_score:
                best_score = score
                best_match = agent["path"]

        return best_match if best_score >= 2 else None

    def suggest_skills_for_agent(self, suggestion: AgentSuggestion) -> List[str]:
        """Suggest relevant skills based on agent suggestion text."""
        keywords_to_skills = {
            "gpu": ["gpu-scheduling", "cuda-management"],
            "scheduler": ["slurm", "workload-management"],
            "slurm": ["slurm", "workload-management"],
            "vendor": ["vendor-management"],
            "ai": ["ai-workloads", "ml-pipelines"],
            "quantum": ["quantum-computing"],
            "storage": ["storage-management", "burst-buffer"],
            "network": ["network-monitoring"],
            "monitoring": ["observability", "metrics"],
            "energy": ["sustainability", "power-management"],
            "edge": ["edge-computing"],
            "cloud": ["cloud-bursting", "hybrid-cloud"],
            "training": ["staff-training"],
            "workflow": ["workflow-automation"],
            "orchestration": ["orchestration"],
        }

        text = (suggestion.name + " " + suggestion.functionality).lower()
        found_skills = []

        for keyword, skills in keywords_to_skills.items():
            if keyword in text:
                found_skills.extend(skills)

        return list(set(found_skills))

    def suggest_sources_for_agent(self, suggestion: AgentSuggestion) -> List[str]:
        """Suggest relevant sources based on agent suggestion text."""
        keywords_to_sources = {
            "gpu": ["rss/hpcwire", "rss/nextplatform"],
            "ai": ["rss/hpcwire", "papers/arxiv"],
            "vendor": ["rss/nextplatform"],
            "quantum": ["papers/arxiv", "github/slurm"],
            "energy": ["rss/hpcwire"],
        }

        text = (suggestion.name + " " + suggestion.functionality).lower()
        found_sources = []

        for keyword, sources in keywords_to_sources.items():
            if keyword in text:
                found_sources.extend(sources)

        return list(set(found_sources))


class EvolutionApplicator:
    """Apply evolution changes with backup and preview."""

    def __init__(self, agents_dir: Path, skills_dir: Path, sources_dir: Path):
        self.agents_dir = agents_dir
        self.skills_dir = skills_dir
        self.sources_dir = sources_dir
        self._original_backups = {}
        BACKUP_DIR.mkdir(exist_ok=True)

    def backup_original(self, path: Path) -> Optional[Path]:
        """Backup the original state of a file once."""
        if path.name in self._original_backups:
            return self._original_backups[path.name]

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_path = BACKUP_DIR / f"{path.name}.bak_{timestamp}"
        if path.exists():
            import shutil
            shutil.copy(path, backup_path)
            self._original_backups[path.name] = backup_path
        return backup_path

    def restore_original(self, path: Path) -> bool:
        """Restore a file to its original state."""
        backup_name = path.name + ".bak_*"
        backups = sorted(BACKUP_DIR.glob(backup_name))
        if not backups:
            return False

        import shutil
        shutil.copy(backups[0], path)
        return True

    def create_agent(self, suggestion: AgentSuggestion, skills: List[str], sources: List[str]) -> Path:
        """Create a new agent file from a suggestion."""
        name_slug = suggestion.name.lower().replace(" ", "-")
        path = self.agents_dir / f"{name_slug}.md"

        if path.exists():
            print(f"  Agent {name_slug}.md already exists")
            return path

        content = f"""---
name: {name_slug}
role: {suggestion.name}
model: openrouter/free
skills:
{chr(10).join(f"  - {s}" for s in skills)}
sources:
{chr(10).join(f"  - {s}" for s in sources)}
---

## Mission

{suggestion.functionality}

## Rationale

{suggestion.rationale}
"""
        path.write_text(content)
        print(f"  Created agent: {path.name}")
        return path

    def update_agent(self, path: Path, add_skills: List[str], add_sources: List[str]) -> bool:
        """Update an existing agent with new skills and sources."""
        if not path.exists():
            return False

        self.backup_original(path)

        post = frontmatter.load(path)
        meta = post.metadata

        existing_skills = set(meta.get("skills", []))
        existing_skills.update(add_skills)
        meta["skills"] = sorted(existing_skills)

        existing_sources = set(meta.get("sources", []))
        existing_sources.update(add_sources)
        meta["sources"] = sorted(existing_sources)

        path.write_text(frontmatter.dumps(post))
        print(f"  Updated: {path.name}")
        return True

    def create_skill(self, name: str, description: str) -> Path:
        """Create a new skill file."""
        path = self.skills_dir / f"{name.lower().replace(' ', '-')}.md"
        if path.exists():
            print(f"  Skill {path.name} already exists")
            return path

        content = f"""# Skill: {name}

{description}
"""
        path.write_text(content)
        print(f"  Created skill: {path.name}")
        return path

    def create_source(self, source: SourceSuggestion) -> Path:
        """Create a new source file."""
        slug = source.title.lower().replace(" ", "-")
        subdir = source.source_type
        if source.source_type == "api":
            subdir = "apis"
        elif source.source_type == "repo":
            subdir = "repos"

        dir_path = self.sources_dir / subdir
        dir_path.mkdir(exist_ok=True)
        path = dir_path / f"{slug}.md"

        if path.exists():
            print(f"  Source {path.name} already exists")
            return path

        content = f"""# {source.title}

URL: {source.url}

Description: {source.description}
"""
        path.write_text(content)
        print(f"  Created source: {path.name}")
        return path


class InteractiveUI:
    """Interactive CLI using questionary or fallback."""

    def __init__(self, use_questionary: bool = QUESTIONARY_AVAILABLE):
        self.use_questionary = use_questionary

    def print_header(self, text: str):
        print(f"\n{'='*60}")
        print(f"  {text}")
        print('='*60)

    def print_section(self, text: str):
        print(f"\n--- {text} ---")

    def confirm(self, message: str, default: bool = False) -> bool:
        if self.use_questionary:
            return questionary.confirm(message, default=default).ask()
        else:
            suffix = " [Y/n]: " if default else " [y/N]: "
            try:
                resp = input(message + suffix).strip().lower()
            except EOFError:
                return default
            if not resp:
                return default
            return resp in ('y', 'yes')

    def select(self, message: str, choices: List[str], default: str = None) -> Optional[str]:
        if self.use_questionary:
            selected = questionary.select(message, choices=choices).ask()
            return selected
        else:
            print(f"\n{message}")
            for i, choice in enumerate(choices, 1):
                print(f"  {i}. {choice}")
            try:
                resp = input("Selection: ").strip()
            except EOFError:
                return default
            if resp.isdigit():
                idx = int(resp) - 1
                if 0 <= idx < len(choices):
                    return choices[idx]
            elif resp in choices:
                return resp
            return default

    def multiselect(self, message: str, choices: List[str]) -> List[str]:
        if self.use_questionary:
            selected = questionary.checkbox(message, choices=choices).ask()
            return selected or []
        else:
            print(f"\n{message}")
            print("Enter numbers separated by commas, 'all' for everything, or press Enter to skip: ")
            for i, choice in enumerate(choices, 1):
                print(f"  {i}. {choice}")
            try:
                resp = input("Selection: ").strip().lower()
            except EOFError:
                return []
            if not resp:
                return []
            if resp == 'all':
                return list(choices)
            try:
                indices = [int(x.strip()) - 1 for x in resp.split(",")]
                return [choices[i] for i in indices if 0 <= i < len(choices)]
            except:
                return []

    def text_input(self, message: str, default: str = "") -> str:
        if self.use_questionary:
            return questionary.text(message, default=default).ask() or default
        else:
            resp = input(f"{message}")
            return resp if resp else default

    def print_summary(self, sections: EvolutionSections):
        """Print a formatted summary of parsed sections."""
        self.print_header("Evolution Summary")

        print(f"\nAgents: {len(sections.agents)}")
        for agent in sections.agents:
            print(f"  - {agent.name}: {agent.functionality[:60]}...")

        print(f"\nSources: {len(sections.sources)}")
        for src in sections.sources:
            print(f"  - [{src.source_type}] {src.title}")

        print(f"\nGaps: {len(sections.gaps)}")
        for gap in sections.gaps:
            print(f"  - {gap.name}")

        print(f"\nWorkflows: {len(sections.workflows)}")
        for wf in sections.workflows:
            print(f"  - {wf.title}")

        print(f"\nPrompts: {len(sections.prompts)}")
        for prompt in sections.prompts:
            print(f"  - {prompt['name']}")


def main():
    parser = argparse.ArgumentParser(
        description="Process evolution.md and apply agent/skills/source changes"
    )
    parser.add_argument("--auto", action="store_true", help="Apply all changes without prompts")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--revert", action="store_true", help="Revert last changes from backups")
    parser.add_argument("--create-agents", action="store_true", help="Create new agent files from suggestions")
    parser.add_argument("--create-skills", action="store_true", help="Create new skill files from suggestions")
    parser.add_argument("--create-sources", action="store_true", help="Create new source files from suggestions")
    args = parser.parse_args()

    ui = InteractiveUI()

    if args.revert:
        ui.print_header("Reverting Changes")
        backed_up = set()
        for backup in sorted(BACKUP_DIR.glob("*.bak_*")):
            import shutil
            original = backup.name.split(".bak_")[0]
            original_path = AGENTS_DIR / original
            if original_path.exists():
                shutil.copy(backup, original_path)
                print(f"  Restored: {original}")
                backed_up.add(original)
            backup.unlink()
        if not backed_up:
            print("No backups found")
        else:
            print("\nRevert complete")
        return

    if not EVOLUTION_PATH.exists():
        print(f"Error: {EVOLUTION_PATH} not found")
        sys.exit(1)

    content = EVOLUTION_PATH.read_text()
    parser = EvolutionParser()
    sections = parser.parse(content)

    ui.print_summary(sections)

    if args.dry_run:
        print("\n[DRY RUN - No changes applied]")
        return

    analyzer = AgentAnalyzer(AGENTS_DIR)
    applicator = EvolutionApplicator(AGENTS_DIR, SKILLS_DIR, SOURCES_DIR)

    confirmed_updates = []

    ui.print_header("Processing Agents")

    for agent in sections.agents:
        ui.print_section(f"Agent: {agent.name}")
        print(f"  Functionality: {agent.functionality}")
        print(f"  Rationale: {agent.rationale}")

        suggested_skills = analyzer.suggest_skills_for_agent(agent)
        suggested_sources = analyzer.suggest_sources_for_agent(agent)

        print(f"  Suggested Skills: {', '.join(suggested_skills) or 'None'}")
        print(f"  Suggested Sources: {', '.join(suggested_sources) or 'None'}")

        match = analyzer.find_matching_agent(agent)
        agent.match_path = match

        if match:
            print(f"  Matching Agent: {match.name}")
            if args.auto:
                confirmed_updates.append((match, suggested_skills, suggested_sources))
            elif ui.confirm(f"  Update {match.name}?", default=True):
                confirmed_updates.append((match, suggested_skills, suggested_sources))
        elif args.create_agents or ui.confirm("  Create new agent?", default=False):
            if suggested_skills or suggested_sources:
                applicator.create_agent(agent, suggested_skills, suggested_sources)
            else:
                print("  Skipped: no skills/sources to assign")

    if sections.skills:
        ui.print_header("Processing Skill Suggestions")
        for skill in sections.skills:
            if args.create_skills or ui.confirm(f"Create skill '{skill.name}'?", default=False):
                applicator.create_skill(skill.name, skill.description)

    if sections.sources:
        ui.print_header("Processing Source Suggestions")
        for source in sections.sources:
            print(f"  [{source.source_type}] {source.title}")
            print(f"    URL: {source.url}")
            print(f"    Description: {source.description}")
            if args.create_sources or (args.auto and source.url and source.url.strip()):
                applicator.create_source(source)
            elif not args.auto and ui.confirm(f"Create source entry?", default=False):
                applicator.create_source(source)

    if sections.gaps:
        ui.print_header("Coverage Gaps")
        for gap in sections.gaps:
            print(f"  - {gap.name}: {gap.description}")
            if args.auto:
                print("    Skipped in auto mode (use --create-agents to create agents from gaps)")
            elif ui.confirm(f"    Create agent for this gap?", default=False):
                agent = AgentSuggestion(
                    name=gap.name,
                    functionality=gap.description,
                    rationale=f"Addresses coverage gap: {gap.name}"
                )
                applicator.create_agent(agent, [], [])

    if sections.workflows:
        ui.print_header("Workflow Improvements")
        for wf in sections.workflows:
            print(f"  - {wf.title}: {wf.description[:80]}...")

    if sections.prompts:
        ui.print_header("Prompt Templates")
        for prompt in sections.prompts:
            print(f"  - {prompt['name']}")
            print(f"    Template: {prompt['template'][:100]}...")

    if confirmed_updates and not args.auto:
        ui.print_header("Selective Updates")
        print("Review and adjust skills/sources before applying:\n")

        final_updates = []
        for match, skills, sources in confirmed_updates:
            print(f"  Agent: {match.name}")
            selected_skills = ui.multiselect("  Skills", skills)
            selected_sources = ui.multiselect("  Sources", sources)
            if selected_skills or selected_sources:
                final_updates.append((match, selected_skills, selected_sources))
            print()

        for match, skills, sources in final_updates:
            applicator.update_agent(match, skills, sources)
    else:
        for match, skills, sources in confirmed_updates:
            applicator.update_agent(match, skills, sources)

    ui.print_header("Evolution Complete")
    print("\nRun again with --auto to apply all changes automatically")
    print("Run with --dry-run to preview without applying")


if __name__ == "__main__":
    main()