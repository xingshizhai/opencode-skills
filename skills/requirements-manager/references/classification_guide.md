# Requirements Classification Guide

## Requirement Types

### Functional Requirements (FR)
Requirements that specify what the system should do.

**Examples:**
- User authentication and authorization
- Data processing and business logic
- User interface interactions
- Reporting and analytics
- API endpoints and integrations

**Identification Keywords:**
- "must", "shall", "need to", "should"
- Feature names, functionality
- User actions, system behaviors
- Input/output specifications

### Non-Functional Requirements (NFR)
Requirements that specify how the system should perform.

**Subcategories:**

1. **Performance**
   - Response time (< 200ms for API calls)
   - Throughput (1000 requests/second)
   - Latency, concurrency, scalability

2. **Reliability**
   - Uptime (99.9% availability)
   - Error rates (< 0.1%)
   - Recovery time, disaster recovery

3. **Security**
   - Authentication (OAuth, JWT, SAML)
   - Data encryption (at rest, in transit)
   - Access control (RBAC, ABAC)
   - Compliance (GDPR, HIPAA, SOC2)

4. **Usability**
   - User interface responsiveness
   - Accessibility (WCAG 2.1 AA)
   - Learning curve, error prevention

5. **Maintainability**
   - Code modularity
   - Documentation standards
   - Testing coverage (> 80%)
   - Deployment automation

**Identification Keywords:**
- Performance terms (fast, slow, response time)
- Security terms (secure, encrypt, authenticate)
- Quality terms (reliable, available, scalable)
- UX terms (usable, accessible, intuitive)

### Constraints (CON)
Restrictions on the system or development process.

**Subcategories:**

1. **Technical Constraints**
   - Technology stack (React, Node.js, PostgreSQL)
   - Platform limitations (mobile, web, desktop)
   - Integration requirements (third-party APIs)
   - Legacy system compatibility

2. **Business Constraints**
   - Budget limits
   - Timeline deadlines
   - Resource availability
   - Market constraints

3. **Regulatory Constraints**
   - Legal requirements
   - Industry standards
   - Compliance certifications
   - Data protection laws

4. **Design Constraints**
   - Architectural patterns (MVC, microservices)
   - Coding standards
   - Design system compliance
   - Brand guidelines

**Identification Keywords:**
- "must use", "limited to", "constraint"
- Technology names, standards
- Budget, deadline, resource mentions
- Legal, compliance, regulation terms

## Priority Levels

### High (P1)
- Critical to system functionality
- Blocks other work
- Regulatory or security critical
- User-facing, high-impact

### Medium (P2)
- Important but not critical
- Enhances functionality
- Nice-to-have features
- Technical debt reduction

### Low (P3)
- Future considerations
- Low-impact features
- Nice improvements
- May be deferred

## Status Values

- **New**: Recently added, not yet started
- **In Progress**: Being worked on
- **Completed**: Fully implemented and tested
- **Deferred**: Postponed indefinitely
- **Cancelled**: No longer needed

## Writing Good Requirements

### SMART Criteria

**S**pecific - Clear and unambiguous
**M**easurable - Can be verified/tested
**A**chievable - Realistic within constraints
**R**elevant - Aligns with project goals
**T**ime-bound - Has deadline or milestone

### Common Anti-Patterns

**Too Vague**:
- "The system should be fast" → "API response time < 200ms for 95% of requests"

**Implementation Details**:
- "Use React hooks for state management" → "Component state must be managed efficiently"

**Non-Testable**:
- "User-friendly interface" → "New users can complete task X in < 5 minutes without help"

**Multiple Requirements**:
- "Users can login, reset password, and manage profile" → Split into 3 separate requirements

### Acceptance Criteria

Good acceptance criteria:
- Testable and verifiable
- Binary (pass/fail)
- Covers all aspects of requirement
- Written from user perspective

Example:
```
As a user, I want to reset my password so I can regain access.

Acceptance Criteria:
- [ ] User can request password reset from login page
- [ ] System sends reset link to user's email within 30 seconds
- [ ] Reset link expires after 1 hour
- [ ] User can set new password using valid reset link
- [ ] Invalid/expired links show clear error message
```
