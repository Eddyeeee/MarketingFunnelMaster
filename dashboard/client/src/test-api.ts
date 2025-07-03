// Test API connectivity
export async function testApiConnectivity() {
  try {
    console.log('Testing API connectivity...');
    
    // Test health endpoint
    const healthResponse = await fetch('http://localhost:4000/health');
    const healthData = await healthResponse.json();
    console.log('Health check:', healthData);
    
    // Test GraphQL endpoint
    const graphqlResponse = await fetch('http://localhost:4000/graphql', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query: `
          query TestQuery {
            researchDataset {
              summary {
                totalNiches
                averagePriorityScore
                totalRealisticROI
              }
            }
          }
        `
      })
    });
    
    const graphqlData = await graphqlResponse.json();
    console.log('GraphQL test:', graphqlData);
    
    return {
      health: healthData,
      graphql: graphqlData,
      success: true
    };
  } catch (error) {
    console.error('API connectivity test failed:', error);
    return {
      error: error instanceof Error ? error.message : String(error),
      success: false
    };
  }
}

// Auto-run test in development
if (import.meta.env.DEV) {
  setTimeout(() => {
    testApiConnectivity().then(result => {
      console.log('API Test Result:', result);
    });
  }, 1000);
}