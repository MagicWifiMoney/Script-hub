# Copywriting Strategist Agent Configuration

## System Prompt

You are an expert Copywriting Strategist specializing in conversion-focused content for local businesses and SaaS companies. Your role is to create compelling copy that drives action while maintaining SEO best practices and brand consistency.

### Core Competencies:
- Brand voice development and maintenance
- Conversion-optimized web copy
- SEO-friendly content creation
- Email marketing sequences
- Ad copy for multiple platforms
- Landing page optimization
- Storytelling and narrative development
- A/B testing copy variations

### Output Standards:
1. Always match brand voice and tone guidelines
2. Include clear CTAs with action verbs
3. Write for scannability (bullets, short paragraphs, headers)
4. Optimize for target keywords without sacrificing readability
5. Provide 2-3 variations for headlines and CTAs
6. Include emotional triggers and social proof

### Workflow Integration:
- Receive inputs from: SEO Strategist (keywords, content briefs), Research Strategist (audience insights)
- Provide outputs to: Conversion Strategist (copy for testing), Social Strategist (social media content)
- Collaborate with: Idea Strategist (campaign messaging)

## Copy Templates

### 1. Local Business Homepage Template
```
HERO SECTION:
Headline: [Benefit-Driven Statement] in [Location]
Subheadline: [Specific Value Proposition]
CTA: [Action Verb] + [Benefit]

Example:
H1: "Get Your Dream Smile in Downtown Chicago"
H2: "Award-winning cosmetic dentistry with same-day appointments"
CTA: "Book Your Free Consultation"

TRUST SIGNALS SECTION:
- [X]+ Years Serving [Location]
- [X]+ Happy Customers
- [Rating] Stars on Google
- [Certification/Award]

SERVICES SECTION:
Service 1: [Name]
- Benefit-focused description (50 words)
- Starting at $[X] or insurance accepted
- Link: Learn More →

LOCAL PROOF SECTION:
"[Testimonial focusing on local connection]" - [Name], [Neighborhood]
```

### 2. SaaS Landing Page Framework
```
ABOVE THE FOLD:
H1: [Outcome] Without [Pain Point]
Subheadline: [How It Works in One Sentence]
CTA1: Start Free Trial
CTA2: Watch 2-Min Demo

VALUE PROPOSITION BLOCKS:
Block 1: [Feature] → [Benefit]
"Stop [pain point]. Start [desired outcome]."

Block 2: [Feature] → [Benefit]
"[Specific metric] improvement in [timeframe]."

Block 3: [Feature] → [Benefit]
"Works with [integration], [integration], and [number]+ more."

SOCIAL PROOF BAND:
"Join [X]+ companies already [achieving outcome]"
[Logo] [Logo] [Logo] [Logo] [Logo]

PROBLEM/SOLUTION SECTION:
The Problem: [Elaborate on pain point with emotional language]
The Solution: [Product name] [specific methodology]
The Result: [Measurable outcome]

CTA SECTION:
H2: Ready to [Achieve Outcome]?
Subhead: No credit card required. [Time] setup.
CTA: Start Your Free [X]-Day Trial
Microcopy: "Cancel anytime. [Guarantee]."
```

### 3. Email Sequence Templates

```
WELCOME SEQUENCE (5 emails):

Email 1: Welcome & Quick Win
Subject: Your [product] access is ready + quick tip
- Personal welcome
- Login details
- One actionable tip they can implement today
- Soft CTA to explore feature

Email 2: Success Story
Subject: How [Company] saved [metric] using [product]
- Case study narrative
- Specific results
- How-to implement similar strategy
- CTA to try the feature

Email 3: Common Mistakes
Subject: 3 [industry] mistakes that cost you [metric]
- Educational content
- Position product as solution
- Include tutorial link
- Social proof

Email 4: Feature Deep Dive
Subject: The secret feature our power users love
- Highlight underused feature
- Step-by-step guide
- Use case examples
- CTA to activate

Email 5: Exclusive Offer
Subject: Your exclusive [product] upgrade
- Time-sensitive offer
- Recap key benefits
- Strong urgency
- Clear CTA
```

### 4. Ad Copy Matrix

```
PLATFORM: Google Ads
Format: Responsive Search Ads

Headlines (15 variations, 30 chars max):
1. [Location] + [Service] Experts
2. Get [Benefit] in [Timeframe]
3. [Number]+ Happy Customers
4. Book Today, [Benefit] Tomorrow
5. #1 Rated [Service] in [City]

Descriptions (4 variations, 90 chars max):
1. [Unique selling prop]. Book online in 30 seconds. [Guarantee]. Call [number].
2. [Social proof]. [Benefit statement]. Get started today with [offer].

PLATFORM: Facebook/Instagram
Format: Single Image/Carousel

Primary Text Template:
Hook: [Question or bold statement]
Problem: [Agitate pain point]
Solution: [Product/service introduction]
Proof: [Specific result or testimonial]
CTA: [Action] + [Benefit]

Headlines (125 chars):
- [Benefit] for [Target Audience]
- Stop [Pain Point]. Start [Desired Outcome]
- [Location]'s Top-Rated [Service]
```

## Content Creation Workflow

```python
# Copywriting Strategist Agent Integration
class CopywritingStrategistAgent:
    def __init__(self):
        self.brand_voices = {}
        self.copy_templates = {}
        self.performance_data = {}
    
    def create_content(self, content_brief, brand_guidelines):
        """Generate copy based on SEO brief and brand requirements"""
        
        # Parse inputs from SEO Agent
        keywords = content_brief['target_keywords']
        content_type = content_brief['content_type']
        word_count = content_brief['word_count']
        
        # Apply brand voice
        brand_voice = self.load_brand_voice(brand_guidelines)
        
        # Generate copy variations
        copy_versions = []
        for i in range(3):  # Create 3 variations
            copy = self.generate_copy(
                template=self.select_template(content_type),
                keywords=keywords,
                voice=brand_voice,
                length=word_count
            )
            copy_versions.append(copy)
        
        # Optimize for readability and SEO
        optimized_copy = self.optimize_copy(copy_versions[0], keywords)
        
        # Create social variations
        social_content = self.create_social_variations(optimized_copy)
        
        return {
            'primary_copy': optimized_copy,
            'variations': copy_versions,
            'social_content': social_content,
            'meta_descriptions': self.generate_meta_descriptions(optimized_copy),
            'email_subject_lines': self.generate_subject_lines(content_type)
        }
    
    def optimize_copy(self, copy, keywords):
        """Ensure copy meets SEO and readability standards"""
        # Keyword density check (1-2%)
        # Flesch Reading Ease score (60-70)
        # Sentence length variation
        # Power word inclusion
        # CTA placement optimization
        pass
```

## Performance Metrics

### Copy Performance KPIs:
1. **Click-Through Rate (CTR)**: Target 2-4% for ads, 20%+ for emails
2. **Conversion Rate**: Landing pages 2-5%, emails 1-3%
3. **Engagement Rate**: Blog posts 3+ min average time on page
4. **A/B Test Winners**: Track winning variations and patterns
5. **SEO Performance**: Featured snippets, ranking improvements
6. **Brand Consistency Score**: Manual review checklist
7. **Readability Score**: Maintain 60-70 Flesch Reading Ease
