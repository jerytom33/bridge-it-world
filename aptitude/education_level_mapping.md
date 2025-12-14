# Education Level Mapping Reference

This document defines the standardized education level values used across the Bridge It World platform.

## Standardized API Values

The backend API accepts the following education level values:

| API Value | Display Name | Description |
|-----------|--------------|-------------|
| `10th` | 10th Standard | SSLC / Secondary School Completed |
| `12th` | 12th Standard | Higher Secondary / Pre-University Completed |
| `Diploma` | Diploma / Polytechnic | Diploma / Vocational Training Completed |
| `Bachelor` | Bachelor's Degree | Undergraduate Degree Completed |
| `Master` | Master's Degree | Post-Graduate / Master's Completed |

## API Endpoints

### Get Personalized Questions

**Endpoint**: `GET /api/aptitude/personalized-questions/`

**Query Parameters**:
- `level` (string, required): Education level - must be one of: `10th`, `12th`, `Diploma`, `Bachelor`, `Master`
- `count` (integer, optional): Number of questions (default: 10, max: 25)

**Example Request**:
```bash
GET /api/aptitude/personalized-questions/?level=Bachelor&count=10
```

**Success Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "questions": [...],
    "education_level": "Bachelor",
    "level_display_name": "Bachelor's Degree",
    "total_questions": 10
  }
}
```

**Error Response - Invalid Level** (400 Bad Request):
```json
{
  "error": "Invalid education level: Bachelors",
  "valid_levels": ["10th", "12th", "Diploma", "Bachelor", "Master"],
  "message": "Please use one of: 10th, 12th, Diploma, Bachelor, Master"
}
```

## Validation Rules

### Backend (Django)

The backend strictly validates education levels in `aptitude/views.py`:

```python
VALID_LEVELS = ['10th', '12th', 'Diploma', 'Bachelor', 'Master']
```

**Important Notes**:
- Values are **case-sensitive**
- Plural forms (`Bachelors`, `Masters`) are **rejected**
- Alternative names (`Degree`, `UG`, `PG`) are **rejected**
- Invalid values return `400 Bad Request` with helpful error message

### Frontend (Flutter)

The Flutter app should send the exact API values listed above:

```dart
// ✓ CORRECT
final level = 'Bachelor';  
final level = 'Master';

// ✗ INCORRECT  
final level = 'Bachelors';  // Will be rejected
final level = 'Masters';    // Will be rejected
final level = 'Degree';     // Will be rejected
```

## Question Difficulty by Level

The AI generates questions with different difficulty distributions for each level:

| Level | Easy | Medium | Hard | Content Focus |
|-------|------|--------|------|---------------|
| 10th | 60% | 30% | 10% | Fundamental concepts, age-appropriate for 15-16 year olds |
| 12th | 30% | 50% | 20% | Pre-university, competitive exam preparation |
| Diploma | 25% | 50% | 25% | Technical/vocational, practical problem-solving |
| Bachelor | 20% | 40% | 40% | Undergraduate analytical thinking |
| Master | 10% | 30% | 60% | Advanced postgraduate critical thinking |

## Migration Notes

### Breaking Changes

If the system previously used plural forms:
- `Bachelors` → `Bachelor` ✓
- `Masters` → `Master` ✓

**Action Required**: Update all Flutter API calls to use singular forms.

### Backward Compatibility

**Not supported**. The backend will reject old plural forms with a clear error message.

## Testing

### Valid Requests
```bash
# All of these should work
curl "http://localhost:8000/api/aptitude/personalized-questions/?level=10th&count=5"
curl "http://localhost:8000/api/aptitude/personalized-questions/?level=12th&count=5"
curl "http://localhost:8000/api/aptitude/personalized-questions/?level=Diploma&count=5"
curl "http://localhost:8000/api/aptitude/personalized-questions/?level=Bachelor&count=5"
curl "http://localhost:8000/api/aptitude/personalized-questions/?level=Master&count=5"
```

### Invalid Requests (Should return 400)
```bash
# These will fail validation
curl "http://localhost:8000/api/aptitude/personalized-questions/?level=Bachelors&count=5"
curl "http://localhost:8000/api/aptitude/personalized-questions/?level=Masters&count=5"
curl "http://localhost:8000/api/aptitude/personalized-questions/?level=UG&count=5"
```

## Logging

The backend logs all aptitude test requests for debugging:

```
INFO: Generating 10 questions for Bachelor's Degree (user: john@example.com)
INFO: Successfully generated 10 questions for Bachelor level (user: john@example.com)
```

Invalid requests are logged as warnings:
```
WARNING: Invalid education level requested: 'Bachelors' (user: john@example.com)
```

---

**Last Updated**: 2025-12-14  
**Version**: 1.0  
**Maintained By**: Backend Team
