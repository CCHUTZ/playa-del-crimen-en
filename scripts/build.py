#!/usr/bin/env python3
"""
Build script for Playa del Crimen
Converts Markdown content to HTML for GitHub Pages
v2.0 — Intelligence Operations Platform Design
"""

import os
import re
import markdown
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
SCENARIOS_DIR = PROJECT_ROOT / "content" / "scenarios"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "scenarios"

# Scenario list
SCENARIOS = [
    {
        'id': '00_the_terror_star',
        'title': 'The Terror Star',
        'number': '00',
        'tagline': 'Sociotechnical intelligence and mapping of informal power networks.',
        'category': 'OSINT · Social Engineering · Threat Intel',
    },
    {
        'id': '01_operation_krakatoa',
        'title': 'Operation Krakatoa',
        'number': '01',
        'tagline': 'Corporate ecosystem analysis and reputational risk in environmental conflicts.',
        'category': 'OSINT · Corporate Risk · Geopolitics',
    },
    {
        'id': '02_the_sewer',
        'title': 'The Sewer',
        'number': '02',
        'tagline': 'Tracing public resource flows and exposing municipal corruption networks.',
        'category': 'OSINT · Political Intelligence · Finance',
    },
    {
        'id': '03_sand_castles',
        'title': 'Sand Castles',
        'number': '03',
        'tagline': 'Digital identity tracking and behavioral profiling in real estate fraud.',
        'category': 'OSINT · Fraud · Digital Identity',
    },
    {
        'id': '04_the_ghost_train',
        'title': 'The Ghost Train',
        'number': '04',
        'tagline': 'Analysis of information manipulation campaigns and disinformation networks.',
        'category': 'OSINT · Disinformation · Network Analysis',
    },
    {
        'id': '05_through_the_back_door_uwu',
        'title': 'Through the Back Door uwu',
        'number': '05',
        'tagline': 'Tracing carding infrastructure, smishing, and large-scale financial fraud.',
        'category': 'Carding · Financial Fraud · Smishing',
    }
]

# Sidebar navigation items for each scenario
SIDEBAR_ITEMS = [
    {'anchor': 'briefing',        'label': 'Briefing',                'icon': '◈'},
    {'anchor': 'team',            'label': 'Estructura del Equipo',   'icon': '◈'},
    {'anchor': 'phase-1',         'label': 'Fase 1',                  'icon': '◈'},
    {'anchor': 'phase-2',         'label': 'Fase 2',                  'icon': '◈'},
    {'anchor': 'phase-3',         'label': 'Fase 3',                  'icon': '◈'},
    {'anchor': 'phase-4',         'label': 'Fase 4',                  'icon': '◈'},
    {'anchor': 'phase-5',         'label': 'Fase 5',                  'icon': '◈'},
    {'anchor': 'exercises',       'label': 'Ejercicios',              'icon': '◈'},
    {'anchor': 'references',      'label': 'Referencias',             'icon': '◈'},
]

HTML_TEMPLATE = """<!DOCTYPE html>
    <html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scenario {number}: {title} | Playa del Crimen</title>
    <meta name="description" content="{tagline}">
    <link rel="stylesheet" href="../style.css">
</head>
<body class="page-scenario">

    <!-- ===== HEADER ===== -->
    <header>
        <div class="header-inner">
            <a href="../index.html" class="header-logo">
                <span class="logo-main">Playa del <span>Crimen</span></span>
                <span class="logo-sub">Intelligence Training Platform</span>
            </a>

            <nav class="header-nav">
                <a href="../index.html">← Scenarios</a>
                <a href="https://github.com/CCHUTZ/playa-del-crimen-en" target="_blank" rel="noopener">GitHub ↗</a>
            </nav>

            <div class="header-status">
                <span class="status-dot"></span>
                <span class="mono">SCENARIO {number}: {title_upper}</span>
            </div>

            <button class="hamburger" aria-label="Menú">
                <span></span><span></span><span></span>
            </button>
        </div>
    </header>

    <!-- ===== LAYOUT WRAPPER ===== -->
    <div class="layout-scenario">

    <!-- ===== SIDEBAR ===== -->
    <aside class="sidebar">
        <p class="sidebar-label">Operation Phases</p>
        <ul class="sidebar-nav">
{sidebar_items}
        </ul>
        <div class="sidebar-divider"></div>
        <ul class="sidebar-nav">
            <li><a href="../index.html"><span class="nav-icon">←</span> Back to Home</a></li>
        </ul>
    </aside>

    <!-- ===== CONTENT ===== -->
    <div class="scenario-content">

        <!-- Scenario Hero -->
        <div class="scenario-hero">
            <div class="scenario-meta">
                <span class="scenario-number">SCENARIO {number}</span>
                <span class="scenario-category">{category}</span>
            </div>
            <h1>{title}</h1>
            <p class="scenario-tagline">{tagline}</p>
        </div>

        <!-- Mobile nav -->
        <details class="mobile-nav-toggle">
            <summary>Operation Phases</summary>
            <ul class="sidebar-nav">
{sidebar_items}
            </ul>
        </details>

        <main>
            <div class="content-body">
{content}
            </div>
        </main>

        <!-- Footer -->
        <footer>
            <div class="footer-inner">
                <span class="footer-disclaimer">PLAYA DEL CRIMEN // EDUCATIONAL SIMULATION // FICTIONAL SCENARIOS // FOR TRAINING PURPOSES ONLY</span>
                <a href="../index.html" class="footer-back">← Back to Home</a>
            </div>
        </footer>

    </div><!-- /scenario-content -->

    </div><!-- /layout-scenario -->

    <script>
    // Sidebar active state on scroll
    (function() {{
        const links = document.querySelectorAll('.sidebar-nav a[href^="#"]');
        const sections = [];
        links.forEach(function(link) {{
            const id = link.getAttribute('href').slice(1);
            const el = document.getElementById(id);
            if (el) sections.push({{ el: el, link: link }});
        }});

        function onScroll() {{
            let current = null;
            sections.forEach(function(s) {{
                if (window.scrollY >= s.el.offsetTop - 100) current = s;
            }});
            links.forEach(function(l) {{ l.classList.remove('active'); }});
            if (current) current.link.classList.add('active');
        }}

        window.addEventListener('scroll', onScroll, {{ passive: true }});
        onScroll();
    }})();
    </script>

</body>
</html>
"""

def build_sidebar_items(scenario_id):
    """Build sidebar navigation items based on what files exist."""
    scenario_dir = SCENARIOS_DIR / scenario_id
    items = []

    # Always include briefing and team
    items.append({'anchor': 'briefing', 'label': 'Briefing', 'icon': '◈'})
    items.append({'anchor': 'team', 'label': 'Team Structure', 'icon': '◈'})

    # Add phase items
    phases_dir = scenario_dir / "phases"
    if phases_dir.exists():
        phase_files = sorted(phases_dir.glob("*.md"))
        for i, pf in enumerate(phase_files, 1):
            # Try to extract title from file
            label = f"Fase {i}"
            try:
                with open(pf, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('#'):
                        label = first_line.lstrip('#').strip()
                        # Shorten if too long
                        if len(label) > 28:
                            label = label[:26] + '…'
            except:
                pass
            items.append({'anchor': f'phase-{i}', 'label': label, 'icon': '◈'})

    # Exercises
    exercises_dir = scenario_dir / "exercises"
    if exercises_dir.exists():
        items.append({'anchor': 'exercises', 'label': 'Exercises', 'icon': '◈'})

    # References
    references_file = scenario_dir / "references.md"
    if references_file.exists():
        items.append({'anchor': 'references', 'label': 'References', 'icon': '◈'})

    return items

def render_sidebar_items(items):
    """Render sidebar items as HTML list items."""
    lines = []
    for item in items:
        lines.append(
            f'            <li><a href="#{item["anchor"]}"><span class="nav-icon">{item["icon"]}</span> {item["label"]}</a></li>'
        )
    return '\n'.join(lines)

def read_markdown_file(filepath):
    """Read a Markdown file and return its content."""
    if not filepath.exists():
        return ""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def convert_markdown_to_html(md_content):
    """Convert Markdown content to HTML."""
    return markdown.markdown(md_content, extensions=['extra', 'codehilite', 'toc'])

def wrap_section(html_content, anchor_id):
    """Wrap a content block in a section with an anchor id."""
    return f'<section id="{anchor_id}">\n{html_content}\n</section>\n'

def build_scenario(scenario):
    """Build a scenario HTML file."""
    scenario_dir = SCENARIOS_DIR / scenario['id']

    sections_html = ""

    # 1. README (intro — no anchor, just prepended)
    readme_md = read_markdown_file(scenario_dir / "README.md")
    if readme_md:
        sections_html += convert_markdown_to_html(readme_md) + "\n"

    # 2. Briefing
    briefing_md = read_markdown_file(scenario_dir / "briefing.md")
    if briefing_md:
        sections_html += wrap_section(convert_markdown_to_html(briefing_md), "briefing")

    # 3. Team Structure — combine all role files
    team_md = read_markdown_file(scenario_dir / "team_structure" / "roles.md")
    team_dir = scenario_dir / "team_structure"
    if team_dir.exists():
        for role_file in sorted(team_dir.glob("*.md")):
            if role_file.name != "roles.md":
                team_md += "\n\n" + read_markdown_file(role_file)
    if team_md:
        sections_html += wrap_section(convert_markdown_to_html(team_md), "team")

    # 4. Phases
    phases_dir = scenario_dir / "phases"
    if phases_dir.exists():
        for i, phase_file in enumerate(sorted(phases_dir.glob("*.md")), 1):
            phase_md = read_markdown_file(phase_file)
            if phase_md:
                sections_html += wrap_section(convert_markdown_to_html(phase_md), f"phase-{i}")

    # 5. Exercises
    exercises_dir = scenario_dir / "exercises"
    if exercises_dir.exists():
        exercises_md = ""
        for ex_file in sorted(exercises_dir.glob("*.md")):
            exercises_md += read_markdown_file(ex_file) + "\n\n---\n\n"
        if exercises_md:
            sections_html += wrap_section(convert_markdown_to_html(exercises_md), "exercises")

    # 6. References
    references_md = read_markdown_file(scenario_dir / "references.md")
    if references_md:
        sections_html += wrap_section(convert_markdown_to_html(references_md), "references")

    # Build sidebar
    sidebar_items = build_sidebar_items(scenario['id'])
    sidebar_html = render_sidebar_items(sidebar_items)

    # Render final HTML
    final_html = HTML_TEMPLATE.format(
        title=scenario['title'],
        title_upper=scenario['title'].upper(),
        number=scenario['number'],
        tagline=scenario.get('tagline', ''),
        category=scenario.get('category', 'OSINT'),
        sidebar_items=sidebar_html,
        content=sections_html
    )

    # Write to output file
    output_file = OUTPUT_DIR / f"{scenario['id']}.html"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"✓ Built: {scenario['title']}")

if __name__ == "__main__":
    print("Building Playa del Crimen (English) scenarios...")
    for scenario in SCENARIOS:
        build_scenario(scenario)
    print("\nBuild complete!")
