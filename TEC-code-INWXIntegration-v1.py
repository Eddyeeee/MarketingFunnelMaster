#!/usr/bin/env python3
"""
INWX API Integration Framework für MarketingFunnelMaster
Version: 1.0
Zweck: Automatisierte Domain-Registrierung und DNS-Management

Autor: Claude Code (HTD-Executor)
Erstellt: 2025-07-03
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
import hashlib
import hmac

# Logging Setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class INWXAPIManager:
    """
    INWX API Manager für automatisierte Domain-Operations
    Unterstützt JSON-RPC und XML-RPC Protocols
    """
    
    def __init__(self, username: str, password: str, api_url: str = None, testing: bool = False):
        """
        Initialize INWX API Manager
        
        Args:
            username (str): INWX Username
            password (str): INWX Password
            api_url (str): API URL (optional)
            testing (bool): Use OT&E testing environment
        """
        self.username = username
        self.password = password
        self.session_id = None
        
        # Use testing environment if specified
        if testing:
            self.api_url = api_url or "https://ote.inwx.com/jsonrpc/"
            logger.info("Using INWX OT&E testing environment")
        else:
            self.api_url = api_url or "https://api.inwx.com/jsonrpc/"
            logger.info("Using INWX production environment")
        
        self.headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'MarketingFunnelMaster/1.0'
        }
        
        # Authenticate on initialization
        self._authenticate()
    
    def _authenticate(self) -> bool:
        """
        Authenticate with INWX API and get session ID
        
        Returns:
            bool: Authentication success
        """
        try:
            auth_data = {
                "method": "account.login",
                "params": {
                    "user": self.username,
                    "pass": self.password
                },
                "id": 1
            }
            
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=auth_data,
                timeout=30
            )
            
            result = response.json()
            
            if result.get('result', {}).get('code') == 1000:
                self.session_id = result['result']['msg']
                logger.info("INWX authentication successful")
                return True
            else:
                logger.error(f"INWX authentication failed: {result}")
                return False
                
        except Exception as e:
            logger.error(f"INWX authentication error: {str(e)}")
            return False
    
    def _make_api_call(self, method: str, params: Dict) -> Dict:
        """
        Make authenticated API call to INWX
        
        Args:
            method (str): API method name
            params (Dict): Method parameters
        
        Returns:
            Dict: API response
        """
        if not self.session_id:
            self._authenticate()
        
        # Add session ID to parameters
        params['sid'] = self.session_id
        
        api_data = {
            "method": method,
            "params": params,
            "id": int(time.time())
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=api_data,
                timeout=30
            )
            
            result = response.json()
            
            # Check for session timeout
            if result.get('result', {}).get('code') == 2200:
                logger.info("Session expired, re-authenticating...")
                self._authenticate()
                # Retry with new session
                params['sid'] = self.session_id
                api_data['params'] = params
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=api_data,
                    timeout=30
                )
                result = response.json()
            
            return result
            
        except Exception as e:
            logger.error(f"API call error for {method}: {str(e)}")
            return {'error': str(e)}
    
    def check_domain_availability(self, domain: str) -> Dict:
        """
        Check if domain is available for registration
        
        Args:
            domain (str): Domain name to check
        
        Returns:
            Dict: Availability result
        """
        try:
            result = self._make_api_call(
                "domain.check",
                {"domain": domain}
            )
            
            if result.get('result', {}).get('code') == 1000:
                availability = result['result']['resData']
                return {
                    'success': True,
                    'domain': domain,
                    'available': availability.get('avail', 0) == 1,
                    'reason': availability.get('reason', '')
                }
            else:
                return {
                    'success': False,
                    'domain': domain,
                    'error': result.get('result', {}).get('msg', 'Unknown error')
                }
                
        except Exception as e:
            logger.error(f"Domain check error for {domain}: {str(e)}")
            return {'success': False, 'domain': domain, 'error': str(e)}
    
    def register_domain(self, domain: str, period: int = 1, 
                       contacts: Dict = None, nameservers: List[str] = None) -> Dict:
        """
        Register a domain
        
        Args:
            domain (str): Domain name to register
            period (int): Registration period in years
            contacts (Dict): Contact information
            nameservers (List[str]): Custom nameservers
        
        Returns:
            Dict: Registration result
        """
        try:
            # Default contacts if not provided
            if not contacts:
                contacts = self._get_default_contacts()
            
            # Default nameservers (Cloudflare)
            if not nameservers:
                nameservers = [
                    "aaron.ns.cloudflare.com",
                    "annie.ns.cloudflare.com"
                ]
            
            params = {
                "domain": domain,
                "period": period,
                "registrant": contacts.get('registrant'),
                "admin": contacts.get('admin'),
                "tech": contacts.get('tech'),
                "billing": contacts.get('billing'),
                "ns": nameservers
            }
            
            result = self._make_api_call("domain.register", params)
            
            if result.get('result', {}).get('code') == 1000:
                logger.info(f"Domain {domain} registered successfully")
                return {
                    'success': True,
                    'domain': domain,
                    'registration_id': result['result']['resData'].get('regId'),
                    'expires': result['result']['resData'].get('exDate')
                }
            else:
                logger.error(f"Domain registration failed for {domain}: {result}")
                return {
                    'success': False,
                    'domain': domain,
                    'error': result.get('result', {}).get('msg', 'Registration failed')
                }
                
        except Exception as e:
            logger.error(f"Domain registration error for {domain}: {str(e)}")
            return {'success': False, 'domain': domain, 'error': str(e)}
    
    def bulk_check_availability(self, domains: List[str]) -> List[Dict]:
        """
        Check availability for multiple domains
        
        Args:
            domains (List[str]): List of domain names
        
        Returns:
            List[Dict]: Availability results
        """
        results = []
        
        for domain in domains:
            result = self.check_domain_availability(domain)
            results.append(result)
            
            # Rate limiting to avoid API limits
            time.sleep(1)
        
        return results
    
    def bulk_register_domains(self, domain_configs: List[Dict]) -> List[Dict]:
        """
        Bulk register multiple domains
        
        Args:
            domain_configs (List[Dict]): List of domain configurations
                Example: [
                    {'name': 'example.com', 'period': 1, 'nameservers': [...]},
                    {'name': 'test.com', 'period': 1}
                ]
        
        Returns:
            List[Dict]: Registration results
        """
        results = []
        
        logger.info(f"Starting bulk registration of {len(domain_configs)} domains")
        
        for config in domain_configs:
            domain = config['name']
            period = config.get('period', 1)
            nameservers = config.get('nameservers')
            contacts = config.get('contacts')
            
            logger.info(f"Registering domain: {domain}")
            
            # Check availability first
            availability = self.check_domain_availability(domain)
            
            if availability['success'] and availability['available']:
                # Register domain
                registration = self.register_domain(
                    domain, period, contacts, nameservers
                )
                results.append(registration)
            else:
                results.append({
                    'success': False,
                    'domain': domain,
                    'error': f"Domain not available: {availability.get('reason', 'Unknown')}"
                })
            
            # Rate limiting
            time.sleep(2)
        
        return results
    
    def update_nameservers(self, domain: str, nameservers: List[str]) -> Dict:
        """
        Update nameservers for a domain
        
        Args:
            domain (str): Domain name
            nameservers (List[str]): New nameservers
        
        Returns:
            Dict: Update result
        """
        try:
            params = {
                "domain": domain,
                "ns": nameservers
            }
            
            result = self._make_api_call("domain.updateNameservers", params)
            
            if result.get('result', {}).get('code') == 1000:
                logger.info(f"Nameservers updated for {domain}")
                return {
                    'success': True,
                    'domain': domain,
                    'nameservers': nameservers
                }
            else:
                return {
                    'success': False,
                    'domain': domain,
                    'error': result.get('result', {}).get('msg', 'Update failed')
                }
                
        except Exception as e:
            logger.error(f"Nameserver update error for {domain}: {str(e)}")
            return {'success': False, 'domain': domain, 'error': str(e)}
    
    def get_domain_info(self, domain: str) -> Dict:
        """
        Get domain information
        
        Args:
            domain (str): Domain name
        
        Returns:
            Dict: Domain information
        """
        try:
            result = self._make_api_call(
                "domain.info",
                {"domain": domain}
            )
            
            if result.get('result', {}).get('code') == 1000:
                return {
                    'success': True,
                    'domain': domain,
                    'info': result['result']['resData']
                }
            else:
                return {
                    'success': False,
                    'domain': domain,
                    'error': result.get('result', {}).get('msg', 'Info retrieval failed')
                }
                
        except Exception as e:
            logger.error(f"Domain info error for {domain}: {str(e)}")
            return {'success': False, 'domain': domain, 'error': str(e)}
    
    def list_domains(self) -> Dict:
        """
        List all domains in account
        
        Returns:
            Dict: Domain list
        """
        try:
            result = self._make_api_call("domain.list", {})
            
            if result.get('result', {}).get('code') == 1000:
                domains = result['result']['resData']['domains']
                return {
                    'success': True,
                    'domains': domains,
                    'count': len(domains)
                }
            else:
                return {
                    'success': False,
                    'error': result.get('result', {}).get('msg', 'List retrieval failed')
                }
                
        except Exception as e:
            logger.error(f"Domain list error: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def _get_default_contacts(self) -> Dict:
        """
        Get default contact information
        Note: In production, this should be configured with real contact data
        
        Returns:
            Dict: Default contact handles
        """
        # This is a placeholder - in production, you'd have actual contact handles
        return {
            'registrant': 'AUTO',  # INWX will use account default
            'admin': 'AUTO',
            'tech': 'AUTO',
            'billing': 'AUTO'
        }
    
    def logout(self) -> bool:
        """
        Logout from INWX API
        
        Returns:
            bool: Logout success
        """
        try:
            result = self._make_api_call("account.logout", {})
            
            if result.get('result', {}).get('code') == 1000:
                self.session_id = None
                logger.info("INWX logout successful")
                return True
            else:
                logger.warning(f"INWX logout failed: {result}")
                return False
                
        except Exception as e:
            logger.error(f"INWX logout error: {str(e)}")
            return False


# Configuration Class
class INWXConfig:
    """Configuration for INWX domain operations"""
    
    # Phase 1 Domain List with TLD-specific configuration
    PHASE1_DOMAINS = [
        # Core Business Domains
        {'name': 'smartringfitness.com', 'tld': 'com', 'priority': 'high', 'period': 1},
        {'name': 'biohackertools.com', 'tld': 'com', 'priority': 'high', 'period': 1},
        {'name': 'ledcontroller-pro.com', 'tld': 'com', 'priority': 'high', 'period': 1},
        {'name': 'aiworkflow-dashboard.com', 'tld': 'com', 'priority': 'high', 'period': 1},
        {'name': 'notiontemplate-hub.com', 'tld': 'com', 'priority': 'high', 'period': 1},
        {'name': 'techgadget-reviews.com', 'tld': 'com', 'priority': 'medium', 'period': 1},
        {'name': 'fitnesstracker-guide.com', 'tld': 'com', 'priority': 'medium', 'period': 1},
        {'name': 'smartdevice-insider.com', 'tld': 'com', 'priority': 'medium', 'period': 1},
        {'name': 'productivity-hacker.com', 'tld': 'com', 'priority': 'medium', 'period': 1},
        {'name': 'gadgetlaunch-tracker.com', 'tld': 'com', 'priority': 'medium', 'period': 1},
        {'name': 'wearabletech-expert.com', 'tld': 'com', 'priority': 'medium', 'period': 1},
        {'name': 'homeautomation-pro.com', 'tld': 'com', 'priority': 'medium', 'period': 1},
        {'name': 'techsavings-finder.com', 'tld': 'com', 'priority': 'medium', 'period': 1},
        {'name': 'digitalhealth-tools.com', 'tld': 'com', 'priority': 'medium', 'period': 1},
        {'name': 'innovation-scanner.com', 'tld': 'com', 'priority': 'medium', 'period': 1},
        {'name': 'techgadget-insider.com', 'tld': 'com', 'priority': 'low', 'period': 1},
        {'name': 'fitnesshub-pro.com', 'tld': 'com', 'priority': 'low', 'period': 1},
        {'name': 'smartdevices-review.com', 'tld': 'com', 'priority': 'low', 'period': 1},
        
        # Regional Domains
        {'name': 'smartringfitness.de', 'tld': 'de', 'priority': 'low', 'period': 1},
        
        # Alternative TLDs
        {'name': 'biohackertools.net', 'tld': 'net', 'priority': 'low', 'period': 1},
        {'name': 'aiworkflow-hub.org', 'tld': 'org', 'priority': 'low', 'period': 1},
        
        # Development Domains
        {'name': 'test-smartring.com', 'tld': 'com', 'priority': 'dev', 'period': 1},
        {'name': 'dev-biohacker.com', 'tld': 'com', 'priority': 'dev', 'period': 1},
        {'name': 'staging-aiworkflow.com', 'tld': 'com', 'priority': 'dev', 'period': 1},
        {'name': 'beta-techgadget.com', 'tld': 'com', 'priority': 'dev', 'period': 1}
    ]
    
    # Cloudflare Nameservers
    CLOUDFLARE_NAMESERVERS = [
        "aaron.ns.cloudflare.com",
        "annie.ns.cloudflare.com"
    ]


# Main execution functions
def setup_inwx_infrastructure(username: str, password: str, testing: bool = True):
    """
    Main function to setup INWX domain infrastructure for Phase 1
    
    Args:
        username (str): INWX username
        password (str): INWX password  
        testing (bool): Use testing environment
    """
    
    logger.info("Starting INWX domain infrastructure setup...")
    
    # Initialize INWX Manager
    inwx_manager = INWXAPIManager(username, password, testing=testing)
    
    # Prepare domain configurations
    domain_configs = []
    for domain_info in INWXConfig.PHASE1_DOMAINS:
        domain_configs.append({
            'name': domain_info['name'],
            'period': domain_info['period'],
            'nameservers': INWXConfig.CLOUDFLARE_NAMESERVERS
        })
    
    # First, check availability for all domains
    logger.info("Checking domain availability...")
    availability_results = inwx_manager.bulk_check_availability(
        [config['name'] for config in domain_configs]
    )
    
    # Filter available domains
    available_domains = []
    unavailable_domains = []
    
    for result in availability_results:
        if result['success'] and result['available']:
            available_domains.append(result['domain'])
        else:
            unavailable_domains.append(result)
    
    logger.info(f"Available domains: {len(available_domains)}")
    logger.info(f"Unavailable domains: {len(unavailable_domains)}")
    
    # Register available domains
    if available_domains:
        logger.info("Starting domain registration...")
        
        # Filter configs for available domains only
        registration_configs = [
            config for config in domain_configs 
            if config['name'] in available_domains
        ]
        
        registration_results = inwx_manager.bulk_register_domains(registration_configs)
    else:
        registration_results = []
    
    # Generate comprehensive report
    successful_registrations = [r for r in registration_results if r['success']]
    failed_registrations = [r for r in registration_results if not r['success']]
    
    print(f"\n=== INWX DOMAIN REGISTRATION RESULTS ===")
    print(f"Available domains: {len(available_domains)}")
    print(f"Successful registrations: {len(successful_registrations)}")
    print(f"Failed registrations: {len(failed_registrations)}")
    print(f"Unavailable domains: {len(unavailable_domains)}")
    
    if successful_registrations:
        print("\n✅ Successfully registered domains:")
        for domain in successful_registrations:
            print(f"  - {domain['domain']}")
    
    if failed_registrations:
        print("\n❌ Failed registrations:")
        for domain in failed_registrations:
            print(f"  - {domain['domain']}: {domain.get('error', 'Unknown error')}")
    
    if unavailable_domains:
        print("\n⚠️ Unavailable domains:")
        for domain in unavailable_domains:
            print(f"  - {domain['domain']}: {domain.get('reason', 'Not available')}")
    
    # Calculate costs
    total_cost = calculate_registration_costs(successful_registrations)
    print(f"\n💰 Total registration cost: €{total_cost:.2f}")
    
    # Logout
    inwx_manager.logout()
    
    return {
        'availability_results': availability_results,
        'registration_results': registration_results,
        'summary': {
            'available': len(available_domains),
            'registered': len(successful_registrations),
            'failed': len(failed_registrations),
            'unavailable': len(unavailable_domains),
            'total_cost': total_cost
        }
    }


def calculate_registration_costs(registration_results: List[Dict]) -> float:
    """
    Calculate total registration costs based on TLD pricing
    
    Args:
        registration_results (List[Dict]): Registration results
    
    Returns:
        float: Total cost in EUR
    """
    # INWX pricing (as of 2025)
    tld_prices = {
        'com': 17.40,
        'net': 18.60,
        'org': 14.29,
        'de': 3.91
    }
    
    total_cost = 0.0
    
    for result in registration_results:
        if result['success']:
            domain = result['domain']
            tld = domain.split('.')[-1]
            cost = tld_prices.get(tld, 17.40)  # Default to .com price
            total_cost += cost
    
    return total_cost


if __name__ == "__main__":
    # Example usage - Replace with actual credentials
    INWX_USERNAME = "your_inwx_username"
    INWX_PASSWORD = "your_inwx_password"
    
    # Use testing environment for development
    TESTING_MODE = True
    
    # Run setup
    setup_results = setup_inwx_infrastructure(
        INWX_USERNAME, 
        INWX_PASSWORD, 
        testing=TESTING_MODE
    )
    
    # Save results to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"inwx_setup_results_{timestamp}.json", "w") as f:
        json.dump(setup_results, f, indent=2, default=str)
    
    print(f"\nResults saved to: inwx_setup_results_{timestamp}.json")