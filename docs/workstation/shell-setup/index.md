---
title: "Shell Setup"
date: 2026-04-05
description: "Git worktree and tag helper functions for .zshrc/.bashrc"
---

# Shell Setup

Helper functions I keep in `.zshrc`/`.bashrc` across devices.

## Git Worktree Helpers

These functions wrap `git worktree` to automatically name worktrees using the pattern `{repo-name}-{branch-name}`.

By default, worktrees are created at `{repo-root}/.worktrees/{repo-name}-{branch-name}`.
Pass `--sibling` to place the worktree as a sibling of the repo directory instead.

### gwtadd

Create a worktree for a **new** branch.

```bash
# Usage: gwtadd [--sibling] <branch-name>
gwtadd() {
    local use_sibling=false
    if [[ "$1" == "--sibling" ]]; then
        use_sibling=true
        shift
    fi

    local branch_name="$1"

    if [ -z "$branch_name" ]; then
        echo "Usage: gwtadd [--sibling] <branch-name>"
        return 1
    fi

    local remote_url=$(git config --get remote.origin.url)
    local repo_name=$(basename "$remote_url" .git)
    local repo_root=$(git rev-parse --show-toplevel)

    local safe_branch_name=$(echo "$branch_name" | sed 's/[\/:]/-/g')

    local worktree_path
    if $use_sibling; then
        local worktrees_parent=$(dirname "$repo_root")
        worktree_path="${worktrees_parent}/${repo_name}-${safe_branch_name}"
    else
        worktree_path="${repo_root}/.worktrees/${repo_name}-${safe_branch_name}"
        mkdir -p "${repo_root}/.worktrees"
    fi

    git worktree add "$worktree_path" -b "$branch_name"

    echo "Worktree created at: $worktree_path"
}
```

### gwtexisting

Create a worktree for an **existing** branch (local or remote).

```bash
# Usage: gwtexisting [--sibling] <existing-branch-name>
gwtexisting() {
    local use_sibling=false
    if [[ "$1" == "--sibling" ]]; then
        use_sibling=true
        shift
    fi

    local branch_name="$1"

    if [ -z "$branch_name" ]; then
        echo "Usage: gwtexisting [--sibling] <existing-branch-name>"
        return 1
    fi

    local remote_url=$(git config --get remote.origin.url)
    local repo_name=$(basename "$remote_url" .git)
    local repo_root=$(git rev-parse --show-toplevel)

    local safe_branch_name=$(echo "$branch_name" | sed 's/[\/:]/-/g')

    local worktree_path
    if $use_sibling; then
        local worktrees_parent=$(dirname "$repo_root")
        worktree_path="${worktrees_parent}/${repo_name}-${safe_branch_name}"
    else
        worktree_path="${repo_root}/.worktrees/${repo_name}-${safe_branch_name}"
        mkdir -p "${repo_root}/.worktrees"
    fi

    # Ensure a local tracking branch exists for the remote branch
    if ! git show-ref --verify --quiet "refs/heads/$branch_name"; then
        if git show-ref --verify --quiet "refs/remotes/origin/$branch_name"; then
            git branch --track "$branch_name" "origin/$branch_name"
        else
            echo "error: branch '$branch_name' not found locally or on origin"
            return 1
        fi
    fi

    git worktree add "$worktree_path" "$branch_name"

    echo "Worktree created at: $worktree_path"
}
```

### gwtremove

Remove a worktree with optional force (`-f`) and branch deletion (`-D`).

If the worktree has uncommitted changes and `-f` wasn't passed, prompts before continuing.
If `-D` wasn't passed, prompts whether to delete the branch after removal.

```bash
# Usage: gwtremove [--sibling] [-f] [-D] <worktree-name>
gwtremove() {
    local use_sibling=false
    if [[ "$1" == "--sibling" ]]; then
        use_sibling=true
        shift
    fi

    local force=false
    local delete_branch=false

    while getopts "fD" opt; do
        case $opt in
            f) force=true ;;
            D) delete_branch=true ;;
            *) echo "Usage: gwtremove [--sibling] [-f] [-D] <worktree-name>"; return 1 ;;
        esac
    done
    shift $((OPTIND - 1))
    OPTIND=1

    local worktree_name="$1"

    if [ -z "$worktree_name" ]; then
        echo "Usage: gwtremove [--sibling] [-f] [-D] <worktree-name>"
        return 1
    fi

    local repo_root=$(git rev-parse --show-toplevel)
    local remote_url=$(git config --get remote.origin.url)
    local repo_name=$(basename "$remote_url" .git)

    # Resolve worktree path
    local worktree_path
    if [[ "$worktree_name" = /* ]]; then
        worktree_path="$worktree_name"
    elif $use_sibling; then
        local worktrees_parent=$(dirname "$repo_root")
        worktree_path="${worktrees_parent}/${worktree_name}"
    else
        if [[ "$worktree_name" = ${repo_name}-* ]]; then
            worktree_path="${repo_root}/.worktrees/${worktree_name}"
        else
            worktree_path="${repo_root}/.worktrees/${repo_name}-${worktree_name}"
        fi
    fi

    if [ ! -d "$worktree_path" ]; then
        echo "Worktree not found: $worktree_path"
        return 1
    fi

    # Resolve the branch name from the worktree
    local branch_name
    branch_name=$(git worktree list --porcelain \
        | awk -v p="$worktree_path" '
            $1 == "worktree" && $2 == p { found=1; next }
            found && $1 == "branch" {
                gsub(/^refs\/heads\//, "", $2);
                print $2;
                exit
            }
        ')

    # Check if worktree has uncommitted changes
    local needs_force=false
    if ! $force; then
        local dirty
        dirty=$(git -C "$worktree_path" status --porcelain 2>/dev/null)
        if [ -n "$dirty" ]; then
            needs_force=true
        fi
    fi

    # Collect all user decisions upfront
    if $needs_force; then
        echo "Worktree has uncommitted changes:"
        git -C "$worktree_path" status --short
        echo -n "Force remove? (y/N): "
        read -r force_reply
        if [[ ! "$force_reply" =~ ^[Yy]$ ]]; then
            return 1
        fi
        force=true
    fi

    if [ -n "$branch_name" ] && ! $delete_branch; then
        echo -n "Delete branch '$branch_name'? (y/N): "
        read -r branch_reply
        if [[ "$branch_reply" =~ ^[Yy]$ ]]; then
            delete_branch=true
        fi
    fi

    # Execute: remove worktree
    if $force; then
        git worktree remove --force "$worktree_path" || return 1
    else
        git worktree remove "$worktree_path" || return 1
    fi

    echo "Worktree removed: $worktree_path"

    # Execute: delete branch
    if [ -n "$branch_name" ] && $delete_branch; then
        git branch -D "$branch_name"
        echo "Branch deleted: $branch_name"
    fi
}
```

## Git Tag Helpers

Semantic versioning helpers that pair well with the worktree workflow.

### latesttag

Print the latest semantic version tag in the repo.

```bash
latesttag() {
    git tag --sort=-v:refname | grep -E '^v?[0-9]+\.[0-9]+\.[0-9]+' | head -n 1
}
```

### bumptag

Calculate the next tag without creating it. Useful for scripting or previewing.

```bash
# Usage: bumptag <major|minor|patch>
bumptag() {
    local bump_type="$1"

    if [[ -z "$bump_type" ]]; then
        echo "Usage: bumptag <major|minor|patch>"
        return 1
    fi

    if [[ "$bump_type" != "major" && "$bump_type" != "minor" && "$bump_type" != "patch" ]]; then
        echo "Error: bump type must be 'major', 'minor', or 'patch'"
        return 1
    fi

    local latest_tag=$(latesttag)

    if [[ -z "$latest_tag" ]]; then
        echo "No semantic version tags found. Starting with v0.0.1"
        echo "v0.0.1"
        return 0
    fi

    # Remove 'v' prefix if present
    local version="${latest_tag#v}"

    # Split version into major.minor.patch
    local major=$(echo "$version" | cut -d. -f1)
    local minor=$(echo "$version" | cut -d. -f2)
    local patch=$(echo "$version" | cut -d. -f3)

    case "$bump_type" in
        major)
            major=$((major + 1))
            minor=0
            patch=0
            ;;
        minor)
            minor=$((minor + 1))
            patch=0
            ;;
        patch)
            patch=$((patch + 1))
            ;;
    esac

    local new_tag="v${major}.${minor}.${patch}"
    echo "$new_tag"
}
```

### createtag

Create an annotated git tag at the next semantic version.

```bash
# Usage: createtag <major|minor|patch>
createtag() {
    local bump_type="$1"

    if [[ -z "$bump_type" ]]; then
        echo "Usage: createtag <major|minor|patch>"
        return 1
    fi

    local new_tag=$(bumptag "$bump_type")

    if [[ -z "$new_tag" ]]; then
        echo "Error: Failed to generate new tag"
        return 1
    fi

    git tag -a "$new_tag" -m "$new_tag"
    echo "Created annotated tag: $new_tag"
}
```
