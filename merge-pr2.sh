#!/bin/bash

echo "🔄 Step 1: Converting PR #2 from Draft to Ready..."
gh pr ready 2 --repo kk121288/BTEC-Smart-Platform-Frontend

echo "✅ Step 2: Merging PR #2 with squash..."
gh pr merge 2 --repo kk121288/BTEC-Smart-Platform-Frontend --squash

echo "📥 Step 3: Updating template branch..."
git checkout template
git pull origin template

echo "✅ PR #2 merged successfully!"
echo "🎉 You can now proceed with creating PR #3 with simulation files."