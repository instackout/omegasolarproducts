#!/usr/bin/env bash
# Point this clone's git hooks at .githooks/ so agent context stays in sync.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
git -C "$ROOT" config core.hooksPath .githooks
echo "Installed git hooks from .githooks (core.hooksPath=.githooks)"
echo "Pre-commit will refresh AGENTS.md when site files change."
