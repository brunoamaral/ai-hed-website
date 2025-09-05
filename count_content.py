#!/usr/bin/env python3
"""
Content Word and Character Counter
Counts words and characters in markdown and HTML files in the content directory.
The goal of this file is to help measure the size of our knowledge base to use with the chatbot.
"""

import os
import re
import argparse
from pathlib import Path
from collections import defaultdict


def clean_markdown_html(text):
    """Remove markdown and HTML formatting to count only actual content."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove markdown links but keep the text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Remove markdown image syntax
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', text)
    
    # Remove markdown headers
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)
    
    # Remove markdown emphasis
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    
    # Remove markdown code blocks
    text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    # Remove YAML front matter
    text = re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL | re.MULTILINE)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def count_words_chars(text):
    """Count words and characters in text."""
    # Clean the text
    clean_text = clean_markdown_html(text)
    
    # Count words (split by whitespace)
    words = len(clean_text.split()) if clean_text else 0
    
    # Count characters (excluding spaces)
    chars_no_spaces = len(clean_text.replace(' ', '')) if clean_text else 0
    
    # Count characters (including spaces)
    chars_with_spaces = len(clean_text) if clean_text else 0
    
    return words, chars_no_spaces, chars_with_spaces


def process_file(file_path):
    """Process a single file and return word/character counts."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        words, chars_no_spaces, chars_with_spaces = count_words_chars(content)
        
        return {
            'words': words,
            'chars_no_spaces': chars_no_spaces,
            'chars_with_spaces': chars_with_spaces,
            'success': True
        }
    except Exception as e:
        return {
            'words': 0,
            'chars_no_spaces': 0,
            'chars_with_spaces': 0,
            'success': False,
            'error': str(e)
        }


def main():
    parser = argparse.ArgumentParser(description='Count words and characters in markdown and HTML files')
    parser.add_argument('--content-dir', default='content', help='Content directory path (default: content)')
    parser.add_argument('--detailed', '-d', action='store_true', help='Show detailed breakdown by file')
    parser.add_argument('--by-type', '-t', action='store_true', help='Show breakdown by file type')
    
    args = parser.parse_args()
    
    content_dir = Path(args.content_dir)
    
    if not content_dir.exists():
        print(f"Error: Content directory '{content_dir}' does not exist")
        return 1
    
    # File extensions to process
    extensions = {'.md', '.html', '.htm'}
    
    # Statistics
    total_stats = defaultdict(int)
    file_stats = []
    type_stats = defaultdict(lambda: defaultdict(int))
    
    # Process all files
    for file_path in content_dir.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            result = process_file(file_path)
            
            if result['success']:
                # Add to totals
                total_stats['words'] += result['words']
                total_stats['chars_no_spaces'] += result['chars_no_spaces']
                total_stats['chars_with_spaces'] += result['chars_with_spaces']
                total_stats['files'] += 1
                
                # Add to type stats
                file_type = file_path.suffix.lower()
                type_stats[file_type]['words'] += result['words']
                type_stats[file_type]['chars_no_spaces'] += result['chars_no_spaces']
                type_stats[file_type]['chars_with_spaces'] += result['chars_with_spaces']
                type_stats[file_type]['files'] += 1
                
                # Store file stats for detailed view
                if args.detailed:
                    file_stats.append({
                        'path': str(file_path.relative_to(content_dir)),
                        'type': file_type,
                        **result
                    })
            else:
                print(f"Warning: Could not process {file_path}: {result['error']}")
    
    # Print results
    print("=" * 60)
    print("CONTENT WORD AND CHARACTER COUNT SUMMARY")
    print("=" * 60)
    
    print(f"\nTotal files processed: {total_stats['files']}")
    print(f"Total words: {total_stats['words']:,}")
    print(f"Total characters (no spaces): {total_stats['chars_no_spaces']:,}")
    print(f"Total characters (with spaces): {total_stats['chars_with_spaces']:,}")
    
    if args.by_type and type_stats:
        print("\n" + "=" * 40)
        print("BREAKDOWN BY FILE TYPE")
        print("=" * 40)
        
        for file_type, stats in sorted(type_stats.items()):
            print(f"\n{file_type.upper()} files:")
            print(f"  Files: {stats['files']}")
            print(f"  Words: {stats['words']:,}")
            print(f"  Characters (no spaces): {stats['chars_no_spaces']:,}")
            print(f"  Characters (with spaces): {stats['chars_with_spaces']:,}")
    
    if args.detailed and file_stats:
        print("\n" + "=" * 40)
        print("DETAILED BREAKDOWN BY FILE")
        print("=" * 40)
        
        # Sort by word count (descending)
        file_stats.sort(key=lambda x: x['words'], reverse=True)
        
        print(f"\n{'File':<50} {'Type':<6} {'Words':<8} {'Chars':<10}")
        print("-" * 80)
        
        for file_info in file_stats:
            print(f"{file_info['path']:<50} {file_info['type']:<6} {file_info['words']:<8,} {file_info['chars_no_spaces']:<10,}")
    
    return 0


if __name__ == '__main__':
    exit(main())
