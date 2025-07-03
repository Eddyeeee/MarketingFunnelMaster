import { WebSocketServer, WebSocket } from 'ws';
import { createServer } from 'http';
import { EventEmitter } from 'events';
import { v4 as uuidv4 } from 'uuid';
import { WebSocketMessage, Process, AIMetrics, RevenueData } from '@intelligence-dashboard/shared';
import { logger } from '../utils/logger';
import { redisClient } from '../redis/client';

interface Client {
  id: string;
  ws: WebSocket;
  subscriptions: Set<string>;
  lastPing: number;
}

export class IntelligenceWebSocketServer extends EventEmitter {
  private wss: WebSocketServer;
  private server: ReturnType<typeof createServer>;
  private clients: Map<string, Client> = new Map();
  private pingInterval!: NodeJS.Timeout;

  constructor(port: number = 4001) {
    super();
    
    this.server = createServer();
    this.wss = new WebSocketServer({ server: this.server });
    
    this.setupWebSocketHandlers();
    this.startPingInterval();
    
    this.server.listen(port, () => {
      logger.info(`WebSocket server listening on port ${port}`);
    });
  }

  private setupWebSocketHandlers() {
    this.wss.on('connection', (ws: WebSocket, _req) => {
      const clientId = uuidv4();
      const client: Client = {
        id: clientId,
        ws,
        subscriptions: new Set(),
        lastPing: Date.now(),
      };
      
      this.clients.set(clientId, client);
      logger.info(`Client ${clientId} connected`);
      
      ws.send(JSON.stringify({
        type: 'connection',
        data: { clientId, timestamp: new Date() },
      }));
      
      ws.on('message', async (data: Buffer) => {
        try {
          const message = JSON.parse(data.toString());
          await this.handleMessage(clientId, message);
        } catch (error) {
          logger.error('Error handling message:', error);
          ws.send(JSON.stringify({
            type: 'error',
            data: { message: 'Invalid message format' },
          }));
        }
      });
      
      ws.on('pong', () => {
        client.lastPing = Date.now();
      });
      
      ws.on('close', () => {
        this.clients.delete(clientId);
        logger.info(`Client ${clientId} disconnected`);
      });
      
      ws.on('error', (error) => {
        logger.error(`WebSocket error for client ${clientId}:`, error);
      });
    });
  }

  private async handleMessage(clientId: string, message: any) {
    const client = this.clients.get(clientId);
    if (!client) return;
    
    switch (message.type) {
      case 'subscribe':
        this.handleSubscribe(clientId, message.channel);
        break;
        
      case 'unsubscribe':
        this.handleUnsubscribe(clientId, message.channel);
        break;
        
      case 'ping':
        client.ws.send(JSON.stringify({ type: 'pong', timestamp: new Date() }));
        break;
        
      case 'get_processes':
        await this.sendProcesses(clientId);
        break;
        
      case 'get_metrics':
        await this.sendMetrics(clientId, message.platform);
        break;
        
      case 'get_revenue':
        await this.sendRevenue(clientId, message.timeframe);
        break;
        
      default:
        client.ws.send(JSON.stringify({
          type: 'error',
          data: { message: `Unknown message type: ${message.type}` },
        }));
    }
  }

  private handleSubscribe(clientId: string, channel: string) {
    const client = this.clients.get(clientId);
    if (!client) return;
    
    client.subscriptions.add(channel);
    logger.info(`Client ${clientId} subscribed to ${channel}`);
    
    client.ws.send(JSON.stringify({
      type: 'subscribed',
      data: { channel },
    }));
  }

  private handleUnsubscribe(clientId: string, channel: string) {
    const client = this.clients.get(clientId);
    if (!client) return;
    
    client.subscriptions.delete(channel);
    logger.info(`Client ${clientId} unsubscribed from ${channel}`);
    
    client.ws.send(JSON.stringify({
      type: 'unsubscribed',
      data: { channel },
    }));
  }

  private async sendProcesses(clientId: string) {
    const client = this.clients.get(clientId);
    if (!client) return;
    
    try {
      const processes = await this.getProcessesFromCache();
      client.ws.send(JSON.stringify({
        type: 'processes',
        data: processes,
        timestamp: new Date(),
      }));
    } catch (error) {
      logger.error('Error sending processes:', error);
    }
  }

  private async sendMetrics(clientId: string, platform?: string) {
    const client = this.clients.get(clientId);
    if (!client) return;
    
    try {
      const metrics = await this.getMetricsFromCache(platform);
      client.ws.send(JSON.stringify({
        type: 'metrics',
        data: metrics,
        timestamp: new Date(),
      }));
    } catch (error) {
      logger.error('Error sending metrics:', error);
    }
  }

  private async sendRevenue(clientId: string, timeframe?: string) {
    const client = this.clients.get(clientId);
    if (!client) return;
    
    try {
      const revenue = await this.getRevenueFromCache(timeframe);
      client.ws.send(JSON.stringify({
        type: 'revenue',
        data: revenue,
        timestamp: new Date(),
      }));
    } catch (error) {
      logger.error('Error sending revenue:', error);
    }
  }

  public broadcast(channel: string, message: WebSocketMessage) {
    const messageStr = JSON.stringify(message);
    
    this.clients.forEach((client) => {
      if (client.subscriptions.has(channel) || channel === '*') {
        if (client.ws.readyState === WebSocket.OPEN) {
          client.ws.send(messageStr);
        }
      }
    });
  }

  public broadcastProcessUpdate(process: Process) {
    this.broadcast('processes', {
      type: 'process_update',
      data: process,
      timestamp: new Date(),
    });
  }

  public broadcastMetricUpdate(metrics: AIMetrics) {
    this.broadcast('metrics', {
      type: 'metric_update',
      data: metrics,
      timestamp: new Date(),
    });
  }

  public broadcastRevenueUpdate(revenue: RevenueData) {
    this.broadcast('revenue', {
      type: 'revenue_update',
      data: revenue,
      timestamp: new Date(),
    });
  }

  public broadcastAlert(alert: { level: string; title: string; message: string }) {
    this.broadcast('*', {
      type: 'alert',
      data: alert,
      timestamp: new Date(),
    });
  }

  private startPingInterval() {
    this.pingInterval = setInterval(() => {
      const now = Date.now();
      const timeout = 30000; // 30 seconds
      
      this.clients.forEach((client, clientId) => {
        if (now - client.lastPing > timeout) {
          logger.info(`Client ${clientId} timed out, disconnecting`);
          client.ws.terminate();
          this.clients.delete(clientId);
        } else if (client.ws.readyState === WebSocket.OPEN) {
          client.ws.ping();
        }
      });
    }, 10000); // Every 10 seconds
  }

  private async getProcessesFromCache(): Promise<Process[]> {
    try {
      const cached = await redisClient.get('processes:all');
      return cached ? JSON.parse(cached) : [];
    } catch (error) {
      logger.error('Error getting processes from cache:', error);
      return [];
    }
  }

  private async getMetricsFromCache(platform?: string): Promise<AIMetrics[]> {
    try {
      const key = platform ? `metrics:${platform}` : 'metrics:all';
      const cached = await redisClient.get(key);
      return cached ? JSON.parse(cached) : [];
    } catch (error) {
      logger.error('Error getting metrics from cache:', error);
      return [];
    }
  }

  private async getRevenueFromCache(timeframe?: string): Promise<RevenueData | null> {
    try {
      const key = timeframe ? `revenue:${timeframe}` : 'revenue:latest';
      const cached = await redisClient.get(key);
      return cached ? JSON.parse(cached) : null;
    } catch (error) {
      logger.error('Error getting revenue from cache:', error);
      return null;
    }
  }

  public close() {
    clearInterval(this.pingInterval);
    
    this.clients.forEach((client) => {
      client.ws.close();
    });
    
    this.wss.close(() => {
      this.server.close(() => {
        logger.info('WebSocket server closed');
      });
    });
  }
}

export const wsServer = new IntelligenceWebSocketServer(
  parseInt(process.env.WS_PORT || '4001', 10)
);