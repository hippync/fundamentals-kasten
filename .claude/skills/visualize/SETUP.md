# Diagram setup

Only `/visualize` needs any of this. Every other Breakpoint skill, and the kasten itself, works without it.

| Tool | For | Install (macOS) | Check |
|---|---|---|---|
| Node.js 18+ | running mermaid-cli | `brew install node`, or [nodejs.org](https://nodejs.org) | `node --version` |
| mermaid-cli | Mermaid → PNG (`mermaid-maker`) | nothing: `npx` fetches the pinned `@mermaid-js/mermaid-cli@12.0.0` on first use, with a headless Chromium (a few hundred MB, once) | `npx -y -p @mermaid-js/mermaid-cli@12.0.0 mmdc --version` |
| rsvg-convert | SVG → PNG (`svg-maker`) | `brew install librsvg` | `rsvg-convert --version` |

On Debian/Ubuntu: `sudo apt install nodejs npm librsvg2-bin`. On Windows, use WSL and the Debian line.

Claude Code asks permission the first time each render command runs. Diagrams land in `_tutor/viz/`, which git ignores like the rest of your session history.
