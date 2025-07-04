#!/usr/bin/env python3
"""Test Vercel API Integration"""

import os
import requests
from dotenv import load_dotenv

load_dotenv('.env.vercel')

VERCEL_TOKEN = os.getenv('VERCEL_TOKEN')
VERCEL_TEAM_ID = os.getenv('VERCEL_TEAM_ID')

def test_vercel_connection():
    """Test Vercel API Verbindung"""
    headers = {
        'Authorization': f'Bearer {VERCEL_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Test 1: User Info
    print("🔍 Test 1: Vercel User Info...")
    response = requests.get('https://api.vercel.com/v2/user', headers=headers)
    if response.status_code == 200:
        print("✅ User authenticated:", response.json()['user']['username'])
    else:
        print("❌ Authentication failed:", response.status_code)
        return False
    
    # Test 2: Team Info
    if VERCEL_TEAM_ID:
        print("\n🔍 Test 2: Team Info...")
        response = requests.get(
            f'https://api.vercel.com/v1/teams/{VERCEL_TEAM_ID}', 
            headers=headers
        )
        if response.status_code == 200:
            print("✅ Team found:", response.json()['name'])
        else:
            print("❌ Team not found:", response.status_code)
    
    # Test 3: Projects List
    print("\n🔍 Test 3: Projects List...")
    response = requests.get(
        'https://api.vercel.com/v8/projects',
        headers=headers,
        params={'teamId': VERCEL_TEAM_ID} if VERCEL_TEAM_ID else {}
    )
    if response.status_code == 200:
        projects = response.json()['projects']
        print(f"✅ Found {len(projects)} projects")
        for project in projects[:3]:
            print(f"  - {project['name']}")
    
    return True

if __name__ == "__main__":
    print("🚀 Vercel API Integration Test")
    print("=" * 40)
    
    if not VERCEL_TOKEN:
        print("❌ VERCEL_TOKEN nicht gesetzt in .env.vercel")
        exit(1)
    
    if test_vercel_connection():
        print("\n✅ Vercel API Integration erfolgreich!")
    else:
        print("\n❌ Vercel API Integration fehlgeschlagen!")