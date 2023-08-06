import re
import yaml

from pathlib import Path

def parse_options(options_pat):
    options = []
    if options_pat:
        options = re.split(',', options_pat)
    return options

def parse_line(line):
    mingzhi = re.search('(\S+):', line).group(1)
    options_pat = re.search('\[(.*?)\]', line).group(1)
    options = parse_options(options_pat)
    return mingzhi, options

def create_mapping(mapping):
    mingzhi_mapping = {}
    lines = mapping.splitlines()
    for line in lines:
        print(line)
        mingzhi, options = parse_line(line)
        mingzhi_mapping[mingzhi] = options
    return mingzhi_mapping


if __name__ == "__main__":
    mapping = Path('./mapping.txt').read_text(encoding='utf-8')
    mingzhi_mapping = create_mapping(mapping)
    mingzhi_mapping = yaml.safe_dump(mingzhi_mapping, sort_keys=False, allow_unicode=True)
    Path('./mingzhi_mapping.yaml').write_text(mingzhi_mapping, encoding='utf-8')