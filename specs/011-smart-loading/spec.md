# Feature Spec: Smart Loading for Web Captures

## Overview
Improve the reliability of screenshots by ensuring images and dynamic content are fully loaded before the capture is taken.

## User Story
As a QA engineer, I want my screenshots to include all images and assets so that I don't have to manually re-run captures for slow-loading pages.

## Functional Requirements
1. **Network Idle Waiting**: By default, the Playwright engine should wait for the `networkidle` state (no network activity for 500ms) before taking a screenshot.
2. **Custom Wait Flag**: Add a `--wait <ms>` flag to the `snap` command to allow for an additional hard-coded pause after the network is idle (default: 0ms).
3. **Lazy-Load Trigger (Optional/Future)**: Consider a simple scroll-to-bottom action if network idle isn't sufficient for specific sites.

## Testing Requirements
1. **Engine Logic**: Verify that the Playwright engine calls `wait_for_load_state("networkidle")`.
2. **CLI Flag**: Verify that the `--wait` flag correctly passes a sleep duration to the engine.

## Acceptance Criteria
- Running `paparazzit snap --url https://example.com` waits for network activity to settle.
- Captures of image-heavy sites show significantly fewer missing assets.
