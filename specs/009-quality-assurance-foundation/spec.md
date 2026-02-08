# Feature Spec: Quality Assurance Foundation

## Overview
Implement automated safeguards to ensure the test suite remains updated and the environment remains healthy.

## Functional Requirements
1. **Pre-commit Hook**: 
    - Install `pre-commit` via `uv`.
    - Configure it to run `pytest` before every commit.
2. **Doctor Command**:
    - Implement `paparazzit doctor`.
    - It should:
        - Run the test suite.
        - Check if `playwright` browsers are installed.
        - Verify `captures/` directory permissions.
3. **Spec Standard**:
    - Update the project guidelines to require a "Testing Requirements" section in all future specs.

## Acceptance Criteria
- Running `git commit` fails if tests are broken.
- Running `paparazzit doctor` provides a health report of the tool and environment.

## Testing Requirements
As part of the QA Foundation, every new feature spec must include a "Testing Requirements" section that outlines:
- **Unit Tests**: Which components require new or updated unit tests.
- **Integration Tests**: How the feature should be tested in concert with other components.
- **Manual Verification**: Specific steps to verify the feature manually if automation is not feasible.
- **Regression**: Existing features that should be re-tested to ensure no breakage.

