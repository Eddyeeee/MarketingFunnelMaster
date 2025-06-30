import axios from 'axios';

// Social Media Service für alle Plattformen
export const socialMediaService = {
  // Facebook API Integration
  async postToFacebook(pageId: string, accessToken: string, content: any) {
    try {
      const response = await axios.post(
        `https://graph.facebook.com/v18.0/${pageId}/feed`,
        {
          message: content.message,
          link: content.link,
          scheduled_publish_time: content.scheduledTime,
          access_token: accessToken
        }
      );

      return {
        success: true,
        postId: response.data.id,
        platform: 'facebook'
      };
    } catch (error) {
      console.error('Facebook Post Fehler:', error);
      throw error;
    }
  },

  // Instagram API Integration
  async postToInstagram(businessAccountId: string, accessToken: string, content: any) {
    try {
      // Erst Media Container erstellen
      const mediaResponse = await axios.post(
        `https://graph.facebook.com/v18.0/${businessAccountId}/media`,
        {
          image_url: content.imageUrl,
          caption: content.caption,
          access_token: accessToken
        }
      );

      // Dann Post veröffentlichen
      const publishResponse = await axios.post(
        `https://graph.facebook.com/v18.0/${businessAccountId}/media_publish`,
        {
          creation_id: mediaResponse.data.id,
          access_token: accessToken
        }
      );

      return {
        success: true,
        postId: publishResponse.data.id,
        platform: 'instagram'
      };
    } catch (error) {
      console.error('Instagram Post Fehler:', error);
      throw error;
    }
  },

  // TikTok API Integration
  async postToTikTok(accessToken: string, content: any) {
    try {
      const response = await axios.post(
        'https://open.tiktokapis.com/v2/post/publish/video/init/',
        {
          post_info: {
            title: content.title,
            description: content.description,
            privacy_level: 'public',
            disable_duet: false,
            disable_comment: false,
            disable_stitch: false,
            video_cover_timestamp_ms: 0
          }
        },
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      return {
        success: true,
        postId: response.data.data.post_id,
        platform: 'tiktok'
      };
    } catch (error) {
      console.error('TikTok Post Fehler:', error);
      throw error;
    }
  },

  // Pinterest API Integration
  async postToPinterest(accessToken: string, content: any) {
    try {
      const response = await axios.post(
        'https://api.pinterest.com/v5/pins',
        {
          board_id: content.boardId,
          title: content.title,
          description: content.description,
          link: content.link,
          media_source: {
            source_type: 'image_url',
            url: content.imageUrl
          }
        },
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      return {
        success: true,
        postId: response.data.id,
        platform: 'pinterest'
      };
    } catch (error) {
      console.error('Pinterest Post Fehler:', error);
      throw error;
    }
  },

  // Twitter/X API Integration
  async postToTwitter(accessToken: string, content: any) {
    try {
      const response = await axios.post(
        'https://api.twitter.com/2/tweets',
        {
          text: content.text
        },
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      return {
        success: true,
        postId: response.data.data.id,
        platform: 'twitter'
      };
    } catch (error) {
      console.error('Twitter Post Fehler:', error);
      throw error;
    }
  },

  // LinkedIn API Integration
  async postToLinkedIn(accessToken: string, content: any) {
    try {
      const response = await axios.post(
        'https://api.linkedin.com/v2/ugcPosts',
        {
          author: `urn:li:person:${content.authorId}`,
          lifecycleState: 'PUBLISHED',
          specificContent: {
            'com.linkedin.ugc.ShareContent': {
              shareCommentary: {
                text: content.text
              },
              shareMediaCategory: 'NONE'
            }
          },
          visibility: {
            'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
          }
        },
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
          }
        }
      );

      return {
        success: true,
        postId: response.data.id,
        platform: 'linkedin'
      };
    } catch (error) {
      console.error('LinkedIn Post Fehler:', error);
      throw error;
    }
  },

  // YouTube API Integration
  async postToYouTube(accessToken: string, content: any) {
    try {
      const response = await axios.post(
        'https://www.googleapis.com/upload/youtube/v3/videos',
        {
          snippet: {
            title: content.title,
            description: content.description,
            tags: content.tags,
            categoryId: '22' // People & Blogs
          },
          status: {
            privacyStatus: 'public'
          }
        },
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          },
          params: {
            part: 'snippet,status',
            uploadType: 'resumable'
          }
        }
      );

      return {
        success: true,
        postId: response.data.id,
        platform: 'youtube'
      };
    } catch (error) {
      console.error('YouTube Post Fehler:', error);
      throw error;
    }
  },

  // Multi-Platform Post
  async postToMultiplePlatforms(platforms: string[], content: any) {
    const results = [];
    
    for (const platform of platforms) {
      try {
        let result;
        
        switch (platform) {
          case 'facebook':
            result = await this.postToFacebook(
              content.facebookPageId,
              content.facebookAccessToken,
              content
            );
            break;
          case 'instagram':
            result = await this.postToInstagram(
              content.instagramBusinessAccountId,
              content.instagramAccessToken,
              content
            );
            break;
          case 'tiktok':
            result = await this.postToTikTok(
              content.tiktokAccessToken,
              content
            );
            break;
          case 'pinterest':
            result = await this.postToPinterest(
              content.pinterestAccessToken,
              content
            );
            break;
          case 'twitter':
            result = await this.postToTwitter(
              content.twitterAccessToken,
              content
            );
            break;
          case 'linkedin':
            result = await this.postToLinkedIn(
              content.linkedinAccessToken,
              content
            );
            break;
          case 'youtube':
            result = await this.postToYouTube(
              content.youtubeAccessToken,
              content
            );
            break;
          default:
            console.warn(`Unbekannte Plattform: ${platform}`);
            continue;
        }
        
        results.push(result);
      } catch (error) {
        console.error(`Fehler beim Posten auf ${platform}:`, error);
        results.push({
          success: false,
          platform,
          error: error.message
        });
      }
    }
    
    return results;
  },

  // Analytics für Social Media Posts
  async getPostAnalytics(platform: string, postId: string, accessToken: string) {
    try {
      let response;
      
      switch (platform) {
        case 'facebook':
          response = await axios.get(
            `https://graph.facebook.com/v18.0/${postId}/insights`,
            {
              params: {
                metric: 'post_impressions,post_reach,post_engagements',
                access_token: accessToken
              }
            }
          );
          break;
        case 'instagram':
          response = await axios.get(
            `https://graph.facebook.com/v18.0/${postId}/insights`,
            {
              params: {
                metric: 'impressions,reach,engagement',
                access_token: accessToken
              }
            }
          );
          break;
        default:
          throw new Error(`Analytics für ${platform} noch nicht implementiert`);
      }
      
      return {
        success: true,
        platform,
        postId,
        analytics: response.data.data
      };
    } catch (error) {
      console.error(`Analytics Fehler für ${platform}:`, error);
      throw error;
    }
  }
}; 