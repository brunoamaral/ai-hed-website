#!/usr/bin/env python3
"""
Subscriber Analytics Script

This script reads CSV files from the subscribers-reports directory and creates
visualizations of subscription and unsubscription trends over time.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import glob
import re
from datetime import datetime
import numpy as np

def extract_summary_stats(file_path):
    """Extract summary statistics from the header of the CSV file"""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    summary = {}
    for line in lines[:10]:  # Check first 10 lines for summary data
        if 'Total active subscribers' in line:
            summary['total_active'] = int(line.split(',')[1].strip())
        elif 'New subscribers today' in line:
            summary['new_today'] = int(line.split(',')[1].strip())
        elif 'New subscribers this month' in line:
            summary['new_this_month'] = int(line.split(',')[1].strip())
        elif 'New (Last year)' in line:
            summary['new_last_year'] = int(line.split(',')[1].strip())
        elif 'Unsubscribed (Last year)' in line:
            summary['unsubscribed_last_year'] = int(line.split(',')[1].strip())
    
    return summary

def load_subscriber_data(reports_dir="subscribers-reports"):
    """Load and process subscriber data from CSV files"""
    csv_files = glob.glob(f"{reports_dir}/*.csv")
    
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {reports_dir}")
    
    all_data = []
    source_files = []
    all_summaries = []
    
    for file in csv_files:
        print(f"Loading {file}...")
        
        # Extract summary statistics
        summary = extract_summary_stats(file)
        all_summaries.append(summary)
        
        # Read the daily data
        # Find the line where daily data starts
        with open(file, 'r') as f:
            lines = f.readlines()
        
        data_start_line = None
        for i, line in enumerate(lines):
            if 'Last year results (by day)' in line:
                data_start_line = i + 1  # Next line has the headers
                break
        
        if data_start_line is None:
            raise ValueError(f"Could not find daily data start in {file}")
        
        # Read daily data starting from the identified line
        daily_data = []
        for line in lines[data_start_line + 1:]:  # Skip the header line
            if line.strip() and ',' in line:
                parts = line.strip().split(',')
                if len(parts) >= 3 and parts[0] and parts[1] and parts[2]:
                    try:
                        date = pd.to_datetime(parts[0])
                        subscribes = int(parts[1]) if parts[1] else 0
                        unsubscribes = int(parts[2]) if parts[2] else 0
                        daily_data.append({
                            'Date': date,
                            'Subscribes': subscribes,
                            'Unsubscribes': unsubscribes
                        })
                    except (ValueError, TypeError):
                        continue  # Skip invalid lines
        
        if daily_data:
            df = pd.DataFrame(daily_data)
            all_data.append(df)
            source_files.append(Path(file).stem)
    
    if not all_data:
        raise ValueError("No valid daily data found in CSV files")
    
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Remove duplicates based on date
    combined_df = combined_df.drop_duplicates(subset=['Date'])
    
    # Sort by date
    combined_df = combined_df.sort_values('Date').reset_index(drop=True)
    
    # Calculate net subscribers and cumulative values
    combined_df['Net_Subscribers'] = combined_df['Subscribes'] - combined_df['Unsubscribes']
    combined_df['Cumulative_Subscribes'] = combined_df['Subscribes'].cumsum()
    combined_df['Cumulative_Unsubscribes'] = combined_df['Unsubscribes'].cumsum()
    combined_df['Cumulative_Net'] = combined_df['Net_Subscribers'].cumsum()
    
    return combined_df, source_files, all_summaries[0] if all_summaries else {}

def create_subscriber_visualizations(df, source_files, summary_stats):
    """Create various charts to analyze subscriber trends"""
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("Set2")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = '_'.join(source_files) if source_files else 'subscriber_analytics'
    
    # 1. Daily Subscriptions and Unsubscriptions Over Time
    fig1, ax1 = plt.subplots(figsize=(16, 8))
    
    # Filter to show only days with activity for better visualization
    active_days = df[(df['Subscribes'] > 0) | (df['Unsubscribes'] > 0)].copy()
    
    if len(active_days) > 0:
        width = 0.35
        x_positions = range(len(active_days))
        
        bars1 = ax1.bar([x - width/2 for x in x_positions], active_days['Subscribes'], 
                        width, label='Subscriptions', alpha=0.8, color='green')
        bars2 = ax1.bar([x + width/2 for x in x_positions], active_days['Unsubscribes'], 
                        width, label='Unsubscriptions', alpha=0.8, color='red')
        
        ax1.set_title('Daily Subscriptions and Unsubscriptions (Active Days Only)', 
                      fontsize=16, fontweight='bold', pad=20)
        ax1.set_xlabel('Date', fontsize=12)
        ax1.set_ylabel('Count', fontsize=12)
        ax1.set_xticks(x_positions)
        ax1.set_xticklabels([date.strftime('%Y-%m-%d') for date in active_days['Date']], 
                            rotation=45, ha='right', fontsize=9)
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if height > 0:
                    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                            f'{int(height)}', ha='center', va='bottom', fontsize=8)
    else:
        ax1.text(0.5, 0.5, 'No subscription activity found in the data', 
                ha='center', va='center', transform=ax1.transAxes, fontsize=14)
        ax1.set_title('Daily Subscriptions and Unsubscriptions', 
                      fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    chart1_file = f"{base_filename}_daily_activity_{timestamp}.png"
    plt.savefig(chart1_file, dpi=300, bbox_inches='tight')
    print(f"Chart 1 saved as: {chart1_file}")
    plt.close()
    
    # 2. Cumulative Subscriptions Over Time (Weekly Grouping)
    fig2, ax2 = plt.subplots(figsize=(16, 8))
    
    # Group data by week for cumulative trends
    df['Week'] = df['Date'].dt.to_period('W')
    weekly_cumulative = df.groupby('Week').agg({
        'Subscribes': 'sum',
        'Unsubscribes': 'sum',
        'Net_Subscribers': 'sum'
    }).reset_index()
    
    # Calculate cumulative values for weekly data
    weekly_cumulative['Cumulative_Subscribes'] = weekly_cumulative['Subscribes'].cumsum()
    weekly_cumulative['Cumulative_Unsubscribes'] = weekly_cumulative['Unsubscribes'].cumsum()
    weekly_cumulative['Cumulative_Net'] = weekly_cumulative['Net_Subscribers'].cumsum()
    
    # Convert Week period to string for plotting
    week_labels = [str(week) for week in weekly_cumulative['Week']]
    
    ax2.plot(week_labels, weekly_cumulative['Cumulative_Subscribes'], 
             marker='o', linewidth=2, markersize=4, color='green', label='Cumulative Subscriptions')
    ax2.plot(week_labels, weekly_cumulative['Cumulative_Unsubscribes'], 
             marker='s', linewidth=2, markersize=4, color='red', label='Cumulative Unsubscriptions')
    ax2.plot(week_labels, weekly_cumulative['Cumulative_Net'], 
             marker='^', linewidth=2, markersize=4, color='blue', label='Cumulative Net Subscribers')
    
    ax2.set_title('Cumulative Subscriber Trends Over Time (Weekly)', fontsize=16, fontweight='bold', pad=20)
    ax2.set_xlabel('Week', fontsize=12)
    ax2.set_ylabel('Cumulative Count', fontsize=12)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Show every nth week label to avoid overcrowding
    step = max(1, len(week_labels) // 20)  # Show roughly 20 labels max
    ax2.set_xticks(range(0, len(week_labels), step))
    ax2.set_xticklabels([week_labels[i] for i in range(0, len(week_labels), step)], 
                        rotation=45, ha='right')
    
    plt.tight_layout()
    chart2_file = f"{base_filename}_cumulative_trends_{timestamp}.png"
    plt.savefig(chart2_file, dpi=300, bbox_inches='tight')
    print(f"Chart 2 saved as: {chart2_file}")
    plt.close()
    
    # 3. Monthly Subscription Summary
    fig3, ax3 = plt.subplots(figsize=(14, 8))
    
    df['Month'] = df['Date'].dt.to_period('M')
    monthly_stats = df.groupby('Month').agg({
        'Subscribes': 'sum',
        'Unsubscribes': 'sum',
        'Net_Subscribers': 'sum'
    }).reset_index()
    
    if len(monthly_stats) > 0:
        x_positions = range(len(monthly_stats))
        width = 0.25
        
        bars1 = ax3.bar([x - width for x in x_positions], monthly_stats['Subscribes'], 
                        width, label='Subscriptions', alpha=0.8, color='green')
        bars2 = ax3.bar(x_positions, monthly_stats['Unsubscribes'], 
                        width, label='Unsubscriptions', alpha=0.8, color='red')
        bars3 = ax3.bar([x + width for x in x_positions], monthly_stats['Net_Subscribers'], 
                        width, label='Net Change', alpha=0.8, color='blue')
        
        ax3.set_title('Monthly Subscription Summary', fontsize=16, fontweight='bold', pad=20)
        ax3.set_xlabel('Month', fontsize=12)
        ax3.set_ylabel('Count', fontsize=12)
        ax3.set_xticks(x_positions)
        ax3.set_xticklabels([str(month) for month in monthly_stats['Month']], rotation=45)
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                if height != 0:
                    ax3.text(bar.get_x() + bar.get_width()/2., 
                            height + (0.5 if height > 0 else -0.5),
                            f'{int(height)}', ha='center', 
                            va='bottom' if height > 0 else 'top', fontsize=9)
    
    plt.tight_layout()
    chart3_file = f"{base_filename}_monthly_summary_{timestamp}.png"
    plt.savefig(chart3_file, dpi=300, bbox_inches='tight')
    print(f"Chart 3 saved as: {chart3_file}")
    plt.close()
    
    # 4. Subscription vs Unsubscription Rate Comparison
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    
    total_subs = df['Subscribes'].sum()
    total_unsubs = df['Unsubscribes'].sum()
    
    if total_subs > 0 or total_unsubs > 0:
        labels = ['Subscriptions', 'Unsubscriptions']
        sizes = [total_subs, total_unsubs]
        colors = ['lightgreen', 'lightcoral']
        explode = (0.05, 0.05)
        
        wedges, texts, autotexts = ax4.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                          colors=colors, explode=explode, startangle=90)
        ax4.set_title('Total Subscriptions vs Unsubscriptions', 
                      fontsize=16, fontweight='bold')
    else:
        ax4.text(0.5, 0.5, 'No subscription data available', 
                ha='center', va='center', transform=ax4.transAxes, fontsize=14)
    
    plt.tight_layout()
    chart4_file = f"{base_filename}_subscription_pie_{timestamp}.png"
    plt.savefig(chart4_file, dpi=300, bbox_inches='tight')
    print(f"Chart 4 saved as: {chart4_file}")
    plt.close()
    
    # 5. Weekly Subscription Activity (Non-cumulative)
    fig5, ax5 = plt.subplots(figsize=(14, 8))
    
    # Calculate weekly stats for this chart
    df_weekly = df.copy()
    df_weekly['Week'] = df_weekly['Date'].dt.to_period('W')
    weekly_stats = df_weekly.groupby('Week').agg({
        'Subscribes': 'sum',
        'Unsubscribes': 'sum',
        'Net_Subscribers': 'sum'
    }).reset_index()
    
    if len(weekly_stats) > 0:
        # Filter to show only weeks with activity for better readability
        active_weeks = weekly_stats[
            (weekly_stats['Subscribes'] > 0) | (weekly_stats['Unsubscribes'] > 0)
        ].copy()
        
        if len(active_weeks) > 0:
            active_week_labels = [str(week) for week in active_weeks['Week']]
            x_pos = range(len(active_weeks))
            
            ax5.bar(x_pos, active_weeks['Subscribes'], 
                   alpha=0.8, color='green', label='Weekly Subscriptions', width=0.6)
            if active_weeks['Unsubscribes'].sum() > 0:
                ax5.bar(x_pos, active_weeks['Unsubscribes'], 
                       alpha=0.8, color='red', label='Weekly Unsubscriptions', width=0.6)
            
            ax5.set_title('Weekly Subscription Activity (Active Weeks Only)', 
                         fontsize=16, fontweight='bold', pad=20)
            ax5.set_xlabel('Week', fontsize=12)
            ax5.set_ylabel('Count', fontsize=12)
            ax5.set_xticks(x_pos)
            ax5.set_xticklabels(active_week_labels, rotation=45, ha='right')
            ax5.legend()
            ax5.grid(True, alpha=0.3, axis='y')
            
            # Add value labels on bars
            for i, (subs, unsubs) in enumerate(zip(active_weeks['Subscribes'], active_weeks['Unsubscribes'])):
                if subs > 0:
                    ax5.text(i, subs + 0.1, str(int(subs)), ha='center', va='bottom', fontsize=9)
                if unsubs > 0:
                    ax5.text(i, unsubs + 0.1, str(int(unsubs)), ha='center', va='bottom', fontsize=9)
        else:
            ax5.text(0.5, 0.5, 'No weekly activity found in the data', 
                    ha='center', va='center', transform=ax5.transAxes, fontsize=14)
            ax5.set_title('Weekly Subscription Activity', fontsize=16, fontweight='bold', pad=20)
    else:
        ax5.text(0.5, 0.5, 'No data available for weekly analysis', 
                ha='center', va='center', transform=ax5.transAxes, fontsize=14)
    
    plt.tight_layout()
    chart5_file = f"{base_filename}_weekly_trends_{timestamp}.png"
    plt.savefig(chart5_file, dpi=300, bbox_inches='tight')
    print(f"Chart 5 saved as: {chart5_file}")
    plt.close()
    
    return [chart1_file, chart2_file, chart3_file, chart4_file, chart5_file]

def save_subscriber_summary_markdown(df, source_files, summary_stats):
    """Save subscriber analysis summary as a markdown file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = '_'.join(source_files) if source_files else 'subscriber_analytics'
    markdown_file = f"{base_filename}_summary_{timestamp}.md"
    
    with open(markdown_file, 'w') as f:
        f.write("# Subscriber Analytics Report\n\n")
        f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Source files:** {', '.join(source_files)}\n\n")
        
        # Summary Statistics
        f.write("## Summary Statistics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        
        if summary_stats:
            for key, value in summary_stats.items():
                readable_key = key.replace('_', ' ').title()
                f.write(f"| {readable_key} | {value:,} |\n")
        
        # Calculated Statistics
        f.write(f"| Total Subscriptions (Period) | {df['Subscribes'].sum():,} |\n")
        f.write(f"| Total Unsubscriptions (Period) | {df['Unsubscribes'].sum():,} |\n")
        f.write(f"| Net Subscriber Change | {df['Net_Subscribers'].sum():,} |\n")
        f.write(f"| Average Daily Subscriptions | {df['Subscribes'].mean():.2f} |\n")
        f.write(f"| Average Daily Unsubscriptions | {df['Unsubscribes'].mean():.2f} |\n")
        f.write(f"| Peak Single Day Subscriptions | {df['Subscribes'].max():,} |\n")
        f.write(f"| Peak Single Day Unsubscriptions | {df['Unsubscribes'].max():,} |\n")
        f.write(f"| Date Range | {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')} |\n")
        f.write(f"| Total Days Analyzed | {len(df):,} |\n")
        f.write(f"| Active Days (with activity) | {len(df[(df['Subscribes'] > 0) | (df['Unsubscribes'] > 0)]):,} |\n\n")
        
        # Monthly Breakdown
        f.write("## Monthly Breakdown\n\n")
        df['Month'] = df['Date'].dt.to_period('M')
        monthly_stats = df.groupby('Month').agg({
            'Subscribes': ['sum', 'mean'],
            'Unsubscribes': ['sum', 'mean'],
            'Net_Subscribers': 'sum'
        }).round(2)
        
        f.write("| Month | Total Subs | Avg Daily Subs | Total Unsubs | Avg Daily Unsubs | Net Change |\n")
        f.write("|-------|------------|-----------------|--------------|-------------------|------------|\n")
        
        for month in monthly_stats.index:
            f.write(f"| {month} | ")
            f.write(f"{int(monthly_stats.loc[month, ('Subscribes', 'sum')]):,} | ")
            f.write(f"{monthly_stats.loc[month, ('Subscribes', 'mean')]:.1f} | ")
            f.write(f"{int(monthly_stats.loc[month, ('Unsubscribes', 'sum')]):,} | ")
            f.write(f"{monthly_stats.loc[month, ('Unsubscribes', 'mean')]:.1f} | ")
            f.write(f"{int(monthly_stats.loc[month, ('Net_Subscribers', 'sum')]):,} |\n")
        
        # Peak Activity Days
        f.write("\n## Peak Activity Days\n\n")
        
        # Top subscription days
        top_sub_days = df.nlargest(5, 'Subscribes')
        f.write("### Top Subscription Days\n")
        for i, (_, row) in enumerate(top_sub_days.iterrows(), 1):
            if row['Subscribes'] > 0:
                f.write(f"{i}. **{row['Date'].strftime('%Y-%m-%d')}** - {row['Subscribes']:,} subscriptions\n")
        
        # Top unsubscription days (if any)
        top_unsub_days = df.nlargest(5, 'Unsubscribes')
        if top_unsub_days['Unsubscribes'].max() > 0:
            f.write("\n### Top Unsubscription Days\n")
            for i, (_, row) in enumerate(top_unsub_days.iterrows(), 1):
                if row['Unsubscribes'] > 0:
                    f.write(f"{i}. **{row['Date'].strftime('%Y-%m-%d')}** - {row['Unsubscribes']:,} unsubscriptions\n")
        
        # Best net growth days
        top_net_days = df.nlargest(5, 'Net_Subscribers')
        f.write("\n### Best Net Growth Days\n")
        for i, (_, row) in enumerate(top_net_days.iterrows(), 1):
            if row['Net_Subscribers'] > 0:
                f.write(f"{i}. **{row['Date'].strftime('%Y-%m-%d')}** - Net +{row['Net_Subscribers']:,} subscribers ({row['Subscribes']:,} subs, {row['Unsubscribes']:,} unsubs)\n")
        
        # Growth trends
        f.write("\n## Growth Trends\n\n")
        if len(df) > 1:
            recent_30_days = df.tail(30)
            f.write(f"**Last 30 days:**\n")
            f.write(f"- Total subscriptions: {recent_30_days['Subscribes'].sum():,}\n")
            f.write(f"- Total unsubscriptions: {recent_30_days['Unsubscribes'].sum():,}\n")
            f.write(f"- Net change: {recent_30_days['Net_Subscribers'].sum():,}\n")
            f.write(f"- Average daily subscriptions: {recent_30_days['Subscribes'].mean():.2f}\n")
        
    print(f"Subscriber summary saved as: {markdown_file}")
    return markdown_file

def print_subscriber_details(df, summary_stats):
    """Print detailed subscriber information"""
    print("\n" + "="*80)
    print("SUBSCRIBER ANALYTICS DETAILS")
    print("="*80)
    
    if summary_stats:
        print("\nSummary Statistics from CSV:")
        for key, value in summary_stats.items():
            readable_key = key.replace('_', ' ').title()
            print(f"{readable_key}: {value:,}")
    
    print(f"\nPeriod Analysis ({df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}):")
    print(f"Total subscriptions: {df['Subscribes'].sum():,}")
    print(f"Total unsubscriptions: {df['Unsubscribes'].sum():,}")
    print(f"Net subscriber change: {df['Net_Subscribers'].sum():,}")
    print(f"Peak single day subscriptions: {df['Subscribes'].max():,}")
    
    if df['Subscribes'].max() > 0:
        peak_day = df.loc[df['Subscribes'].idxmax(), 'Date']
        print(f"Peak subscription day: {peak_day.strftime('%Y-%m-%d')}")
    
    active_days = df[(df['Subscribes'] > 0) | (df['Unsubscribes'] > 0)]
    print(f"Days with activity: {len(active_days):,} out of {len(df):,} total days")

def main():
    """Main function to run the subscriber analytics"""
    try:
        print("Loading subscriber data...")
        df, source_files, summary_stats = load_subscriber_data()
        
        print(f"Loaded {len(df)} daily records")
        print(f"Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
        
        # Create visualizations
        print("\nCreating visualizations...")
        chart_files = create_subscriber_visualizations(df, source_files, summary_stats)
        
        # Save summary as markdown
        print("\nSaving subscriber summary...")
        markdown_file = save_subscriber_summary_markdown(df, source_files, summary_stats)
        
        # Print detailed information
        print_subscriber_details(df, summary_stats)
        
        print(f"\nGenerated files:")
        print(f"📄 Summary report: {markdown_file}")
        chart_descriptions = [
            "Daily subscription activity (active days only)",
            "Cumulative growth trends (weekly aggregation)", 
            "Monthly subscription summary",
            "Total subscriptions vs unsubscriptions",
            "Weekly subscription activity (active weeks only)"
        ]
        for i, (chart_file, description) in enumerate(zip(chart_files, chart_descriptions), 1):
            print(f"📊 Chart {i}: {chart_file}")
            print(f"    📈 {description}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
