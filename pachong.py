import re
from bs4 import BeautifulSoup
import pandas as pd

# 读取html源码
with open(r'C:\Users\70976\OneDrive\Desktop\学习\Facility Detail.html', encoding='utf-8') as f:
    html = f.read()

# 只定位到“Wellbore Data for Original Wellbore”下的内容
soup = BeautifulSoup(html, 'html.parser')
# 找到包含 Wellbore Data for Original Wellbore 的 tr
target_tr = None
for tr in soup.find_all('tr'):
    if tr.find(string=re.compile('Wellbore Data for Original Wellbore')):
        target_tr = tr
        break

# 找到目标tr后，向下找“Casing”和“Cement”行
results = []
if target_tr:
    next_tr = target_tr.find_next_sibling('tr')
    while next_tr:
        text = next_tr.get_text(separator=' ', strip=True)
        if 'Wellbore Completed' in text or 'Casing:' in text or 'Cement:' in text:
            if 'Casing:' in text:
                casing_info = text
                results.append({'type': 'casing', 'info': casing_info})
            elif 'Cement:' in text:
                cement_info = text
                results.append({'type': 'cement', 'info': cement_info})
        # 遇到下一个section就停
        if re.search(r'Wellbore Classification|Plugged Wellbore Data|Wellbore Data for', text) and not 'Casing:' in text and not 'Cement:' in text:
            break
        next_tr = next_tr.find_next_sibling('tr')

# 分组拼接
casing_keys = ['String Type', 'Hole Size', 'Size', 'Top', 'Depth', 'Weight', 'Citings Type']
cement_keys = ['Sacks', 'Top', 'Bottom', 'Determination Method']
rows = []
for i in range(0, len(results), 2):
    casing = {k: '0' for k in casing_keys}
    cement = {k: '0' for k in cement_keys}
    # 解析casing
    if i < len(results) and results[i]['type'] == 'casing':
        for k in casing_keys:
            m = re.search(rf'{k}:\s*([^,]*)', results[i]['info'])
            if m:
                casing[k] = m.group(1).strip() if m.group(1).strip() else '0'
    # 解析cement
    if i+1 < len(results) and results[i+1]['type'] == 'cement':
        for k in cement_keys:
            m = re.search(rf'{k}:\s*([^,]*)', results[i+1]['info'])
            if m:
                cement[k] = m.group(1).strip() if m.group(1).strip() else '0'
    rows.append({**casing, **cement})

# 拼出你要的格式（所有组平铺一行，可直接加入API等其他列）
out = []
for idx, row in enumerate(rows, 1):
    for k in casing_keys:
        out.append(f'Casing{idx} {k}: {row[k]}')
    for k in cement_keys:
        out.append(f'Cement{idx} {k}: {row[k]}')

print(', '.join(out))

# 如需输出excel/csv
header = []
data = []
for idx, row in enumerate(rows, 1):
    for k in casing_keys:
        header.append(f'Casing{idx} {k}')
    for k in cement_keys:
        header.append(f'Cement{idx} {k}')
for row in rows:
    data_row = []
    for k in casing_keys:
        data_row.append(row[k])
    for k in cement_keys:
        data_row.append(row[k])
    data.append(data_row)
df = pd.DataFrame([sum(data, [])], columns=header)
df.to_csv(r'C:\Users\70976\OneDrive\Desktop\学习\parsed_casing_cement.csv', index=False)
print('已保存至 parsed_casing_cement.csv')
