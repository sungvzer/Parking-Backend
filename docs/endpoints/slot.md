# Slot endpoint

## Description
Query a certain parking slot and the eventual car parked there.

## URL endpoint
`/slot`

## Method
GET

## Arguments
- `auth_key`: The authentication key obtained via the [/authenticate](./authenticate.md) endpoint.
- `number`: The parking slot that needs to be queried.

## Usage example
```
/slot?auth_key=92fdb80ac10&number=0
```

## Response HTTP codes
- 200: Successful request
- 400: Malformed request, missing a required argument or more, or the parking slot is outside the existing bounds (e.g. a negative slot, or one that's bigger than the size of the parking)
- 401: Bad authentication

## Response body
A json object containing either information about the parking slot, if it's empty or not, and the license plate parked in there:
```json
{
    "license_plate": "",
    "slot_number": 2,
    "is_empty": true
}
```

Or a description about the error:

```json
{
    "description": "Invalid slot number"
}
```
