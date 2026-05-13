from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER

resume = {
    'name': 'Pranav Vaidyanathan',
    'contact': 'pranav.vaidyanathan@gmail.com | linkedin.com/in/pranav-vaidyanathan | +1-732-766-2251',
    'sections': [
        {
            'title': 'EXPERIENCE',
            'items': [
                {
                    'heading': 'Pernod Ricard USA  |  New York, NY',
                    'subheading': 'Supply Chain Performance Analyst – Inventory Optimization and Data Automation  |  January 2023 – May 2026',
                    'bullets': [
                        'Identified business challenges and opportunities through rigorous analytics, developing strategic and tactical recommendations that drove $35K monthly savings—demonstrating quantitative decision-making on major company challenges.',
                        'Performed statistical modeling and hypothesis testing across 500K+ transactions and 120 product portfolios, connecting performance drivers to historical behavior to surface actionable insights for senior leadership.',
                        'Supported product strategy and pricing optimization initiatives by building Power BI analytics infrastructure to monitor portfolio health and segment high-risk segments, enabling data-driven go-to-market strategies.',
                        'Developed execution roadmaps encompassing problem frameworks, hypotheses, testing and analysis, solution development, operational feasibility scoping, and monitoring plans—translating complex data into strategic business outcomes.',
                        'Drove cross-functional partnerships with IT, Sales, Operations, and Finance to improve volume, profitability, and service quality—demonstrating tenacious decision-making and strategic influencing in a fast-paced, entrepreneurial environment.',
                        'Engineered scalable analytics pipelines by transforming 900K+ rows of data across 15+ sources, enabling feasibility analysis and implementation oversight for high-impact product and pricing programs.'
                    ]
                },
                {
                    'heading': 'Tata Consultancy Services  |  Midland, MI',
                    'subheading': 'Data Analyst – Global Insights Team  |  March 2021 - December 2022',
                    'bullets': [
                        'Created risk models and analytics frameworks connecting credit performance drivers to historical consumer behavior, delivering strategic recommendations that achieved 19% efficiency improvements and 6% performance gains.',
                        'Built enterprise analytics infrastructure for $30M+ in pricing and operational metrics, enabling cross-functional teams to make rigorous, data-driven product decisions and exceed business targets through analytics.',
                        'Supported market research initiatives and direct-to-consumer insights for $400K+ in portfolio analysis, translating quantitative findings into strategic product and go-to-market recommendations that informed customer experience design.',
                        'Engineered analytics reporting for 12,000+ monthly transactions using statistical modeling and anomaly detection to improve forecast accuracy by 8%, demonstrating rigorous monitoring and analysis across portfolios.'
                    ]
                },
                {
                    'heading': 'Biogen Inc.  |  New Brunswick, NJ',
                    'subheading': 'Project Intern – Sustainability and Risk  |  September 2020 - December 2020',
                    'bullets': [
                        'Co-led development of risk assessment framework connecting exposure drivers to historical performance, identifying $100K+ in savings opportunities and supporting strategic decision-making through quantitative analysis.'
                    ]
                },
                {
                    'heading': 'Rutgers Supply Chain Analytics Laboratory  |  Piscataway, NJ',
                    'subheading': 'Research Assistant – Global Markets  |  May 2020 - August 2020',
                    'bullets': [
                        'Performed rigorous market research using Tableau on 20+ years of historical data across 3,000+ products, identifying trends, risks, and opportunities to support strategic and tactical recommendations for market entry.',
                        'Conducted quantitative analysis to define analytics requirements, performed data transformation and ETL, and synthesized findings into actionable strategic recommendations informed by rigorous monitoring of market drivers.'
                    ]
                },
                {
                    'heading': 'Matrimony.com Limited  |  Chennai, India',
                    'subheading': 'Decision Support Analyst – Customer Retention  |  December 2018 - March 2019',
                    'bullets': [
                        'Built and deployed Python-based risk and propensity models that achieved 90% targeting accuracy, demonstrating impact on strategic decision-making for customer acquisition and lifetime value optimization.'
                    ]
                }
            ]
        },
        {
            'title': 'SKILLS /TOOLS',
            'items': [
                {
                    'heading': None,
                    'subheading': None,
                    'bullets': [
                        'Programming: SQL, Python, R',
                        'Software: Power BI, Tableau, Excel, Anaplan, Power Automate',
                        'Expertise: Statistical Model Building, Market Research, Hypothesis Testing, Credit Risk Modeling, Product Pricing Analytics, Quantitative Analysis, Cross-functional Leadership, Data Visualization, Problem Framing, Analytics-Driven Decision Making'
                    ]
                }
            ]
        },
        {
            'title': 'CERTIFICATIONS',
            'items': [
                {
                    'heading': None,
                    'subheading': None,
                    'bullets': [
                        'Advanced Power BI: Expert Data Analysis and Visualization – Udemy',
                        'Fast Track to Power BI – XelPlus',
                        'Power BI Essential Training, Power BI Data Modeling with DAX, Cognitive Technologies: The Real Opportunities for Business – LinkedIn Learning'
                    ]
                }
            ]
        },
        {
            'title': 'EDUCATION',
            'items': [
                {
                    'heading': 'RUTGERS BUSINESS SCHOOL (RBS)  |  New Brunswick, NJ',
                    'subheading': 'Master of Supply Chain Analytics degree, January 2021',
                    'bullets': []
                },
                {
                    'heading': 'ANNA UNIVERSITY – Sri Venkateswara College of Engineering (SVCE)  |  Chennai, India',
                    'subheading': 'Bachelor of Engineering, Computer Science and Engineering, May 2019',
                    'bullets': []
                }
            ]
        }
    ]
}


def build_pdf(output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter,
                            leftMargin=0.6*inch, rightMargin=0.6*inch,
                            topMargin=0.6*inch, bottomMargin=0.6*inch)
    styles = getSampleStyleSheet()
    name_style = ParagraphStyle('Name', parent=styles['Title'], alignment=TA_CENTER, spaceAfter=6)
    contact_style = ParagraphStyle('Contact', parent=styles['Normal'], alignment=TA_CENTER, spaceAfter=12)
    section_style = ParagraphStyle('Section', parent=styles['Heading3'], spaceBefore=12, spaceAfter=6)
    item_heading_style = ParagraphStyle('ItemHeading', parent=styles['Heading4'], spaceAfter=2)
    subheading_style = ParagraphStyle('Subheading', parent=styles['Normal'], leftIndent=12, fontSize=10, spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], spaceAfter=2, leading=13)

    story = []
    story.append(Paragraph(resume['name'], name_style))
    story.append(Paragraph(resume['contact'], contact_style))

    for section in resume['sections']:
        story.append(Paragraph(section['title'], section_style))
        for item in section['items']:
            if item['heading']:
                story.append(Paragraph(item['heading'], item_heading_style))
            if item['subheading']:
                story.append(Paragraph(item['subheading'], subheading_style))
            if item['bullets']:
                bullets = [ListItem(Paragraph(b, body_style), leftIndent=12) for b in item['bullets']]
                story.append(ListFlowable(bullets, bulletType='bullet', start='circle', leftIndent=18))
            story.append(Spacer(1, 0.1*inch))
        story.append(Spacer(1, 0.2*inch))

    doc.build(story)


if __name__ == '__main__':
    build_pdf(r'c:\Users\prana\OneDrive\Desktop\Agent-Skills\resume-pilot\customized_template_resume.pdf')