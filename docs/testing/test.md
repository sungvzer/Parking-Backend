# Testing
This API uses the [pytest](https://pypi.org/project/pytest/) library to test its functionality.

Currently, `server_test.py` is the file containing all testing functionality.

To run tests just run this command in the repository root.
It will automatically find and execute all tests.
```
pytest
```

I actually suggest running the command with the following parameters:
```
pytest -rP -v
```

so it will automatically print all _stdout_ text emitted during tests, the `-v` parameters makes the pytest output verbose. 

This is just personal preference, though.
