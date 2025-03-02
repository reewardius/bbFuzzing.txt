import re
import json
import tempfile
from collections import Counter
import argparse

def extract_domains(line):
    match = re.search(r'https?://([^/]+)', line)
    return match.group(1) if match else None

def json_to_txt(json_file):
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for result in data.get("results", []):
        url = result.get("url")
        if url:
            temp_file.write(url + "\n")
    
    temp_file.close()
    return temp_file.name

def process_file(input_file, output_file, fp_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    domains = [extract_domains(line) for line in lines]
    domain_counts = Counter(filter(None, domains))
    
    frequent_domains = {domain for domain, count in domain_counts.items() if count > 20}
    
    with open(fp_file, 'w', encoding='utf-8') as fp_out:
        for domain in sorted(frequent_domains):
            fp_out.write(domain + "\n")
    
    filtered_lines = [line for line in lines if extract_domains(line) not in frequent_domains]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(filtered_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--json_file", help="Input JSON file", required=True)
    parser.add_argument("-o", "--output_file", help="Output text file", required=True)
    parser.add_argument("-fp", "--fp_file", help="File to save frequent domains", required=True)
    args = parser.parse_args()
    
    temp_file = json_to_txt(args.json_file)
    process_file(temp_file, args.output_file, args.fp_file)