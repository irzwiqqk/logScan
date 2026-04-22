import argparse
import re
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--file', required=True, help = 'Path to the logs file')
parser.add_argument('--verbose', action = 'store_true', help = 'Display the logs')
args = parser.parse_args()

try:
    with open(args.file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Ошибка: Файл '{args.file}' не найден!")
    sys.exit(1)
results = []
for line in lines:
    search_IP = re.search(r'\d+\.\d+\.\d+\.\d+', line)
    search_HASH = re.search(r'[a-fA-F0-9]{64}', line)
    ip_value = None
    hash_value = None
    if search_IP or search_HASH:
        if search_IP:
            ip_value = search_IP.group(0)
        if search_HASH:
            hash_value = search_HASH.group(0)
        results.append({
            'ip': ip_value,
            'hash': hash_value,
            'raw': line.strip()
        })
        if args.verbose:
            print(f"Найдено: IP:  {ip_value} | HASH: {hash_value}")
if results:
    print(f"Количество найденных угроз - {len(results)}")
else:
    print("Файл чист, ничего не найдено")

if results:
    with(open("report.txt", 'w', encoding= 'utf-8')) as report:
        report.write(f"Отчет о сканировании:\n")
        for i in results:
            report.write(f"IP: {i['ip']} | HASH: {i['hash']}\n")
    print("Результаты также сохранены в report.txt")
else:
    print("Файл чист, ничего не найдено")