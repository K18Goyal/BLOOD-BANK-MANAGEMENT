import os
import re

def fix_routes(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Remove is_connected blocks
                content = re.sub(r'(\s+)if not conn\.is_connected\(\):[\s]+conn\.reconnect\(\)', '', content)
                
                # Replace all %s with ? globally (since they are only used in SQL queries here)
                content = content.replace('%s', '?')

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed {file}")

fix_routes('c:/Users/khush/OneDrive/Desktop/BloodBank/routes')
