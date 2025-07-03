import { useState, useEffect } from 'react';
import { useQuery, useSubscription } from '@apollo/client';
import { GET_PROCESSES, PROCESS_UPDATED } from '../../graphql/queries';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { ScrollArea } from '@/components/ui/scroll-area';
import { 
  Play, 
  Square, 
  RefreshCw, 
  Cpu, 
  MemoryStick, 
  Activity,
  Clock,
  AlertCircle,
  XCircle,
  MinusCircle,
  ChevronDown,
  ChevronRight,
  Terminal
} from 'lucide-react';
import { Process } from '@intelligence-dashboard/shared';
import { wsClient } from '@/services/websocket';
import { formatNumber, formatDate, getStatusBadgeClass, getLogLevelClass } from '@/lib/utils';


interface ProcessViewerProps {
  className?: string;
}

export function ProcessViewer({ className }: ProcessViewerProps) {
  const [expandedProcess, setExpandedProcess] = useState<string | null>(null);
  const [processes, setProcesses] = useState<Process[]>([]);

  const { data, loading, error, refetch } = useQuery(GET_PROCESSES, {
    pollInterval: 30000,
    errorPolicy: 'all',
  });

  useSubscription(PROCESS_UPDATED, {
    onData: ({ data: subscriptionData }) => {
      if (subscriptionData?.data?.processUpdated) {
        const updatedProcess = subscriptionData.data.processUpdated;
        setProcesses(prev => 
          prev.map(p => p.id === updatedProcess.id ? updatedProcess : p)
        );
      }
    },
  });

  useEffect(() => {
    if (data?.processes) {
      setProcesses(data.processes);
    }
  }, [data]);

  useEffect(() => {
    wsClient.connect();
    wsClient.subscribe('processes');

    const handleProcessUpdate = (data: unknown) => {
      const process = data as Process;
      setProcesses(prev => 
        prev.map(p => p.id === process.id ? process : p)
      );
    };

    wsClient.on('process_update', handleProcessUpdate);

    return () => {
      wsClient.off('process_update', handleProcessUpdate);
    };
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return <Play className="h-4 w-4 text-green-500" />;
      case 'stopped':
        return <Square className="h-4 w-4 text-gray-500" />;
      case 'error':
        return <XCircle className="h-4 w-4 text-red-500" />;
      case 'pending':
        return <MinusCircle className="h-4 w-4 text-yellow-500" />;
      default:
        return <MinusCircle className="h-4 w-4 text-gray-500" />;
    }
  };

  const toggleExpanded = (processId: string) => {
    setExpandedProcess(expandedProcess === processId ? null : processId);
  };

  if (loading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle>Live Process Viewer</CardTitle>
          <CardDescription>Real-time process monitoring</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-32">
            <RefreshCw className="h-6 w-6 animate-spin" />
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle>Live Process Viewer</CardTitle>
          <CardDescription>Real-time process monitoring</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center h-32 text-red-500">
            <AlertCircle className="h-6 w-6 mr-2" />
            <span>Error loading processes</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Live Process Viewer</CardTitle>
            <CardDescription>Real-time process monitoring and control</CardDescription>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => refetch()}
            disabled={loading}
          >
            <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-96">
          <div className="space-y-4">
            {processes.map((process) => (
              <div
                key={process.id}
                className="border rounded-lg p-4 hover:bg-muted/50 transition-colors"
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => toggleExpanded(process.id)}
                      className="p-1 h-6 w-6"
                    >
                      {expandedProcess === process.id ? (
                        <ChevronDown className="h-4 w-4" />
                      ) : (
                        <ChevronRight className="h-4 w-4" />
                      )}
                    </Button>
                    {getStatusIcon(process.status)}
                    <h3 className="font-medium">{process.name}</h3>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Badge variant="outline" className={getStatusBadgeClass(process.status)}>
                      {process.status}
                    </Badge>
                    <span className="text-sm text-muted-foreground">
                      {process.type}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-2">
                  <div className="flex items-center space-x-2">
                    <Cpu className="h-4 w-4 text-blue-500" />
                    <span className="text-sm">CPU: {process.metrics.cpu.toFixed(1)}%</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <MemoryStick className="h-4 w-4 text-green-500" />
                    <span className="text-sm">Memory: {formatNumber(process.metrics.memory)}MB</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Activity className="h-4 w-4 text-purple-500" />
                    <span className="text-sm">RPM: {formatNumber(process.metrics.requestsPerMinute)}</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Clock className="h-4 w-4 text-orange-500" />
                    <span className="text-sm">RT: {process.metrics.avgResponseTime}ms</span>
                  </div>
                </div>

                <div className="mb-2">
                  <div className="flex justify-between text-sm mb-1">
                    <span>Progress</span>
                    <span>{process.progress}%</span>
                  </div>
                  <Progress value={process.progress} className="h-2" />
                </div>

                <div className="flex justify-between text-sm text-muted-foreground mb-2">
                  <span>Started: {formatDate(process.startTime)}</span>
                  <span>Updated: {formatDate(process.lastUpdate)}</span>
                </div>

                {expandedProcess === process.id && (
                  <div className="mt-4 pt-4 border-t">
                    <div className="flex items-center space-x-2 mb-2">
                      <Terminal className="h-4 w-4" />
                      <h4 className="font-medium">Recent Logs</h4>
                    </div>
                    <ScrollArea className="h-32">
                      <div className="space-y-1">
                        {process.logs.slice(-10).map((log) => (
                          <div key={log.id} className="text-sm font-mono">
                            <span className="text-muted-foreground mr-2">
                              {formatDate(log.timestamp)}
                            </span>
                            <span className={`mr-2 ${getLogLevelClass(log.level)}`}>
                              [{log.level.toUpperCase()}]
                            </span>
                            <span>{log.message}</span>
                          </div>
                        ))}
                      </div>
                    </ScrollArea>
                  </div>
                )}
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}