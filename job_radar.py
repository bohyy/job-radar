import subprocess, json, datetime
import argparse

def fetch_serpapi(api_key, query, location, gl, token=None):
    """SerpAPI 版本抓取函数（免费）"""
    url = (f"https://serpapi.com/search?engine=google_jobs"
           f"&q={query.replace(' ','+')}&location={location.replace(' ','+')}"
           f"&gl={gl}&hl=en&api_key={api_key}")
    if token: url += f"&next_page_token={token}"
    r = subprocess.run(['curl','-s', url], capture_output=True, text=True)
    d = json.loads(r.stdout)
    return d.get('jobs_results',[]), d.get('serpapi_pagination',{}).get('next_page_token','')

def fetch_caravo(api_key, query, location, gl, token=None):
    """Caravo 版本抓取函数（付费）"""
    body = {"q":query,"location":location,"gl":gl,"hl":"en","google_domain":"google.com"}
    if token: body["next_page_token"] = token
    r = subprocess.run([
        'curl','-s','-X','POST',
        'https://www.caravo.ai/api/tools/google-data/jobs-search/execute',
        '-H', f'Authorization: Bearer {api_key}',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(body)
    ], capture_output=True, text=True)
    d = json.loads(r.stdout).get('output',{}).get('json',{})
    return d.get('jobs_results',[]), d.get('serpapi_pagination',{}).get('next_page_token','')

def is_new(p):
    """判断是否是24小时内新发职位"""
    return bool(p and any(x in p.lower() for x in ['hour','just now','minute']))

def is_remote(j):
    """判断是否是远程职位"""
    e = j.get('detected_extensions',{})
    return bool(e.get('work_from_home') or 'remote' in (j.get('location','')+j.get('title','')).lower())

def to_cn(p):
    """把英文时间翻译成中文"""
    if not p: return '时间未知'
    return (p.replace('hours ago','小时前').replace('hour ago','小时前')
             .replace('days ago','天前').replace('day ago','天前')
             .replace('minutes ago','分钟前').replace('just now','刚刚'))

def main(api_key, query, location, gl, source='serpapi'):
    """主函数：抓取职位并输出格式化结果"""
    fetch_func = fetch_serpapi if source == 'serpapi' else fetch_caravo

    # 抓取两页数据
    jobs1, tok = fetch_func(api_key, query, location, gl)
    jobs2, _   = fetch_func(api_key, query, location, gl, tok) if tok else ([], '')

    # 去重
    seen, pool = set(), []
    for j in jobs1 + jobs2:
        k = (j.get('title',''), j.get('company_name',''))
        if k not in seen: seen.add(k); pool.append(j)
    pool = pool[:20]

    # 格式化数据
    rows = []
    for j in pool:
        e  = j.get('detected_extensions',{})
        ao = j.get('apply_options',[])
        rows.append({
            'title':   j.get('title',''),
            'company': j.get('company_name',''),
            'loc':     j.get('location',''),
            'posted':  e.get('posted_at',''),
            'salary':  e.get('salary',''),
            'remote':  is_remote(j),
            'type':    e.get('schedule_type',''),
            'desc':    j.get('description','')[:180],
            'link':    ao[0].get('link','') if ao else ''
        })

    # 统计信息
    today = datetime.date.today().strftime('%Y年%-m月%-d日')
    new_c = sum(1 for r in rows if is_new(r['posted']))
    rem_c = sum(1 for r in rows if r['remote'])

    # 输出结果
    out = [
        f"🎯 {query} 职位雷达 · {today}",
        f"📦 共 {len(rows)} 个 · 🔥 {new_c} 个24h新发 · 🌐 {rem_c} 个远程",
        ""
    ]
    for i, r in enumerate(rows, 1):
        out += [
            "─"*32,
            f"**{i}. {r['title']}**" + (" 🔥NEW" if is_new(r['posted']) else ""),
            f"🏢 {r['company']}",
            f"📍 {r['loc']} · {'🌐 远程' if r['remote'] else '🏢 线下/混合'}",
            f"🕐 {to_cn(r['posted'])}",
        ]
        if r['salary']: out.append(f"💰 {r['salary']}")
        if r['type']:   out.append(f"💼 {r['type']}")
        if r['desc']:   out.append(f"📋 {r['desc']}...")
        out.append(f"🔗 申请：{r['link'] or '暂无链接'}")
        out.append("")

    # 趋势分析
    cos = list(dict.fromkeys(r['company'] for r in rows))[:5]
    sal = [r['salary'] for r in rows if r['salary']]
    out += [
        "═"*32,
        "📊 今日趋势",
        f"• 主要招聘方：{'、'.join(cos)}",
        f"• 薪资披露：{len(sal)} 个岗位{('，含 '+sal[0]) if sal else '，大多未披露'}",
        f"• 远程占比：{rem_c}/{len(rows)} ({rem_c*100//max(len(rows),1)}%)",
    ]

    print('\n'.join(out))
    return rows

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Job Radar - 每日职位自动抓取工具')
    parser.add_argument('--api-key', required=True, help='SerpAPI 或 Caravo API Key')
    parser.add_argument('--query', required=True, help='搜索关键词，例如：AI Marketing')
    parser.add_argument('--location', required=True, help='地区，例如：United States')
    parser.add_argument('--gl', required=True, help='国家代码，例如：us')
    parser.add_argument('--source', default='serpapi', choices=['serpapi', 'caravo'], help='数据源选择，默认 serpapi')

    args = parser.parse_args()
    main(args.api_key, args.query, args.location, args.gl, args.source)
