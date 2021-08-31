$body = @{
    username = 'admin'
    password = 'AdminPassword'
}

$authenticationResponse = Invoke-WebRequest '127.0.0.1:5000/authenticate' -Body $body -Method 'POST'

$authenticationKey = $authenticationResponse.Content

"Logged in, authentication key is:"
$($authenticationKey|ConvertFrom-Json).key
