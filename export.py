import os

def save_report(pc_name, content):
    filename = f"{pc_name}.txt"
    path = os.path.join(os.getcwd(), filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path