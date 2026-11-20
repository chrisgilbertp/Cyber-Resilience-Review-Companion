#!/usr/bin/env python3
"""Reproduce numerical checks for the IoT SSA higher-education review."""

import csv
import json
from pathlib import Path

def load_register(path):
    with open(path, newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def main():
    base = Path('.')
    register = load_register(base / 'study_register.csv')
    print(f'Publications in register: {len(register)}')
    
    # Simple count by country
    from collections import Counter
    countries = Counter(row.get('country', 'Unknown') for row in register)
    print('By country:')
    for c, n in sorted(countries.items()):
        print(f'  {c}: {n}')
    
    # Load numerical inputs
    with open(base / 'numerical_inputs.json') as f:
        inputs = json.load(f)
    
    print('\nNumerical inputs loaded.')
    print('Nigerian lab pilot paired completers:', inputs['nigerian_lab_pilot']['paired_completers'])
    print('Run complete. See results/ for full outputs when plots are enabled.')

if __name__ == '__main__':
    main()
