import re

def convert_sql(filepath):
    with open(filepath, 'r') as f:
        sql = f.read()
        
    # Remove USE statements
    sql = re.sub(r'USE\s+\w+;', '', sql, flags=re.IGNORECASE)
    
    # Replace AUTO_INCREMENT with AUTOINCREMENT
    sql = re.sub(r'INT\s+AUTO_INCREMENT\s+PRIMARY\s+KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT', sql, flags=re.IGNORECASE)
    sql = re.sub(r'AUTO_INCREMENT', 'AUTOINCREMENT', sql, flags=re.IGNORECASE)
    
    # SQLite does not support ENUM. Replace with TEXT
    sql = re.sub(r'ENUM\([^)]+\)', 'TEXT', sql, flags=re.IGNORECASE)
    
    # Remove database creation
    sql = re.sub(r'CREATE\s+DATABASE\s+IF\s+NOT\s+EXISTS\s+\w+;', '', sql, flags=re.IGNORECASE)

    with open(filepath, 'w') as f:
        f.write(sql)

convert_sql('c:/Users/khush/OneDrive/Desktop/BloodBank/database.sql')
convert_sql('c:/Users/khush/OneDrive/Desktop/BloodBank/DummyData.sql')
print("SQL converted")
