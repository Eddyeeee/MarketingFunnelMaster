"""
Vercel SDK Integration für MarketingFunnelMaster
Meilenstein 1D - Deployment Pipeline
"""

import os
import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import aiohttp
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv('.env.vercel')


class DeploymentConfig(BaseModel):
    """Konfiguration für einzelne Deployments"""
    project_name: str
    domain: str
    environment: str = "production"
    build_command: Optional[str] = "npm run build"
    output_directory: Optional[str] = "dist"
    env_vars: Dict[str, str] = Field(default_factory=dict)
    
    
class DeploymentResult(BaseModel):
    """Ergebnis eines Deployments"""
    deployment_id: str
    url: str
    domain: str
    status: str
    created_at: datetime
    ready_at: Optional[datetime] = None
    error: Optional[str] = None


class VercelSDK:
    """Vercel API SDK für Multi-Site Deployments"""
    
    def __init__(self):
        self.token = os.getenv('VERCEL_TOKEN')
        self.team_id = os.getenv('VERCEL_TEAM_ID')
        self.base_url = "https://api.vercel.com"
        self.headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }
        
    async def create_project(self, name: str, framework: str = "nextjs") -> Dict[str, Any]:
        """Erstellt ein neues Vercel Projekt"""
        async with aiohttp.ClientSession() as session:
            data = {
                "name": name,
                "framework": framework,
                "publicSource": False,
                "installCommand": "npm install",
                "buildCommand": "npm run build",
                "devCommand": "npm run dev",
                "outputDirectory": "dist"
            }
            
            params = {'teamId': self.team_id} if self.team_id else {}
            
            async with session.post(
                f"{self.base_url}/v8/projects",
                headers=self.headers,
                json=data,
                params=params
            ) as response:
                return await response.json()
    
    async def deploy_project(self, config: DeploymentConfig) -> DeploymentResult:
        """Deployed ein Projekt zu Vercel"""
        async with aiohttp.ClientSession() as session:
            # Create deployment
            deployment_data = {
                "name": config.project_name,
                "env": config.env_vars,
                "target": config.environment,
                "gitSource": {
                    "ref": "main",
                    "repoId": "marketing-funnel-master"
                }
            }
            
            params = {'teamId': self.team_id} if self.team_id else {}
            
            async with session.post(
                f"{self.base_url}/v13/deployments",
                headers=self.headers,
                json=deployment_data,
                params=params
            ) as response:
                result = await response.json()
                
                return DeploymentResult(
                    deployment_id=result.get('id', ''),
                    url=result.get('url', ''),
                    domain=config.domain,
                    status=result.get('readyState', 'BUILDING'),
                    created_at=datetime.utcnow(),
                    error=result.get('error', {}).get('message') if 'error' in result else None
                )
    
    async def add_domain(self, project_id: str, domain: str) -> bool:
        """Fügt eine Domain zu einem Projekt hinzu"""
        async with aiohttp.ClientSession() as session:
            data = {"name": domain}
            params = {'teamId': self.team_id} if self.team_id else {}
            
            async with session.post(
                f"{self.base_url}/v8/projects/{project_id}/domains",
                headers=self.headers,
                json=data,
                params=params
            ) as response:
                return response.status == 200
    
    async def check_deployment_status(self, deployment_id: str) -> str:
        """Überprüft den Status eines Deployments"""
        async with aiohttp.ClientSession() as session:
            params = {'teamId': self.team_id} if self.team_id else {}
            
            async with session.get(
                f"{self.base_url}/v13/deployments/{deployment_id}",
                headers=self.headers,
                params=params
            ) as response:
                result = await response.json()
                return result.get('readyState', 'UNKNOWN')
    
    async def get_deployment_logs(self, deployment_id: str) -> List[str]:
        """Holt die Logs eines Deployments"""
        async with aiohttp.ClientSession() as session:
            params = {'teamId': self.team_id} if self.team_id else {}
            
            async with session.get(
                f"{self.base_url}/v2/deployments/{deployment_id}/events",
                headers=self.headers,
                params=params
            ) as response:
                result = await response.json()
                return [event.get('text', '') for event in result.get('events', [])]
    
    async def list_projects(self) -> List[Dict[str, Any]]:
        """Listet alle Projekte"""
        async with aiohttp.ClientSession() as session:
            params = {'teamId': self.team_id} if self.team_id else {}
            
            async with session.get(
                f"{self.base_url}/v8/projects",
                headers=self.headers,
                params=params
            ) as response:
                result = await response.json()
                return result.get('projects', [])


class BulkDeploymentOrchestrator:
    """Orchestriert Bulk Deployments für Multiple Sites"""
    
    def __init__(self, sdk: VercelSDK):
        self.sdk = sdk
        self.max_concurrent = int(os.getenv('PARALLEL_DEPLOYMENTS', '50'))
        
    async def deploy_batch(self, configs: List[DeploymentConfig]) -> List[DeploymentResult]:
        """Deployed mehrere Sites parallel"""
        semaphore = asyncio.Semaphore(self.max_concurrent)
        
        async def deploy_with_limit(config: DeploymentConfig) -> DeploymentResult:
            async with semaphore:
                return await self.sdk.deploy_project(config)
        
        tasks = [deploy_with_limit(config) for config in configs]
        return await asyncio.gather(*tasks)
    
    async def monitor_deployments(self, deployment_ids: List[str]) -> Dict[str, str]:
        """Überwacht mehrere Deployments"""
        status_checks = []
        for deployment_id in deployment_ids:
            status_checks.append(self.sdk.check_deployment_status(deployment_id))
        
        statuses = await asyncio.gather(*status_checks)
        return dict(zip(deployment_ids, statuses))


# Cost Monitoring Integration
class VercelCostMonitor:
    """Überwacht Vercel Kosten und Usage"""
    
    def __init__(self, sdk: VercelSDK):
        self.sdk = sdk
        self.budget_limit = float(os.getenv('MONTHLY_BUDGET_LIMIT', '25'))
        self.alert_threshold = float(os.getenv('ALERT_THRESHOLD', '20'))
        
    async def get_current_usage(self) -> Dict[str, Any]:
        """Holt aktuelle Usage Daten"""
        async with aiohttp.ClientSession() as session:
            params = {'teamId': self.sdk.team_id} if self.sdk.team_id else {}
            
            async with session.get(
                f"{self.sdk.base_url}/v1/usage",
                headers=self.sdk.headers,
                params=params
            ) as response:
                return await response.json()
    
    async def check_budget_status(self) -> Dict[str, Any]:
        """Überprüft Budget Status"""
        usage = await self.get_current_usage()
        current_cost = usage.get('total', {}).get('amount', 0) / 100  # Cents to Euro
        
        return {
            'current_cost': current_cost,
            'budget_limit': self.budget_limit,
            'percentage_used': (current_cost / self.budget_limit) * 100,
            'alert_triggered': current_cost >= self.alert_threshold,
            'remaining_budget': self.budget_limit - current_cost
        }


# Example Usage
async def example_deployment():
    """Beispiel für ein Deployment"""
    sdk = VercelSDK()
    orchestrator = BulkDeploymentOrchestrator(sdk)
    
    # Single deployment
    config = DeploymentConfig(
        project_name="qmoney-landing-v2",
        domain="landing-v2.qmoney.de",
        env_vars={
            "NEXT_PUBLIC_API_URL": "https://api.qmoney.de",
            "DATABASE_URL": os.getenv('NEON_DATABASE_URL', '')
        }
    )
    
    result = await sdk.deploy_project(config)
    print(f"Deployment started: {result.deployment_id}")
    
    # Check status
    status = await sdk.check_deployment_status(result.deployment_id)
    print(f"Status: {status}")
    
    # Bulk deployment
    configs = [
        DeploymentConfig(
            project_name=f"site-{i}",
            domain=f"site-{i}.qmoney.de"
        )
        for i in range(5)
    ]
    
    results = await orchestrator.deploy_batch(configs)
    print(f"Deployed {len(results)} sites")


if __name__ == "__main__":
    # Test connection
    import asyncio
    asyncio.run(example_deployment())