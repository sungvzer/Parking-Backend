# Parking API
## Running the back-end server
There are a few requirements to run this application:
- [Python 3.9.6 or newer](https://www.python.org/downloads/)
- [Flask 2.0.1 or newer](https://pypi.org/project/Flask/)
- [Flask-RESTful 0.3.9 or newer](https://pypi.org/project/Flask-RESTful/)
- [python-dotenv 0.19.0 or newer](https://pypi.org/project/python-dotenv/)

After installing the necessary packages, just run `script.py`, having the root of this repository as current directory in the terminal.

Something like this: 

`~/drop_backend/ $ python3 ./script.py`

## Accessing the API
### Running the server
By default, the server will run on the local machine, and will be accessible via localhost, default port being 5000.

Should any of this information change, there will be a message right when the script starts, containing the correct address and port to connect to.

### Authenticating
At the moment every action on the API needs authentication, which can be achieved with a POST request to the [/authenticate](./docs/endpoints/authenticate.md) endpoint.

To make life a bit easier, the `authenticate.ps1` script will print out the current key to use with the server. It needs to run under PowerShell.

To authenticate a GET request to the API, just add an `auth_key` argument, and include the authentication key. For example:

```
http://127.0.0.1:5000/park?auth_key=AUTH_KEY...
```

### API Endpoints
The following list contains all the endpoints API endpoints and their relative HTTP method expected to be used.

| Name                                             | Link endpoint   | Description                                   |  Method  |
| ------------------------------------------------ | :-------------: | :-------------------------------------------: | --------:|
| [Park](./docs/endpoints/park.md)                 | `/park`         | Add a license plate to the parking            | GET      |
| [Unpark](./docs/endpoints/unpark.md)             | `/unpark`       | Remove a license plate from the parking       | GET      |
| [Slot](./docs/endpoints/slot.md)                 | `/slot`         | Query a certain slot in the parking           | GET      |
| [Authenticate](./docs/endpoints/authenticate.md) | `/authenticate` | Retrieve an authentication key to use the API | POST     |
