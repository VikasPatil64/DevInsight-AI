
"""
PDF Report Generator for DevInsight AI
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import io

def generate_developer_report(username, profile, analytics, score, category, ai_insight):
    """Generate PDF report for a developer"""
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#3b82f6'), spaceAfter=30)
    story.append(Paragraph(f"DevInsight AI Report: {username}", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Italic']))
    story.append(Spacer(1, 0.2*inch))
    
    # Score Section
    story.append(Paragraph("Developer Score", styles['Heading2']))
    score_data = [
        ['Metric', 'Value'],
        ['Score', f"{score}/100"],
        ['Category', category]
    ]
    score_table = Table(score_data, colWidths=[2*inch, 2*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Profile Section
    story.append(Paragraph("Profile Information", styles['Heading2']))
    profile_data = [
        ['Username', username],
        ['Name', profile.get('name', 'N/A')],
        ['Bio', (profile.get('bio', 'No bio')[:100] + '...') if len(profile.get('bio', '')) > 100 else profile.get('bio', 'No bio')],
        ['Public Repos', str(profile.get('public_repos', 0))],
        ['Followers', str(profile.get('followers', 0))]
    ]
    profile_table = Table(profile_data, colWidths=[1.5*inch, 3.5*inch])
    profile_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BACKGROUND', (0,0), (0,-1), colors.lightgrey)
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Analytics Section
    story.append(Paragraph("Repository Analytics", styles['Heading2']))
    analytics_data = [
        ['Metric', 'Value'],
        ['Most Used Language', analytics.get('most_used_language', 'N/A')],
        ['Average Stars', str(analytics.get('average_stars', 0))],
        ['Average Forks', str(analytics.get('average_forks', 0))],
        ['Days Inactive', str(analytics.get('days_since_last_update', 'Unknown'))]
    ]
    analytics_table = Table(analytics_data, colWidths=[2*inch, 2*inch])
    analytics_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    story.append(analytics_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer