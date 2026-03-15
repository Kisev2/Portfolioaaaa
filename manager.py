import json
import os
import subprocess

def update_github():
    print("\n--- Uploading to GitHub ---")
    try:
        # These commands talk to Git on your computer
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Added new video via Manager"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Successfully updated your website!")
    except Exception as e:
        print(f"Error updating GitHub: {e}")

def main():
    print("----------------------")
    print("PORTFOLIO MANAGER TOOL")
    print("----------------------")
    
    # Check if projects.json exists and is not empty
    if os.path.exists('projects.json') and os.path.getsize('projects.json') > 0:
        with open('projects.json', 'r') as f:
            try:
                data = json.load(f)
            except:
                data = []
    else:
        data = []

    # 1. Get Input from you
    title = input("Project Title: ")
    url = input("Video URL/Path (e.g. loganima/5.mp4): ")
    desc = input("Description: ")
    print("Categories: 1=logo, 2=text, 3=drawing")
    cat_choice = input("Choice (1-3): ")
    
    cats = {"1": "logo", "2": "text", "3": "drawing"}
    category = cats.get(cat_choice, "logo")

    # 2. Add the new video to the list
    new_project = {
        "title": title,
        "url": url,
        "description": desc,
        "category": category
    }
    
    data.append(new_project)

    # 3. Save the file
    with open('projects.json', 'w') as f:
        json.dump(data, f, indent=4)

    print(f"\nSUCCESS: Added '{title}' to {category} category.")

    # 4. Ask to upload
    confirm = input("\nPush to GitHub now? (y/n): ")
    if confirm.lower() == 'y':
        update_github()
    else:
        print("Saved locally, but not uploaded.")

if __name__ == "__main__":
    main()