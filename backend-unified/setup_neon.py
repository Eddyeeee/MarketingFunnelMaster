#!/usr/bin/env python3
"""
Neon PostgreSQL Setup Script for Milestone 1C
Sets up Neon database with pgvector and Agentic RAG schema

Usage:
python setup_neon.py --action [test|create-schema|sample-data|performance]

Executor: Claude Code
Erstellt: 2025-07-03 - Milestone 1C Week 1 Day 1
"""

import asyncio
import logging
import argparse
import sys
import os
from datetime import datetime

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.neon_database import (
    init_neon_database,
    create_agentic_rag_schema,
    insert_sample_data,
    test_neon_connection,
    get_neon_performance_metrics,
    close_neon_database,
    neon_db_manager
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'neon_setup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)

logger = logging.getLogger(__name__)

async def test_connection():
    """Test Neon PostgreSQL connection"""
    logger.info("🔍 Testing Neon PostgreSQL connection...")
    
    try:
        await init_neon_database()
        
        success = await test_neon_connection()
        if success:
            logger.info("✅ Neon connection test successful!")
            
            # Get performance metrics
            metrics = await get_neon_performance_metrics()
            logger.info(f"📊 Performance metrics: {metrics}")
            
        else:
            logger.error("❌ Neon connection test failed!")
            return False
            
        return True
        
    except Exception as e:
        logger.error(f"❌ Connection test error: {e}")
        return False
    finally:
        await close_neon_database()

async def setup_schema():
    """Create Agentic RAG database schema"""
    logger.info("🗄️ Setting up Agentic RAG schema...")
    
    try:
        await init_neon_database()
        await create_agentic_rag_schema()
        
        logger.info("✅ Schema setup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Schema setup failed: {e}")
        return False
    finally:
        await close_neon_database()

async def insert_test_data():
    """Insert sample data for testing"""
    logger.info("📝 Inserting sample data...")
    
    try:
        await init_neon_database()
        await create_agentic_rag_schema()
        await insert_sample_data()
        
        logger.info("✅ Sample data inserted successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Sample data insertion failed: {e}")
        return False
    finally:
        await close_neon_database()

async def run_performance_test():
    """Run performance tests on Neon database"""
    logger.info("⚡ Running performance tests...")
    
    try:
        await init_neon_database()
        
        # Test basic query performance
        start_time = datetime.now()
        success = await test_neon_connection()
        query_time = (datetime.now() - start_time).total_seconds() * 1000
        
        logger.info(f"🕐 Basic query time: {query_time:.2f}ms")
        
        if query_time > 500:
            logger.warning("⚠️ Query time exceeds 500ms target")
        else:
            logger.info("✅ Query performance within target (<500ms)")
        
        # Get detailed metrics
        metrics = await get_neon_performance_metrics()
        logger.info(f"📊 Detailed metrics: {metrics}")
        
        # Test vector query if embeddings exist
        if metrics.get('embedding_count', 0) > 0:
            from config.neon_database import get_neon_session
            from sqlalchemy import text
            
            start_time = datetime.now()
            async with get_neon_session() as session:
                # Test vector similarity query
                result = await session.execute(text("""
                    SELECT content_id, 
                           embedding <-> '[0.1,0.1,0.1]'::vector as distance
                    FROM empire_embeddings 
                    ORDER BY embedding <-> '[0.1,0.1,0.1]'::vector 
                    LIMIT 5
                """))
                vector_results = result.fetchall()
            
            vector_time = (datetime.now() - start_time).total_seconds() * 1000
            logger.info(f"🧮 Vector query time: {vector_time:.2f}ms")
            logger.info(f"📋 Vector results: {len(vector_results)} items")
            
            if vector_time > 500:
                logger.warning("⚠️ Vector query time exceeds 500ms target")
            else:
                logger.info("✅ Vector query performance within target")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Performance test failed: {e}")
        return False
    finally:
        await close_neon_database()

async def full_setup():
    """Run complete Neon setup process"""
    logger.info("🚀 Running complete Neon setup...")
    
    steps = [
        ("Connection Test", test_connection),
        ("Schema Creation", setup_schema),
        ("Sample Data", insert_test_data),
        ("Performance Test", run_performance_test)
    ]
    
    results = {}
    
    for step_name, step_func in steps:
        logger.info(f"\n{'='*50}")
        logger.info(f"🔧 Step: {step_name}")
        logger.info(f"{'='*50}")
        
        try:
            success = await step_func()
            results[step_name] = success
            
            if success:
                logger.info(f"✅ {step_name} completed successfully")
            else:
                logger.error(f"❌ {step_name} failed")
                break
                
        except Exception as e:
            logger.error(f"❌ {step_name} error: {e}")
            results[step_name] = False
            break
    
    # Summary
    logger.info(f"\n{'='*50}")
    logger.info("📊 SETUP SUMMARY")
    logger.info(f"{'='*50}")
    
    all_success = True
    for step, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        logger.info(f"{step}: {status}")
        if not success:
            all_success = False
    
    if all_success:
        logger.info("\n🎉 Neon setup completed successfully!")
        logger.info("Ready for Milestone 1C implementation!")
    else:
        logger.error("\n💥 Neon setup failed!")
        logger.error("Please check the logs and fix any issues.")
    
    return all_success

def print_connection_info():
    """Print connection information for manual setup"""
    print("\n" + "="*60)
    print("🔧 NEON POSTGRESQL SETUP INFORMATION")
    print("="*60)
    print()
    print("📋 Manual Setup Steps:")
    print("1. Create Neon account at: https://neon.tech/")
    print("2. Create new project: 'MarketingFunnelMaster-AgenticRAG'")
    print("3. Select region: EU Central (Frankfurt)")
    print("4. Choose Scale tier (€20/month)")
    print("5. Create database: 'empire_rag_db'")
    print("6. Create user: 'empire_user'")
    print()
    print("🔐 Environment Variables to Set:")
    print("export NEON_DATABASE_PASSWORD='your-secure-password'")
    print("export NEON_DATABASE_URL='postgresql+asyncpg://empire_user:password@your-host/empire_rag_db?sslmode=require'")
    print()
    print("📦 Required Extensions:")
    print("- pgvector (for vector embeddings)")
    print("- uuid-ossp (for UUID generation)")
    print()
    print("🎯 Performance Targets:")
    print("- Vector queries: <500ms")
    print("- Basic queries: <100ms")
    print("- Connection pool: 20 connections")
    print()
    print("💾 Storage Estimates:")
    print("- Initial setup: ~100MB")
    print("- With 10k embeddings: ~2GB")
    print("- Production (100k embeddings): ~20GB")
    print()

async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Neon PostgreSQL Setup for Milestone 1C')
    parser.add_argument(
        '--action',
        choices=['test', 'create-schema', 'sample-data', 'performance', 'full-setup', 'info'],
        default='info',
        help='Action to perform'
    )
    
    args = parser.parse_args()
    
    print("🚀 Neon PostgreSQL Setup - Milestone 1C")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print(f"Action: {args.action}")
    print()
    
    if args.action == 'info':
        print_connection_info()
        return
    
    # Check if password is set
    if not os.getenv('NEON_DATABASE_PASSWORD'):
        logger.warning("⚠️ NEON_DATABASE_PASSWORD environment variable not set")
        logger.info("This script will use placeholder values for demonstration")
        logger.info("Set the password for actual database operations")
        print()
    
    success = False
    
    if args.action == 'test':
        success = await test_connection()
    elif args.action == 'create-schema':
        success = await setup_schema()
    elif args.action == 'sample-data':
        success = await insert_test_data()
    elif args.action == 'performance':
        success = await run_performance_test()
    elif args.action == 'full-setup':
        success = await full_setup()
    
    if success:
        print(f"\n✅ Action '{args.action}' completed successfully!")
        sys.exit(0)
    else:
        print(f"\n❌ Action '{args.action}' failed!")
        sys.exit(1)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)