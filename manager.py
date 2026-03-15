import json
import os
import subprocess
import time
import shutil  # To copy the file you select
from tkinter import filedialog, Tk # To open the file selector

# --- CONFIG ---
FOLDERS = {
    "1": "loganima",
    "2": "textan",
    "3": "drawan"
}

def run_git(commands):
    result = subprocess.run(commands, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"DONE: {' '.join(commands)}")
        return True
    else:
        print(f"GIT ERROR: {result.stderr}")
        return False

def select_file():
    """Opens a Windows file explorer to pick a video"""
    root = Tk()
    root.withdraw() # Hide the tiny white window
    root.attributes('-topmost', True) # Bring the selector to the front
    file_path = filedialog.askopenfilename(
        title="Select your animation video",
        filetypes=[("Video files", "*.mp4 *.mov *.webm")]
    )
    root.destroy()
    return file_path

def main():
    print("==============================")
    print("   KISE MANUAL FILE UPLOADER")
    print("==============================")

    # 1. Pick the video file from your computer
    print("\n[STEP 1] Please select your video file...")
    source_file = select_file()

    if not source_file:
        print("No file selected. Exiting.")
        return
    
    filename = os.path.basename(source_file)
    print(f"Selected: {filename}")

    # 2. Select Category
    print("\n[STEP 2] Which category is this for?")
    print("1: Logo Animation")
    print("2: Text Animation")
    print("3: Drawing Animation")
    choice = input("Choice (1-3): ")
    
    target_dir = FOLDERS.get(choice)
    if not target_dir:
        print("Invalid choice.")
        return

    # Create folder if it doesn't exist
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 3. Copy the file into the project folder
    destination_path = os.path.join(target_dir, filename)
    print(f"Copying file to {destination_path}...")
    shutil.copy2(source_file, destination_path)

    # 4. Details
    auto_title = filename.split('.')[0].replace('_', ' ').replace('-', ' ').title()
    title = input(f"Title [{auto_title}]: ") or auto_title
    desc = input("Description: ")

    # 5. Update JSON
    try:
        with open('projects.json', 'r') as f:
            data = json.load(f)
    except:
        data = []

    cat_map = {"1": "logo", "2": "text", "3": "drawing"}
    data.append({
        "title": title,
        "url": f"{target_dir}/{filename}",
        "description": desc,
        "category": cat_map[choice]
    })

    with open('projects.json', 'w') as f:
        json.dump(data, f, indent=4)

    # 6. Upload to GitHub
    print("\n[STEP 3] Uploading to GitHub...")
    run_git(["git", "add", "."])
    run_git(["git", "commit", "-m", f"Added {filename}"])
    if run_git(["git", "push", "origin", "master"]):
        print("\n✅ SUCCESS! File copied and uploaded to GitHub.")
    else:
        print("\n❌ UPLOAD FAILED. Check your terminal for errors.")

    input("\nPress Enter to close...")

if __name__ == "__main__":
    main()