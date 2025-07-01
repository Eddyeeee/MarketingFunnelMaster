const axios = require('axios');
const { ApiConfig } = require('../config/api-config');

class SocialTrendScanner {
    constructor(config = {}) {
        this.config = {
            minEngagement: config.minEngagement || 1000,
            maxRequestsPerHour: config.maxRequestsPerHour || 100,
            trendThreshold: config.trendThreshold || 0.2, // 20% growth
            platforms: config.platforms || ['twitter', 'instagram', 'tiktok', 'youtube', 'reddit'],
            keywords: config.keywords || ['money', 'business', 'investing', 'passive income', 'side hustle'],
            ...config
        };
        
        this.apiConfig = new ApiConfig();
        this.requestCount = 0;
        this.lastResetTime = Date.now();
        this.trendCache = new Map();
        this.cacheExpiry = 30 * 60 * 1000; // 30 minutes
    }

    async scan() {
        const opportunities = [];
        
        try {
            const platformPromises = this.config.platforms.map(platform => 
                this.scanPlatform(platform).catch(error => {
                    console.error(`Error scanning ${platform}:`, error.message);
                    return [];
                })
            );

            const results = await Promise.all(platformPromises);
            results.forEach(platformOpportunities => {
                opportunities.push(...platformOpportunities);
            });

            // Filter and rank by trend velocity
            const trendingOpportunities = opportunities
                .filter(opp => opp.trendVelocity >= this.config.trendThreshold)
                .sort((a, b) => b.trendVelocity - a.trendVelocity);

            return trendingOpportunities;

        } catch (error) {
            console.error('Social trend scanning error:', error);
            throw error;
        }
    }

    async scanPlatform(platform) {
        const cacheKey = `${platform}_trends_${Math.floor(Date.now() / this.cacheExpiry)}`;
        
        if (this.trendCache.has(cacheKey)) {
            return this.trendCache.get(cacheKey);
        }

        await this.rateLimitCheck();

        let opportunities = [];

        try {
            switch (platform) {
                case 'twitter':
                    opportunities = await this.scanTwitter();
                    break;
                case 'instagram':
                    opportunities = await this.scanInstagram();
                    break;
                case 'tiktok':
                    opportunities = await this.scanTikTok();
                    break;
                case 'youtube':
                    opportunities = await this.scanYouTube();
                    break;
                case 'reddit':
                    opportunities = await this.scanReddit();
                    break;
                default:
                    console.warn(`Unknown platform: ${platform}`);
            }

            this.trendCache.set(cacheKey, opportunities);
            return opportunities;

        } catch (error) {
            console.error(`Error scanning ${platform}:`, error.message);
            return [];
        }
    }

    async scanTwitter() {
        const opportunities = [];
        const config = this.apiConfig.getNetworkConfig('twitter');
        
        if (!config) return opportunities;

        try {
            // Search for trending topics related to business/money
            for (const keyword of this.config.keywords) {
                const response = await axios.get(`${config.baseUrl}/2/tweets/search/recent`, {
                    headers: {
                        'Authorization': `Bearer ${config.bearerToken}`
                    },
                    params: {
                        query: `${keyword} lang:de OR lang:en -is:retweet`,
                        'tweet.fields': 'public_metrics,created_at,context_annotations',
                        'user.fields': 'public_metrics,verified',
                        'expansions': 'author_id',
                        max_results: 100
                    }
                });

                if (response.data?.data) {
                    const tweets = response.data.data;
                    const users = response.data.includes?.users || [];
                    
                    // Analyze tweet clusters and engagement patterns
                    const trendAnalysis = this.analyzeTweetTrends(tweets, users, keyword);
                    
                    if (trendAnalysis.isActive) {
                        opportunities.push({
                            id: `twitter_${keyword}_${Date.now()}`,
                            title: `${keyword} trending on Twitter`,
                            description: `High engagement around "${keyword}" with ${tweets.length} recent posts`,
                            keyword: keyword,
                            platform: 'twitter',
                            source: 'social_trend',
                            type: 'trending_topic',
                            engagement: trendAnalysis.totalEngagement,
                            trendVelocity: trendAnalysis.velocity,
                            sentiment: trendAnalysis.sentiment,
                            topTweets: trendAnalysis.topTweets,
                            lastUpdated: new Date().toISOString(),
                            metrics: {
                                tweetCount: tweets.length,
                                averageEngagement: trendAnalysis.averageEngagement,
                                influencerMentions: trendAnalysis.influencerMentions,
                                hashtagDensity: trendAnalysis.hashtagDensity
                            }
                        });
                    }
                }
            }
        } catch (error) {
            console.error('Twitter API error:', error.response?.data || error.message);
        }

        return opportunities;
    }

    async scanInstagram() {
        const opportunities = [];
        const config = this.apiConfig.getNetworkConfig('instagram');
        
        if (!config) return opportunities;

        try {
            // Use Instagram Basic Display API for hashtag analysis
            for (const keyword of this.config.keywords) {
                const hashtag = keyword.replace(/\s+/g, '');
                
                const response = await axios.get(`${config.baseUrl}/ig_hashtag_search`, {
                    params: {
                        user_id: config.userId,
                        access_token: config.accessToken,
                        q: hashtag
                    }
                });

                if (response.data?.data) {
                    for (const hashtagData of response.data.data) {
                        const mediaResponse = await axios.get(`${config.baseUrl}/${hashtagData.id}/recent_media`, {
                            params: {
                                user_id: config.userId,
                                access_token: config.accessToken,
                                fields: 'id,media_type,media_url,permalink,timestamp,like_count,comments_count'
                            }
                        });

                        if (mediaResponse.data?.data) {
                            const analysis = this.analyzeInstagramPosts(mediaResponse.data.data, hashtag);
                            
                            if (analysis.isActive) {
                                opportunities.push({
                                    id: `instagram_${hashtag}_${Date.now()}`,
                                    title: `#${hashtag} trending on Instagram`,
                                    description: `High engagement on Instagram hashtag #${hashtag}`,
                                    keyword: hashtag,
                                    platform: 'instagram',
                                    source: 'social_trend',
                                    type: 'trending_hashtag',
                                    engagement: analysis.totalEngagement,
                                    trendVelocity: analysis.velocity,
                                    topPosts: analysis.topPosts,
                                    lastUpdated: new Date().toISOString(),
                                    metrics: {
                                        postCount: mediaResponse.data.data.length,
                                        averageEngagement: analysis.averageEngagement,
                                        mediaTypes: analysis.mediaTypes
                                    }
                                });
                            }
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Instagram API error:', error.response?.data || error.message);
        }

        return opportunities;
    }

    async scanTikTok() {
        const opportunities = [];
        const config = this.apiConfig.getNetworkConfig('tiktok');
        
        if (!config) return opportunities;

        try {
            // Use TikTok Research API for trend analysis
            for (const keyword of this.config.keywords) {
                const response = await axios.post(`${config.baseUrl}/research/video/query/`, {
                    query: {
                        and: [
                            {
                                operation: "IN",
                                field_name: "keyword",
                                field_values: [keyword]
                            }
                        ]
                    },
                    max_count: 100,
                    cursor: 0,
                    search_id: `${keyword}_${Date.now()}`
                }, {
                    headers: {
                        'Authorization': `Bearer ${config.accessToken}`,
                        'Content-Type': 'application/json'
                    }
                });

                if (response.data?.data?.videos) {
                    const analysis = this.analyzeTikTokVideos(response.data.data.videos, keyword);
                    
                    if (analysis.isActive) {
                        opportunities.push({
                            id: `tiktok_${keyword}_${Date.now()}`,
                            title: `${keyword} trending on TikTok`,
                            description: `Viral content around "${keyword}" on TikTok`,
                            keyword: keyword,
                            platform: 'tiktok',
                            source: 'social_trend',
                            type: 'trending_content',
                            engagement: analysis.totalEngagement,
                            trendVelocity: analysis.velocity,
                            topVideos: analysis.topVideos,
                            lastUpdated: new Date().toISOString(),
                            metrics: {
                                videoCount: response.data.data.videos.length,
                                averageViews: analysis.averageViews,
                                viralPotential: analysis.viralPotential
                            }
                        });
                    }
                }
            }
        } catch (error) {
            console.error('TikTok API error:', error.response?.data || error.message);
        }

        return opportunities;
    }

    async scanYouTube() {
        const opportunities = [];
        const config = this.apiConfig.getNetworkConfig('youtube');
        
        if (!config) return opportunities;

        try {
            for (const keyword of this.config.keywords) {
                const response = await axios.get(`${config.baseUrl}/search`, {
                    params: {
                        part: 'snippet',
                        q: keyword,
                        type: 'video',
                        order: 'relevance',
                        publishedAfter: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
                        maxResults: 50,
                        key: config.apiKey
                    }
                });

                if (response.data?.items) {
                    const videoIds = response.data.items.map(item => item.id.videoId).join(',');
                    
                    const statsResponse = await axios.get(`${config.baseUrl}/videos`, {
                        params: {
                            part: 'statistics,snippet',
                            id: videoIds,
                            key: config.apiKey
                        }
                    });

                    if (statsResponse.data?.items) {
                        const analysis = this.analyzeYouTubeVideos(statsResponse.data.items, keyword);
                        
                        if (analysis.isActive) {
                            opportunities.push({
                                id: `youtube_${keyword}_${Date.now()}`,
                                title: `${keyword} trending on YouTube`,
                                description: `Popular YouTube content about "${keyword}"`,
                                keyword: keyword,
                                platform: 'youtube',
                                source: 'social_trend',
                                type: 'trending_videos',
                                engagement: analysis.totalEngagement,
                                trendVelocity: analysis.velocity,
                                topVideos: analysis.topVideos,
                                lastUpdated: new Date().toISOString(),
                                metrics: {
                                    videoCount: statsResponse.data.items.length,
                                    averageViews: analysis.averageViews,
                                    engagementRate: analysis.engagementRate
                                }
                            });
                        }
                    }
                }
            }
        } catch (error) {
            console.error('YouTube API error:', error.response?.data || error.message);
        }

        return opportunities;
    }

    async scanReddit() {
        const opportunities = [];
        const config = this.apiConfig.getNetworkConfig('reddit');
        
        if (!config) return opportunities;

        try {
            const subreddits = ['business', 'entrepreneur', 'investing', 'personalfinance', 'sidehustle'];
            
            for (const subreddit of subreddits) {
                const response = await axios.get(`${config.baseUrl}/r/${subreddit}/hot.json`, {
                    params: {
                        limit: 100
                    },
                    headers: {
                        'User-Agent': config.userAgent
                    }
                });

                if (response.data?.data?.children) {
                    const posts = response.data.data.children.map(child => child.data);
                    const analysis = this.analyzeRedditPosts(posts, subreddit);
                    
                    if (analysis.isActive) {
                        opportunities.push({
                            id: `reddit_${subreddit}_${Date.now()}`,
                            title: `Hot topics in r/${subreddit}`,
                            description: `Trending discussions in r/${subreddit}`,
                            keyword: subreddit,
                            platform: 'reddit',
                            source: 'social_trend',
                            type: 'trending_discussions',
                            engagement: analysis.totalEngagement,
                            trendVelocity: analysis.velocity,
                            topPosts: analysis.topPosts,
                            lastUpdated: new Date().toISOString(),
                            metrics: {
                                postCount: posts.length,
                                averageScore: analysis.averageScore,
                                commentDensity: analysis.commentDensity
                            }
                        });
                    }
                }
            }
        } catch (error) {
            console.error('Reddit API error:', error.response?.data || error.message);
        }

        return opportunities;
    }

    analyzeTweetTrends(tweets, users, keyword) {
        const userMap = new Map(users.map(user => [user.id, user]));
        let totalEngagement = 0;
        let totalInfluencerMentions = 0;
        let hashtagCount = 0;
        
        const topTweets = tweets
            .map(tweet => {
                const user = userMap.get(tweet.author_id);
                const engagement = (tweet.public_metrics?.like_count || 0) + 
                                 (tweet.public_metrics?.retweet_count || 0) + 
                                 (tweet.public_metrics?.reply_count || 0);
                
                totalEngagement += engagement;
                
                if (user?.verified || (user?.public_metrics?.followers_count || 0) > 10000) {
                    totalInfluencerMentions++;
                }
                
                if (tweet.text?.includes('#')) {
                    hashtagCount++;
                }
                
                return { ...tweet, engagement, user };
            })
            .sort((a, b) => b.engagement - a.engagement)
            .slice(0, 5);

        const averageEngagement = totalEngagement / tweets.length;
        const velocity = this.calculateTrendVelocity(tweets);
        
        return {
            isActive: averageEngagement >= this.config.minEngagement && velocity >= this.config.trendThreshold,
            totalEngagement,
            averageEngagement,
            velocity,
            influencerMentions: totalInfluencerMentions,
            hashtagDensity: hashtagCount / tweets.length,
            topTweets,
            sentiment: this.calculateSentiment(tweets.map(t => t.text))
        };
    }

    analyzeInstagramPosts(posts, hashtag) {
        let totalEngagement = 0;
        const mediaTypes = { image: 0, video: 0, carousel: 0 };
        
        const topPosts = posts
            .map(post => {
                const engagement = (post.like_count || 0) + (post.comments_count || 0);
                totalEngagement += engagement;
                mediaTypes[post.media_type.toLowerCase()]++;
                return { ...post, engagement };
            })
            .sort((a, b) => b.engagement - a.engagement)
            .slice(0, 5);

        const averageEngagement = totalEngagement / posts.length;
        const velocity = this.calculateEngagementVelocity(posts);
        
        return {
            isActive: averageEngagement >= this.config.minEngagement && velocity >= this.config.trendThreshold,
            totalEngagement,
            averageEngagement,
            velocity,
            topPosts,
            mediaTypes
        };
    }

    analyzeTikTokVideos(videos, keyword) {
        let totalViews = 0;
        let totalEngagement = 0;
        
        const topVideos = videos
            .map(video => {
                const views = video.video_description?.view_count || 0;
                const likes = video.video_description?.like_count || 0;
                const comments = video.video_description?.comment_count || 0;
                const shares = video.video_description?.share_count || 0;
                
                totalViews += views;
                const engagement = likes + comments + shares;
                totalEngagement += engagement;
                
                return { ...video, views, engagement };
            })
            .sort((a, b) => b.engagement - a.engagement)
            .slice(0, 5);

        const averageViews = totalViews / videos.length;
        const averageEngagement = totalEngagement / videos.length;
        const velocity = this.calculateTrendVelocity(videos);
        
        return {
            isActive: averageViews >= this.config.minEngagement && velocity >= this.config.trendThreshold,
            totalEngagement,
            averageViews,
            velocity,
            topVideos,
            viralPotential: this.calculateViralPotential(videos)
        };
    }

    analyzeYouTubeVideos(videos, keyword) {
        let totalViews = 0;
        let totalEngagement = 0;
        
        const topVideos = videos
            .map(video => {
                const views = parseInt(video.statistics?.viewCount || 0);
                const likes = parseInt(video.statistics?.likeCount || 0);
                const comments = parseInt(video.statistics?.commentCount || 0);
                
                totalViews += views;
                const engagement = likes + comments;
                totalEngagement += engagement;
                
                return { ...video, views, engagement };
            })
            .sort((a, b) => b.engagement - a.engagement)
            .slice(0, 5);

        const averageViews = totalViews / videos.length;
        const engagementRate = totalViews > 0 ? (totalEngagement / totalViews) * 100 : 0;
        const velocity = this.calculateTrendVelocity(videos);
        
        return {
            isActive: averageViews >= this.config.minEngagement && velocity >= this.config.trendThreshold,
            totalEngagement,
            averageViews,
            engagementRate,
            velocity,
            topVideos
        };
    }

    analyzeRedditPosts(posts, subreddit) {
        let totalScore = 0;
        let totalComments = 0;
        
        const topPosts = posts
            .map(post => {
                const score = post.score || 0;
                const comments = post.num_comments || 0;
                
                totalScore += score;
                totalComments += comments;
                
                return { ...post, engagement: score + comments };
            })
            .sort((a, b) => b.engagement - a.engagement)
            .slice(0, 5);

        const averageScore = totalScore / posts.length;
        const commentDensity = totalComments / posts.length;
        const velocity = this.calculateTrendVelocity(posts);
        
        return {
            isActive: averageScore >= this.config.minEngagement && velocity >= this.config.trendThreshold,
            totalEngagement: totalScore + totalComments,
            averageScore,
            commentDensity,
            velocity,
            topPosts
        };
    }

    calculateTrendVelocity(items) {
        if (items.length < 2) return 0;
        
        const now = Date.now();
        const recentItems = items.filter(item => {
            const itemTime = new Date(item.created_at || item.timestamp || item.created_utc * 1000);
            return (now - itemTime.getTime()) <= 24 * 60 * 60 * 1000; // Last 24 hours
        });
        
        const olderItems = items.filter(item => {
            const itemTime = new Date(item.created_at || item.timestamp || item.created_utc * 1000);
            const timeDiff = now - itemTime.getTime();
            return timeDiff > 24 * 60 * 60 * 1000 && timeDiff <= 48 * 60 * 60 * 1000; // 24-48 hours ago
        });
        
        if (olderItems.length === 0) return recentItems.length > 5 ? 1 : 0;
        
        const recentCount = recentItems.length;
        const olderCount = olderItems.length;
        
        return olderCount > 0 ? (recentCount - olderCount) / olderCount : recentCount > 5 ? 1 : 0;
    }

    calculateEngagementVelocity(posts) {
        const now = Date.now();
        const recentEngagement = posts
            .filter(post => {
                const postTime = new Date(post.timestamp || post.created_at);
                return (now - postTime.getTime()) <= 6 * 60 * 60 * 1000; // Last 6 hours
            })
            .reduce((sum, post) => sum + ((post.like_count || 0) + (post.comments_count || 0)), 0);
        
        const olderEngagement = posts
            .filter(post => {
                const postTime = new Date(post.timestamp || post.created_at);
                const timeDiff = now - postTime.getTime();
                return timeDiff > 6 * 60 * 60 * 1000 && timeDiff <= 12 * 60 * 60 * 1000;
            })
            .reduce((sum, post) => sum + ((post.like_count || 0) + (post.comments_count || 0)), 0);
        
        return olderEngagement > 0 ? (recentEngagement - olderEngagement) / olderEngagement : 0;
    }

    calculateViralPotential(videos) {
        const shareRates = videos.map(video => {
            const shares = video.video_description?.share_count || 0;
            const views = video.video_description?.view_count || 1;
            return shares / views;
        });
        
        return shareRates.reduce((sum, rate) => sum + rate, 0) / shareRates.length;
    }

    calculateSentiment(texts) {
        const positiveWords = ['good', 'great', 'excellent', 'amazing', 'love', 'best', 'awesome'];
        const negativeWords = ['bad', 'terrible', 'awful', 'hate', 'worst', 'horrible'];
        
        let positiveCount = 0;
        let negativeCount = 0;
        
        texts.forEach(text => {
            const lowerText = text.toLowerCase();
            positiveCount += positiveWords.filter(word => lowerText.includes(word)).length;
            negativeCount += negativeWords.filter(word => lowerText.includes(word)).length;
        });
        
        if (positiveCount > negativeCount) return 'positive';
        if (negativeCount > positiveCount) return 'negative';
        return 'neutral';
    }

    async rateLimitCheck() {
        const now = Date.now();
        
        if (now - this.lastResetTime >= 3600000) { // Reset every hour
            this.requestCount = 0;
            this.lastResetTime = now;
        }
        
        if (this.requestCount >= this.config.maxRequestsPerHour) {
            const waitTime = 3600000 - (now - this.lastResetTime);
            await new Promise(resolve => setTimeout(resolve, waitTime));
            this.requestCount = 0;
            this.lastResetTime = Date.now();
        }
        
        this.requestCount++;
    }

    clearCache() {
        this.trendCache.clear();
    }

    getStats() {
        return {
            cacheSize: this.trendCache.size,
            requestCount: this.requestCount,
            platforms: this.config.platforms,
            keywords: this.config.keywords
        };
    }
}

module.exports = { SocialTrendScanner };