# Unpark endpoint

## Description
Remove a license plate from the parking slot.

## URL endpoint
`/unpark`

## Method
GET

## Arguments
- `auth_key`: The authentication key obtained via the [/authenticate](./authenticate.md) endpoint.
- `license_plate`: The license plate to be removed.

## Usage example
```
/unpark?auth_key=92fdb80ac10&license_plate=LP1
```

## Response HTTP codes
- 200: Successful request
- 400: Malformed request, missing a required argument or more
- 401: Bad authentication
- 404: No car with that license plate was found

## Response body
A json object containing either information about the parking slot, and the license plate removed from there:
```json
{
    "license_plate": "CG402PO",
    "slot_number": 0
}
```

Or a description about the error:

```json
{
    "description": "No car with this license plate is parked here"
}
```
