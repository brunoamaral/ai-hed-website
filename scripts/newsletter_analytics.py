#!/usr/bin/env python3
"""
Newsletter Analytics Script

This script reads CSV files from the newsletter-reports directory and creates
visualizations of email campaign performance metrics.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import glob
import re
from datetime import datetime

def parse_percentage(value):
    """Convert percentage string to float"""
    if isinstance(value, str) and value.endswith('%'):
        return float(value.rstrip('%'))
    return float(value) if value else 0.0

def load_newsletter_data(reports_dir="newsletter-reports"):
    """Load and combine all CSV files from the reports directory"""
    csv_files = glob.glob(f"{reports_dir}/*.csv")
    
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {reports_dir}")
    
    all_data = []
    source_files = []
    
    for file in csv_files:
        print(f"Loading {file}...")
        df = pd.read_csv(file)
        
        # Clean and convert data types
        df['Sent'] = pd.to_datetime(df['Sent'])
        df['Total emails sent'] = pd.to_numeric(df['Total emails sent'])
        df['Opened'] = pd.to_numeric(df['Opened'])
        df['Clicked'] = pd.to_numeric(df['Clicked'])
        df['Open Rate'] = df['Open Rate'].apply(parse_percentage)
        df['Click Rate'] = df['Click Rate'].apply(parse_percentage)
        df['Soft bounces'] = pd.to_numeric(df['Soft bounces'])
        df['Hard bounces'] = pd.to_numeric(df['Hard bounces'])
        df['Unsubscribed'] = pd.to_numeric(df['Unsubscribed'])
        
        # Create unique campaign identifier using Campaign name + Sent date
        df['Campaign ID'] = df['Campaign name'] + ' (' + df['Sent'].dt.strftime('%Y-%m-%d %H:%M') + ')'
        
        all_data.append(df)
        source_files.append(Path(file).stem)
    
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Remove duplicates based on campaign name and sent date
    combined_df = combined_df.drop_duplicates(subset=['Campaign name', 'Sent'])
    
    # Sort by sent date
    combined_df = combined_df.sort_values('Sent').reset_index(drop=True)
    
    return combined_df, source_files

def create_visualizations(df, source_files):
    """Create various charts to analyze newsletter performance"""
    
    # Set up the plotting style
    plt.style.use('default')
    sns.set_palette("husl")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = '_'.join(source_files) if source_files else 'newsletter_analytics'
    
    # 1. Open Rate and Click Rate bar chart (instead of line chart)
    fig1, ax1 = plt.subplots(figsize=(14, 8))
    
    x_positions = range(len(df))
    width = 0.35
    
    bars1 = ax1.bar([x - width/2 for x in x_positions], df['Open Rate'], 
                    width, label='Open Rate (%)', alpha=0.8, color='steelblue')
    bars2 = ax1.bar([x + width/2 for x in x_positions], df['Click Rate'], 
                    width, label='Click Rate (%)', alpha=0.8, color='orange')
    
    ax1.set_title('Open Rate and Click Rate by Campaign', fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('Campaign', fontsize=12)
    ax1.set_ylabel('Rate (%)', fontsize=12)
    ax1.set_xticks(x_positions)
    ax1.set_xticklabels([f"{row['Campaign name'][:30]}...\n({row['Sent'].strftime('%Y-%m-%d')})" 
                         if len(row['Campaign name']) > 30 
                         else f"{row['Campaign name']}\n({row['Sent'].strftime('%Y-%m-%d')})" 
                         for _, row in df.iterrows()], 
                        rotation=45, ha='right', fontsize=9)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    chart1_file = f"{base_filename}_open_click_rates_{timestamp}.png"
    plt.savefig(chart1_file, dpi=300, bbox_inches='tight')
    print(f"Chart 1 saved as: {chart1_file}")
    plt.close()
    
    # 2. Total emails sent bar chart
    fig2, ax2 = plt.subplots(figsize=(14, 8))
    bars = ax2.bar(x_positions, df['Total emails sent'], alpha=0.7, color='steelblue')
    ax2.set_title('Total Emails Sent per Campaign', fontsize=16, fontweight='bold', pad=20)
    ax2.set_xlabel('Campaign', fontsize=12)
    ax2.set_ylabel('Emails Sent', fontsize=12)
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels([f"{row['Campaign name'][:30]}...\n({row['Sent'].strftime('%Y-%m-%d')})" 
                         if len(row['Campaign name']) > 30 
                         else f"{row['Campaign name']}\n({row['Sent'].strftime('%Y-%m-%d')})" 
                         for _, row in df.iterrows()], 
                        rotation=45, ha='right', fontsize=9)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{int(height)}', ha='center', va='bottom', fontsize=10)
    
    plt.tight_layout()
    chart2_file = f"{base_filename}_emails_sent_{timestamp}.png"
    plt.savefig(chart2_file, dpi=300, bbox_inches='tight')
    print(f"Chart 2 saved as: {chart2_file}")
    plt.close()
    
    # 3. Click-through rate vs Open rate scatter plot
    fig3, ax3 = plt.subplots(figsize=(12, 8))
    scatter = ax3.scatter(df['Open Rate'], df['Click Rate'], 
                         s=df['Total emails sent']*2, alpha=0.6, c=range(len(df)), cmap='viridis')
    ax3.set_title('Click Rate vs Open Rate\n(Size = Emails Sent)', fontsize=16, fontweight='bold', pad=20)
    ax3.set_xlabel('Open Rate (%)', fontsize=12)
    ax3.set_ylabel('Click Rate (%)', fontsize=12)
    ax3.grid(True, alpha=0.3)
    
    # Add labels for each point
    for i, row in df.iterrows():
        ax3.annotate(f"{row['Campaign name'][:20]}...\n{row['Sent'].strftime('%m/%d')}" 
                     if len(row['Campaign name']) > 20 
                     else f"{row['Campaign name']}\n{row['Sent'].strftime('%m/%d')}", 
                     (row['Open Rate'], row['Click Rate']), 
                     xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.8)
    
    # Add colorbar for campaign chronology
    cbar = plt.colorbar(scatter, ax=ax3)
    cbar.set_label('Campaign Order (chronological)', fontsize=10)
    
    plt.tight_layout()
    chart3_file = f"{base_filename}_scatter_plot_{timestamp}.png"
    plt.savefig(chart3_file, dpi=300, bbox_inches='tight')
    print(f"Chart 3 saved as: {chart3_file}")
    plt.close()
    
    # 4. Engagement metrics comparison (pie chart)
    fig4, ax4 = plt.subplots(figsize=(10, 8))
    metrics = ['Opened', 'Clicked', 'Unsubscribed']
    totals = [df[metric].sum() for metric in metrics]
    colors = ['lightgreen', 'orange', 'lightcoral']
    
    wedges, texts, autotexts = ax4.pie(totals, labels=metrics, autopct='%1.1f%%', 
                                      colors=colors, startangle=90)
    ax4.set_title('Total Engagement Distribution', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    chart4_file = f"{base_filename}_engagement_pie_{timestamp}.png"
    plt.savefig(chart4_file, dpi=300, bbox_inches='tight')
    print(f"Chart 4 saved as: {chart4_file}")
    plt.close()
    
    # 5. Monthly performance trends with campaign names
    fig5, ax5 = plt.subplots(figsize=(16, 10))
    
    # Group by month but keep individual campaigns visible
    df_monthly = df.copy()
    df_monthly['Month'] = df_monthly['Sent'].dt.to_period('M')
    df_monthly['Month_str'] = df_monthly['Month'].astype(str)
    
    # Create a more detailed x-axis with campaign info
    df_monthly['Campaign_Short'] = df_monthly.apply(
        lambda row: f"{row['Campaign name'][:15]}...\n{row['Sent'].strftime('%m/%d')}" 
        if len(row['Campaign name']) > 15 
        else f"{row['Campaign name']}\n{row['Sent'].strftime('%m/%d')}", axis=1)
    
    ax5_twin = ax5.twinx()
    
    # Bar chart for emails sent
    bars = ax5.bar(range(len(df_monthly)), df_monthly['Total emails sent'], 
                   alpha=0.6, label='Emails Sent', color='lightblue')
    
    # Line charts for rates
    line1 = ax5_twin.plot(range(len(df_monthly)), df_monthly['Open Rate'], 
                         'o-', color='red', label='Open Rate (%)', linewidth=2, markersize=6)
    line2 = ax5_twin.plot(range(len(df_monthly)), df_monthly['Click Rate'], 
                         's-', color='darkred', label='Click Rate (%)', linewidth=2, markersize=6)
    
    ax5.set_title('Campaign Performance Over Time', fontsize=16, fontweight='bold', pad=20)
    ax5.set_xlabel('Campaign', fontsize=12)
    ax5.set_ylabel('Emails Sent', color='blue', fontsize=12)
    ax5_twin.set_ylabel('Rate (%)', color='red', fontsize=12)
    
    ax5.set_xticks(range(len(df_monthly)))
    ax5.set_xticklabels(df_monthly['Campaign_Short'], rotation=45, ha='right', fontsize=9)
    
    # Combine legends
    lines1, labels1 = ax5.get_legend_handles_labels()
    lines2, labels2 = ax5_twin.get_legend_handles_labels()
    ax5.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    ax5.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    chart5_file = f"{base_filename}_performance_trends_{timestamp}.png"
    plt.savefig(chart5_file, dpi=300, bbox_inches='tight')
    print(f"Chart 5 saved as: {chart5_file}")
    plt.close()
    
    return [chart1_file, chart2_file, chart3_file, chart4_file, chart5_file]

def save_campaign_summary_markdown(df, source_files):
    """Save campaign summary as a markdown file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_filename = '_'.join(source_files) if source_files else 'newsletter_analytics'
    markdown_file = f"{base_filename}_summary_{timestamp}.md"
    
    with open(markdown_file, 'w') as f:
        f.write("# Newsletter Campaign Analytics Report\n\n")
        f.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Source files:** {', '.join(source_files)}\n\n")
        
        # Overall Statistics
        f.write("## Overall Statistics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|--------|-------|\n")
        f.write(f"| Total campaigns analyzed | {len(df)} |\n")
        f.write(f"| Total emails sent | {df['Total emails sent'].sum():,} |\n")
        f.write(f"| Total opens | {df['Opened'].sum():,} |\n")
        f.write(f"| Total clicks | {df['Clicked'].sum():,} |\n")
        f.write(f"| Average open rate | {df['Open Rate'].mean():.1f}% |\n")
        f.write(f"| Average click rate | {df['Click Rate'].mean():.1f}% |\n")
        f.write(f"| Best performing campaign (open rate) | {df.loc[df['Open Rate'].idxmax(), 'Campaign name']} ({df['Open Rate'].max():.1f}%) |\n")
        f.write(f"| Best performing campaign (click rate) | {df.loc[df['Click Rate'].idxmax(), 'Campaign name']} ({df['Click Rate'].max():.1f}%) |\n")
        f.write(f"| Date range | {df['Sent'].min().strftime('%Y-%m-%d')} to {df['Sent'].max().strftime('%Y-%m-%d')} |\n\n")
        
        # Detailed Campaign Performance
        f.write("## Campaign Performance Details\n\n")
        f.write("| Campaign Name | Date Sent | Emails Sent | Opens | Open Rate | Clicks | Click Rate | Unsubscribed |\n")
        f.write("|---------------|-----------|-------------|-------|-----------|--------|------------|-------------|\n")
        
        for _, row in df.iterrows():
            f.write(f"| {row['Campaign name']} | ")
            f.write(f"{row['Sent'].strftime('%Y-%m-%d %H:%M')} | ")
            f.write(f"{row['Total emails sent']:,} | ")
            f.write(f"{row['Opened']:,} | ")
            f.write(f"{row['Open Rate']:.1f}% | ")
            f.write(f"{row['Clicked']:,} | ")
            f.write(f"{row['Click Rate']:.1f}% | ")
            f.write(f"{row['Unsubscribed']} |\n")
        
        # Monthly Summary
        f.write("\n## Monthly Summary\n\n")
        df_monthly = df.copy()
        df_monthly['Month'] = df_monthly['Sent'].dt.to_period('M')
        monthly_stats = df_monthly.groupby('Month').agg({
            'Total emails sent': 'sum',
            'Opened': 'sum',
            'Clicked': 'sum',
            'Open Rate': 'mean',
            'Click Rate': 'mean',
            'Campaign name': 'count'
        }).reset_index()
        monthly_stats.rename(columns={'Campaign name': 'Campaigns'}, inplace=True)
        
        f.write("| Month | Campaigns | Emails Sent | Total Opens | Total Clicks | Avg Open Rate | Avg Click Rate |\n")
        f.write("|-------|-----------|-------------|-------------|--------------|---------------|----------------|\n")
        
        for _, row in monthly_stats.iterrows():
            f.write(f"| {row['Month']} | ")
            f.write(f"{row['Campaigns']} | ")
            f.write(f"{row['Total emails sent']:,} | ")
            f.write(f"{row['Opened']:,} | ")
            f.write(f"{row['Clicked']:,} | ")
            f.write(f"{row['Open Rate']:.1f}% | ")
            f.write(f"{row['Click Rate']:.1f}% |\n")
        
        # Top Performers
        f.write("\n## Top Performing Campaigns\n\n")
        f.write("### By Open Rate\n")
        top_open = df.nlargest(3, 'Open Rate')
        for i, (_, row) in enumerate(top_open.iterrows(), 1):
            f.write(f"{i}. **{row['Campaign name']}** - {row['Open Rate']:.1f}% open rate ({row['Sent'].strftime('%Y-%m-%d')})\n")
        
        f.write("\n### By Click Rate\n")
        top_click = df.nlargest(3, 'Click Rate')
        for i, (_, row) in enumerate(top_click.iterrows(), 1):
            f.write(f"{i}. **{row['Campaign name']}** - {row['Click Rate']:.1f}% click rate ({row['Sent'].strftime('%Y-%m-%d')})\n")
        
        f.write("\n### By Total Engagement (Opens + Clicks)\n")
        df['Total Engagement'] = df['Opened'] + df['Clicked']
        top_engagement = df.nlargest(3, 'Total Engagement')
        for i, (_, row) in enumerate(top_engagement.iterrows(), 1):
            f.write(f"{i}. **{row['Campaign name']}** - {row['Total Engagement']:,} total engagements ({row['Sent'].strftime('%Y-%m-%d')})\n")
    
    print(f"Campaign summary saved as: {markdown_file}")
    return markdown_file

def print_campaign_details(df):
    """Print detailed information about each campaign"""
    print("\n" + "="*80)
    print("CAMPAIGN PERFORMANCE DETAILS")
    print("="*80)
    
    for idx, row in df.iterrows():
        print(f"\nCampaign: {row['Campaign name']}")
        print(f"Sent: {row['Sent'].strftime('%Y-%m-%d %H:%M')}")
        print(f"Total Emails Sent: {row['Total emails sent']:,}")
        print(f"Opened: {row['Opened']:,} ({row['Open Rate']:.1f}%)")
        print(f"Clicked: {row['Clicked']:,} ({row['Click Rate']:.1f}%)")
        if row['Unsubscribed'] > 0:
            print(f"Unsubscribed: {row['Unsubscribed']}")
        if row['Soft bounces'] > 0 or row['Hard bounces'] > 0:
            print(f"Bounces: {row['Soft bounces']} soft, {row['Hard bounces']} hard")
        print("-" * 50)

def main():
    """Main function to run the newsletter analytics"""
    try:
        print("Loading newsletter data...")
        df, source_files = load_newsletter_data()
        
        print(f"Loaded {len(df)} campaign records")
        print(f"Date range: {df['Sent'].min().strftime('%Y-%m-%d')} to {df['Sent'].max().strftime('%Y-%m-%d')}")
        
        # Create visualizations (separate charts)
        print("\nCreating visualizations...")
        chart_files = create_visualizations(df, source_files)
        
        # Save campaign summary as markdown
        print("\nSaving campaign summary...")
        markdown_file = save_campaign_summary_markdown(df, source_files)
        
        # Print detailed campaign information
        print_campaign_details(df)
        
        # Print overall statistics
        print("\n" + "="*80)
        print("OVERALL STATISTICS")
        print("="*80)
        print(f"Total campaigns analyzed: {len(df)}")
        print(f"Total emails sent: {df['Total emails sent'].sum():,}")
        print(f"Total opens: {df['Opened'].sum():,}")
        print(f"Total clicks: {df['Clicked'].sum():,}")
        print(f"Average open rate: {df['Open Rate'].mean():.1f}%")
        print(f"Average click rate: {df['Click Rate'].mean():.1f}%")
        print(f"Best performing campaign (open rate): {df.loc[df['Open Rate'].idxmax(), 'Campaign name']} ({df['Open Rate'].max():.1f}%)")
        print(f"Best performing campaign (click rate): {df.loc[df['Click Rate'].idxmax(), 'Campaign name']} ({df['Click Rate'].max():.1f}%)")
        
        print(f"\nGenerated files:")
        print(f"📄 Summary report: {markdown_file}")
        for i, chart_file in enumerate(chart_files, 1):
            print(f"📊 Chart {i}: {chart_file}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
