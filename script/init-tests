#!/bin/bash
set -euxo pipefail

FILES=".github/workflows/*.yaml"
SEARCH="test-flags: --version"

for file in $FILES; do
	sed -i '' -e "/$SEARCH/d" "$file"
done
