# Authenticate endpoint

## Description
Retrieve an authentication key to be used with all other endpoints.
Valid credentials are hard-coded at the moment, and they are
`admin:AdminPassword`.

## URL endpoint
`/authenticate`

## Method
POST with form data

## Arguments
All of them need to be included in form data
- `username`: Identifying the current user that needs to authenticate
- `password`: Password relative to the username

## Response HTTP codes
- 200: Successful authentication
- 400: Malformed request, missing username or password
- 401: Unauthorized username or wrong password

## Response body
A json object containing either the authentication key:
```json
{
    "description": "success",
    "key": "5e8c7c4ef23964b4a5d1fa3349968db5b1adcfc68c31eb65c50ef573077257c1"
}
```

Or a description about the error:

```json
{
    "description": "no username provided"
}
```
