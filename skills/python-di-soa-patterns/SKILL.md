---
name: python-di-soa-patterns
description: DI/SOA decision tree with full code examples for Python architecture decisions
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Decision tree and code examples for choosing between DI/SOA and lightweight script patterns in Python"
    when_to_use: "When deciding on architecture patterns for a new Python project or module"
    quick_start: "Use the decision tree to determine if DI/SOA or lightweight patterns fit your use case"
context_limit: 700
tags:
  - python
  - architecture
  - dependency-injection
  - service-oriented
  - design-patterns
  - decision-tree
requires_tools: []
---

# When to Use DI/SOA vs Simple Scripts

## Use DI/SOA Pattern (Service-Oriented Architecture) For:
- **Web Applications**: Flask/FastAPI apps with multiple routes and services
- **Background Workers**: Celery tasks, async workers processing queues
- **Microservices**: Services with API endpoints and business logic
- **Data Pipelines**: ETL with multiple stages, transformations, and validations
- **CLI Tools with Complexity**: Multi-command CLIs with shared state and configuration
- **Systems with External Dependencies**: Apps requiring mock testing (databases, APIs, caches)
- **Domain-Driven Design**: Applications with complex business rules and aggregates

**Benefits**: Testability (mock dependencies), maintainability (clear separation), extensibility (swap implementations)

## Skip DI/SOA (Keep It Simple) For:
- **One-Off Scripts**: Data migration scripts, batch processing, ad-hoc analysis
- **Simple CLI Tools**: Single-purpose utilities without shared state
- **Jupyter Notebooks**: Exploratory analysis and prototyping
- **Configuration Files**: Environment setup, deployment scripts
- **Glue Code**: Simple wrappers connecting two systems
- **Proof of Concepts**: Quick prototypes to validate ideas

**Benefits**: Less boilerplate, faster development, easier to understand

## Decision Tree
```
Is this a long-lived service or multi-step process?
  YES -> Use DI/SOA (testability, maintainability matter)
  NO |

Does it need mock testing or swappable dependencies?
  YES -> Use DI/SOA (dependency injection enables testing)
  NO |

Is it a one-off script or simple automation?
  YES -> Skip DI/SOA (keep it simple, minimize boilerplate)
  NO |

Will it grow in complexity over time?
  YES -> Use DI/SOA (invest in architecture upfront)
  NO -> Skip DI/SOA (don't over-engineer)
```

## Example: When NOT to Use DI/SOA

**Lightweight Script Pattern**:
```python
# Simple CSV processing script - NO DI needed
import pandas as pd
from pathlib import Path

def process_sales_data(input_path: Path, output_path: Path) -> None:
    """Process sales CSV and generate summary report.
    
    This is a one-off script, so we skip DI/SOA patterns.
    No need for IFileReader interface or dependency injection.
    """
    # Read CSV directly - no repository pattern needed
    df = pd.read_csv(input_path)
    
    # Transform data
    df['total'] = df['quantity'] * df['price']
    summary = df.groupby('category').agg({
        'total': 'sum',
        'quantity': 'sum'
    }).reset_index()
    
    # Write output directly - no abstraction needed
    summary.to_csv(output_path, index=False)
    print(f"Summary saved to {output_path}")

if __name__ == "__main__":
    process_sales_data(
        Path("data/sales.csv"),
        Path("data/summary.csv")
    )
```

**Same Task with Unnecessary DI/SOA (Over-Engineering)**:
```python
# DON'T DO THIS for simple scripts!
from abc import ABC, abstractmethod
from dataclasses import dataclass
import pandas as pd
from pathlib import Path

class IDataReader(ABC):
    @abstractmethod
    def read(self, path: Path) -> pd.DataFrame: ...

class IDataWriter(ABC):
    @abstractmethod
    def write(self, df: pd.DataFrame, path: Path) -> None: ...

class CSVReader(IDataReader):
    def read(self, path: Path) -> pd.DataFrame:
        return pd.read_csv(path)

class CSVWriter(IDataWriter):
    def write(self, df: pd.DataFrame, path: Path) -> None:
        df.to_csv(path, index=False)

@dataclass
class SalesProcessor:
    reader: IDataReader
    writer: IDataWriter
    
    def process(self, input_path: Path, output_path: Path) -> None:
        df = self.reader.read(input_path)
        df['total'] = df['quantity'] * df['price']
        summary = df.groupby('category').agg({
            'total': 'sum',
            'quantity': 'sum'
        }).reset_index()
        self.writer.write(summary, output_path)

# Too much boilerplate for a simple script!
if __name__ == "__main__":
    processor = SalesProcessor(
        reader=CSVReader(),
        writer=CSVWriter()
    )
    processor.process(
        Path("data/sales.csv"),
        Path("data/summary.csv")
    )
```

**Key Principle**: Use DI/SOA when you need testability, maintainability, or extensibility. For simple scripts, direct calls and minimal abstraction are perfectly fine.
