#!/usr/bin/env python3

import os
import subprocess
import sys

def run_command(command, cwd=None, allow_failure=False):
    """Run a shell command. Exit if it fails, unless allow_failure=True."""
    try:
        result = subprocess.run(command, cwd=cwd, shell=True, check=not allow_failure, text=True, capture_output=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        if not allow_failure:
            print(f"❌ Error running command: {command}")
            print(e.stderr)
            sys.exit(1)
        return None

def has_staged_changes():
    """Check if there are staged changes using `git diff --cached --quiet`"""
    result = subprocess.run("git diff --cached --quiet", shell=True)
    return result.returncode != 0  # if not quiet, means there ARE staged changes

def main():
    print("🚀 GitHub Auto-Push Script (Remote: github_origin)")
    print("-" * 50)

    # 1. Ask for GitHub repo URL
    repo_url = input("👉 Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): ").strip()

    if not repo_url:
        print("❌ Repository URL is required. Exiting.")
        sys.exit(1)

    # 2. Check if current directory is a Git repo; if not, initialize one
    if not os.path.exists(".git"):
        print("📂 Initializing new Git repository...")
        run_command("git init")

    # Define remote name
    remote_name = "github_origin"

    # 3. Check if remote 'github_origin' exists; if not, add it
    try:
        existing_remotes = run_command("git remote")
        remotes = existing_remotes.splitlines() if existing_remotes else []
        if remote_name not in remotes:
            print(f"🔗 Adding remote '{remote_name}' -> {repo_url}")
            run_command(f"git remote add {remote_name} {repo_url}")
        else:
            print(f"🔁 Remote '{remote_name}' already exists. Updating URL just in case...")
            run_command(f"git remote set-url {remote_name} {repo_url}")
    except Exception as e:
        print(f"⚠️  Could not check remotes: {e}")

    # 4. Add all files
    print("📥 Adding all files...")
    run_command("git add .")

    # 5. Commit changes — ONLY if there are staged changes
    if has_staged_changes():
        commit_message = input("📝 Enter commit message (default: 'Auto commit'): ").strip()
        if not commit_message:
            commit_message = "Auto commit"
        print(f"✅ Committing with message: '{commit_message}'")
        run_command(f'git commit -m "{commit_message}"')
    else:
        print("ℹ️  No changes staged to commit. Skipping commit step.")

    # 6. Get current branch name
    try:
        current_branch = run_command("git rev-parse --abbrev-ref HEAD")
    except:
        current_branch = "main"  # fallback

    # 7. Push to remote
    print(f"⬆️  Pushing to remote '{remote_name}' ({repo_url}) on branch '{current_branch}'...")
    try:
        # Try to push
        run_command(f"git push -u {remote_name} {current_branch}")
    except:
        print("🔄 Remote has changes. Attempting to pull first...")
        try:
            # Pull with rebase to avoid merge commit
            run_command(f"git pull {remote_name} {current_branch} --rebase")
            run_command(f"git push -u {remote_name} {current_branch}")
        except:
            print("❌ Pull failed. You may need to manually resolve conflicts.")
            sys.exit(1)

    print("✅ Successfully pushed to GitHub!")

if __name__ == "__main__":
    main()