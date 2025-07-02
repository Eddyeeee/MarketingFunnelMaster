import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { typeDefs } from './graphql/schema';
import { resolvers } from './graphql/resolvers';
import { redisClient } from './redis/client';
import { wsServer } from './websocket/server';
import { logger } from './utils/logger';

const PORT = process.env.PORT || 4000;
const GRAPHQL_PATH = process.env.GRAPHQL_PATH || '/graphql';

async function startServer() {
  try {
    await redisClient.connect();
    logger.info('Connected to Redis');

    const app = express();
    const httpServer = createServer(app);

    const schema = makeExecutableSchema({ typeDefs, resolvers });

    const wsServerGraphQL = new WebSocketServer({
      server: httpServer,
      path: '/graphql-ws',
    });

    const serverCleanup = useServer({ schema }, wsServerGraphQL);

    const server = new ApolloServer({
      schema,
      plugins: [
        ApolloServerPluginDrainHttpServer({ httpServer }),
        {
          async serverWillStart() {
            return {
              async drainServer() {
                await serverCleanup.dispose();
              },
            };
          },
        },
      ],
    });

    await server.start();

    // Global CORS configuration for all routes
    app.use(cors<cors.CorsRequest>({
      origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
      credentials: true,
      methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
      allowedHeaders: ['Content-Type', 'Authorization', 'Apollo-Require-Preflight'],
    }));

    app.use(
      GRAPHQL_PATH,
      express.json({ limit: '10mb' }),
      expressMiddleware(server, {
        context: async ({ req }) => {
          return {
            req,
            user: null, // Add authentication context here
          };
        },
      })
    );

    app.get('/health', (req, res) => {
      res.json({ 
        status: 'healthy', 
        timestamp: new Date().toISOString(),
        services: {
          redis: redisClient.status,
          websocket: wsServer ? 'connected' : 'disconnected',
        }
      });
    });

    app.get('/metrics', async (req, res) => {
      try {
        const metrics = {
          uptime: process.uptime(),
          memory: process.memoryUsage(),
          cpu: process.cpuUsage(),
          timestamp: new Date().toISOString(),
        };
        res.json(metrics);
      } catch (error) {
        logger.error('Error getting metrics:', error);
        res.status(500).json({ error: 'Failed to get metrics' });
      }
    });

    app.use((req, res) => {
      res.status(404).json({ error: 'Not found' });
    });

    app.use((error: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {
      logger.error('Express error:', error);
      res.status(500).json({ error: 'Internal server error' });
    });

    await new Promise<void>((resolve) => httpServer.listen({ port: PORT }, resolve));
    
    logger.info(`🚀 Server ready at http://localhost:${PORT}${GRAPHQL_PATH}`);
    logger.info(`🚀 Subscriptions ready at ws://localhost:${PORT}/graphql-ws`);
    logger.info(`🌐 WebSocket Intelligence Server ready at ws://localhost:${parseInt(process.env.WS_PORT || '4001', 10)}`);

    startBackgroundTasks();

  } catch (error) {
    logger.error('Failed to start server:', error);
    process.exit(1);
  }
}

function startBackgroundTasks() {
  setInterval(async () => {
    try {
      const mockMetrics = {
        id: Date.now().toString(),
        timestamp: new Date(),
        platform: 'perplexity' as const,
        metrics: {
          searchRanking: Math.random() * 100,
          visibility: Math.random() * 100,
          answerEnginePerformance: Math.random() * 100,
          voiceSearchAnalytics: {
            queries: Math.floor(Math.random() * 1000) + 500,
            accuracy: Math.random() * 100,
            avgResponseTime: Math.random() * 2 + 0.5,
            topQueries: ['AI trends', 'market analysis', 'competition'],
          },
          competitorPosition: Math.floor(Math.random() * 10) + 1,
        },
      };

      wsServer.broadcastMetricUpdate(mockMetrics);
    } catch (error) {
      logger.error('Error in background metrics task:', error);
    }
  }, 10000);

  setInterval(async () => {
    try {
      const mockRevenue = {
        id: Date.now().toString(),
        timestamp: new Date(),
        actual: Math.floor(Math.random() * 50000) + 100000,
        projected: Math.floor(Math.random() * 50000) + 150000,
        byChannel: [],
        byProduct: [],
        ltv: {
          average: Math.floor(Math.random() * 200) + 400,
          bySegment: [],
          projections: [],
        },
      };

      wsServer.broadcastRevenueUpdate(mockRevenue);
    } catch (error) {
      logger.error('Error in background revenue task:', error);
    }
  }, 15000);

  setInterval(async () => {
    try {
      const shouldAlert = Math.random() < 0.1;
      if (shouldAlert) {
        const alerts = [
          { level: 'warning', title: 'High CPU Usage', message: 'CPU usage exceeded 80%' },
          { level: 'info', title: 'New Opportunity', message: 'Trending topic detected in your niche' },
          { level: 'error', title: 'API Limit Reached', message: 'OpenAI API limit reached' },
        ];

        const alert = alerts[Math.floor(Math.random() * alerts.length)];
        wsServer.broadcastAlert(alert);
      }
    } catch (error) {
      logger.error('Error in background alert task:', error);
    }
  }, 30000);
}

process.on('SIGINT', async () => {
  logger.info('Received SIGINT, shutting down gracefully');
  
  try {
    wsServer.close();
    await redisClient.disconnect();
    process.exit(0);
  } catch (error) {
    logger.error('Error during shutdown:', error);
    process.exit(1);
  }
});

process.on('SIGTERM', async () => {
  logger.info('Received SIGTERM, shutting down gracefully');
  
  try {
    wsServer.close();
    await redisClient.disconnect();
    process.exit(0);
  } catch (error) {
    logger.error('Error during shutdown:', error);
    process.exit(1);
  }
});

startServer();