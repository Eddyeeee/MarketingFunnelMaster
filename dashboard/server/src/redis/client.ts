import Redis from 'ioredis';
import { logger } from '../utils/logger';

const redisConfig = {
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379', 10),
  password: process.env.REDIS_PASSWORD || undefined,
  maxRetriesPerRequest: 3,
  retryDelayOnFailover: 100,
  enableReadyCheck: true,
  maxRetriesPerRequest: null,
  lazyConnect: true,
};

export const redisClient = new Redis(redisConfig);

redisClient.on('connect', () => {
  logger.info('Redis client connected');
});

redisClient.on('ready', () => {
  logger.info('Redis client ready');
});

redisClient.on('error', (error) => {
  logger.error('Redis client error:', error);
});

redisClient.on('close', () => {
  logger.info('Redis client connection closed');
});

redisClient.on('reconnecting', (delay) => {
  logger.info(`Redis client reconnecting in ${delay}ms`);
});

export const cacheGet = async <T>(key: string): Promise<T | null> => {
  try {
    const value = await redisClient.get(key);
    return value ? JSON.parse(value) : null;
  } catch (error) {
    logger.error(`Error getting cache key ${key}:`, error);
    return null;
  }
};

export const cacheSet = async <T>(
  key: string,
  value: T,
  ttl: number = 300 // 5 minutes default
): Promise<boolean> => {
  try {
    await redisClient.setex(key, ttl, JSON.stringify(value));
    return true;
  } catch (error) {
    logger.error(`Error setting cache key ${key}:`, error);
    return false;
  }
};

export const cacheDel = async (key: string): Promise<boolean> => {
  try {
    await redisClient.del(key);
    return true;
  } catch (error) {
    logger.error(`Error deleting cache key ${key}:`, error);
    return false;
  }
};

export const cacheFlush = async (): Promise<boolean> => {
  try {
    await redisClient.flushall();
    return true;
  } catch (error) {
    logger.error('Error flushing cache:', error);
    return false;
  }
};

export const cacheKeys = async (pattern: string): Promise<string[]> => {
  try {
    return await redisClient.keys(pattern);
  } catch (error) {
    logger.error(`Error getting cache keys with pattern ${pattern}:`, error);
    return [];
  }
};

export const cacheExists = async (key: string): Promise<boolean> => {
  try {
    const exists = await redisClient.exists(key);
    return exists === 1;
  } catch (error) {
    logger.error(`Error checking cache key existence ${key}:`, error);
    return false;
  }
};

export const cacheIncrement = async (key: string, by: number = 1): Promise<number> => {
  try {
    return await redisClient.incrby(key, by);
  } catch (error) {
    logger.error(`Error incrementing cache key ${key}:`, error);
    return 0;
  }
};

export const cacheExpire = async (key: string, ttl: number): Promise<boolean> => {
  try {
    const result = await redisClient.expire(key, ttl);
    return result === 1;
  } catch (error) {
    logger.error(`Error setting expiration for cache key ${key}:`, error);
    return false;
  }
};

export const cacheHSet = async (key: string, field: string, value: any): Promise<boolean> => {
  try {
    await redisClient.hset(key, field, JSON.stringify(value));
    return true;
  } catch (error) {
    logger.error(`Error setting hash field ${field} in key ${key}:`, error);
    return false;
  }
};

export const cacheHGet = async <T>(key: string, field: string): Promise<T | null> => {
  try {
    const value = await redisClient.hget(key, field);
    return value ? JSON.parse(value) : null;
  } catch (error) {
    logger.error(`Error getting hash field ${field} from key ${key}:`, error);
    return null;
  }
};

export const cacheHGetAll = async <T>(key: string): Promise<Record<string, T>> => {
  try {
    const hash = await redisClient.hgetall(key);
    const result: Record<string, T> = {};
    
    for (const [field, value] of Object.entries(hash)) {
      try {
        result[field] = JSON.parse(value);
      } catch {
        result[field] = value as T;
      }
    }
    
    return result;
  } catch (error) {
    logger.error(`Error getting all hash fields from key ${key}:`, error);
    return {};
  }
};

export const cacheLPush = async (key: string, value: any): Promise<number> => {
  try {
    return await redisClient.lpush(key, JSON.stringify(value));
  } catch (error) {
    logger.error(`Error pushing to list ${key}:`, error);
    return 0;
  }
};

export const cacheLRange = async <T>(key: string, start: number = 0, stop: number = -1): Promise<T[]> => {
  try {
    const values = await redisClient.lrange(key, start, stop);
    return values.map(value => JSON.parse(value));
  } catch (error) {
    logger.error(`Error getting list range from ${key}:`, error);
    return [];
  }
};

export const cacheLTrim = async (key: string, start: number, stop: number): Promise<boolean> => {
  try {
    await redisClient.ltrim(key, start, stop);
    return true;
  } catch (error) {
    logger.error(`Error trimming list ${key}:`, error);
    return false;
  }
};