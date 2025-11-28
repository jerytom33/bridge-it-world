# Flutter API Service Changes Needed

Based on the current Django backend implementation, here are the changes needed for your Flutter API service:

## 1. Endpoint URL Updates

Update the base URL constants to match the correct API endpoints:

```dart
// Change profile setup URL from:
'profile/setup/'

// To:
'auth/profile/'
```

## 2. Response Data Structure Fixes

### Register Method
The current UserSignupView returns:
```json
{
  "email": "user@example.com",
  "first_name": "First",
  "last_name": "Last"
}
```

Not the expected structure with tokens. You'll need to login separately after registration.

### Login Method
The current LoginView returns:
```json
{
  "success": true,
  "token": "access_token",
  "refresh": "refresh_token",
  "user_id": 1
}
```

Update your Flutter code to match this structure:
```dart
// Change from:
data['access']
data['user']['id']

// To:
data['token']
data['user_id']
```

### Profile Methods
Added new endpoint `auth/profile/` that supports both GET and PUT methods:
- GET: Retrieve current user's profile
- PUT: Update current user's profile

## 3. Specific Code Changes Needed

### Update Login Method:
```dart
Future<Map<String, dynamic>> login({
  required String email,
  required String password,
}) async {
  try {
    final response = await _dio.post(
      'auth/login/',
      data: {
        'email': email,
        'password': password,
      },
    );

    // Save auth data if login successful
    if (response.statusCode == 200) {
      final data = response.data;
      await AuthService.saveAuthData(
        data['token'], // Changed from data['access']
        data['refresh'],
        data['user_id'].toString(), // Changed from data['user']['id']
      );
    }

    return {'success': true, 'data': response.data};
  } on DioException catch (e) {
    final errorMsg = (e.response?.data is Map)
        ? (e.response?.data['error'] ?? e.response?.data['detail'] ?? 'Login failed')
        : 'Unexpected error: ${e.message}';
    return {'success': false, 'error': errorMsg};
  }
}
```

### Update Setup Profile Method:
```dart
Future<Map<String, dynamic>> setupProfile(
    Map<String, dynamic> profileData) async {
  try {
    final response = await _dio.put('auth/profile/', data: profileData); // Changed to PUT and updated URL
    return {'success': true, 'data': response.data};
  } on DioException catch (e) {
    final errorMsg = (e.response?.data is Map)
        ? (e.response?.data['detail'] ?? 'Failed to setup profile')
        : 'Unexpected error: ${e.message} (Check if URL exists)';
    return {'success': false, 'error': errorMsg};
  }
}
```

### Add Get Profile Method:
```dart
Future<Map<String, dynamic>> getProfile() async {
  try {
    final response = await _dio.get('auth/profile/');
    return {'success': true, 'data': response.data['data']}; // Extract data from response
  } on DioException catch (e) {
    final errorMsg = (e.response?.data is Map)
        ? (e.response?.data['detail'] ?? 'Failed to fetch profile')
        : 'Unexpected error: ${e.message}';
    return {'success': false, 'error': errorMsg};
  }
}
```

## 4. Error Handling Improvements

Update all error handling to check for both 'error' and 'detail' keys in the response:

```dart
final errorMsg = (e.response?.data is Map)
    ? (e.response?.data['error'] ?? e.response?.data['detail'] ?? 'Operation failed')
    : 'Unexpected error: ${e.message}';
```

These changes will ensure your Flutter app works correctly with the current Django backend implementation.