import React, { useState, useEffect } from 'react';
import { useLazyQuery } from '@apollo/client';
import { gql } from 'graphql-tag';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { TreeView } from '@/components/features/tree-view';
import { 
  Search, 
  Filter, 
  Clock, 
  TrendingUp,
  BarChart3,
  Globe,
  Users,
  Building,
  MapPin,
  Package,
  AlertCircle
} from 'lucide-react';
import { ResearchData, ResearchResult } from '@intelligence-dashboard/shared';
import { formatDate, formatNumber } from '@/lib/utils';

const SEARCH_RESEARCH = gql`
  query SearchResearch($query: String!, $filters: JSON) {
    searchResearch(query: $query, filters: $filters) {
      id
      query
      results {
        id
        title
        content
        url
        relevanceScore
        entities {
          name
          type
          confidence
        }
        sentiment {
          score
          label
        }
        children {
          id
          title
          content
          url
          relevanceScore
          entities {
            name
            type
            confidence
          }
          sentiment {
            score
            label
          }
        }
      }
      timestamp
      source
      metadata {
        duration
        sources
        filters
      }
    }
  }
`;

interface SearchInterfaceProps {
  className?: string;
}

export function SearchInterface({ className }: SearchInterfaceProps) {
  const [query, setQuery] = useState('');
  const [searchHistory, setSearchHistory] = useState<string[]>([]);
  const [selectedResult, setSelectedResult] = useState<ResearchResult | null>(null);

  const [searchResearch, { data, loading, error }] = useLazyQuery(SEARCH_RESEARCH, {
    errorPolicy: 'all',
  });

  useEffect(() => {
    const saved = localStorage.getItem('searchHistory');
    if (saved) {
      setSearchHistory(JSON.parse(saved));
    }
  }, []);

  const handleSearch = () => {
    if (!query.trim()) return;

    searchResearch({
      variables: {
        query: query.trim(),
        filters: {},
      },
    });

    // Add to search history
    const newHistory = [query, ...searchHistory.filter(h => h !== query)].slice(0, 10);
    setSearchHistory(newHistory);
    localStorage.setItem('searchHistory', JSON.stringify(newHistory));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const getEntityIcon = (type: string) => {
    switch (type) {
      case 'person':
        return <Users className="h-3 w-3" />;
      case 'organization':
        return <Building className="h-3 w-3" />;
      case 'location':
        return <MapPin className="h-3 w-3" />;
      case 'product':
        return <Package className="h-3 w-3" />;
      default:
        return <Globe className="h-3 w-3" />;
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive':
        return 'text-green-600 bg-green-100 border-green-200';
      case 'negative':
        return 'text-red-600 bg-red-100 border-red-200';
      default:
        return 'text-gray-600 bg-gray-100 border-gray-200';
    }
  };

  const transformResultsToTreeData = (results: ResearchResult[]) => {
    return results.map(result => ({
      id: result.id,
      label: result.title,
      data: result,
      children: result.children?.map(child => ({
        id: child.id,
        label: child.title,
        data: child,
        children: [],
      })) || [],
    }));
  };

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>Intelligence Search</CardTitle>
        <CardDescription>Search and analyze research data with AI-powered insights</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Search Bar */}
          <div className="flex space-x-2">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search research data, trends, competitors..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                className="pl-10"
              />
            </div>
            <Button onClick={handleSearch} disabled={loading || !query.trim()}>
              {loading ? 'Searching...' : 'Search'}
            </Button>
            <Button variant="outline" size="icon">
              <Filter className="h-4 w-4" />
            </Button>
          </div>

          {/* Search History */}
          {searchHistory.length > 0 && (
            <div className="flex flex-wrap gap-2">
              <span className="text-sm text-muted-foreground">Recent:</span>
              {searchHistory.slice(0, 5).map((term, index) => (
                <Button
                  key={index}
                  variant="outline"
                  size="sm"
                  onClick={() => setQuery(term)}
                  className="h-6 text-xs"
                >
                  <Clock className="h-3 w-3 mr-1" />
                  {term}
                </Button>
              ))}
            </div>
          )}

          {/* Search Results */}
          {data?.searchResearch && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
              {/* Results Tree */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-medium">Search Results</h3>
                  <Badge variant="outline">
                    {data.searchResearch.length} dataset(s)
                  </Badge>
                </div>
                
                <ScrollArea className="h-96 border rounded-lg p-4">
                  {data.searchResearch.map((research: ResearchData) => (
                    <div key={research.id} className="mb-6 last:mb-0">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-sm">{research.query}</h4>
                        <Badge variant="secondary" className="text-xs">
                          {research.source}
                        </Badge>
                      </div>
                      
                      <div className="text-xs text-muted-foreground mb-2">
                        {formatDate(research.timestamp)} • {formatNumber(research.metadata.duration)}ms
                      </div>

                      <TreeView
                        data={transformResultsToTreeData(research.results)}
                        onSelect={(item) => setSelectedResult(item.data as ResearchResult)}
                        className="max-h-64"
                      />
                    </div>
                  ))}
                </ScrollArea>
              </div>

              {/* Result Details */}
              <div className="space-y-4">
                <h3 className="font-medium">Result Details</h3>
                
                {selectedResult ? (
                  <ScrollArea className="h-96 border rounded-lg p-4">
                    <div className="space-y-4">
                      <div>
                        <h4 className="font-medium mb-2">{selectedResult.title}</h4>
                        {selectedResult.url && (
                          <a
                            href={selectedResult.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-sm text-blue-600 hover:underline mb-2 block"
                          >
                            {selectedResult.url}
                          </a>
                        )}
                        <div className="flex items-center space-x-2 mb-2">
                          <Badge variant="outline">
                            <TrendingUp className="h-3 w-3 mr-1" />
                            {(selectedResult.relevanceScore * 100).toFixed(1)}% relevant
                          </Badge>
                          <Badge 
                            variant="outline" 
                            className={getSentimentColor(selectedResult.sentiment.label)}
                          >
                            {selectedResult.sentiment.label}
                          </Badge>
                        </div>
                      </div>

                      <div>
                        <h5 className="font-medium text-sm mb-2">Content</h5>
                        <p className="text-sm text-muted-foreground leading-relaxed">
                          {selectedResult.content}
                        </p>
                      </div>

                      {selectedResult.entities.length > 0 && (
                        <div>
                          <h5 className="font-medium text-sm mb-2">Entities</h5>
                          <div className="flex flex-wrap gap-2">
                            {selectedResult.entities.map((entity, index) => (
                              <Badge
                                key={index}
                                variant="outline"
                                className="text-xs"
                              >
                                {getEntityIcon(entity.type)}
                                <span className="ml-1">{entity.name}</span>
                                <span className="ml-1 text-muted-foreground">
                                  ({(entity.confidence * 100).toFixed(0)}%)
                                </span>
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}

                      {selectedResult.children && selectedResult.children.length > 0 && (
                        <div>
                          <h5 className="font-medium text-sm mb-2">Sub-analyses</h5>
                          <div className="space-y-2">
                            {selectedResult.children.map((child) => (
                              <div
                                key={child.id}
                                className="p-2 border rounded cursor-pointer hover:bg-muted/50"
                                onClick={() => setSelectedResult(child)}
                              >
                                <div className="font-medium text-sm">{child.title}</div>
                                <div className="text-xs text-muted-foreground truncate">
                                  {child.content}
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </ScrollArea>
                ) : (
                  <div className="h-96 border rounded-lg flex items-center justify-center text-muted-foreground">
                    <div className="text-center">
                      <BarChart3 className="h-8 w-8 mx-auto mb-2" />
                      <p>Select a result to view details</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="flex items-center justify-center h-32">
              <div className="text-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-2"></div>
                <p className="text-sm text-muted-foreground">Searching intelligence data...</p>
              </div>
            </div>
          )}

          {/* Error State */}
          {error && (
            <div className="flex items-center justify-center h-32 text-red-500">
              <AlertCircle className="h-6 w-6 mr-2" />
              <span>Error searching data</span>
            </div>
          )}

          {/* Empty State */}
          {!data && !loading && !error && (
            <div className="flex items-center justify-center h-32 text-muted-foreground">
              <div className="text-center">
                <Search className="h-8 w-8 mx-auto mb-2" />
                <p>Enter a search query to find intelligence data</p>
                <p className="text-xs mt-1">Try: &quot;AI trends&quot;, &quot;competitor analysis&quot;, &quot;market opportunities&quot;</p>
              </div>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}