taxonomy_num_to_text_map = {
    "top_categories": {
        "1": "Architectural Analysis & Understanding",
        "2": "Performance & Scalability",
        "3": "Integration & Extension",
        "4": "Refactoring & Evolution",
        "5": "Data Management & Processing",
        "6": "Resilience & Reliability",
        "7": "Security & Compliance",
        "8": "Event-Driven & Real-Time Systems",
        "9": "Deployment & Operations",
        "10": "Domain-Specific Architectures",
        "11": "Cross-Cutting Concerns",
    },
    "sub_categories": {
        "1.1": "Flow Tracing & Documentation",
        "1.2": "Pattern Identification & Explanation",
        "1.3": "System Mapping & Component Analysis",
        "2.1": "Bottleneck Diagnosis",
        "2.2": "Optimization Strategies",
        "2.3": "Scalability Assessment",
        "3.1": "New Feature Integration",
        "3.2": "System Extension",
        "4.1": "Architectural Refactoring",
        "4.2": "Code Quality & Structure",
        "5.1": "Data Flow Architecture",
        "5.2": "Persistence & Storage",
        "5.3": "Data Quality & Integrity",
        "6.1": "Fault Tolerance",
        "6.2": "System Resilience",
        "7.1": "Access Control & Authentication",
        "7.2": "Compliance & Governance",
        "8.1": "Event Architecture",
        "8.2": "Real-Time Processing",
        "9.1": "Deployment Strategies",
        "9.2": "Observability & Monitoring",
        "10.1": "Financial Systems",
        "10.2": "Healthcare Systems",
        "10.3": "Gaming & Multimedia",
        "10.4": "ML/AI Systems",
        "11.1": "Configuration Management",
        "11.2": "Cross-Service Communication",
    },
}

TAXONOMY_PROMPT="""
### 1. **Architectural Analysis & Understanding**
*1.1 Flow Tracing & Documentation*
- Data Flow Tracing (telemetry, transactions, requests)
- Event Flow Analysis (assessment completion, user actions)
- Workflow Documentation (order creation, medication orders)
- Request Lifecycle Tracing (authentication, GraphQL queries)

*1.2 Pattern Identification & Explanation*
- Architectural Pattern Analysis (CQRS, Hexagonal, Repository)
- Design Pattern Recognition (Observer, Factory, Strategy)
- System Communication Patterns (RPC vs Event Bus, REST vs GraphQL)

*1.3 System Mapping & Component Analysis*
- Component Responsibility Mapping
- Feature-to-Module Mapping
- Service Interaction Analysis
- Configuration Management Analysis

### 2. **Performance & Scalability**
*2.1 Bottleneck Diagnosis*
- Processing Pipeline Bottlenecks (ML, multimedia, data)
- API Performance Issues (latency, degradation)
- Database/Query Performance
- System-Wide Performance Degradation

*2.2 Optimization Strategies*
- Caching Strategies (query-side, GraphQL, user-specific)
- Parallelism & Concurrency Implementation
- Asynchronous Processing Refactoring
- Load Balancing & Distribution

*2.3 Scalability Assessment*
- High-Volume Data Ingestion Analysis
- High-Concurrency Read/Write Operations
- Microservice Scalability Audits
- System Scaling Strategies

### 3. **Integration & Extension**
*3.1 New Feature Integration*
- Third-Party Service Integration (payment, authentication, analytics)
- New Data Source Integration
- Cross-System Integration Planning
- Plugin/Extension System Design

*3.2 System Extension*
- API Extension (new endpoints, data models)
- Pipeline Extension (new processing stages)
- Service Mesh Extension
- Feature Enhancement Architecture

### 4. **Refactoring & Evolution**
*4.1 Architectural Refactoring*
- Monolith Decomposition
- Service Decoupling
- Pattern Implementation (Repository, CQRS, Saga)
- Legacy System Migration

*4.2 Code Quality & Structure*
- Technical Debt Remediation
- Code Consolidation & Standardization
- Testability & Maintainability Improvements
- Architecture Drift Correction

### 5. **Data Management & Processing**
*5.1 Data Flow Architecture*
- Ingestion Pipeline Design
- ETL/ELT Processing
- Stream vs Batch Processing
- Data Transformation Strategies

*5.2 Persistence & Storage*
- Database Architecture
- Caching Layer Design
- File Storage Strategies
- Data Synchronization (offline/cloud)

*5.3 Data Quality & Integrity*
- Validation Mechanisms
- Error Handling & Recovery
- Data Lineage & Auditing
- Consistency Patterns (Saga, Transactions)

### 6. **Resilience & Reliability**
*6.1 Fault Tolerance*
- Circuit Breaker Implementation
- Retry & Fallback Strategies
- Dead Letter Queue Design
- Failure Recovery Mechanisms

*6.2 System Resilience*
- Cascading Failure Prevention
- High Availability Design
- Disaster Recovery Planning
- Graceful Degradation

### 7. **Security & Compliance**
*7.1 Access Control & Authentication*
- Authentication Flow Design
- Authorization Mechanisms (RBAC, ABAC)
- Multi-Tenant Security
- Cross-Service Auth Flows

*7.2 Compliance & Governance*
- Regulatory Compliance (HIPAA, FERPA, GDPR)
- Audit Trail Implementation
- Data Privacy Architecture
- Security Scanning Integration

### 8. **Event-Driven & Real-Time Systems**
*8.1 Event Architecture*
- Event-Driven System Design
- Real-Time Notification Systems
- Event Sourcing Implementation
- Message Brokering Patterns

*8.2 Real-Time Processing*
- Live Data Processing
- Real-Time Analytics
- Collaborative Features (editing, notifications)
- WebSocket Architecture

### 9. **Deployment & Operations**
*9.1 Deployment Strategies*
- Canary/Blue-Green Deployments
- Serverless Architecture
- Container Orchestration
- Feature Flag Systems

*9.2 Observability & Monitoring*
- Logging System Architecture
- Monitoring & Alerting Design
- Distributed Tracing Implementation
- Health Check Systems

### 10. **Domain-Specific Architectures**
*10.1 Financial Systems*
- Payment Processing Architectures
- Transaction Flows & Settlement
- Fraud Detection Systems
- Cross-Currency Processing

*10.2 Healthcare Systems*
- Patient Data Management
- Medical Record Processing
- Compliance-Driven Architectures
- Clinical Trial Systems

*10.3 Gaming & Multimedia*
- Game Engine Architecture
- Media Processing Pipelines
- Real-Time Physics Systems
- Multiplayer Synchronization

*10.4 ML/AI Systems*
- Model Serving Architecture
- Training Pipeline Design
- Inference Optimization
- MLOps Infrastructure

### 11. **Cross-Cutting Concerns**
*11.1 Configuration Management*
- Dynamic Configuration Systems
- Environment-Specific Configuration
- Configuration Loading Mechanisms
- Secret Management

*11.2 Cross-Service Communication*
- API Gateway Design
- Service Mesh Implementation
- Inter-Service Authentication
- Data Consistency Across Services"""


def _create_num_to_text_taxonomy_map() -> None:
    """
    Generates a hashmap for mapping taxonomy number
    to taxonomy name (top level and finegrained level)
    from the TAXONOMY_PROMPT above;
    Used for easier post-processing of LLM responses
    """
    import re

    # top level
    match = re.findall(r"\*\*(.*?)\*\*", TAXONOMY_PROMPT)
    top_tax_map = {str(idx+1):val for idx,val in enumerate(match)}

    # finegrained level
    match_sub = re.findall(r"\*(.*?)\*", TAXONOMY_PROMPT)
    match_sub = [m for m in match_sub if m]
    sub_tax_map = {m.split(' ',1)[0]: m.split(' ',1)[-1] for m in match_sub}

    tax_map = {"top_categories": top_tax_map, "sub_categories": sub_tax_map}
    print(tax_map)
