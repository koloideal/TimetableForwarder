import json
from pprint import pprint
import re
from typing import Any

def process_schedule_items(items, top_tolerance=3.0, left_tolerance=30.0):
    if not items:
        return []

    # 1. Группируем слова в строки на основе 'top'
    items_sorted_by_top = sorted(items, key=lambda x: x['top'])
    lines = []
    if items_sorted_by_top:
        current_line = [items_sorted_by_top[0]]
        for item in items_sorted_by_top[1:]:
            avg_top = sum(i['top'] for i in current_line) / len(current_line)
            if abs(item['top'] - avg_top) <= top_tolerance:
                current_line.append(item)
            else:
                lines.append(current_line)
                current_line = [item]
        lines.append(current_line)

    # 2. В каждой строке группируем слова в колонки и форматируем вывод
    final_result = []
    for line in lines:
        line_sorted_by_left = sorted(line, key=lambda x: x['left'])
        
        columns = []
        if line_sorted_by_left:
            current_column = [line_sorted_by_left[0]]
            for item in line_sorted_by_left[1:]:
                avg_left = sum(i['left'] for i in current_column) / len(current_column)
                if abs(item['left'] - avg_left) <= left_tolerance:
                    current_column.append(item)
                else:
                    columns.append(current_column)
                    current_column = [item]
            columns.append(current_column)

        column_texts = []
        for col_group in columns:
            col_group.sort(key=lambda x: x['left'])
            column_texts.append(' '.join(item['text'] for item in col_group))
        
        joined_line = ' '.join(column_texts)
        
        avg_line_top = sum(item['top'] for item in line) / len(line)
        final_result.append({
            'top': avg_line_top,
            'line': joined_line
        })
        
    return final_result

def parse_schedule_from_ocr(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        ocr_data = json.load(f)

    lines = ocr_data["ParsedResults"][0]["TextOverlay"]["Lines"]

    date = None
    for line in lines:
        if "РАСПИСАНИЕ ЗАНЯТИЙ НА" in line["LineText"]:
            match = re.search(r'\d{2}\.\d{2}\.\d{4}', line["LineText"])
            if match:
                date = match.group(0)
            break
            
    test = []
    for line in lines:
        match = re.search(r'^\d{4}', rd := re.sub(r'["\']', '', line["LineText"]))
        if match:
            test.append({
                'group': rd,
                'top': line['Words'][0]['Top']
            })
    test.sort(key=lambda c: c['top'])

    res = []
    for k, group_info in enumerate(test):
        lower_bound = group_info['top']
        upper_bound = test[k+1]['top'] if k + 1 < len(test) else float('inf')

        items_in_range = filter(lambda x: lower_bound < x['Words'][0]['Top'] < upper_bound, lines)
        
        all_words = []
        for line_item in items_in_range:
            for word_item in line_item['Words']:
                all_words.append({
                    'text': word_item['WordText'], 
                    'top': word_item['Top'], 
                    'left': word_item['Left']
                })

        processed_lines = process_schedule_items(all_words, top_tolerance=3.0, left_tolerance=30.0)

        res.append({
            'group': group_info['group'],
            'schedule': processed_lines
        })

    pprint(res)

parse_schedule_from_ocr('response.json')
