#!/usr/bin/env python3
"""Find Vercel Team ID"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.vercel')

VERCEL_TOKEN = os.getenv('VERCEL_TOKEN')

def list_teams():
    """List all teams for the authenticated user"""
    headers = {
        'Authorization': f'Bearer {VERCEL_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    print("🔍 Fetching user information...")
    # First get user info
    response = requests.get('https://api.vercel.com/v2/user', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        print(f"✅ Authenticated as: {user_data['user']['username']}")
        print(f"   Email: {user_data['user']['email']}")
        print(f"   Name: {user_data['user']['name']}")
    else:
        print(f"❌ Authentication failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return
    
    print("\n🔍 Fetching teams...")
    # List all teams
    response = requests.get('https://api.vercel.com/v2/teams', headers=headers)
    if response.status_code == 200:
        teams_data = response.json()
        teams = teams_data.get('teams', [])
        
        if not teams:
            print("📝 No teams found. You might be using a personal account.")
            print("\n💡 For personal accounts, you don't need to specify a team ID.")
            print("   Just remove the VERCEL_TEAM_ID from your .env.vercel file")
            print("   or leave it empty.")
        else:
            print(f"\n✅ Found {len(teams)} team(s):")
            for team in teams:
                print(f"\n   Team Name: {team.get('name', 'N/A')}")
                print(f"   Team ID: {team.get('id', 'N/A')}")
                print(f"   Team Slug: {team.get('slug', 'N/A')}")
                print(f"   Created: {team.get('created', 'N/A')}")
                
                # Check if this could be "Eduard Wolf's projects"
                if 'eduard' in team.get('name', '').lower() or 'wolf' in team.get('name', '').lower():
                    print("   ⭐ This might be 'Eduard Wolf's projects'!")
    else:
        print(f"❌ Failed to fetch teams: {response.status_code}")
        print(f"   Response: {response.text}")
    
    print("\n🔍 Testing API access without team ID...")
    # Try to list projects without team ID (personal account)
    response = requests.get('https://api.vercel.com/v8/projects', headers=headers)
    if response.status_code == 200:
        projects = response.json().get('projects', [])
        print(f"✅ Can access projects without team ID. Found {len(projects)} project(s)")
        if projects:
            print("   First few projects:")
            for project in projects[:3]:
                print(f"   - {project['name']}")
    else:
        print(f"❌ Cannot access projects without team ID: {response.status_code}")

if __name__ == "__main__":
    print("🚀 Vercel Team Finder")
    print("=" * 50)
    
    if not VERCEL_TOKEN:
        print("❌ VERCEL_TOKEN not set in .env.vercel")
        exit(1)
    
    list_teams()
    
    print("\n" + "=" * 50)
    print("📝 Next steps:")
    print("1. If you found a team, update VERCEL_TEAM_ID in .env.vercel")
    print("   Use either the 'id' or 'slug' value")
    print("2. If no teams found (personal account), remove VERCEL_TEAM_ID")
    print("3. Run test-vercel-api.py again to verify")