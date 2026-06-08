with open(r'D:\code\cherry studio\复习\index.html', 'r', encoding='utf-8') as f:
    content = f.read()
if 'formulasHTML' in content:
    idx = content.find('formulasHTML')
    # Print the next 300 chars
    print(content[idx:idx+400])
else:
    print('formulasHTML not found')
