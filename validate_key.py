import subprocess, json, sys

def validate_serpapi(key):
    """验证 SerpAPI Key 是否有效"""
    r = subprocess.run([
        'curl','-s',
        f'https://serpapi.com/search?engine=google_jobs&q=AI+Marketing&location=United+States&gl=us&hl=en&api_key={key}'
    ], capture_output=True, text=True)
    d = json.loads(r.stdout)
    jobs = d.get('jobs_results', [])
    return len(jobs) > 0, f'✅ 有效，找到{len(jobs)}个职位' if jobs else f'❌ 无效：{d.get("error","未知错误")}'

def validate_caravo(key):
    """验证 Caravo Key 是否有效"""
    r = subprocess.run([
        'curl','-s','-X','POST',
        'https://www.caravo.ai/api/tools/google-data/jobs-search/execute',
        '-H', f'Authorization: Bearer {key}',
        '-H', 'Content-Type: application/json',
        '-d', '{"q":"AI Marketing","location":"United States","gl":"us","hl":"en","google_domain":"google.com"}'
    ], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout)
        jobs = d.get('output',{}).get('json',{}).get('jobs_results', [])
        return len(jobs) > 0, f'✅ 有效，找到{len(jobs)}个职位' if jobs else f'❌ 无效：{d}'
    except Exception as e:
        return False, f'❌ 无效：{str(e)}'

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法：python validate_key.py <数据源> <API Key>")
        print("数据源选项：serpapi 或 caravo")
        sys.exit(1)

    source = sys.argv[1]
    key = sys.argv[2]

    if source == 'serpapi':
        success, msg = validate_serpapi(key)
    elif source == 'caravo':
        success, msg = validate_caravo(key)
    else:
        print("错误：数据源只能是 serpapi 或 caravo")
        sys.exit(1)

    print(msg)
    sys.exit(0 if success else 1)
