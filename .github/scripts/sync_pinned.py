import html, json, re, urllib.request

PROFILE = 'https://github.com/HigorADS?tab=overview'
request = urllib.request.Request(PROFILE, headers={'User-Agent': 'higor-galhardo-portfolio-sync'})
with urllib.request.urlopen(request, timeout=30) as response:
    page = response.read().decode('utf-8', 'ignore')

match = re.search(r'<ol[^>]*js-pinned-items-reorder-list[^>]*>(.*?)</ol>', page, re.S)
if not match:
    raise SystemExit('GitHub pinned list not found')

items = []
for index, card in enumerate(re.findall(r'<li[^>]*pinned-item-list-item[^>]*>.*?</li>', match.group(1), re.S)):
    link = re.search(r'href="/HigorADS/([^"/?#]+)"[^>]*>.*?<span[^>]*class="repo"[^>]*>([^<]+)</span>', card, re.S)
    if not link:
        continue
    name = html.unescape(link.group(2).strip())
    desc_match = re.search(r'class="[^"]*pinned-item-desc[^"]*"[^>]*>(.*?)</p>', card, re.S)
    description = re.sub(r'<[^>]+>', ' ', desc_match.group(1)) if desc_match else 'Projeto público selecionado no GitHub.'
    description = ' '.join(html.unescape(description).split())
    color = '#f6c177' if index % 2 == 0 else '#f0883e'
    items.append({
        'name': name,
        'description': description,
        'language': 'GitHub',
        'color': color,
        'href': f'https://github.com/HigorADS/{name}',
    })

if not items:
    raise SystemExit('No pinned repositories found')
with open('pinned.json', 'w', encoding='utf-8') as output:
    json.dump(items, output, ensure_ascii=False, indent=2)
    output.write('\n')
print(f'Synced {len(items)} pinned repositories')
