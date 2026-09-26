import json
import urllib.request

SOURCE = 'https://raw.githubusercontent.com/HigorADS/HigorADS/main/projects.json'
request = urllib.request.Request(SOURCE, headers={'User-Agent': 'higor-galhardo-portfolio-sync'})

with urllib.request.urlopen(request, timeout=30) as response:
    selected = json.loads(response.read().decode('utf-8'))

if not isinstance(selected, list):
    raise SystemExit('projects.json must contain a list')

items = []
for index, project in enumerate(selected):
    required = ('name', 'url', 'description')
    if not all(project.get(field) for field in required):
        raise SystemExit(f'Invalid project entry: {project!r}')

    tags = project.get('tags') or ['Projeto']
    items.append({
        'name': project['name'],
        'description': project['description'],
        'language': ' / '.join(tags[:3]),
        'color': '#f6c177' if index % 2 == 0 else '#f0883e',
        'href': project['url'],
    })

with open('pinned.json', 'w', encoding='utf-8') as output:
    json.dump(items, output, ensure_ascii=False, indent=2)
    output.write('\n')

print(f'Synced {len(items)} selected profile projects from HigorADS/projects.json')
