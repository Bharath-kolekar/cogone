import re

with open('backend/app/routers/orchestration_router.py') as f:
    content = f.read()
    count = len(re.findall(r'@router\.(get|post|put|delete|patch)', content))
    print(f'orchestration_router.py now has {count} endpoints')


