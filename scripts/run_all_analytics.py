#!/usr/bin/env python3
"""
Newsletter Analytics Suite

This script provides a unified interface to run both newsletter campaign analytics
and subscriber analytics reports.
"""

import sys
import subprocess
from pathlib import Path

def run_script(script_name, description):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"Running {description}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              cwd=Path(__file__).parent,
                              capture_output=False, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
        else:
            print(f"❌ {description} failed with exit code {result.returncode}")
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False
    
    return True

def main():
    """Main function to run all analytics"""
    print("🚀 Newsletter Analytics Suite")
    print("=" * 60)
    
    scripts = [
        ("newsletter_analytics.py", "Newsletter Campaign Analytics"),
        ("subscriber_analytics.py", "Subscriber Analytics")
    ]
    
    success_count = 0
    
    for script_name, description in scripts:
        script_path = Path(__file__).parent / script_name
        
        if not script_path.exists():
            print(f"❌ Script not found: {script_name}")
            continue
        
        if run_script(script_name, description):
            success_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary: {success_count}/{len(scripts)} analytics completed successfully")
    print('='*60)
    
    if success_count == len(scripts):
        print("🎉 All analytics completed successfully!")
        print("\nGenerated files can be found in the current directory:")
        print("📊 PNG charts for visualizations")
        print("📄 Markdown (.md) files for detailed reports")
        return 0
    else:
        print("⚠️  Some analytics failed. Check the output above for details.")
        return 1

if __name__ == "__main__":
    exit(main())
