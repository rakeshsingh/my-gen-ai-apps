# Tests for GenAI Apps Helper Modules

This directory contains comprehensive unit tests for all helper modules in the `helpers/` folder.

## Test Coverage

The following modules are tested:

1. **test_config_handler.py** - Tests for configuration file handling
2. **test_docs_db_handler.py** - Tests for document database operations
3. **test_llm_handler.py** - Tests for LangChain chain setup and management
4. **test_tools.py** - Tests for custom tools (math, search, retriever)
5. **test_retriever.py** - Tests for document retrieval functionality
6. **test_session_handler.py** - Tests for chat session management
7. **test_rag.py** - Tests for RAG (Retrieval-Augmented Generation) operations
8. **test_indexer.py** - Tests for document indexing and vector store setup

## Running Tests

### Run All Tests
```bash
cd tests
python run_tests.py
```

### Run Specific Test Module
```bash
cd tests
python run_tests.py config_handler
```

### Run Individual Test Files
```bash
cd tests
python -m unittest test_config_handler.py
python -m unittest test_docs_db_handler.py
# ... etc
```

### Run with Coverage
```bash
cd tests
coverage run --source=../helpers -m unittest discover
coverage report
coverage html  # Generates HTML coverage report
```

## Test Structure

Each test file follows the same structure:
- **setUp()** method to initialize test fixtures
- Individual test methods for each function/method
- Mock objects to isolate units under test
- Edge case and error condition testing
- Comprehensive assertions to verify expected behavior

## Key Testing Features

- **Mocking**: Extensive use of `unittest.mock` to isolate components
- **File System Mocking**: Mock file operations to avoid actual file I/O
- **Configuration Mocking**: Mock configuration reading for different scenarios
- **Error Testing**: Test error conditions and exception handling
- **Edge Cases**: Test boundary conditions and unusual inputs

## Dependencies

The tests require the following packages (install with `pip install -r test_requirements.txt`):
- unittest (built-in)
- unittest.mock (built-in)
- coverage (for coverage reporting)
- pytest (alternative test runner)

## Test Data

Tests use mock data and fixtures to simulate:
- Configuration files with various settings
- Document collections and chunks
- Vector stores and retrievers
- Chat sessions and message histories
- Tool responses and embeddings

## Continuous Integration

These tests are designed to run in CI/CD pipelines and provide:
- Clear pass/fail status
- Detailed error messages
- Coverage reporting
- Isolated test execution (no external dependencies)

## Contributing

When adding new functionality to helper modules:
1. Add corresponding test methods
2. Maintain test coverage above 80%
3. Test both success and failure scenarios
4. Use descriptive test method names
5. Add docstrings explaining test purpose
