# Kairix Todo API

A FastAPI-based todo list application with tags, reminders, and optimized full-text search using SQLite FTS5.

## Features

- Task management with titles, due dates, and additional details
- Tag system for categorizing tasks
- Reminder system for task notifications
- Advanced full-text search using SQLite FTS5
- Optimized database performance

## Search API

The search API provides powerful full-text search capabilities for tasks using SQLite's FTS5 extension. It supports:

- Simple text search with query parameters
- Advanced search with filtering, sorting, and pagination
- Relevance scoring based on BM25 algorithm
- Field-specific searching (title, additional details, or both)
- Different match modes (all, phrase, token)

### Quick Search

For simple searches, use the `GET /tasks/search` endpoint:

```
GET /tasks/search?q=project&skip=0&limit=10
```

Parameters:
- `q`: Search query text
- `skip`: Number of records to skip (for pagination)
- `limit`: Maximum number of records to return

### Advanced Search

For more complex searches, use the `POST /tasks/search` endpoint:

```json
POST /tasks/search
{
  "query": "project meeting",
  "match_mode": "phrase",
  "search_fields": ["title"],
  "filters": {
    "tags": ["Work", "Important"],
    "tags_operator": "AND",
    "completed": false,
    "due_date_from": "2025-04-01",
    "due_date_to": "2025-04-30",
    "has_reminders": true
  },
  "skip": 0,
  "limit": 20,
  "sort_by": "relevance",
  "sort_order": "desc",
  "include_relevance_scores": true
}
```

Parameters:
- `query`: Full-text search query
- `match_mode`: Search match mode (all, phrase, token)
- `search_fields`: Fields to search in (title, additional_details, both)
- `filters`: Complex filtering options
  - `tags`: Filter by tag names
  - `tags_operator`: Logical operator for tag filtering (AND, OR)
  - `completed`: Filter by completion status
  - `due_date_from`: Filter tasks due on or after this date
  - `due_date_to`: Filter tasks due on or before this date
  - `created_after`: Filter tasks created after this timestamp
  - `has_reminders`: Filter tasks that have reminders
  - `upcoming_reminder_days`: Filter tasks with reminders in the next X days
- `skip`: Number of records to skip (for pagination)
- `limit`: Maximum number of records to return
- `sort_by`: Field to sort by (relevance, due_date, created_at, title)
- `sort_order`: Sort order (asc, desc)
- `include_relevance_scores`: Whether to include relevance scores in the response

### Search Syntax Help

To get help with the search syntax, use the `GET /tasks/search/syntax-help` endpoint:

```
GET /tasks/search/syntax-help
```

This returns documentation about the supported search syntax, including examples and operator descriptions.

## Database Optimization

The API includes endpoints for database maintenance and optimization:

### Optimize Database

To optimize the database for better performance, use the `POST /database/optimize` endpoint:

```
POST /database/optimize
```

This performs several optimizations:
- Rebuilds and optimizes the FTS5 index
- Vacuums the database to reclaim space
- Analyzes tables for query optimization

### Database Statistics

To get statistics about the database, use the `GET /database/stats` endpoint:

```
GET /database/stats
```

This returns information about:
- Database size
- Table counts
- FTS index consistency
- Other database metrics

## Development

### Prerequisites

- Python 3.9 or higher
- Poetry (for dependency management)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/kairix-todo.git
   cd kairix-todo
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

### Running the Application

To run the development server:

```bash
poetry run poe dev
```

To run the production server:

```bash
poetry run poe prod
```

### Testing

To run the tests:

```bash
poetry run poe test
```

To run linting and formatting:

```bash
poetry run poe format  # Auto-fixes formatting issues
poetry run poe lint    # Checks code quality without modifying
```

To run type checking:

```bash
poetry run poe typecheck
```

To run comprehensive checks (lint + test):

```bash
poetry run poe check
```

## API Documentation

For detailed API documentation, see the OpenAPI specification in `openapi.json`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
