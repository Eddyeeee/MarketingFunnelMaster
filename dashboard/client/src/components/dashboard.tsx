import React, { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ProcessViewer } from '@/components/features/process-viewer';
import { SearchInterface } from '@/components/features/search-interface';
import { AIMetricsDashboard } from '@/components/features/ai-metrics-dashboard';
import { ResearchIntelligence } from '@/components/features/research-intelligence';
import { ResearchOverview } from '@/components/features/research-overview';
import { ResearchMetricsDashboard } from '@/components/features/research-metrics-dashboard';
import { StatusCheck } from '@/components/status-check';
import { 
  LayoutDashboard, 
  Search, 
  BarChart3, 
  TrendingUp, 
  Users, 
  DollarSign, 
  Settings, 
  Brain,
  Zap,
  Target,
  Activity,
  Menu,
  X,
  Database,
  CheckCircle
} from 'lucide-react';

export function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeView, setActiveView] = useState('overview');

  const navigationItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'research', label: 'Research Intelligence', icon: Database },
    { id: 'processes', label: 'Live Processes', icon: Activity },
    { id: 'search', label: 'Intelligence Search', icon: Search },
    { id: 'ai-metrics', label: 'Research Metrics', icon: Brain },
    { id: 'predictive', label: 'Predictive Intelligence', icon: TrendingUp },
    { id: 'channels', label: 'Multi-Channel', icon: Users },
    { id: 'revenue', label: 'Revenue Intelligence', icon: DollarSign },
    { id: 'automation', label: 'Automation Monitor', icon: Zap },
    { id: 'scaling', label: 'Scaling Assistant', icon: Target },
    { id: 'status', label: 'System Status', icon: CheckCircle },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  const renderContent = () => {
    switch (activeView) {
      case 'overview':
        return (
          <div className="space-y-6">
            <ResearchOverview />
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ProcessViewer />
              <ResearchMetricsDashboard />
            </div>
          </div>
        );
      case 'research':
        return <ResearchIntelligence className="w-full" />;
      case 'processes':
        return <ProcessViewer className="w-full" />;
      case 'search':
        return <SearchInterface className="w-full" />;
      case 'ai-metrics':
        return <ResearchMetricsDashboard className="w-full" />;
      case 'predictive':
        return (
          <Card>
            <CardHeader>
              <CardTitle>Predictive Intelligence</CardTitle>
              <CardDescription>AI-powered trend prediction and market opportunity detection</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12">
                <TrendingUp className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-muted-foreground">Predictive Intelligence module coming soon</p>
              </div>
            </CardContent>
          </Card>
        );
      case 'channels':
        return (
          <Card>
            <CardHeader>
              <CardTitle>Multi-Channel Orchestrator</CardTitle>
              <CardDescription>Unified content distribution and cross-platform performance tracking</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12">
                <Users className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-muted-foreground">Multi-Channel Orchestrator coming soon</p>
              </div>
            </CardContent>
          </Card>
        );
      case 'revenue':
        return (
          <Card>
            <CardHeader>
              <CardTitle>Revenue Intelligence</CardTitle>
              <CardDescription>Real-time revenue tracking with advanced analytics and projections</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12">
                <DollarSign className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-muted-foreground">Revenue Intelligence dashboard coming soon</p>
              </div>
            </CardContent>
          </Card>
        );
      case 'automation':
        return (
          <Card>
            <CardHeader>
              <CardTitle>Automation Monitor</CardTitle>
              <CardDescription>Comprehensive workflow health monitoring and performance optimization</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12">
                <Zap className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-muted-foreground">Automation Monitor coming soon</p>
              </div>
            </CardContent>
          </Card>
        );
      case 'scaling':
        return (
          <Card>
            <CardHeader>
              <CardTitle>Scaling Assistant</CardTitle>
              <CardDescription>AI-powered growth recommendations and bottleneck detection</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12">
                <Target className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-muted-foreground">Scaling Assistant coming soon</p>
              </div>
            </CardContent>
          </Card>
        );
      case 'status':
        return <StatusCheck />;
      case 'settings':
        return (
          <Card>
            <CardHeader>
              <CardTitle>Settings</CardTitle>
              <CardDescription>Dashboard configuration and system preferences</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12">
                <Settings className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-muted-foreground">Settings panel coming soon</p>
              </div>
            </CardContent>
          </Card>
        );
      default:
        return null;
    }
  };

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-card border-r transform transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
        lg:translate-x-0 lg:static lg:inset-0
      `}>
        <div className="flex items-center justify-between h-16 px-4 border-b">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
              <Brain className="h-5 w-5 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-semibold">Intelligence</h1>
              <p className="text-xs text-muted-foreground">Dashboard</p>
            </div>
          </div>
          <Button
            variant="ghost"
            size="sm"
            className="lg:hidden"
            onClick={() => setSidebarOpen(false)}
          >
            <X className="h-4 w-4" />
          </Button>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            return (
              <Button
                key={item.id}
                variant={activeView === item.id ? 'default' : 'ghost'}
                className="w-full justify-start"
                onClick={() => {
                  setActiveView(item.id);
                  setSidebarOpen(false);
                }}
              >
                <Icon className="h-4 w-4 mr-2" />
                {item.label}
              </Button>
            );
          })}
        </nav>

        <div className="p-4 border-t">
          <div className="bg-gradient-to-r from-blue-500/10 to-purple-600/10 rounded-lg p-3">
            <div className="flex items-center space-x-2 mb-2">
              <Badge variant="secondary" className="text-xs">
                ENTERPRISE
              </Badge>
              <span className="text-xs text-muted-foreground">2025 Ready</span>
            </div>
            <p className="text-xs text-muted-foreground">
              AI-powered intelligence platform for the modern marketer
            </p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="h-16 bg-card border-b flex items-center justify-between px-4">
          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              size="sm"
              className="lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="h-4 w-4" />
            </Button>
            <div>
              <h2 className="text-lg font-semibold">
                {navigationItems.find(item => item.id === activeView)?.label || 'Dashboard'}
              </h2>
              <p className="text-sm text-muted-foreground">
                Real-time intelligence for marketing automation
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <Badge variant="outline" className="animate-pulse-glow">
              <div className="w-2 h-2 bg-green-500 rounded-full mr-2" />
              Live
            </Badge>
            <Button variant="outline" size="sm">
              <BarChart3 className="h-4 w-4 mr-2" />
              Export
            </Button>
          </div>
        </header>

        {/* Content */}
        <main className="flex-1 overflow-auto p-6">
          {renderContent()}
        </main>
      </div>

      {/* Mobile Overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}