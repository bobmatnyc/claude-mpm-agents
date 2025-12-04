#!/usr/bin/env python3
"""
Phase 3 Agent Optimization Script
Optimizes ops and engineer agent files by:
1. Softening aggressive imperatives
2. Removing emoji pollution
3. Adding WHY context
4. Improving code comments
5. Reducing token count
"""

import re
from pathlib import Path
from typing import Tuple

def soften_imperatives(text: str) -> str:
    """Convert aggressive imperatives to guidance."""
    replacements = {
        r'\bMUST\b': 'should',
        r'\bNEVER\b': 'avoid',
        r'\bALWAYS\b': 'prefer',
        r'\bREQUIRED\b': 'recommended',
        r'\bMANDATORY\b': 'important',
        r'\bESSENTIAL\b': 'valuable',
        r'\bCRITICAL\b': 'important',
        r'\bFORBIDDEN\b': 'not recommended',
    }

    result = text
    for pattern, replacement in replacements.items():
        result = re.sub(pattern, replacement, result)

    return result

def remove_emojis(text: str) -> str:
    """Remove emoji pollution from headers and sections."""
    # Remove common emojis used in agent files
    emoji_pattern = r'[🔴⚠️✅❌🚨💡🎯📋🔧⚡🏗️💻🐛🧪📝🎨🔄🤖]'
    return re.sub(emoji_pattern, '', text)

def improve_code_comments(text: str) -> str:
    """Convert harsh code comments to explanatory quality."""
    # Replace WRONG/CORRECT patterns
    text = re.sub(
        r'#\s*(WRONG|BAD|AVOID THIS):\s*',
        '# Problem: ',
        text,
        flags=re.MULTILINE
    )
    text = re.sub(
        r'#\s*(CORRECT|GOOD|USE THIS):\s*',
        '# Solution: ',
        text,
        flags=re.MULTILINE
    )

    # Replace ❌/✅ in code comments
    text = re.sub(r'❌\s*', '# Not recommended: ', text)
    text = re.sub(r'✅\s*', '# Recommended: ', text)

    return text

def add_why_context(text: str) -> str:
    """Add explanatory context to prohibitions."""
    # This is context-aware, so we'll handle specific patterns

    # Git commit patterns
    text = re.sub(
        r"avoid committing files containing",
        "avoid committing files containing (to prevent credential exposure)",
        text
    )

    # YJIT patterns
    text = re.sub(
        r"avoid skipping YJIT",
        "avoid skipping YJIT (results in 18-30% performance loss)",
        text
    )

    # N+1 query patterns
    text = re.sub(
        r"avoid N\+1 queries",
        "avoid N+1 queries (causes performance degradation)",
        text
    )

    return text

def optimize_file(filepath: Path) -> Tuple[int, int, int]:
    """
    Optimize a single agent file.
    Returns: (violations_before, violations_after, tokens_saved)
    """
    content = filepath.read_text()
    original_content = content

    # Count original violations
    violations_before = count_violations(content)
    original_tokens = len(content.split())

    # Apply transformations
    content = soften_imperatives(content)
    content = remove_emojis(content)
    content = improve_code_comments(content)
    content = add_why_context(content)

    # Remove redundant warnings
    content = remove_redundant_warnings(content)

    # Clean up extra whitespace
    content = re.sub(r'\n{4,}', '\n\n\n', content)

    # Count after optimization
    violations_after = count_violations(content)
    final_tokens = len(content.split())
    tokens_saved = original_tokens - final_tokens

    # Write optimized content
    filepath.write_text(content)

    return violations_before, violations_after, tokens_saved

def count_violations(text: str) -> int:
    """Count total violations in text."""
    patterns = {
        'aggressive_imperatives': r'\b(MUST|NEVER|ALWAYS|CRITICAL|MANDATORY|REQUIRED|ESSENTIAL)\b',
        'emoji_pollution': r'[🔴⚠️✅❌🚨💡🎯📋🔧⚡🏗️💻🐛🧪📝🎨🔄]',
        'bad_code_comments': r'(WRONG|CORRECT|BAD|GOOD|AVOID THIS|USE THIS):',
    }

    total = 0
    for pattern in patterns.values():
        total += len(re.findall(pattern, text, re.MULTILINE))

    return total

def remove_redundant_warnings(text: str) -> str:
    """Remove redundant warning sections."""
    # Remove repeated "Warning:" or "Important:" sections
    lines = text.split('\n')
    cleaned_lines = []
    last_warning = None

    for line in lines:
        # Check if this is a warning/important line
        if re.match(r'^(Warning|Important|Note):', line.strip()):
            if line.strip() != last_warning:
                cleaned_lines.append(line)
                last_warning = line.strip()
        else:
            cleaned_lines.append(line)
            last_warning = None

    return '\n'.join(cleaned_lines)

def main():
    """Main optimization function."""
    base_path = Path(__file__).parent / "agents"

    files_to_optimize = [
        "ops/tooling/version-control.md",
        "ops/core/ops.md",
        "ops/platform/vercel-ops.md",
        "ops/platform/gcp-ops.md",
        "engineer/backend/ruby-engineer.md",
        "engineer/backend/php-engineer.md",
        "engineer/backend/golang-engineer.md",
        "engineer/backend/rust-engineer.md",
        "engineer/backend/javascript-engineer.md",
        "engineer/frontend/react-engineer.md",
    ]

    total_violations_before = 0
    total_violations_after = 0
    total_tokens_saved = 0

    results = []

    print("Phase 3 Agent Optimization - Processing 10 files...")
    print("=" * 70)

    for file_rel_path in files_to_optimize:
        filepath = base_path / file_rel_path

        if not filepath.exists():
            print(f"SKIP: {file_rel_path} (not found)")
            continue

        before, after, tokens = optimize_file(filepath)
        eliminated = before - after

        total_violations_before += before
        total_violations_after += after
        total_tokens_saved += tokens

        results.append({
            'file': filepath.name,
            'before': before,
            'after': after,
            'eliminated': eliminated,
            'tokens_saved': tokens,
        })

        print(f"{filepath.name:40s} | {before:3d} → {after:3d} | -{eliminated:3d} violations | -{tokens:4d} tokens")

    print("=" * 70)
    print(f"{'TOTAL':40s} | {total_violations_before:3d} → {total_violations_after:3d} | -{total_violations_before - total_violations_after:3d} violations | -{total_tokens_saved:4d} tokens")
    print()
    print(f"Elimination rate: {((total_violations_before - total_violations_after) / total_violations_before * 100):.1f}%")
    print(f"Token reduction: {(total_tokens_saved / (total_tokens_saved + sum(len(f['file'].split()) for f in results)) * 100):.1f}%")
    print()
    print("Phase 3 optimization complete!")

if __name__ == '__main__':
    main()
