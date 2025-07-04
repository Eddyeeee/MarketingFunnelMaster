# Preview Deployments Guide

## Overview

Preview deployments are automatically created for every pull request in the MarketingFunnelMaster project. This enables reviewers to test changes in a production-like environment before merging.

## Features

### 🚀 Automatic Deployment
- Every PR gets its own preview deployment
- Updates automatically with new commits
- Accessible via custom URL: `pr-{number}-marketing-funnel-master.vercel.app`

### 💬 PR Comments
- Automatic comment with preview URL
- Includes deployment details and quick test links
- Updates with each new deployment

### 🧹 Automatic Cleanup
- Preview deployments are removed when PR is closed
- Stale deployments cleaned up after 7 days
- Failed deployments cleaned up after 24 hours

## How It Works

### 1. Opening a Pull Request
When you open a PR:
1. GitHub Actions triggers the preview deployment workflow
2. Vercel builds and deploys your branch
3. A comment is posted with the preview URL

### 2. Updating Your PR
When you push new commits:
1. The preview automatically rebuilds
2. The PR comment updates with the new deployment info
3. Old preview deployments are kept (up to 3)

### 3. Closing Your PR
When you close or merge a PR:
1. All preview deployments are removed
2. The custom alias is deleted
3. A final comment confirms cleanup

## Preview URL Structure

Each PR gets multiple URLs:
- **Direct URL**: `https://{deployment-id}.vercel.app`
- **PR Alias**: `https://pr-{number}-marketing-funnel-master.vercel.app`
- **Inspector**: Link to Vercel dashboard for logs and metrics

## Testing Your Preview

### Quick Tests
The PR comment includes links to:
- Lighthouse performance report
- Bundle size analysis
- Deployment logs

### Manual Testing
1. Click the preview URL
2. Test your changes in a production-like environment
3. Share the URL with stakeholders for feedback

## Advanced Features

### Performance Budgets
Preview deployments are subject to the same performance budgets as production:
- LCP < 2.5s
- FID < 100ms
- CLS < 0.1

Failed performance checks will block the PR.

### Environment Variables
Preview deployments use a special set of environment variables:
- Database: Staging database
- APIs: Staging endpoints
- Features: Preview-specific feature flags

## Troubleshooting

### Preview Not Deploying
1. Check GitHub Actions tab for errors
2. Ensure Vercel integration is active
3. Verify branch has no merge conflicts

### Preview URL Not Working
1. Wait 2-3 minutes for deployment to complete
2. Check deployment status in PR comment
3. Click "View logs" for error details

### Performance Issues
1. Run local Lighthouse test first
2. Check bundle size in build output
3. Review performance budget violations

## Best Practices

1. **Keep PRs Focused**: Smaller changes deploy faster
2. **Test Thoroughly**: Use the preview to catch issues early
3. **Share Previews**: Get feedback from team members
4. **Monitor Performance**: Check Lighthouse scores before merging

## Configuration

Preview deployments are configured in:
- `.github/workflows/preview-deployments.yml`
- `scripts/preview-deployment-manager.ts`
- `vercel.json` (preview-specific settings)

## Security

- Preview deployments use staging data only
- No production secrets are exposed
- URLs are publicly accessible (don't include sensitive data)
- Deployments are automatically cleaned up

---

For more information, see the [Vercel Documentation](https://vercel.com/docs/concepts/deployments/preview-deployments).