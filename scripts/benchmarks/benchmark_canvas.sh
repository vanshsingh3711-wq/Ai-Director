#!/bin/bash
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT/packages/motion-components"
echo "Running Canvas + FFmpeg Benchmark..."
/usr/bin/time -v node benchmark_canvas.js
