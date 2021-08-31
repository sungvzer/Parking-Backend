$body = @{
    username = 'admin'
    password = 'AdminPassword'
}

$authenticationResponse = Invoke-WebRequest '127.0.0.1:5000/authenticate' -Body $($body|ConvertTo-Json) -ContentType 'application/json' -Method 'POST'

$authenticationKey = $authenticationResponse.Content

"Logged in, authentication key is:"
$($authenticationKey|ConvertFrom-Json).key
