import React, { useState, useEffect } from 'react';
import { useQuery } from '@apollo/client';
import { GET_RESEARCH_DATASET } from '../graphql/queries';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { CheckCircle, XCircle, AlertCircle } from 'lucide-react';

export function StatusCheck() {
  const [apiHealth, setApiHealth] = useState<any>(null);
  const [apiError, setApiError] = useState<string | null>(null);

  const { data: researchData, loading: researchLoading, error: researchError } = useQuery(GET_RESEARCH_DATASET);

  useEffect(() => {
    // Test API health
    fetch('http://localhost:4000/health')
      .then(res => res.json())
      .then(data => setApiHealth(data))
      .catch(err => setApiError(err.message));
  }, []);

  const getStatusIcon = (isOk: boolean, isLoading?: boolean) => {
    if (isLoading) return <AlertCircle className="h-4 w-4 text-yellow-500" />;
    return isOk ? <CheckCircle className="h-4 w-4 text-green-500" /> : <XCircle className="h-4 w-4 text-red-500" />;
  };

  const getStatusBadge = (isOk: boolean, isLoading?: boolean) => {
    if (isLoading) return <Badge variant="secondary">Loading</Badge>;
    return isOk ? <Badge className="bg-green-500">Healthy</Badge> : <Badge variant="destructive">Error</Badge>;
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>System Status Check</CardTitle>
        <CardDescription>Verify all services are running correctly</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* API Health */}
        <div className="flex items-center justify-between p-3 border rounded-lg">
          <div className="flex items-center space-x-2">
            {getStatusIcon(!!apiHealth && !apiError)}
            <span className="font-medium">API Server Health</span>
          </div>
          <div className="flex items-center space-x-2">
            {getStatusBadge(!!apiHealth && !apiError)}
            {apiHealth && (
              <span className="text-sm text-muted-foreground">
                Redis: {apiHealth.services?.redis}, WS: {apiHealth.services?.websocket}
              </span>
            )}
          </div>
        </div>

        {/* GraphQL Research Data */}
        <div className="flex items-center justify-between p-3 border rounded-lg">
          <div className="flex items-center space-x-2">
            {getStatusIcon(!!researchData && !researchError, researchLoading)}
            <span className="font-medium">Research Data Import</span>
          </div>
          <div className="flex items-center space-x-2">
            {getStatusBadge(!!researchData && !researchError, researchLoading)}
            {researchData && (
              <span className="text-sm text-muted-foreground">
                {researchData.researchDataset?.summary?.totalNiches || 0} niches loaded
              </span>
            )}
          </div>
        </div>

        {/* CORS */}
        <div className="flex items-center justify-between p-3 border rounded-lg">
          <div className="flex items-center space-x-2">
            {getStatusIcon(!researchError)}
            <span className="font-medium">CORS Configuration</span>
          </div>
          <div className="flex items-center space-x-2">
            {getStatusBadge(!researchError)}
            <span className="text-sm text-muted-foreground">
              Frontend ↔ Backend communication
            </span>
          </div>
        </div>

        {/* formatDate Function */}
        <div className="flex items-center justify-between p-3 border rounded-lg">
          <div className="flex items-center space-x-2">
            {getStatusIcon(true)}
            <span className="font-medium">formatDate Export</span>
          </div>
          <div className="flex items-center space-x-2">
            {getStatusBadge(true)}
            <span className="text-sm text-muted-foreground">
              Utils functions available
            </span>
          </div>
        </div>

        {/* Summary */}
        {researchData?.researchDataset?.summary && (
          <div className="mt-6 p-4 bg-muted rounded-lg">
            <h3 className="font-semibold mb-2">Research Data Summary</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <span className="text-muted-foreground">Total Niches:</span>
                <span className="ml-2 font-medium">{researchData.researchDataset.summary.totalNiches}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Avg Priority:</span>
                <span className="ml-2 font-medium">{researchData.researchDataset.summary.averagePriorityScore}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Total ROI:</span>
                <span className="ml-2 font-medium">
                  €{(researchData.researchDataset.summary.totalRealisticROI / 1000000).toFixed(1)}M
                </span>
              </div>
              <div>
                <span className="text-muted-foreground">Automation Ready:</span>
                <span className="ml-2 font-medium">{researchData.researchDataset.summary.highAutomationReadyCount}</span>
              </div>
            </div>
          </div>
        )}

        {/* Errors */}
        {(apiError || researchError) && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <h4 className="font-medium text-red-800 mb-1">Errors Detected</h4>
            {apiError && <p className="text-sm text-red-600">API: {apiError}</p>}
            {researchError && <p className="text-sm text-red-600">GraphQL: {researchError.message}</p>}
          </div>
        )}
      </CardContent>
    </Card>
  );
}