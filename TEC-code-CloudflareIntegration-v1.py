#!/usr/bin/env python3
"""
Cloudflare Integration Framework für MarketingFunnelMaster
Version: 1.0
Zweck: Automatisierte DNS & CDN-Konfiguration für 25 Domains Phase 1

Autor: Claude Code (HTD-Executor)
Erstellt: 2025-07-03
"""

import CloudFlare
import requests
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudflareManager:
    """
    Cloudflare API Manager für MarketingFunnelMaster
    Unterstützt automatisierte DNS-Konfiguration und CDN-Setup
    """
    
    def __init__(self, api_token: str, email: str = None):
        """
        Initialize Cloudflare Manager
        
        Args:
            api_token (str): Cloudflare API Token
            email (str): Cloudflare account email (optional)
        """
        self.api_token = api_token
        self.email = email
        
        # Initialize Cloudflare client
        if email:
            self.cf = CloudFlare.CloudFlare(email=email, token=api_token)
        else:
            self.cf = CloudFlare.CloudFlare(token=api_token)
        
        logger.info("Cloudflare Manager initialized")
    
    def add_domain_to_cloudflare(self, domain: str, plan_type: str = "free") -> Dict:
        """
        Add domain to Cloudflare and configure basic settings
        
        Args:
            domain (str): Domain name to add
            plan_type (str): Plan type (free, pro, business)
        
        Returns:
            Dict: Zone creation result
        """
        try:
            # Add zone to Cloudflare
            zone_data = {
                'name': domain,
                'account': {'id': self._get_account_id()},
                'plan': {'id': self._get_plan_id(plan_type)}
            }
            
            zone = self.cf.zones.post(data=zone_data)
            zone_id = zone['id']
            
            logger.info(f"Domain {domain} added to Cloudflare with Zone ID: {zone_id}")
            
            # Configure basic security settings
            self._configure_security_settings(zone_id)
            
            # Enable caching
            self._configure_caching(zone_id)
            
            return {
                'success': True,
                'zone_id': zone_id,
                'nameservers': zone['name_servers'],
                'domain': domain,
                'plan': plan_type
            }
            
        except Exception as e:
            logger.error(f"Error adding domain {domain}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def setup_dns_records(self, domain: str, server_ip: str) -> Dict:
        """
        Setup standard DNS records for a domain
        
        Args:
            domain (str): Domain name
            server_ip (str): Hetzner server IP address
        
        Returns:
            Dict: DNS setup result
        """
        try:
            zone_id = self._get_zone_id(domain)
            if not zone_id:
                return {'success': False, 'error': 'Zone not found'}
            
            records_created = []
            
            # A Record for root domain
            a_record = self._create_dns_record(
                zone_id, 'A', '@', server_ip, proxied=True
            )
            records_created.append(a_record)
            
            # CNAME for www
            www_record = self._create_dns_record(
                zone_id, 'CNAME', 'www', domain, proxied=True
            )
            records_created.append(www_record)
            
            # A Record for API subdomain
            api_record = self._create_dns_record(
                zone_id, 'A', 'api', server_ip, proxied=True
            )
            records_created.append(api_record)
            
            logger.info(f"DNS records created for {domain}")
            
            return {
                'success': True,
                'domain': domain,
                'records': records_created
            }
            
        except Exception as e:
            logger.error(f"Error setting up DNS for {domain}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def bulk_domain_setup(self, domain_list: List[Dict]) -> List[Dict]:
        """
        Bulk setup multiple domains with DNS configuration
        
        Args:
            domain_list (List[Dict]): List of domains with configuration
                Example: [
                    {'name': 'example.com', 'plan': 'free', 'ip': '1.2.3.4'},
                    {'name': 'test.com', 'plan': 'pro', 'ip': '1.2.3.4'}
                ]
        
        Returns:
            List[Dict]: Results for each domain
        """
        results = []
        
        for domain_config in domain_list:
            domain = domain_config['name']
            plan = domain_config.get('plan', 'free')
            server_ip = domain_config['ip']
            
            logger.info(f"Processing domain: {domain}")
            
            # Add domain to Cloudflare
            zone_result = self.add_domain_to_cloudflare(domain, plan)
            
            if zone_result['success']:
                # Setup DNS records
                dns_result = self.setup_dns_records(domain, server_ip)
                
                # Combine results
                result = {
                    'domain': domain,
                    'zone_creation': zone_result,
                    'dns_setup': dns_result,
                    'nameservers': zone_result.get('nameservers', [])
                }
            else:
                result = {
                    'domain': domain,
                    'zone_creation': zone_result,
                    'dns_setup': {'success': False, 'error': 'Zone creation failed'},
                    'nameservers': []
                }
            
            results.append(result)
            
            # Rate limiting - avoid API limits
            time.sleep(2)
        
        return results
    
    def enable_security_features(self, domain: str) -> Dict:
        """
        Enable Cloudflare security features for a domain
        
        Args:
            domain (str): Domain name
        
        Returns:
            Dict: Security configuration result
        """
        try:
            zone_id = self._get_zone_id(domain)
            if not zone_id:
                return {'success': False, 'error': 'Zone not found'}
            
            security_settings = [
                # Always Use HTTPS
                {'id': 'always_use_https', 'value': 'on'},
                
                # Security Level
                {'id': 'security_level', 'value': 'medium'},
                
                # Challenge Passage
                {'id': 'challenge_ttl', 'value': 1800},
                
                # Browser Integrity Check
                {'id': 'browser_check', 'value': 'on'},
                
                # Hotlink Protection
                {'id': 'hotlink_protection', 'value': 'off'},
                
                # IP Geolocation
                {'id': 'ip_geolocation', 'value': 'on'},
                
                # WAF (if available on plan)
                {'id': 'waf', 'value': 'on'}
            ]
            
            for setting in security_settings:
                try:
                    self.cf.zones.settings.patch(
                        zone_id, 
                        setting['id'], 
                        data={'value': setting['value']}
                    )
                except Exception as e:
                    logger.warning(f"Could not set {setting['id']}: {str(e)}")
            
            logger.info(f"Security features enabled for {domain}")
            return {'success': True, 'domain': domain}
            
        except Exception as e:
            logger.error(f"Error enabling security for {domain}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def get_domain_analytics(self, domain: str, since_days: int = 7) -> Dict:
        """
        Get analytics data for a domain
        
        Args:
            domain (str): Domain name
            since_days (int): Number of days to look back
        
        Returns:
            Dict: Analytics data
        """
        try:
            zone_id = self._get_zone_id(domain)
            if not zone_id:
                return {'success': False, 'error': 'Zone not found'}
            
            # Calculate date range
            import datetime
            end_date = datetime.datetime.utcnow()
            start_date = end_date - datetime.timedelta(days=since_days)
            
            # Get analytics
            analytics = self.cf.zones.analytics.dashboard.get(
                zone_id,
                params={
                    'since': start_date.isoformat() + 'Z',
                    'until': end_date.isoformat() + 'Z'
                }
            )
            
            return {
                'success': True,
                'domain': domain,
                'analytics': analytics
            }
            
        except Exception as e:
            logger.error(f"Error getting analytics for {domain}: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _get_zone_id(self, domain: str) -> Optional[str]:
        """Get Zone ID for a domain"""
        try:
            zones = self.cf.zones.get(params={'name': domain})
            if zones:
                return zones[0]['id']
            return None
        except Exception:
            return None
    
    def _get_account_id(self) -> str:
        """Get first account ID"""
        try:
            accounts = self.cf.accounts.get()
            return accounts[0]['id']
        except Exception:
            raise Exception("Could not get account ID")
    
    def _get_plan_id(self, plan_type: str) -> str:
        """Get plan ID based on plan type"""
        plan_mapping = {
            'free': 'free',
            'pro': 'pro',
            'business': 'business',
            'enterprise': 'enterprise'
        }
        return plan_mapping.get(plan_type, 'free')
    
    def _create_dns_record(self, zone_id: str, record_type: str, 
                          name: str, content: str, proxied: bool = True) -> Dict:
        """Create DNS record"""
        record_data = {
            'type': record_type,
            'name': name,
            'content': content,
            'proxied': proxied
        }
        
        record = self.cf.zones.dns_records.post(zone_id, data=record_data)
        return record
    
    def _configure_security_settings(self, zone_id: str):
        """Configure basic security settings for a zone"""
        settings = [
            {'id': 'always_use_https', 'value': 'on'},
            {'id': 'ssl', 'value': 'flexible'},
            {'id': 'security_level', 'value': 'medium'},
            {'id': 'browser_check', 'value': 'on'}
        ]
        
        for setting in settings:
            try:
                self.cf.zones.settings.patch(
                    zone_id, 
                    setting['id'], 
                    data={'value': setting['value']}
                )
            except Exception as e:
                logger.warning(f"Could not set {setting['id']}: {str(e)}")
    
    def _configure_caching(self, zone_id: str):
        """Configure caching settings"""
        cache_settings = [
            {'id': 'caching_level', 'value': 'aggressive'},
            {'id': 'browser_cache_ttl', 'value': 14400},  # 4 hours
            {'id': 'edge_cache_ttl', 'value': 7200}       # 2 hours
        ]
        
        for setting in cache_settings:
            try:
                self.cf.zones.settings.patch(
                    zone_id, 
                    setting['id'], 
                    data={'value': setting['value']}
                )
            except Exception as e:
                logger.warning(f"Could not set cache {setting['id']}: {str(e)}")


# Configuration Class
class CloudflareConfig:
    """Configuration for Cloudflare setup"""
    
    # Phase 1 Domain Configuration
    PHASE1_DOMAINS = [
        {'name': 'smartringfitness.com', 'plan': 'pro', 'priority': 'high'},
        {'name': 'biohackertools.com', 'plan': 'pro', 'priority': 'high'},
        {'name': 'ledcontroller-pro.com', 'plan': 'pro', 'priority': 'high'},
        {'name': 'aiworkflow-dashboard.com', 'plan': 'pro', 'priority': 'high'},
        {'name': 'notiontemplate-hub.com', 'plan': 'pro', 'priority': 'high'},
        {'name': 'techgadget-reviews.com', 'plan': 'free', 'priority': 'medium'},
        {'name': 'fitnesstracker-guide.com', 'plan': 'free', 'priority': 'medium'},
        {'name': 'smartdevice-insider.com', 'plan': 'free', 'priority': 'medium'},
        {'name': 'productivity-hacker.com', 'plan': 'free', 'priority': 'medium'},
        {'name': 'gadgetlaunch-tracker.com', 'plan': 'free', 'priority': 'medium'},
        {'name': 'wearabletech-expert.com', 'plan': 'free', 'priority': 'medium'},
        {'name': 'homeautomation-pro.com', 'plan': 'free', 'priority': 'medium'},
        {'name': 'techsavings-finder.com', 'plan': 'free', 'priority': 'medium'},
        {'name': 'digitalhealth-tools.com', 'plan': 'free', 'priority': 'medium'},
        {'name': 'innovation-scanner.com', 'plan': 'free', 'priority': 'medium'},
        {'name': 'smartringfitness.de', 'plan': 'free', 'priority': 'low'},
        {'name': 'biohackertools.net', 'plan': 'free', 'priority': 'low'},
        {'name': 'aiworkflow-hub.org', 'plan': 'free', 'priority': 'low'},
        {'name': 'techgadget-insider.com', 'plan': 'free', 'priority': 'low'},
        {'name': 'fitnesshub-pro.com', 'plan': 'free', 'priority': 'low'},
        {'name': 'smartdevices-review.com', 'plan': 'free', 'priority': 'low'},
        {'name': 'test-smartring.com', 'plan': 'free', 'priority': 'dev'},
        {'name': 'dev-biohacker.com', 'plan': 'free', 'priority': 'dev'},
        {'name': 'staging-aiworkflow.com', 'plan': 'free', 'priority': 'dev'},
        {'name': 'beta-techgadget.com', 'plan': 'free', 'priority': 'dev'}
    ]
    
    # Server IP (will be updated with Hetzner IP)
    HETZNER_SERVER_IP = "116.203.XXX.XXX"  # Placeholder - wird mit echter IP ersetzt


# Main execution function
def setup_cloudflare_infrastructure(api_token: str, server_ip: str):
    """
    Main function to setup Cloudflare infrastructure for Phase 1
    
    Args:
        api_token (str): Cloudflare API token
        server_ip (str): Hetzner server IP address
    """
    
    logger.info("Starting Cloudflare infrastructure setup...")
    
    # Initialize Cloudflare Manager
    cf_manager = CloudflareManager(api_token)
    
    # Prepare domain list with server IP
    domain_configs = []
    for domain_info in CloudflareConfig.PHASE1_DOMAINS:
        domain_configs.append({
            'name': domain_info['name'],
            'plan': domain_info['plan'],
            'ip': server_ip
        })
    
    # Bulk setup domains
    results = cf_manager.bulk_domain_setup(domain_configs)
    
    # Generate report
    successful_domains = [r for r in results if r['zone_creation']['success']]
    failed_domains = [r for r in results if not r['zone_creation']['success']]
    
    print(f"\n=== CLOUDFLARE SETUP RESULTS ===")
    print(f"Successful domains: {len(successful_domains)}")
    print(f"Failed domains: {len(failed_domains)}")
    
    if successful_domains:
        print("\n✅ Successfully configured domains:")
        for domain in successful_domains:
            print(f"  - {domain['domain']}")
    
    if failed_domains:
        print("\n❌ Failed domains:")
        for domain in failed_domains:
            print(f"  - {domain['domain']}: {domain['zone_creation'].get('error', 'Unknown error')}")
    
    # Generate nameserver update instructions
    print(f"\n=== NAMESERVER UPDATE REQUIRED ===")
    print("Update nameservers at INWX for the following domains:")
    for domain in successful_domains:
        nameservers = domain['nameservers']
        print(f"\nDomain: {domain['domain']}")
        for i, ns in enumerate(nameservers, 1):
            print(f"  NS{i}: {ns}")
    
    return results


if __name__ == "__main__":
    # Example usage - Replace with actual values
    API_TOKEN = "your_cloudflare_api_token_here"
    SERVER_IP = "116.203.XXX.XXX"  # Replace with actual Hetzner IP
    
    # Run setup
    setup_results = setup_cloudflare_infrastructure(API_TOKEN, SERVER_IP)
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"cloudflare_setup_results_{timestamp}.json", "w") as f:
        json.dump(setup_results, f, indent=2, default=str)
    
    print(f"\nResults saved to: cloudflare_setup_results_{timestamp}.json")