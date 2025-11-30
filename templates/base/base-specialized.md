# Base Specialized Template

---
template_type: base
category: specialized
version: 1.0.0
description: Base template for specialized agents with domain expertise patterns, integration guidelines, and tool-specific workflows
usage: Reference patterns from specific specialized agent templates using extends/inherits/overrides
---

## Purpose

This base template provides common patterns for specialized agents that focus on specific domains, tools, or technologies (imagemagick, circuit-breakers, git-file-tracking, content-agent, etc.). Agent templates inherit these patterns and customize them for their specialized domains.

## Pattern Categories

### Domain Expertise Patterns {#domain_expertise_patterns}

**Specialized Knowledge Areas**:
- **Tool-Specific**: Deep knowledge of specific tools (ImageMagick, Git, Docker)
- **Technology Stack**: Expertise in particular frameworks or platforms
- **Domain Logic**: Business domain knowledge (payments, auth, media processing)
- **Integration**: Connecting systems and services

**Expertise Documentation**:
```markdown
## Domain Expertise: [Specialization]

### Core Capabilities
- [Capability 1]: [Description of what agent can do]
- [Capability 2]: [Description of what agent can do]

### Use Cases
- **Use Case 1**: [When to use this specialization]
  - Input: [What agent receives]
  - Process: [How agent processes]
  - Output: [What agent produces]

### Limitations
- [Limitation 1]: [What agent cannot do]
- [Limitation 2]: [When to hand off to other agents]

### Prerequisites
- [Requirement 1]: [System/tool dependencies]
- [Requirement 2]: [Knowledge prerequisites]
```

**Example - Image Processing Agent**:
```markdown
## Domain Expertise: Image Processing with ImageMagick

### Core Capabilities
- Image format conversion (PNG, JPG, WebP, AVIF)
- Resizing and cropping with aspect ratio preservation
- Batch processing with consistent transformations
- Optimization for web delivery

### Use Cases
- **Thumbnail Generation**:
  - Input: High-resolution image
  - Process: Resize to 200x200px, optimize for web
  - Output: Optimized thumbnail with preserved aspect ratio

### Limitations
- Cannot edit image content (object removal, filtering)
- Cannot perform AI-based operations (face detection, style transfer)
- Hand off to AI/ML agents for advanced image analysis

### Prerequisites
- ImageMagick 7.0+ installed
- Sufficient disk space for temporary files
- Understanding of image formats and compression
```

### Integration Guidelines {#integration_guidelines}

**Integration Patterns**:
- **API Integration**: Connect to external services
- **Tool Chaining**: Combine multiple specialized tools
- **Event-Driven**: React to system events or triggers
- **Workflow Orchestration**: Coordinate multi-step processes

**API Integration Template**:
```python
# Example: External API integration pattern
class ExternalServiceClient:
    """Client for integrating with external service.

    Design Decision: Use retry with exponential backoff for
    resilience against transient network failures.

    Error Handling:
    - Retries: Up to 3 attempts with exponential backoff
    - Timeout: 30 seconds per request
    - Circuit Breaker: Open after 5 consecutive failures
    """

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
        return session

    @retry(max_attempts=3, backoff_factor=2.0)
    def fetch_data(self, endpoint: str) -> dict:
        """Fetch data from external service with retry logic."""
        response = self.session.get(
            f"{self.base_url}/{endpoint}",
            timeout=30
        )
        response.raise_for_status()
        return response.json()
```

**Tool Chaining**:
```bash
# Example: Multi-tool workflow
# Image processing pipeline: Resize -> Optimize -> Upload

# Step 1: Resize with ImageMagick
convert input.jpg -resize 800x600 resized.jpg

# Step 2: Optimize with oxipng (for PNG) or mozjpeg (for JPG)
mozjpeg -quality 85 resized.jpg > optimized.jpg

# Step 3: Upload to storage (S3, CDN)
aws s3 cp optimized.jpg s3://bucket/images/optimized.jpg
```

**Error Handling in Integration**:
```python
# Example: Graceful degradation pattern
def process_with_fallback(data):
    try:
        # Try primary processing method
        return external_service.process(data)
    except ServiceUnavailableError:
        logger.warning("External service unavailable, using fallback")
        return local_fallback_processor.process(data)
    except ValidationError as e:
        logger.error(f"Data validation failed: {e}")
        raise  # Don't fall back on validation errors
```

### Tool-Specific Workflows {#tool_specific_workflows}

**Workflow Template**:
```markdown
## Workflow: [Tool/Domain Specific Task]

### Prerequisites
- [Tool/dependency]: Version X.Y+
- [Environment]: Configuration requirements
- [Permissions]: Required access levels

### Input Requirements
- **Format**: [Expected input format]
- **Validation**: [How to verify input is valid]
- **Constraints**: [Size limits, type restrictions]

### Process Steps
1. **Validation**: Verify input meets requirements
2. **Preprocessing**: Prepare data for processing
3. **Execution**: Perform core operation
4. **Postprocessing**: Clean up and format output
5. **Verification**: Confirm successful completion

### Output Specification
- **Format**: [Output format]
- **Location**: [Where output is stored]
- **Metadata**: [Additional information provided]

### Error Scenarios
- **Error Type 1**: [How to handle]
- **Error Type 2**: [How to handle]

### Example
[Concrete example with commands/code]
```

**Example - Git File Tracking Workflow**:
```markdown
## Workflow: Track File Changes with Git

### Prerequisites
- Git 2.0+
- Repository initialized (.git directory exists)
- Write permissions to repository

### Input Requirements
- **Format**: File path (absolute or relative to repo root)
- **Validation**: File exists and is within repository
- **Constraints**: File size < 100MB (Git LFS for larger)

### Process Steps
1. **Validation**: Check file exists and is in repo
   ```bash
   test -f "$FILE_PATH" || exit 1
   git ls-files --error-unmatch "$FILE_PATH" 2>/dev/null
   ```

2. **Track Changes**: Add file to staging area
   ```bash
   git add "$FILE_PATH"
   ```

3. **Commit**: Create commit with descriptive message
   ```bash
   git commit -m "track: Add $FILE_PATH to version control"
   ```

4. **Verification**: Confirm file is tracked
   ```bash
   git ls-files | grep "$FILE_PATH"
   ```

### Output Specification
- **Format**: Commit SHA (40 character hex)
- **Location**: Git history (.git/objects/)
- **Metadata**: Author, timestamp, commit message

### Error Scenarios
- **File Not Found**: Exit with error, suggest creating file first
- **File Too Large**: Suggest Git LFS for files >100MB
- **Merge Conflict**: Resolve conflicts before committing
```

### Configuration Management {#configuration_management}

**Configuration Patterns**:
```python
# Example: Layered configuration pattern
from dataclasses import dataclass
from typing import Optional

@dataclass
class ToolConfig:
    """Configuration for specialized tool.

    Priority (highest to lowest):
    1. Environment variables
    2. Config file
    3. Default values
    """

    # Connection settings
    api_endpoint: str = "https://api.example.com"
    api_key: Optional[str] = None
    timeout_seconds: int = 30

    # Processing settings
    batch_size: int = 100
    max_retries: int = 3
    enable_caching: bool = True

    @classmethod
    def from_env(cls) -> "ToolConfig":
        """Load config from environment variables."""
        import os
        return cls(
            api_endpoint=os.getenv("API_ENDPOINT", cls.api_endpoint),
            api_key=os.getenv("API_KEY"),
            timeout_seconds=int(os.getenv("TIMEOUT", cls.timeout_seconds)),
            batch_size=int(os.getenv("BATCH_SIZE", cls.batch_size)),
            max_retries=int(os.getenv("MAX_RETRIES", cls.max_retries)),
            enable_caching=os.getenv("ENABLE_CACHE", "true").lower() == "true"
        )

    def validate(self) -> None:
        """Validate configuration values."""
        if not self.api_key:
            raise ValueError("API_KEY is required")
        if self.timeout_seconds < 1:
            raise ValueError("Timeout must be positive")
        if self.batch_size < 1:
            raise ValueError("Batch size must be positive")
```

**Configuration Documentation**:
```markdown
## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| API_ENDPOINT | No | https://api.example.com | API base URL |
| API_KEY | Yes | - | Authentication key |
| TIMEOUT | No | 30 | Request timeout in seconds |
| BATCH_SIZE | No | 100 | Items per batch |
| ENABLE_CACHE | No | true | Enable response caching |

### Configuration File

Location: `config/tool.json`

```json
{
  "api_endpoint": "https://api.example.com",
  "timeout_seconds": 30,
  "batch_size": 100,
  "enable_caching": true
}
```

### Validation

Configuration is validated on startup:
- API_KEY must be provided (via env or config)
- Timeout must be positive integer
- Batch size must be positive integer
```

### Specialized Testing {#specialized_testing}

**Domain-Specific Test Patterns**:
```python
# Example: Testing image processing
def test_image_resize_preserves_aspect_ratio():
    """Test that resize maintains original aspect ratio."""
    # Arrange
    input_image = create_test_image(800, 600)  # 4:3 aspect ratio

    # Act
    output_image = resize_image(input_image, width=400)

    # Assert
    assert output_image.width == 400
    assert output_image.height == 300  # Maintains 4:3 ratio
    assert calculate_aspect_ratio(output_image) == pytest.approx(4/3)

# Example: Testing API integration
@mock.patch('external_service.requests.Session')
def test_api_retry_on_failure(mock_session):
    """Test that API client retries on transient failures."""
    # Arrange: Fail twice, then succeed
    mock_session.get.side_effect = [
        requests.exceptions.Timeout(),
        requests.exceptions.Timeout(),
        mock_response(status_code=200, json={"data": "success"})
    ]

    # Act
    client = ExternalServiceClient(api_key="test")
    result = client.fetch_data("endpoint")

    # Assert
    assert result == {"data": "success"}
    assert mock_session.get.call_count == 3  # Retried twice
```

**Test Coverage for Specialized Logic**:
- Happy path: Tool works with valid inputs
- Edge cases: Boundary conditions (empty input, max size)
- Error handling: Invalid input, tool unavailable
- Integration: Tool interacts correctly with dependencies

### Performance Optimization {#performance_optimization}

**Domain-Specific Optimizations**:
```python
# Example: Batch processing optimization
def process_images_batch(images: list[Image], output_dir: Path) -> list[Path]:
    """Process images in batches for better performance.

    Performance optimizations:
    - Batch processing reduces overhead (single tool invocation)
    - Parallel processing with worker pool (CPU-bound)
    - Streaming to avoid loading all images in memory

    Benchmarks:
    - Sequential: 10 images/second
    - Batch (10 images): 50 images/second (5x improvement)
    - Parallel (4 workers): 150 images/second (15x improvement)
    """
    import concurrent.futures
    from itertools import batched

    output_paths = []

    # Process in batches of 10 with 4 workers
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        futures = []

        for batch in batched(images, 10):
            future = executor.submit(process_single_batch, batch, output_dir)
            futures.append(future)

        for future in concurrent.futures.as_completed(futures):
            output_paths.extend(future.result())

    return output_paths
```

**Caching Strategies**:
```python
# Example: Result caching for expensive operations
from functools import lru_cache
import hashlib

@lru_cache(maxsize=128)
def process_content(content: str, options: tuple) -> str:
    """Process content with caching.

    Caching strategy:
    - LRU cache (128 most recent results)
    - Cache key: hash of content + options
    - Cache invalidation: LRU eviction

    Performance:
    - Cache hit: <1ms
    - Cache miss: ~100ms (processing time)
    - Cache hit rate: 85% (typical workload)
    """
    # Expensive processing operation
    return expensive_processing(content, options)

# Usage
result = process_content("data", ("option1", "option2"))
```

## Anti-Patterns {#anti_patterns}

### Tight Coupling to External Services

```python
# ❌ WRONG - Direct dependency on external service
def process_data(data):
    result = external_api.process(data)  # Tightly coupled
    return result

# ✅ CORRECT - Abstraction with dependency injection
class DataProcessor:
    def __init__(self, processor: ProcessorInterface):
        self.processor = processor

    def process_data(self, data):
        return self.processor.process(data)

# Can inject ExternalAPIProcessor or LocalProcessor
processor = DataProcessor(ExternalAPIProcessor())
```

### Missing Error Context

```python
# ❌ WRONG - Generic error message
raise Exception("Processing failed")

# ✅ CORRECT - Specific error with context
raise ImageProcessingError(
    f"Failed to resize image {image_path}: "
    f"Invalid dimensions {width}x{height}. "
    f"Width and height must be positive integers."
)
```

### No Graceful Degradation

```python
# ❌ WRONG - Fail completely if external service unavailable
def generate_thumbnail(image):
    return external_service.thumbnail(image)  # Fails if service down

# ✅ CORRECT - Fallback to local processing
def generate_thumbnail(image):
    try:
        return external_service.thumbnail(image)
    except ServiceUnavailableError:
        logger.warning("External service unavailable, using local processing")
        return local_thumbnail_generator.create(image)
```

## Memory Routing {#memory_routing}

**Memory Categories**:
- **Domain Expertise**: Specialized knowledge and capabilities
- **Integration Patterns**: How to connect with other systems
- **Tool Configurations**: Setup and configuration details
- **Workflow Procedures**: Step-by-step processes

**Keywords**:
- specialized, domain, tool, integration, workflow
- configuration, setup, API, external service
- processing, transformation, validation
- batch, optimize, cache, performance

**File Paths**:
- Tool configs: `config/`, `.toolrc`, `tool.config.js`
- Integration: `integrations/`, `api/`, `clients/`
- Workflows: `workflows/`, `scripts/`, `automation/`

## Extension Points

Specialized agent templates can extend this base with:
- **Tool-Specific Commands**: ImageMagick commands, Git operations, API calls
- **Domain Logic**: Business rules, validation patterns, data transformations
- **Integration Details**: API endpoints, authentication methods, data formats
- **Workflow Automation**: Multi-step processes, error recovery, monitoring

## Versioning

**Current Version**: 1.0.0

**Changelog**:
- **1.0.0** (2025-11-30): Initial base specialized template with patterns for domain-specific agents

---

**Maintainer**: Claude MPM Team
**Last Updated**: 2025-11-30
**Status**: ✅ Active
