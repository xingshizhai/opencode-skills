---
name: requirements-manager
description: Extract and organize project requirements from chat conversations, then update documentation in project docs directory. Use when user discusses features, functionalities, or system requirements during development, including collecting requirements from conversation, categorizing and structuring requirements, updating or creating requirements.md in docs/, and maintaining requirement traceability
---

# Requirements Manager

## Overview

Manage project requirements by extracting information from development conversations and maintaining organized documentation in the project's docs directory.

## Quick Start

When user discusses project requirements during chat:

1. Extract requirements from conversation context
2. Categorize by type (functional, non-functional, constraints)
3. Update or create `docs/requirements.md`
4. Maintain version history and traceability

## Requirements Extraction

### When to Extract Requirements

Trigger this skill when user mentions:
- New features or functionality
- System behaviors or specifications
- Performance, security, or usability requirements
- Technical constraints or dependencies
- Business rules or logic

### Extraction Process

1. Scan conversation for requirement-related statements
2. Identify explicit requirements (clear statements)
3. Infer implicit requirements (implied needs)
4. Clarify ambiguous requirements with user
5. Prioritize by importance and urgency

### Requirement Categories

**Functional Requirements:**
- Features and capabilities
- User interactions and workflows
- Business rules and logic
- Data inputs and outputs

**Non-Functional Requirements:**
- Performance (response time, throughput)
- Reliability and availability
- Scalability
- Security and privacy
- Usability and accessibility

**Constraints:**
- Technical constraints (platform, technology)
- Business constraints (budget, timeline)
- Regulatory constraints (compliance, standards)
- Design constraints (architecture, patterns)

## Requirements Documentation

### Document Structure

Location: `docs/requirements.md`

Standard format:

```markdown
# Project Requirements

## Version History
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | YYYY-MM-DD | Initial version | ... |

## Functional Requirements
[FR-001] Requirement description
[FR-002] Requirement description

## Non-Functional Requirements
[NFR-001] Requirement description

## Constraints
[CON-001] Requirement description

## Out of Scope
[OOS-001] Excluded functionality
```

### Requirement Format

Each requirement should include:
- **ID**: Unique identifier (FR-001, NFR-001, CON-001)
- **Title**: Brief descriptive title
- **Description**: Clear, testable description
- **Priority**: High/Medium/Low
- **Status**: New/In Progress/Completed/Deferred
- **Source**: Where requirement originated (chat, meeting, etc.)
- **Acceptance Criteria**: How to verify requirement is met

### Updating Requirements

When adding new requirements:

1. Review existing requirements for duplicates
2. Assign appropriate ID (next sequential number)
3. Document source with timestamp
4. Mark status as "New"
5. Add to appropriate category section
6. Update version history

### Requirement Traceability

Maintain traceability by:
- Linking requirements to features/PRs
- Tracking requirement status changes
- Documenting requirement changes/rejections
- Mapping requirements to acceptance criteria

## Workflow

### During Development Conversation

When user mentions requirements:

1. **Capture**: Note requirement details from conversation
2. **Clarify**: Ask clarifying questions if ambiguous
3. **Classify**: Determine category (FR/NFR/Constraint)
4. **Document**: Add to requirements.md
5. **Confirm**: Briefly confirm with user what was documented

### Example Workflow

**User**: "I need the system to send email notifications when tasks are completed"

**Response**:
- Extract requirement: Email notification on task completion
- Classify: Functional requirement
- Document: `[FR-015] Send email notification when task status changes to 'completed'`
- Confirm: "I've added requirement FR-015 to docs/requirements.md for email notifications on task completion"

## Best Practices

1. Keep requirements concise and testable
2. Use "shall" for mandatory requirements, "should" for optional
3. Avoid implementation details in requirements
4. Review requirements periodically for relevance
5. Archive deprecated requirements instead of deleting
6. Use version control to track requirement changes

## Resources
