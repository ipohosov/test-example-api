# JSONPlaceholder API Testing Suite

This repository contains automated test cases for the JSONPlaceholder API (https://jsonplaceholder.typicode.com/), a fake REST API for testing and prototyping.

## API Overview

JSONPlaceholder provides the following endpoints:
- `/posts` - Blog posts
- `/users` - User information
- `/comments` - Comments on posts
- `/albums` - Photo albums
- `/photos` - Photos in albums

## Test Cases

| Test Case | Method | Endpoint | Description | Validation Used | Reason of test                                                                                               |
|-----------|---------|----------|-------------|-----------------|--------------------------------------------------------------------------------------------------------------|
| **test_get_all_resources_count** | GET | `/posts`, `/users`, `/comments`, `/albums`, `/photos` | Tests retrieving all resources and validates count | Status code (200), response time (<2s), content-type (JSON), data type (list), count validation | The test validates that the basic endpoints work and return the response fast.                               |
| **test_get_specific_post** | GET | `/posts/{id}` | Tests retrieving specific posts with valid/invalid IDs | Status code (200/404), data structure, field presence, data types, value validation | The test validates posts enpoint with positive and negative scenarious                                       |
| **test_get_specific_user** | GET | `/users/{id}` | Tests retrieving specific users with valid/invalid IDs | Status code (200/404), nested object structure, email format, required fields | The test validates users enpoint with positive and negative scenarious                                       |
| **test_create_post** | POST | `/posts` | Tests creating new posts with various data combinations | Status code (201), response structure, data reflection, ID generation | The test validates new post creation                                                                         |                                                                            
| **test_update_post** | PUT | `/posts/{id}` | Tests updating existing posts | Status code (200), data updates, partial updates | The test validates post update                                                                               |  
| **test_delete_post** | DELETE | `/posts/{id}` | Tests deleting posts | Status code (200), successful deletion | The test validates post removal                                                                              | 
| **test_headers_validation** | GET | `/posts` | Tests HTTP headers validation | Content-type, CORS headers, cache headers | The test validates headers of posts endpoint. Posts endpoint is used as example to validate default headers. |
| **test_pagination_and_filtering** | GET | `/posts` with query params | Tests pagination, filtering, and sorting | Limit functionality, filter accuracy, sort order | Test validates pagination and filters.                                                                       |


## Running the Tests

### Prerequisites
```bash
pip install -r requirements.txt
```

### Execute Tests
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run with HTML report
pytest --html=report.html --self-contained-html

# Run specific test class
pytest test_jsonplaceholder.py::TestJSONPlaceholderAPI

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_get_specific"
```

### Test Categories

#### **Positive Tests** (Happy Path)
- Valid resource retrieval
- Successful data creation
- Proper data updates
- Expected response formats

#### **Negative Tests** (Error Handling)
- Invalid resource IDs
- Non-existent endpoints
- Malformed requests

#### **Performance Tests**
- Response time validation
- Load testing capabilities

#### **Integration Tests**
- End-to-end workflow validation
- Cross-endpoint data consistency

## Test Configuration

The test suite uses pytest fixtures for:
- **Base URL**: Centralized API endpoint configuration
- **Session**: HTTP session management for connection reuse
- **Test Data**: Predefined data structures for consistent testing
- **Expected Keys**: Schema validation helpers

## API Testing Best Practices Implemented

1. **Separation of Concerns**: Each test focuses on specific functionality
2. **Data-Driven Testing**: Parametrized tests for comprehensive coverage
3. **Fixture Usage**: Reusable test components
4. **Clear Assertions**: Descriptive error messages
5. **Performance Monitoring**: Response time tracking
6. **Header Validation**: HTTP compliance checking
7. **Error Handling**: Negative test scenarios
8. **Schema Validation**: Data structure verification

## Coverage Areas

- ✅ GET operations (retrieve resources)
- ✅ POST operations (create resources)
- ✅ PUT operations (update resources)
- ✅ DELETE operations (remove resources)
- ✅ Error handling (404, invalid data)
- ✅ Performance testing (response times)
- ✅ Data validation (types, structure)
- ✅ HTTP headers verification
- ✅ Query parameters (filtering, sorting, pagination)

## Execution example
![execution.gif](execution.gif)