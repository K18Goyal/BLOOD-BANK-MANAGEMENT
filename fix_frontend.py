import os
import re

frontend_dir = 'c:/Users/khush/OneDrive/Desktop/BloodBank/frontend'
for root, dirs, files in os.walk(frontend_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.js'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace localhost URLs with relative URLs
            new_content = re.sub(r'http://(?:127\.0\.0\.1|localhost):5000(/api)', r'\1', content)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Fixed {file}")

print("Frontend URLs fixed.")
