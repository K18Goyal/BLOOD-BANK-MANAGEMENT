import os
import re
import sqlite3

def replace_in_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Replace mysql.connector with sqlite3
                content = content.replace('import mysql.connector', 'import sqlite3')
                content = content.replace('mysql.connector.Error', 'sqlite3.Error')
                content = content.replace('dictionary=True', '') # sqlite3 doesn't need this if row_factory is used

                # Replace %s with ? in execute and query strings
                # This is a bit tricky, but a simple regex works for standard cases
                # Find all SQL string literals (single or double quotes) containing %s
                def replacer(match):
                    return match.group(0).replace('%s', '?')
                
                content = re.sub(r'(["\'])(?:(?=(\\?))\2.)*?\1', replacer, content)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

replace_in_files('c:/Users/khush/OneDrive/Desktop/BloodBank/routes')
print("Migrated routes to sqlite3")
