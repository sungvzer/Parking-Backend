# Park endpoint

## Description
Adds a license plate to the first available slot.

## URL endpoint
`/park`

## Method
GET

## Arguments
- `auth_key`: The authentication key obtained via the [/authenticate](./authenticate.md) endpoint.
- `license_plate`: The car's license plate that needs to be parked.

## Usage example
```
/park?auth_key=92fdb80ac10&license_plate=LP1
```

## Response HTTP codes
- 200: Successful request
- 400: Malformed request, missing a required argument or more
- 401: Bad authentication
- 403: Car is already parked in another slot
- 404: No empty slot found

## Response body
A json object containing either information about the parking slot and the license plate parked in there:
```json
{
    "license_plate": "AC201BD",
    "slot": 21
}
```

Or a description about the error:

```json
{
    "description": "Car with license plate AC201BD is already parked in slot 21"
}
```
