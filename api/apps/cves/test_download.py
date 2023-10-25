from apps.cves.models import RedHatError
import json
import re
from concurrent.futures import ThreadPoolExecutor

def get_error_table(error_code):
    r, created = RedHatError.objects.get_or_create(error_code=error_code)
    return r.get_error_table()

def main():
    with open('/Users/danielhamilton/redhat/api/apps/cves/test_file.txt' , 'r') as f:
        data = f.read()
    pattern = r'CVE-\d{4}-\d{4,7}'
    error_codes = re.findall(pattern, data)
    with ThreadPoolExecutor() as executor:
        error_tables = list(executor.map(get_error_table, error_codes))
    with open('output.json', 'w') as f:
        json.dump(error_tables, f, indent=4)
   