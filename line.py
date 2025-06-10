import os
import argparse
import csv
from pathlib import Path

def count_lines_words(file_path):
    lines = 0
    words = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line:  # Only count non-empty lines
                    lines += 1
                    words += len(stripped_line.split())
    except (UnicodeDecodeError, PermissionError):
        # 忽略二进制文件或无权限文件
        return 0, 0
    return lines, words

def should_exclude(path, exclude_dirs, exclude_files):
    path = Path(path).resolve()
    for excluded in exclude_dirs + exclude_files:
        excluded_path = Path(excluded).resolve()
        try:
            if path == excluded_path or excluded_path in path.parents:
                return True
        except (PermissionError, FileNotFoundError):
            continue
    return False

def scan_directory(directory, extensions, exclude_dirs, exclude_files):
    results = []
    file_count = 0
    processed_count = 0
    # 先计算总文件数用于进度显示
    print("正在扫描文件...")
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), exclude_dirs, exclude_files)]
        file_count += len([f for f in files if not should_exclude(os.path.join(root, f), exclude_dirs, exclude_files)])
    print(f"共发现 {file_count} 个文件，开始统计...")
    for root, dirs, files in os.walk(directory):
        # 修改dirs列表来排除目录（原地修改）
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), exclude_dirs, exclude_files)]
        for file in files:
            file_path = os.path.join(root, file)
            if should_exclude(file_path, exclude_dirs, exclude_files):
                continue
            if extensions:
                ext = os.path.splitext(file)[1][1:]  # 去掉点号
                if ext.lower() not in [e.lower() for e in extensions]:
                    continue
            processed_count += 1
            print(f"\r处理进度: {processed_count}/{file_count} ({processed_count/file_count:.1%}) | 当前文件: {file_path}", end='', flush=True)
            lines, words = count_lines_words(file_path)
            if lines > 0:  # 只统计有效的文件
                results.append({
                    'file': file_path,
                    'lines': lines,
                    'words': words
                })
    print("\n统计完成!")
    return results

def save_to_csv(results, csv_file):
    print(f"正在保存结果到 {csv_file}...")
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['file', 'lines', 'words'])
        writer.writeheader()
        writer.writerows(results)
    print("保存完成!")

def main():
    parser = argparse.ArgumentParser(description='统计目录下文件的代码行数和字数')
    parser.add_argument('--ext', nargs='*', help='要统计的文件扩展名列表', default=[])
    parser.add_argument('--exclude-dirs', nargs='*', help='要排除的目录列表', default=[])
    parser.add_argument('--csv', help='输出CSV文件路径')
    #args = parser.parse_args()
    class args:
        csv = "lines.csv"
        ext = ['py', 'c']
        exclude_dirs = ".ENV build TESTWORK Termination4.build Termination4.dist Termination4.onefile-build TESTWORK/.ENV TESTWORK/Build TLUI/.TEST_ENV .inf/.ENV tools-ocr/stb".split(" ")
    current_dir = os.getcwd()
    results = scan_directory(current_dir, args.ext, args.exclude_dirs, [])
    if args.csv:
        save_to_csv(results, args.csv)
    total_lines = sum(r['lines'] for r in results)
    total_words = sum(r['words'] for r in results)
    print(f"\n统计结果:")
    print(f"文件总数: {len(results)}")
    print(f"总行数: {total_lines}")
    print(f"总字数: {total_words}")

if __name__ == '__main__':
    main()
    #c:/Users/Lenovo/Desktop/Termination4/line.py --ext py c --exclude-dirs .ENV build TESTWORK Termination4.build Termination4.dist Termination4.onefile-build TESTWORK/.ENV TESTWORK/Build TLUI/.TEST_ENV tools-ocr/stb --csv lines.csv