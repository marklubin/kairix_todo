# Simplified Search Feature Design

## Problem Statement

The current implementation of search in the Kairix Todo application uses SQLite's FTS5 (Full-Text Search) functionality, which is causing test failures and adding unnecessary complexity. We need a simpler approach that still provides the core functionality of searching tasks and filtering by various criteria.

## Goals

1. Simplify the search implementation by removing FTS5 dependency
2. Maintain core search functionality (text search, filtering by tags, dates, completion status)
3. Ensure good performance through appropriate indexing
4. Create a clean, intuitive API
5. Ensure thorough test coverage

## Non-Goals

1. Advanced text search features like relevance scoring, phrase matching, etc.
2. Complex query syntax support

## Simplified Approach

Instead of using SQLite's FTS5, we'll implement search using standard SQLAlchemy queries with `LIKE`/`ILIKE` operators for text search. This approach is:

- Simpler to implement and maintain
- More straightforward to test
- Sufficient for the needs of a todo application

## API Design

### Endpoint

```
GET /tasks/search
```

### Query Parameters

| Parameter  | Type                | Description                                      | Example                |
|------------|---------------------|--------------------------------------------------|------------------------|
| q          | string (optional)   | Text to search in title and additional details   | ?q=meeting             |
| tags       | string (optional)   | Comma-separated list of tag names                | ?tags=work,important   |
| from_date  | date (optional)     | Filter tasks due on or after this date           | ?from_date=2023-04-15  |
| to_date    | date (optional)     | Filter tasks due on or before this date          | ?to_date=2023-04-30    |
| completed  | boolean (optional)  | Filter by completion status                      | ?completed=true        |
| limit      | integer (optional)  | Maximum number of results to return              | ?limit=20              |
| offset     | integer (optional)  | Number of results to skip (for pagination)       | ?offset=20             |

### Response Format

```json
{
  "tasks": [
    {
      "id": "uuid",
      "title": "Task title",
      "completed": false,
      "due_date": "2023-04-15",
      "additional_details": "Details here",
      "tags": [
        {
          "id": "uuid",
          "name": "important"
        },
        {
          "id": "uuid",
          "name": "work"
        }
      ]
    }
  ],
  "count": 1,
  "total": 10
}
```

## Implementation Details

### Database Indexes

To ensure good performance, we'll add the following indexes to the Task model:

```python
__table_args__ = (
    Index('idx_task_title', 'title'),
    Index('idx_task_due_date', 'due_date'),
    Index('idx_task_completed', 'completed'),
)
```

### Search Function

The core search function will be implemented in `src/kairix_todo/utils/search_utils.py`:

```python
def search_tasks(
    session, 
    query=None, 
    tags=None, 
    from_date=None, 
    to_date=None, 
    completed=None,
    limit=100,
    offset=0
):
    """Search for tasks with various filters.
    
    Args:
        session: SQLAlchemy database session
        query: Text to search in title and additional details
        tags: List of tag names to filter by
        from_date: Filter tasks due on or after this date
        to_date: Filter tasks due on or before this date
        completed: Filter by completion status
        limit: Maximum number of results to return
        offset: Number of results to skip
        
    Returns:
        Tuple of (tasks, total_count)
    """
    task_query = session.query(Task)
    
    # Text search
    if query:
        task_query = task_query.filter(
            or_(
                Task.title.ilike(f"%{query}%"),
                Task.additional_details.ilike(f"%{query}%")
            )
        )
    
    # Tag filtering
    if tags:
        for tag in tags:
            task_query = task_query.filter(Task.tags.any(Tag.name == tag))
    
    # Date filtering
    if from_date:
        task_query = task_query.filter(Task.due_date >= from_date)
    if to_date:
        task_query = task_query.filter(Task.due_date <= to_date)
    
    # Completion status
    if completed is not None:
        task_query = task_query.filter(Task.completed == completed)
    
    # Get total count before pagination
    total_count = task_query.count()
    
    # Apply pagination
    tasks = task_query.limit(limit).offset(offset).all()
    
    return tasks, total_count
```

### Controller Implementation

The search controller will be implemented in `src/kairix_todo/controller/search_controller.py`:

```python
@blueprint.route('/search', methods=['GET'])
def search():
    """Search for tasks with various filters."""
    # Parse query parameters
    query = request.args.get('q')
    
    tags = request.args.get('tags')
    if tags:
        tags = tags.split(',')
    
    from_date = request.args.get('from_date')
    if from_date:
        from_date = date.fromisoformat(from_date)
    
    to_date = request.args.get('to_date')
    if to_date:
        to_date = date.fromisoformat(to_date)
    
    completed = request.args.get('completed')
    if completed is not None:
        completed = completed.lower() == 'true'
    
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    # Execute search
    tasks, total = search_tasks(
        session, 
        query=query, 
        tags=tags, 
        from_date=from_date, 
        to_date=to_date, 
        completed=completed,
        limit=limit,
        offset=offset
    )
    
    # Format response
    return jsonify({
        'tasks': [task.to_dict() for task in tasks],
        'count': len(tasks),
        'total': total
    })
```

## Testing Strategy

We'll create comprehensive tests for the search functionality:

1. **Unit Tests**: Test the `search_tasks` function with various combinations of parameters
2. **Integration Tests**: Test the search endpoint with HTTP requests
3. **Edge Cases**: Test with empty results, large result sets, special characters in search terms, etc.

### Test Cases

1. Basic text search
2. Filtering by tags
3. Filtering by date range
4. Filtering by completion status
5. Combining multiple filters
6. Pagination
7. Edge cases (empty results, special characters, etc.)

## Migration Plan

1. Remove FTS-specific code and tests
2. Implement the simplified search functionality
3. Update the API documentation
4. Run tests to ensure everything works as expected

## Performance Considerations

For a typical todo application with hundreds or even a few thousand tasks, the simplified approach with proper indexes will be perfectly adequate. If performance becomes an issue in the future, we can consider more advanced solutions.
