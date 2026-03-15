import json
import os
import subprocess

def run_git(commands):
    try:
        # We use shell=True to help Windows handle the commands better
        subprocess.run(commands, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"Git Error: {e.stderr}")
        return False
    return True

def update_github():
    print("\n--- Syncing with GitHub ---")
    
    # 1. Pull latest (using master branch)
    run_git(["git", "pull", "origin", "master"])
    
    # 2. Add, Commit, Push
    print("Pushing updates to GitHub...")
    if run_git(["git", "add", "."]):
        # The commit message is automatic
        if run_git(["git", "commit", "-m", "Automatic update via Portfolio Manager"]):
            if run_git(["git", "push", "origin", "master"]):
                print("✅ LIVE ON GITHUB!")
                return
    print("❌ Upload failed. Make sure you are connected to the internet.")

def main():
    print("==========================")
    print(" KISE PORTFOLIO MANAGER ")
    print("==========================")
    
    # Load existing data
    filename = 'projects.json'
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []

    # Get Input
    title = input("\nProject Title: ")
    url = input("Video Filename (e.g., loganima/1.mp4): ")
    desc = input("Description: ")
    print("1: Logo | 2: Text | 3: Drawing")
    cat_choice = input("Category (1-3): ")
    
    cats = {"1": "logo", "2": "text", "3": "drawing"}
    category = cats.get(cat_choice, "logo")

    # Update Data
    data.append({
        "title": title,
        "url": url,
        "description": desc,
        "category": category
    })

    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"\nSaved '{title}' locally.")

    # Auto Upload
    update_github()
    print("\nDone! Refresh your website in a moment.")
    input("Press Enter to close...")

if __name__ == "__main__":
    main()