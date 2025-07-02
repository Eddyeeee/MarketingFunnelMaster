#!/usr/bin/env python3
"""
Data Input Interface for Research Data

Easy-to-use interface for feeding research data from Gemini/ChatGPT research
into the Creator Analyzer learning system.
"""

import asyncio
import json
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path

from research_data_ingestion import ResearchDataIngestion, ResearchSource

class DataInputInterface:
    """Simple interface for inputting research data"""
    
    def __init__(self):
        self.ingestion_system = ResearchDataIngestion()
        self.templates = self._create_templates()
    
    def _create_templates(self) -> Dict[str, Dict]:
        """Create data templates for easy input"""
        
        return {
            'influencer': {
                'name': '',  # Required: Full name
                'handle': '',  # Social media handle
                'platforms': [],  # ['Instagram', 'YouTube', 'TikTok', 'LinkedIn']
                'primary_platform': '',  # Main platform
                'followers': {
                    # 'instagram': 0,
                    # 'youtube': 0,
                    # 'tiktok': 0
                },
                'tier': 'micro',  # nano, micro, macro, mega
                'niche': 'online_marketing',  # Main niche
                'sub_niches': [],  # Additional niches
                
                # Content Analysis
                'content_themes': [],  # Main content themes
                'posting_frequency': '',  # daily, weekly, etc.
                'content_formats': [],  # video, carousel, story, etc.
                
                # Funnel Structure
                'funnel_type': '',  # course, coaching, product, etc.
                'funnel_stages': [],  # awareness, interest, etc.
                'lead_magnets': [],  # free content offerings
                'pricing_strategy': {},  # price points
                'products_services': [],  # what they sell
                
                # Current Strategies 2024/2025
                'current_hooks': [],  # hook examples
                'hook_patterns': [],  # patterns they use
                'trending_strategies': [],  # what's working now
                'content_innovations': [],  # new approaches
                
                # Performance
                'engagement_rate': 0.0,  # average engagement %
                'estimated_revenue': '',  # revenue estimate
                'conversion_indicators': [],  # signs of success
                
                # Meta
                'confidence_score': 0.8,  # how confident in data
                'profile_urls': {},  # links to profiles
                'funnel_examples': [],  # example funnel links
                'case_study_links': []  # relevant case studies
            },
            
            'hook': {
                'hook_text': '',  # The actual hook text
                'hook_category': '',  # curiosity, fear, desire, etc.
                'structure_pattern': '',  # pattern description
                'german_specific': True,  # True for German market
                'effectiveness_score': 0.0,  # 0-1 effectiveness
                'usage_examples': [],  # where seen used
                'source_influencer': '',  # who uses it
                'platform_optimized': '',  # best platform
                'trend_period': '2024',  # when trending
                'psychological_trigger': ''  # psychological basis
            },
            
            'funnel': {
                'influencer_name': '',  # Who owns this funnel
                'funnel_name': '',  # Funnel name/description
                'funnel_type': '',  # webinar, course, product, etc.
                
                # Funnel Stages
                'awareness_stage': {},  # how they create awareness
                'interest_stage': {},  # how they build interest
                'consideration_stage': {},  # how they handle consideration
                'conversion_stage': {},  # how they convert
                'retention_stage': {},  # how they retain customers
                
                # Pricing
                'entry_price': 0.0,  # lowest price point
                'mid_tier_price': 0.0,  # middle price point
                'premium_price': 0.0,  # highest price point
                'pricing_psychology': [],  # pricing tactics used
                
                # Hooks & Strategies
                'primary_hooks': [],  # main hooks used
                'secondary_hooks': [],  # supporting hooks
                'urgency_tactics': [],  # urgency methods
                'social_proof_elements': [],  # social proof types
                
                # 2024/2025 Innovations
                'new_strategies': [],  # new approaches
                'trend_adaptations': [],  # trend adaptations
                'platform_specific_tactics': {},  # platform-specific tactics
                
                # Performance
                'estimated_conversion_rate': 0.0,  # conversion %
                'estimated_monthly_revenue': 0.0,  # monthly revenue
                'success_indicators': []  # signs of success
            },
            
            'strategy': {
                'strategy_name': '',  # Strategy name
                'strategy_description': '',  # What it is
                'implementation_details': {},  # How to implement
                'target_audience': '',  # Who it's for
                'required_resources': [],  # What's needed
                'expected_results': {},  # Expected outcomes
                'risk_factors': [],  # Potential risks
                'source_influencers': [],  # Who uses it
                'trend_status': 'emerging',  # emerging, established, declining
                'market_fit_score': 0.0  # 0-1 market fit
            }
        }
    
    def show_templates(self):
        """Show available templates"""
        print("📝 AVAILABLE TEMPLATES:")
        print("=" * 50)
        
        for template_name, template in self.templates.items():
            print(f"\n🎯 {template_name.upper()} TEMPLATE:")
            print(f"Required fields: {[k for k, v in template.items() if v == '' or v == 0.0]}")
            print(f"Optional fields: {len([k for k, v in template.items() if v not in ['', 0.0]])}")
    
    def create_influencer_data(self, **kwargs) -> Dict[str, Any]:
        """Create influencer data from input"""
        data = self.templates['influencer'].copy()
        data.update(kwargs)
        return data
    
    def create_hook_data(self, **kwargs) -> Dict[str, Any]:
        """Create hook data from input"""
        data = self.templates['hook'].copy()
        data.update(kwargs)
        return data
    
    def create_funnel_data(self, **kwargs) -> Dict[str, Any]:
        """Create funnel data from input"""
        data = self.templates['funnel'].copy()
        data.update(kwargs)
        return data
    
    def create_strategy_data(self, **kwargs) -> Dict[str, Any]:
        """Create strategy data from input"""
        data = self.templates['strategy'].copy()
        data.update(kwargs)
        return data
    
    async def submit_research_session(self, 
                                    session_name: str,
                                    researcher_name: str,
                                    research_source: str,
                                    data: Dict[str, List[Dict]]) -> str:
        """Submit a complete research session"""
        
        source_enum = ResearchSource(research_source.lower())
        
        session_id = await self.ingestion_system.ingest_research_session(
            session_name=session_name,
            researcher_name=researcher_name,
            research_source=source_enum,
            data=data
        )
        
        print(f"✅ Research session submitted: {session_id}")
        print(f"📊 Stats: {self.ingestion_system.get_ingestion_stats()}")
        
        return session_id
    
    def save_research_to_file(self, data: Dict[str, Any], filename: str):
        """Save research data to JSON file for later submission"""
        
        filepath = Path(__dirname__).parent.parent / "exports" / f"{filename}.json"
        filepath.parent.mkdir(exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Research data saved to: {filepath}")
    
    def load_research_from_file(self, filename: str) -> Dict[str, Any]:
        """Load research data from JSON file"""
        
        filepath = Path(__dirname__).parent.parent / "exports" / f"{filename}.json"
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print(f"📂 Research data loaded from: {filepath}")
        return data
    
    async def quick_submit_influencer(self, influencer_data: Dict[str, Any]) -> str:
        """Quick submit single influencer"""
        
        session_data = {
            'influencers': [influencer_data],
            'hooks': [],
            'funnels': [],
            'strategies': []
        }
        
        return await self.submit_research_session(
            session_name=f"Quick Submit: {influencer_data.get('name', 'Unknown')}",
            researcher_name="Manual Input",
            research_source="manual_human",
            data=session_data
        )
    
    async def batch_submit_from_gemini_research(self, gemini_data: Dict[str, Any]) -> str:
        """Submit research data specifically from Gemini research"""
        
        return await self.submit_research_session(
            session_name=f"Gemini Research: {gemini_data.get('session_name', datetime.now().strftime('%Y-%m-%d'))}",
            researcher_name="Gemini AI Assistant",
            research_source="manual_gemini",
            data=gemini_data
        )
    
    async def batch_submit_from_chatgpt_research(self, chatgpt_data: Dict[str, Any]) -> str:
        """Submit research data specifically from ChatGPT research"""
        
        return await self.submit_research_session(
            session_name=f"ChatGPT Research: {chatgpt_data.get('session_name', datetime.now().strftime('%Y-%m-%d'))}",
            researcher_name="ChatGPT Assistant",
            research_source="manual_chatgpt",
            data=chatgpt_data
        )
    
    def create_german_marketing_session_template(self) -> Dict[str, Any]:
        """Create template for German marketing influencer research session"""
        
        return {
            'session_name': 'Top 20 German Online Marketing Influencers 2024/2025',
            'research_focus': 'German online marketing space',
            'target_count': 20,
            'influencers': [],  # Fill with influencer data
            'hooks': [],        # Fill with hook data
            'funnels': [],      # Fill with funnel data  
            'strategies': [],   # Fill with strategy data
            'research_notes': {
                'methodology': 'Manual research using Gemini and ChatGPT',
                'focus_areas': [
                    'Funnel structures and pricing',
                    'Current hooks and strategies 2024/2025',
                    'Platform-specific adaptations',
                    'German market specifics'
                ],
                'data_quality': 'High - manually verified',
                'completion_date': datetime.now().isoformat()
            }
        }

# Example usage functions
def example_german_influencer():
    """Example of how to create German influencer data"""
    
    interface = DataInputInterface()
    
    # Example: Tobias Beck (hypothetical data for demonstration)
    tobias_beck = interface.create_influencer_data(
        name="Tobias Beck",
        handle="@tobiasxbeck",
        platforms=["Instagram", "YouTube", "LinkedIn"],
        primary_platform="Instagram",
        followers={
            "instagram": 850000,
            "youtube": 320000,
            "linkedin": 45000
        },
        tier="macro",
        niche="personal_development",
        sub_niches=["business_mindset", "success_coaching", "entrepreneurship"],
        content_themes=[
            "Mindset-Training",
            "Erfolgsprinzipien", 
            "Persönlichkeitsentwicklung",
            "Business-Psychologie"
        ],
        posting_frequency="daily",
        content_formats=["video", "carousel", "story", "reel"],
        funnel_type="coaching_program",
        funnel_stages=[
            "Free content attraction",
            "Email list building", 
            "Webinar presentation",
            "High-ticket coaching offer"
        ],
        lead_magnets=[
            "Kostenloses Mindset-Training",
            "7 Erfolgsgeheimnisse PDF",
            "Persönlichkeitstest"
        ],
        pricing_strategy={
            "entry_level": 97,
            "coaching_program": 2997,
            "vip_coaching": 9997
        },
        current_hooks=[
            "Das haben 99% der Menschen noch nie gehört...",
            "Warum reiche Menschen anders denken",
            "Der Mindset-Fehler, der dich arm hält",
            "3 Sekunden entscheiden über deinen Erfolg"
        ],
        hook_patterns=[
            "Exklusivität (99% der Menschen...)",
            "Autorität (Reiche Menschen...)",
            "Problem-Lösung (Fehler + Lösung)",
            "Zeitdruck (3 Sekunden...)"
        ],
        trending_strategies=[
            "Story-driven Content",
            "Live-Coaching Sessions",
            "Community Building",
            "Personal Branding"
        ],
        engagement_rate=8.5,
        estimated_revenue="6-stellig pro Monat",
        confidence_score=0.9
    )
    
    return tobias_beck

def example_german_hook():
    """Example of how to create German hook data"""
    
    interface = DataInputInterface()
    
    hook = interface.create_hook_data(
        hook_text="Das haben 99% der Menschen noch nie gehört...",
        hook_category="curiosity",
        structure_pattern="[Percentage] der Menschen + [never heard/seen/done] + [secret/truth]",
        german_specific=True,
        effectiveness_score=0.89,
        usage_examples=[
            "Instagram Stories",
            "YouTube Video Titles", 
            "Email Subject Lines"
        ],
        source_influencer="Tobias Beck",
        platform_optimized="Instagram",
        trend_period="2024",
        psychological_trigger="exclusivity + curiosity"
    )
    
    return hook

def example_session_submission():
    """Example of how to submit a complete research session"""
    
    interface = DataInputInterface()
    
    # Create session template
    session = interface.create_german_marketing_session_template()
    
    # Add example data
    session['influencers'] = [example_german_influencer()]
    session['hooks'] = [example_german_hook()]
    
    # Save to file for later submission
    interface.save_research_to_file(session, "german_marketing_research_2024")
    
    print("📝 Example session created and saved!")
    print("💡 You can now modify the JSON file and submit it later.")

# Interactive helper functions
def interactive_influencer_input():
    """Interactive function to input influencer data"""
    
    print("🎯 GERMAN INFLUENCER DATA INPUT")
    print("=" * 40)
    
    interface = DataInputInterface()
    
    # Basic info
    name = input("Name: ")
    handle = input("Handle (@username): ")
    platform = input("Primary Platform (Instagram/YouTube/TikTok): ")
    
    # Followers
    followers = {}
    if platform.lower() == 'instagram':
        followers['instagram'] = int(input("Instagram Followers: ") or 0)
    elif platform.lower() == 'youtube':
        followers['youtube'] = int(input("YouTube Subscribers: ") or 0)
    
    # Niche
    niche = input("Main Niche (online_marketing/personal_development/business): ")
    
    # Create influencer data
    influencer = interface.create_influencer_data(
        name=name,
        handle=handle,
        primary_platform=platform,
        followers=followers,
        niche=niche
    )
    
    print("\n✅ Influencer data created!")
    print(f"📄 Preview: {json.dumps(influencer, indent=2, ensure_ascii=False)[:200]}...")
    
    save = input("\n💾 Save to file? (y/n): ")
    if save.lower() == 'y':
        filename = input("Filename: ") or f"influencer_{name.lower().replace(' ', '_')}"
        interface.save_research_to_file({'influencers': [influencer]}, filename)
    
    return influencer

if __name__ == "__main__":
    print("🎯 RESEARCH DATA INPUT INTERFACE")
    print("=" * 50)
    
    interface = DataInputInterface()
    
    print("\n📝 Available Commands:")
    print("1. Show templates")
    print("2. Create example data")
    print("3. Interactive input")
    print("4. Submit example session")
    
    choice = input("\nSelect option (1-4): ")
    
    if choice == "1":
        interface.show_templates()
    elif choice == "2":
        example_session_submission()
    elif choice == "3":
        interactive_influencer_input()
    elif choice == "4":
        async def submit_example():
            session = interface.create_german_marketing_session_template()
            session['influencers'] = [example_german_influencer()]
            session['hooks'] = [example_german_hook()]
            
            session_id = await interface.submit_research_session(
                session_name="Example German Marketing Research",
                researcher_name="Demo User",
                research_source="manual_human",
                data=session
            )
            
            print(f"✅ Example session submitted: {session_id}")
        
        asyncio.run(submit_example())
    else:
        print("ℹ️  Use this interface to input your Gemini/ChatGPT research data!")
        print("💡 See example functions for guidance.")