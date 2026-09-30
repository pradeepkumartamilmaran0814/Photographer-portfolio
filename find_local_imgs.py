import os

for root, dirs, files in os.walk('.'):
    if '.git' in root or '.venv' in root or 'brain' in root:
        continue
    for f in files:
        if f.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            # print all images
            p = os.path.join(root, f)
            print(f, os.path.getsize(p))
