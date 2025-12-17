import os

def tree(path, prefix=""):
    files = sorted(os.listdir(path))
    for i, name in enumerate(files):
        full_path = os.path.join(path, name)
        connector = "└── " if i == len(files) - 1 else "├── "
        print(prefix + connector + name)
        if os.path.isdir(full_path):
            extension = "    " if i == len(files) - 1 else "│   "
            tree(full_path, prefix + extension)

print("trading_app/")
tree(".")
