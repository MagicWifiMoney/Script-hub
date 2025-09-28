#!/usr/bin/env python3
"""
Client Intelligence System - Premium Marketing AI
Smart client profiling, knowledge base building, and context management

Features:
- Automated client discovery from website URL
- Persistent client profiles with SQLite
- Intelligent context extraction
- Smart recommendations based on client data
- Campaign history and performance tracking
"""

import os
import sqlite3
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse
import hashlib

# Import our existing tools
from seo_analysis_engine import analyze_website_seo
from python_scripts.marketing_agents.research_strategist import AutonomousResearchEngine
from api_clients import get_ai_client

class ClientIntelligenceSystem:
    """Manages client profiles, knowledge bases, and context-aware recommendations"""

    def __init__(self, db_path: str = "client_intelligence.db"):
        self.db_path = db_path
        self.ai_client = get_ai_client()
        self.research_engine = AutonomousResearchEngine()
        self._initialize_database()

    def _initialize_database(self):
        """Initialize SQLite database with client intelligence schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Client profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_name TEXT NOT NULL,
                website_url TEXT UNIQUE,
                industry TEXT,
                business_type TEXT,
                target_audience TEXT,
                brand_tone TEXT DEFAULT 'professional',
                company_size TEXT,
                primary_goals TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_analysis_date DATE,
                seo_score INTEGER,
                profile_completion REAL DEFAULT 0.0
            )
        ''')

        # Knowledge base table for extracted intelligence
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                knowledge_type TEXT NOT NULL,
                knowledge_data TEXT NOT NULL,
                confidence_score REAL DEFAULT 0.8,
                source TEXT,
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES client_profiles (id)
            )
        ''')

        # Campaign history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS campaign_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                campaign_type TEXT NOT NULL,
                campaign_data TEXT NOT NULL,
                tools_used TEXT,
                generation_time REAL,
                performance_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES client_profiles (id)
            )
        ''')

        # Recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS client_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                recommendation_type TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                priority INTEGER DEFAULT 5,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (client_id) REFERENCES client_profiles (id)
            )
        ''')

        conn.commit()
        conn.close()

    def create_client_from_website(self, website_url: str, client_name: str = None) -> Dict:
        """Smart client onboarding - create profile from website URL"""

        discovery_start = time.time()

        # Normalize URL
        if not website_url.startswith(('http://', 'https://')):
            website_url = f"https://{website_url}"

        parsed_url = urlparse(website_url)
        domain = parsed_url.netloc

        if not client_name:
            client_name = domain.replace('www.', '').replace('.com', '').replace('.', ' ').title()

        print(f"🔍 SMART CLIENT DISCOVERY INITIALIZING...")
        print(f"🌐 Website: {website_url}")
        print(f"🏢 Client: {client_name}")
        print("⏳ Discovering business intelligence...\n")

        try:
            # Phase 1: Website Analysis & SEO Intelligence
            print("📊 Phase 1: Website Intelligence Extraction...")
            seo_results = analyze_website_seo(website_url, "comprehensive", client_name)

            # Phase 2: Market Intelligence
            print("🔍 Phase 2: Market & Industry Intelligence...")
            market_results = self.research_engine.conduct_research(
                research_type="industry",
                target_subject=f"{client_name} {domain}",
                client_name=client_name
            )

            # Phase 3: AI-Powered Business Intelligence
            print("🤖 Phase 3: AI Business Profile Analysis...")
            business_intelligence = self._extract_business_intelligence(seo_results, market_results, website_url)

            # Phase 4: Create Client Profile
            print("📋 Phase 4: Building Client Profile...")
            client_profile = self._build_client_profile(
                client_name, website_url, seo_results, market_results, business_intelligence
            )

            # Phase 5: Store in Database
            client_id = self._save_client_profile(client_profile)
            self._store_knowledge_base(client_id, seo_results, market_results, business_intelligence)

            # Phase 6: Generate Smart Recommendations
            recommendations = self._generate_client_recommendations(client_id, client_profile)
            self._save_recommendations(client_id, recommendations)

            discovery_time = round(time.time() - discovery_start, 2)

            result = {
                "success": True,
                "client_id": client_id,
                "client_profile": client_profile,
                "recommendations": recommendations,
                "discovery_time": discovery_time,
                "profile_completion": client_profile.get("profile_completion", 0.8)
            }

            print(f"✅ Client Discovery Complete ({discovery_time}s)")
            print(f"📊 Profile Completion: {client_profile.get('profile_completion', 80):.0f}%")

            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "client_name": client_name,
                "website_url": website_url
            }

    def _extract_business_intelligence(self, seo_data: Dict, market_data: Dict, website_url: str) -> Dict:
        """Use AI to extract deep business intelligence"""

        try:
            # Compile data for AI analysis
            analysis_prompt = f"""
            Analyze this business data and extract key intelligence:

            WEBSITE: {website_url}

            SEO DATA:
            - SEO Score: {seo_data.get('seo_score', 'N/A')}
            - Technical Data: {json.dumps(seo_data.get('technical_data', {}), indent=2)[:1000]}

            MARKET RESEARCH:
            {json.dumps(market_data, indent=2)[:2000]}

            Extract and return the following business intelligence as JSON:
            {{
                "industry": "specific industry category",
                "business_type": "e.g., B2B, B2C, SaaS, Local Service, E-commerce",
                "company_size": "Startup, Small, Medium, or Enterprise",
                "target_audience": "detailed description of primary audience",
                "value_proposition": "main value they provide",
                "primary_goals": "likely marketing/business goals",
                "competitive_advantage": "what sets them apart",
                "growth_stage": "Early, Growth, Mature, or Declining",
                "marketing_maturity": "Beginner, Intermediate, Advanced",
                "recommended_brand_tone": "professional, casual, friendly, or authoritative",
                "key_challenges": ["list", "of", "challenges"],
                "opportunities": ["list", "of", "opportunities"]
            }}

            Focus on actionable insights for marketing strategy.
            """

            ai_response = self.ai_client.generate_content(analysis_prompt)

            if ai_response.success:
                # Try to parse JSON from AI response
                ai_content = ai_response.data.get("content", "")
                try:
                    # Extract JSON from the response
                    json_start = ai_content.find('{')
                    json_end = ai_content.rfind('}') + 1
                    if json_start >= 0 and json_end > json_start:
                        intelligence_json = ai_content[json_start:json_end]
                        return json.loads(intelligence_json)
                except:
                    pass

                # Fallback to basic analysis
                return {
                    "analysis_text": ai_content,
                    "industry": "General Business",
                    "business_type": "Unknown",
                    "target_audience": "General audience",
                    "recommended_brand_tone": "professional"
                }

            return {"error": "AI analysis failed"}

        except Exception as e:
            return {"error": str(e)}

    def _build_client_profile(self, client_name: str, website_url: str,
                            seo_data: Dict, market_data: Dict, ai_intelligence: Dict) -> Dict:
        """Build comprehensive client profile"""

        # Calculate profile completion score
        profile_fields = ['industry', 'business_type', 'target_audience', 'primary_goals']
        completed_fields = sum(1 for field in profile_fields if ai_intelligence.get(field))
        profile_completion = (completed_fields / len(profile_fields)) * 0.6  # 60% for basic fields

        # Add bonus for additional data
        if seo_data.get('seo_score'):
            profile_completion += 0.2
        if market_data.get('success'):
            profile_completion += 0.2

        # Only include fields that exist in the database schema
        profile = {
            "client_name": client_name,
            "website_url": website_url,
            "industry": str(ai_intelligence.get("industry", "General Business")),
            "business_type": str(ai_intelligence.get("business_type", "Unknown")),
            "target_audience": str(ai_intelligence.get("target_audience", "General audience")),
            "brand_tone": str(ai_intelligence.get("recommended_brand_tone", "professional")),
            "company_size": str(ai_intelligence.get("company_size", "Unknown")),
            "primary_goals": str(ai_intelligence.get("primary_goals", "Increase online presence")),
            "seo_score": seo_data.get("seo_score") if seo_data.get("seo_score") is not None else 0,
            "profile_completion": min(profile_completion, 1.0),
            "last_analysis_date": datetime.now().date().isoformat()
        }

        return profile

    def _save_client_profile(self, profile: Dict) -> int:
        """Save client profile to database and return client_id"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Validate and sanitize all values for SQLite compatibility
            sanitized_values = (
                str(profile.get("client_name", "Unknown Client")),
                str(profile.get("website_url", "")),
                str(profile.get("industry", "General Business")),
                str(profile.get("business_type", "Unknown")),
                str(profile.get("target_audience", "General audience")),
                str(profile.get("brand_tone", "professional")),
                str(profile.get("company_size", "Unknown")),
                str(profile.get("primary_goals", "Increase online presence")),
                int(profile.get("seo_score", 0)) if profile.get("seo_score") is not None else 0,
                float(profile.get("profile_completion", 0.0)),
                str(profile.get("last_analysis_date", datetime.now().date().isoformat()))
            )

            cursor.execute('''
                INSERT OR REPLACE INTO client_profiles
                (client_name, website_url, industry, business_type, target_audience,
                 brand_tone, company_size, primary_goals, seo_score, profile_completion, last_analysis_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sanitized_values)

            client_id = cursor.lastrowid
            conn.commit()

            print(f"✅ Client profile saved successfully (ID: {client_id})")
            return client_id

        except Exception as e:
            print(f"❌ Error saving client profile: {str(e)}")
            print(f"Profile data: {profile}")
            conn.rollback()
            raise
        finally:
            conn.close()

    def _store_knowledge_base(self, client_id: int, seo_data: Dict, market_data: Dict, ai_intelligence: Dict):
        """Store extracted knowledge in the knowledge base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        knowledge_items = [
            ("seo_analysis", json.dumps(seo_data), 0.9, "SEO Analysis Engine"),
            ("market_research", json.dumps(market_data), 0.8, "Research Intelligence"),
            ("ai_intelligence", json.dumps(ai_intelligence), 0.85, "AI Analysis")
        ]

        for knowledge_type, data, confidence, source in knowledge_items:
            cursor.execute('''
                INSERT INTO client_knowledge
                (client_id, knowledge_type, knowledge_data, confidence_score, source)
                VALUES (?, ?, ?, ?, ?)
            ''', (client_id, knowledge_type, data, confidence, source))

        conn.commit()
        conn.close()

    def _generate_client_recommendations(self, client_id: int, profile: Dict) -> List[Dict]:
        """Generate smart recommendations based on client profile"""
        recommendations = []

        # SEO-based recommendations
        if profile.get("seo_score", 0) < 70:
            recommendations.append({
                "type": "seo_improvement",
                "title": "SEO Optimization Required",
                "description": f"Current SEO score is {profile.get('seo_score', 0)}/100. Immediate improvements needed.",
                "priority": 1,
                "estimated_impact": "High"
            })

        # Content recommendations based on business type
        business_type = profile.get("business_type", "").lower()
        if "saas" in business_type or "software" in business_type:
            recommendations.append({
                "type": "content_strategy",
                "title": "SaaS Content Marketing Strategy",
                "description": "Create educational content, case studies, and free tools to attract prospects.",
                "priority": 2,
                "estimated_impact": "Medium"
            })
        elif "local" in business_type or "service" in business_type:
            recommendations.append({
                "type": "local_seo",
                "title": "Local SEO Optimization",
                "description": "Focus on Google My Business, local keywords, and location-based content.",
                "priority": 1,
                "estimated_impact": "High"
            })

        # Marketing maturity recommendations
        if profile.get("marketing_maturity") == "Beginner":
            recommendations.append({
                "type": "foundation",
                "title": "Marketing Foundation Setup",
                "description": "Establish basic marketing infrastructure: analytics, email marketing, social presence.",
                "priority": 1,
                "estimated_impact": "High"
            })

        # Growth stage recommendations
        if profile.get("growth_stage") == "Early":
            recommendations.append({
                "type": "growth_strategy",
                "title": "Growth Stage Marketing",
                "description": "Focus on customer acquisition and retention strategies.",
                "priority": 2,
                "estimated_impact": "Medium"
            })

        return recommendations

    def _save_recommendations(self, client_id: int, recommendations: List[Dict]):
        """Save recommendations to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for rec in recommendations:
            cursor.execute('''
                INSERT INTO client_recommendations
                (client_id, recommendation_type, recommendation, priority)
                VALUES (?, ?, ?, ?)
            ''', (
                client_id,
                rec["type"],
                json.dumps(rec),
                rec.get("priority", 5)
            ))

        conn.commit()
        conn.close()

    def get_client_profiles(self) -> List[Dict]:
        """Get all client profiles"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, client_name, website_url, industry, business_type,
                   target_audience, profile_completion, last_analysis_date, seo_score
            FROM client_profiles
            ORDER BY updated_at DESC
        ''')

        profiles = []
        for row in cursor.fetchall():
            profiles.append({
                "id": row[0],
                "client_name": row[1],
                "website_url": row[2],
                "industry": row[3],
                "business_type": row[4],
                "target_audience": row[5],
                "profile_completion": row[6],
                "last_analysis_date": row[7],
                "seo_score": row[8]
            })

        conn.close()
        return profiles

    def list_clients(self) -> List[Dict]:
        """Get simplified client list for UI display"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT id, client_name, website_url
                FROM client_profiles
                ORDER BY updated_at DESC
            ''')

            clients = []
            for row in cursor.fetchall():
                # Extract domain from website_url for cleaner display
                website_url = row[2] or ""
                domain = website_url.replace("https://", "").replace("http://", "").split("/")[0]

                clients.append({
                    "id": row[0],
                    "name": row[1],
                    "domain": domain
                })

            return clients

        except Exception as e:
            print(f"❌ Error listing clients: {str(e)}")
            return []
        finally:
            conn.close()

    def get_client_profile(self, client_id: int) -> Dict:
        """Get single client profile by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT client_name, website_url, industry, business_type, target_audience,
                       brand_tone, company_size, primary_goals, seo_score, profile_completion,
                       last_analysis_date
                FROM client_profiles
                WHERE id = ?
            ''', (client_id,))

            row = cursor.fetchone()
            if not row:
                return None

            # Extract domain for cleaner display
            website_url = row[1] or ""
            domain = website_url.replace("https://", "").replace("http://", "").split("/")[0]

            return {
                "id": client_id,
                "name": row[0],
                "domain": domain,
                "website_url": row[1],
                "industry": row[2],
                "business_type": row[3],
                "target_audience": row[4],
                "brand_tone": row[5],
                "company_size": row[6],
                "primary_goals": row[7],
                "seo_score": row[8],
                "profile_completion": row[9],
                "last_analysis_date": row[10],
                "location": ""  # Add empty location for compatibility
            }

        except Exception as e:
            print(f"❌ Error getting client profile: {str(e)}")
            return None
        finally:
            conn.close()

    def get_client_recommendations(self, client_id: int) -> List[str]:
        """Get client recommendations as simple strings for UI display"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT recommendation
                FROM client_recommendations
                WHERE client_id = ?
                ORDER BY priority DESC
            ''', (client_id,))

            recommendations = []
            for row in cursor.fetchall():
                try:
                    # The recommendation is stored as JSON, extract the text
                    rec_data = json.loads(row[0])
                    rec_text = rec_data.get("text", str(rec_data))
                    recommendations.append(rec_text)
                except:
                    # Fallback to raw text
                    recommendations.append(str(row[0]))

            return recommendations

        except Exception as e:
            print(f"❌ Error getting client recommendations: {str(e)}")
            return []
        finally:
            conn.close()

    def get_client_context(self, client_id: int) -> Dict:
        """Get full client context for tool integration"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get client profile
        cursor.execute('SELECT * FROM client_profiles WHERE id = ?', (client_id,))
        profile_row = cursor.fetchone()

        if not profile_row:
            return {"error": "Client not found"}

        # Get knowledge base
        cursor.execute('SELECT knowledge_type, knowledge_data FROM client_knowledge WHERE client_id = ?', (client_id,))
        knowledge_items = cursor.fetchall()

        # Get recommendations
        cursor.execute('SELECT recommendation FROM client_recommendations WHERE client_id = ? AND status = "pending"', (client_id,))
        recommendations = [json.loads(row[0]) for row in cursor.fetchall()]

        conn.close()

        # Build complete context
        context = {
            "client_id": client_id,
            "client_name": profile_row[1],
            "website_url": profile_row[2],
            "industry": profile_row[3],
            "business_type": profile_row[4],
            "target_audience": profile_row[5],
            "brand_tone": profile_row[6],
            "company_size": profile_row[7],
            "primary_goals": profile_row[8],
            "seo_score": profile_row[12],
            "profile_completion": profile_row[13],
            "knowledge_base": {},
            "recommendations": recommendations
        }

        # Add knowledge base data
        for knowledge_type, knowledge_data in knowledge_items:
            try:
                context["knowledge_base"][knowledge_type] = json.loads(knowledge_data)
            except:
                context["knowledge_base"][knowledge_type] = knowledge_data

        return context

    def refresh_client_intelligence(self, client_id: int) -> Dict:
        """Refresh client intelligence with latest data"""
        # Get current profile
        context = self.get_client_context(client_id)
        if "error" in context:
            return context

        website_url = context["website_url"]
        client_name = context["client_name"]

        # Re-run discovery process
        return self.create_client_from_website(website_url, client_name)

def format_client_discovery_output(result: Dict) -> str:
    """Format client discovery results for display"""

    if not result["success"]:
        return f"""
🚨 CLIENT DISCOVERY FAILED
==========================

Error: {result.get('error', 'Unknown error')}
Client: {result.get('client_name', 'Unknown')}
Website: {result.get('website_url', 'Unknown')}

Please check the website URL and try again.
"""

    profile = result["client_profile"]
    recommendations = result["recommendations"]

    output = f"""
🔍 SMART CLIENT DISCOVERY COMPLETE
=================================

📊 CLIENT PROFILE:
• Client ID: {result['client_id']}
• Name: {profile['client_name']}
• Website: {profile['website_url']}
• Industry: {profile['industry']}
• Business Type: {profile['business_type']}
• Company Size: {profile['company_size']}
• Growth Stage: {profile.get('growth_stage', 'Unknown')}
• Marketing Maturity: {profile.get('marketing_maturity', 'Unknown')}
• Profile Completion: {profile['profile_completion']*100:.0f}%
• Discovery Time: {result['discovery_time']}s

👥 TARGET AUDIENCE:
{profile['target_audience']}

🎯 PRIMARY GOALS:
{profile['primary_goals']}

💡 VALUE PROPOSITION:
{profile.get('value_proposition', 'To be determined')}

⚡ COMPETITIVE ADVANTAGE:
{profile.get('competitive_advantage', 'To be analyzed')}

📊 SEO PERFORMANCE:
Current Score: {profile.get('seo_score', 'N/A')}/100
"""

    if recommendations:
        output += f"""
🎯 SMART RECOMMENDATIONS:
========================
"""
        for i, rec in enumerate(recommendations, 1):
            priority_emoji = "🔴" if rec["priority"] == 1 else "🟡" if rec["priority"] == 2 else "🟢"
            output += f"""
{i}. {priority_emoji} {rec['title']} (Priority {rec['priority']})
   {rec['description']}
   Expected Impact: {rec.get('estimated_impact', 'Medium')}
"""

    output += f"""
{"="*50}
✅ CLIENT INTELLIGENCE SYSTEM READY
Profile stored with ID: {result['client_id']}
All marketing tools now have full client context!
{"="*50}
"""

    return output