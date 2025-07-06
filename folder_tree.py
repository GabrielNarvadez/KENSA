import os

# Folders and files to exclude from the listing
EXCLUDE = {
    'venv', 'node_modules', '.git', '__pycache__', '.mypy_cache__', '.idea',
    '.DS_Store', '.env', '.vscode', '.pytest_cache', 'media', 'staticfiles'
}

EXCLUDE_EXTENSIONS = {'.db', '.sqlite3', '.pyc', '.log', '.js'}

def print_tree(startpath, prefix=""):
    entries = sorted(os.listdir(startpath))
    entries = [e for e in entries if e not in EXCLUDE and not any(e.endswith(ext) for ext in EXCLUDE_EXTENSIONS)]
    for i, name in enumerate(entries):
        path = os.path.join(startpath, name)
        is_last = i == len(entries) - 1
        print(prefix + ("└── " if is_last else "├── ") + name)
        if os.path.isdir(path):
            print_tree(path, prefix + ("    " if is_last else "│   "))

if __name__ == "__main__":
    print("PROJECT DIRECTORY TREE:\n")
    print_tree(".")
