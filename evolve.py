#!/usr/bin/env python3
import re
import sys
import argparse
from pathlib import Path
import frontmatter
import shutil
from datetime import datetime

EVOLUTION_PATH = Path("workspace/memory/evolution.md")
AGENTS_DIR = Path("agents")
BACKUP_DIR = AGENTS_DIR / ".backups"
CONFIDENCE_THRESHOLD = 0.5

# Ensure backup directory exists
BACKUP_DIR.mkdir(exist_ok=True)


def safe_backup(path: Path):
    """Create a timestamped backup of a file"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    backup_path = BACKUP_DIR / f"{path.name}.bak_{timestamp}"
    shutil.copy(path, backup_path)
    return backup_path


def restore_backup(path: Path):
    """Restore the most recent backup of a file"""
    backups = sorted(BACKUP_DIR.glob(f"{path.name}.bak_*"))
    if not backups:
        return False
    latest_backup = backups[-1]
    shutil.copy(latest_backup, path)
    latest_backup.unlink(missing_ok=True)
    return True


def parse_evolution(content):
    """Parse all sections from evolution.md"""
    sections = {
        "agents": [],
        "prompts": [],
        "sources": {"rss": [], "apis": [], "repos": []},
        "gaps": [],
        "workflows": []
    }
    
    lines = content.split('\n')
    current_section = None
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith("## New Agents"):
            current_section = "agents"
            i += 1
            continue
        elif line.startswith("## Prompt Refinements"):
            current_section = "prompts"
            i += 1
            continue
        elif line.startswith("## Source Additions"):
            current_section = "sources"
            i += 1
            continue
        elif line.startswith("## Coverage Gaps"):
            current_section = "gaps"
            i += 1
            continue
        elif line.startswith("## Workflow Improvements"):
            current_section = "workflows"
            i += 1
            continue
        elif line.startswith("##"):
            current_section = None
            i += 1
            continue
        
        if current_section == "agents":
            name_match = re.search(r'-\s*\*\*([^*]+)\*\*', line)
            if name_match:
                name = name_match.group(1).strip()
                functionality = ""
                rationale = ""
                j = i + 1
                while j < len(lines) and j < i + 10:
                    if "*Focus:" in lines[j]:
                        functionality = lines[j].split("*Focus:", 1)[1].strip().rstrip(".")
                    if "*Rationale:" in lines[j]:
                        rationale = lines[j].split("*Rationale:", 1)[1].strip().rstrip(".")
                    j += 1
                sections["agents"].append({
                    "name": name,
                    "functionality": functionality,
                    "rationale": rationale
                })
        
        elif current_section == "prompts":
            name_match = re.search(r'-\s*\*\*([^*]+)\*\*', line)
            if name_match:
                name = name_match.group(1).strip()
                prompt = ""
                j = i + 1
                while j < len(lines) and j < i + 5:
                    stripped = lines[j].strip()
                    if stripped.startswith('"') or stripped.startswith("'"):
                        prompt = stripped
                    j += 1
                sections["prompts"].append({"name": name, "prompt": prompt})
        
        elif current_section == "sources":
            if "RSS Feeds:" in line:
                current_sub = "rss"
            elif "APIS:" in line:
                current_sub = "apis"
            elif "REPOSITORIES:" in line:
                current_sub = "repos"
            elif current_sub and line.startswith("- ["):
                link_match = re.search(r'\[([^\]]+)]\(([^)]+)\)', line)
                if link_match:
                    title = link_match.group(1)
                    url = link_match.group(2)
                    desc = line.split("](", 1)[1].split(")", 1)[0] if ")" in line else ""
                    sections["sources"][current_sub].append({
                        "title": title,
                        "url": url,
                        "description": desc
                    })
        
        elif current_section == "gaps":
            name_match = re.search(r'- \*\*([^*]+):\*\*\s*(.+)', line)
            if name_match:
                sections["gaps"].append({
                    "name": name_match.group(1).strip(),
                    "description": name_match.group(2).strip()
                })
        
        elif current_section == "workflows":
            title_match = re.search(r'- \*\*([^*]+)\*\*', line)
            if title_match:
                title = title_match.group(1).strip()
                description = ""
                j = i + 1
                while j < len(lines) and j < i + 5:
                    if lines[j].strip() and not lines[j].startswith("- "):
                        description += lines[j].strip() + " "
                    j += 1
                sections["workflows"].append({
                    "title": title,
                    "description": description.strip()
                })
        
        i += 1
    
    return sections


def compute_confidence(suggestion, search_terms):
    """Simple confidence score based on keyword overlap"""
    score = 0
    total_terms = len(search_terms)
    if total_terms == 0:
        return 0
    suggestion_lower = suggestion["functionality"].lower()
    for term in search_terms:
        if term in suggestion_lower:
            score += 1
    return score / total_terms


def generate_fields(suggestion, keywords):
    """Generate relevant skills/sources based on suggestion"""
    name = suggestion["name"].lower().replace(" ", "-")
    role = suggestion["name"]
    
    # Extract relevant topics
    relevant_skills = []
    relevant_sources = []
    
    # Skills
    if any(kw in suggestion["functionality"].lower() for kw in ["gpu", "scheduler", "slurm", "allocation", "orchestration"]):
        relevant_skills.extend(["gpu-scheduling", "resource-allocation"])
    if any(kw in suggestion["functionality"].lower() for kw in ["vendor", "supply", "procurement", "contract", "sla"]):
        relevant_skills.extend(["vendor-management", "contract-negotiation"])
    if any(kw in suggestion["functionality"].lower() for kw in ["telemetry", "observability", "ebpf", "monitoring"]):
        relevant_skills.extend(["observability", "telemetry-pipeline"])
    if any(kw in suggestion["functionality"].lower() for kw in ["edge", "decentral", "distributed", "edge-computing"]):
        relevant_skills.extend(["edge-integration"])
    if any(kw in suggestion["functionality"].lower() for kw in ["firmware", "debug", "diagnose", "failure", "asics", "fpga"]):
        relevant_skills.extend(["firmware-debugging"])
    
    # Sources
    for src in sections["sources"]["rss"]:
        if any(kw in src["description"].lower() for kw in ["gpu", "hardware", "tools"]):
            relevant_sources.append("rss/hpcwire")
    for src in sections["sources"]["apis"]:
        if any(kw in src["description"].lower() for kw in ["gpu", "telemetry", "observability"]):
            if "nvidia" in src["title"].lower():
                relevant_sources.append("nvidia-management-api")
            elif "opentelemetry" in src["title"].lower():
                relevant_sources.append("opentelemetry-collector")
    for src in sections["sources"]["repos"]:
        relevant_sources.append(src["title"].lower().replace(" ", "-"))
    
    # Add gap topics as skills
    for gap in sections["gaps"]:
        if "firmware" in gap["name"].lower():
            relevant_skills.append("firmware-debugging")
        if "procurement" in gap["name"].lower():
            relevant_skills.append("decentralized-procurement")
        if "orchestration" in gap["name"].lower():
            relevant_skills.append("cross-vendor-orchestration")
        if "edge" in gap["name"].lower():
            relevant_skills.append("edge-hpc-integration")
    
    # Add workflow titles as notes
    if sections["workflows"]:
        relevant_skills.extend([w["title"] for w in sections["workflows"]])
    
    return {
        "name": name,
        "role": role,
        "relevant_skills": list(set(relevant_skills)),
        "relevant_sources": list(set(relevant_sources)),
        "keywords": keywords  # for confidence calculation
    }


def find_matching_agent(fields):
    """Find the most relevant existing agent to update"""
    agent_files = list(AGENTS_DIR.glob("*.md"))
    agent_files = [a for a in agent_files if a.name not in ("agents.md", "evolution.md")]
    
    if not agent_files:
        return None
    
    best_match = None
    best_score = 0
    
    for agent_path in agent_files:
        agent_data = load_agent(agent_path)
        meta = agent_data["metadata"]
        agent_role = (meta.get("role", "") + " " + meta.get("name", "")).lower()
        agent_skills = " ".join(meta.get("skills", [])).lower()
        agent_content = agent_data["content"].lower()
        
        score = 0
        # Match against role, skills, content
        for kw in fields["keywords"]:
            kw_lower = kw.lower()
            if kw_lower in agent_role:
                score += 3
            if kw_lower in agent_skills:
                score += 2
            if kw_lower in agent_content:
                score += 1
        
        # Bonus for skill overlap
        for skill in fields["relevant_skills"]:
            skill_lower = skill.lower()
            if skill_lower in agent_skills:
                score += 2
            if skill_lower.replace("-", " ") in agent_role:
                score += 1
        
        if score > best_score:
            best_score = score
            best_match = agent_path
    
    return best_match if best_score > 0 else None


def load_agent(path):
    post = frontmatter.load(path)
    return {"metadata": post.metadata, "content": post.content}


def save_agent(path, metadata, content):
    post = frontmatter.Post(content, **metadata)
    path.write_text(frontmatter.dumps(post))


def update_agent(file_path, fields, apply_changes=True):
    """Update an agent's skills/sources with backup"""
    if not file_path.exists():
        return False
    
    backup_path = safe_backup(file_path)
    
    agent_data = load_agent(file_path)
    meta = agent_data["metadata"]
    content = agent_data["content"]
    
    # Initialize sections if missing
    meta.setdefault("skills", [])
    meta.setdefault("sources", [])
    meta.setdefault("workflows", [])
    
    # Merge new skills
    existing_skills = set(meta.get("skills", []))
    new_skills = existing_skills.union(fields["relevant_skills"])
    meta["skills"] = sorted(new_skills)
    
    # Merge new sources
    existing_sources = set(meta.get("sources", []))
    new_sources = existing_sources.union(fields["relevant_sources"])
    meta["sources"] = sorted(new_sources)
    
    # Update role if missing
    if not meta.get("role"):
        meta["role"] = fields["role"]
    
    # Save only if requested
    if apply_changes:
        save_agent(file_path, meta, content)
        print(f"✓ Updated {file_path.name}")
        return True
    else:
        # Restore from backup without saving
        restore_path = restore_backup(file_path)
        print(f"⇆ Reverted {file_path.name}")
        return False


def add_topics_to_agentsmd(sections, apply_changes=True):
    """Add topics to agents.md with optional apply"""
    agents_path = AGENTS_DIR / "agents.md"
    if not agents_path.exists():
        return
    
    content = agents_path.read_text()
    
    # Ensure section exists
    if "## Evolved Topics" not in content:
        content += "\n## Evolved Topics\n"
    
    modifications = []
    
    # Add new topics
    for agent in sections["agents"]:
        entry = f"- {agent['name']}: {agent['functionality']}\n"
        if entry not in content:
            modifications.append(("add_topic", entry))
            if apply_changes:
                content += entry
    
    # Add gap topics
    for gap in sections["gaps"]:
        entry = f"- {gap['name']}: {gap['description']}\n"
        if entry not in content:
            modifications.append(("add_topic", entry))
            if apply_changes:
                content += entry
    
    # Add workflow improvements
    for workflow in sections["workflows"]:
        entry = f"- {workflow['title']}: {workflow['description']}\n"
        if entry not in content:
            modifications.append(("add_topic", entry))
            if apply_changes:
                content += entry
    
    # Add source entries
    for src in sections["sources"]["rss"]:
        entry = f"- RSS: {src['title']} ({src['url']})\n"
        if entry not in content:
            modifications.append(("add_source", entry))
            if apply_changes:
                content += entry
    
    if apply_changes:
        agents_path.write_text(content)
        print("✓ Updated agents.md with new topics")
    else:
        # Revert: just restore original content (we didn't write yet)
        pass
    
    return modifications


def main():
    parser = argparse.ArgumentParser(description="Evolve agent configurations based on evolution.md")
    parser.add_argument("--auto", action="store_true", help="Automatically apply changes without prompts")
    parser.add_argument("--threshold", type=float, default=CONFIDENCE_THRESHOLD, help="Minimum confidence threshold for automatic application")
    parser.add_argument("--revert", action="store_true", help="Revert all recent changes using backups")
    args = parser.parse_args()
    
    # Handle revert mode
    if args.revert:
        print("Reverting all changes...")
        for agent_file in AGENTS_DIR.glob("*.md"):
            if agent_file.name not in ("agents.md", "evolution.md"):
                restore_backup(agent_file)
        restore_backup(AGENTS_DIR / "agents.md")
        print("✓ All changes reverted")
        return
    
    # Read evolution file
    content = EVOLUTION_PATH.read_text()
    sections = parse_evolution(content)
    
    # Prepare for processing
    keywords = []
    for agent in sections["agents"]:
        keywords.append(agent["name"])
        keywords.extend(agent["functionality"].split())
    for prompt in sections["prompts"]:
        keywords.extend(prompt["prompt"].split())
    for gap in sections["gaps"]:
        keywords.extend(gap["name"].split())
        keywords.extend(gap["description"].split())
    
    # Process each agent suggestion
    print(f"\n=== Evolution Processor ({'AUTO' if args.auto else 'INTERACTIVE'} MODE) ===")
    print(f"Threshold: {args.threshold:.2f}")
    
    applied_any = False
    
    for suggestion in sections["agents"]:
        fields = generate_fields(suggestion, keywords)
        confidence = compute_confidence(suggestion, keywords)
        print(f"\n--- Processing: {suggestion['name']} (confidence: {confidence:.2f}) ---")
        
        if args.auto:
            apply = confidence >= args.threshold
        else:
            apply = None  # Will prompt
        
        if not args.auto:
            # Interactive prompt
            resp = input(f"Update matching agent with new skills/sources? (y/N): ").strip().lower()
            apply = resp == 'y' or (apply is None and confidence >= args.threshold)
        
        if apply:
            match = find_matching_agent(fields)
            if match:
                updated = update_agent(match, fields, apply_changes=True)
                if updated:
                    applied_any = True
            else:
                # No match - add to reference section
                add_topics_to_agentsmd({"agents": [suggestion]}, apply_changes=False)
                print("  ✓ Added to reference section (no matching agent)")
                applied_any = True
        else:
            print("  Skipped")
            applied_any = True  # Count as processed
    
    # Add topics to main reference file
    add_topics_to_agentsmd(sections, apply_changes=not args.auto)
    
    print(f"\n=== Evolution Complete ({'AUTO' if args.auto else 'INTERACTIVE'} Mode) ===")
    if args.auto and not applied_any:
        print("⚠ No suggestions met confidence threshold")
    elif not args.auto:
        print("✓ Changes require manual confirmation (use --auto to bypass)")


if __name__ == "__main__":
    main()