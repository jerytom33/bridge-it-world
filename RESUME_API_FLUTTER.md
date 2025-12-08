# Resume Analyzer API - Flutter Integration Guide

**Base URL**: `http://0.0.0.0:8000` (Development) / `https://your-domain.com` (Production)

---

## Authentication

All endpoints require JWT authentication. Include the access token in the Authorization header.

```dart
// Add to your HTTP headers
final headers = {
  'Authorization': 'Bearer $accessToken',
  'Content-Type': 'multipart/form-data', // For file uploads
};
```

---

## Endpoints

### 1. Upload Resume

Upload and analyze a PDF resume.

#### Endpoint
```
POST /api/resume/upload/
```

#### Headers
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

#### Request Body
```dart
// Form data with PDF file
FormData formData = FormData.fromMap({
  'pdf_file': await MultipartFile.fromFile(
    filePath,
    filename: 'resume.pdf',
  ),
});
```

#### Response (200 OK)
```json
{
  "id": 1,
  "user": 5,
  "pdf_file": "http://0.0.0.0:8000/media/resumes/resume.pdf",
  "created_at": "2025-12-07T10:30:00Z",
  
  // Gemini AI Analysis
  "gemini_response": {
    "suitable_career_paths": ["Software Developer", "Data Analyst"],
    "skill_gaps": ["Cloud Computing", "DevOps"],
    "recommended_courses": ["AWS Certification", "Docker & Kubernetes"],
    "suggested_next_steps": ["Build portfolio projects", "Get certified"],
    "overall_summary": "Strong technical background with room for cloud skills"
  },
  
  // Resume Analyzer Results
  "candidate_name": "John Doe",
  "candidate_email": "john.doe@example.com",
  "candidate_phone": "1234567890",
  "candidate_level": "Intermediate",
  "predicted_field": "Web Development",
  "resume_score": 75,
  "detected_skills": [
    "React", "Django", "Python", "JavaScript", "HTML", "CSS"
  ],
  "recommended_skills": [
    "Node JS", "TypeScript", "Angular JS", "React JS", "Flask"
  ],
  "recommended_courses": [
    {
      "name": "Django Crash Course [Free]",
      "link": "https://youtu.be/e1IyzVyrLSU"
    },
    {
      "name": "Full Stack Web Developer by Udacity",
      "link": "https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044"
    }
  ],
  "score_breakdown": [
    "[+] Added Objective/Summary",
    "[+] Added Education Details",
    "[+] Added Skills",
    "[-] Missing Certifications",
    "[+] Added Projects"
  ]
}
```

#### Error Responses

**400 Bad Request** - No file provided
```json
{
  "error": "No PDF file provided"
}
```

**400 Bad Request** - Wrong file type
```json
{
  "error": "Only PDF files are allowed"
}
```

**500 Internal Server Error** - Processing failed
```json
{
  "error": "Failed to process resume: <error details>"
}
```

---

### 2. Get Resume History

Retrieve all resume analyses for the authenticated user.

#### Endpoint
```
GET /api/resume/history/
```

#### Headers
```
Authorization: Bearer <access_token>
```

#### Response (200 OK)
```json
[
  {
    "id": 1,
    "candidate_name": "John Doe",
    "candidate_level": "Intermediate",
    "predicted_field": "Web Development",
    "resume_score": 75,
    "created_at": "2025-12-07T10:30:00Z"
  },
  {
    "id": 2,
    "candidate_name": "John Doe",
    "candidate_level": "Experienced",
    "predicted_field": "Data Science",
    "resume_score": 85,
    "created_at": "2025-12-06T14:20:00Z"
  }
]
```

---

## Flutter/Dart Implementation

### Data Models

```dart
// resume_analysis.dart
class ResumeAnalysis {
  final int id;
  final String candidateName;
  final String candidateEmail;
  final String candidatePhone;
  final String candidateLevel;
  final String predictedField;
  final int resumeScore;
  final List<String> detectedSkills;
  final List<String> recommendedSkills;
  final List<Course> recommendedCourses;
  final List<String> scoreBreakdown;
  final GeminiResponse geminiResponse;
  final DateTime createdAt;

  ResumeAnalysis({
    required this.id,
    required this.candidateName,
    required this.candidateEmail,
    required this.candidatePhone,
    required this.candidateLevel,
    required this.predictedField,
    required this.resumeScore,
    required this.detectedSkills,
    required this.recommendedSkills,
    required this.recommendedCourses,
    required this.scoreBreakdown,
    required this.geminiResponse,
    required this.createdAt,
  });

  factory ResumeAnalysis.fromJson(Map<String, dynamic> json) {
    return ResumeAnalysis(
      id: json['id'],
      candidateName: json['candidate_name'] ?? '',
      candidateEmail: json['candidate_email'] ?? '',
      candidatePhone: json['candidate_phone'] ?? '',
      candidateLevel: json['candidate_level'] ?? '',
      predictedField: json['predicted_field'] ?? '',
      resumeScore: json['resume_score'] ?? 0,
      detectedSkills: List<String>.from(json['detected_skills'] ?? []),
      recommendedSkills: List<String>.from(json['recommended_skills'] ?? []),
      recommendedCourses: (json['recommended_courses'] as List)
          .map((course) => Course.fromJson(course))
          .toList(),
      scoreBreakdown: List<String>.from(json['score_breakdown'] ?? []),
      geminiResponse: GeminiResponse.fromJson(json['gemini_response'] ?? {}),
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}

class Course {
  final String name;
  final String link;

  Course({required this.name, required this.link});

  factory Course.fromJson(Map<String, dynamic> json) {
    return Course(
      name: json['name'],
      link: json['link'],
    );
  }
}

class GeminiResponse {
  final List<String> suitableCareerPaths;
  final List<String> skillGaps;
  final List<String> recommendedCourses;
  final List<String> suggestedNextSteps;
  final String overallSummary;

  GeminiResponse({
    required this.suitableCareerPaths,
    required this.skillGaps,
    required this.recommendedCourses,
    required this.suggestedNextSteps,
    required this.overallSummary,
  });

  factory GeminiResponse.fromJson(Map<String, dynamic> json) {
    return GeminiResponse(
      suitableCareerPaths: List<String>.from(json['suitable_career_paths'] ?? []),
      skillGaps: List<String>.from(json['skill_gaps'] ?? []),
      recommendedCourses: List<String>.from(json['recommended_courses'] ?? []),
      suggestedNextSteps: List<String>.from(json['suggested_next_steps'] ?? []),
      overallSummary: json['overall_summary'] ?? '',
    );
  }
}
```

### API Service

```dart
// resume_service.dart
import 'package:dio/dio.dart';

class ResumeService {
  final Dio _dio;
  final String baseUrl = 'http://0.0.0.0:8000'; // Change for production

  ResumeService(this._dio);

  /// Upload and analyze resume
  Future<ResumeAnalysis> uploadResume(String filePath, String accessToken) async {
    try {
      FormData formData = FormData.fromMap({
        'pdf_file': await MultipartFile.fromFile(
          filePath,
          filename: filePath.split('/').last,
        ),
      });

      final response = await _dio.post(
        '$baseUrl/api/resume/upload/',
        data: formData,
        options: Options(
          headers: {'Authorization': 'Bearer $accessToken'},
        ),
      );

      return ResumeAnalysis.fromJson(response.data);
    } on DioException catch (e) {
      if (e.response != null) {
        throw Exception(e.response!.data['error'] ?? 'Upload failed');
      } else {
        throw Exception('Network error: ${e.message}');
      }
    }
  }

  /// Get resume analysis history
  Future<List<ResumeAnalysis>> getResumeHistory(String accessToken) async {
    try {
      final response = await _dio.get(
        '$baseUrl/api/resume/history/',
        options: Options(
          headers: {'Authorization': 'Bearer $accessToken'},
        ),
      );

      return (response.data as List)
          .map((json) => ResumeAnalysis.fromJson(json))
          .toList();
    } on DioException catch (e) {
      if (e.response != null) {
        throw Exception(e.response!.data['error'] ?? 'Failed to fetch history');
      } else {
        throw Exception('Network error: ${e.message}');
      }
    }
  }
}
```

### Usage Example

```dart
// resume_upload_screen.dart
import 'package:file_picker/file_picker.dart';

Future<void> _pickAndUploadResume() async {
  FilePickerResult? result = await FilePicker.platform.pickFiles(
    type: FileType.custom,
    allowedExtensions: ['pdf'],
  );

  if (result != null) {
    setState(() => _isUploading = true);

    try {
      final accessToken = await AuthService.getAccessToken();
      
      final analysis = await _resumeService.uploadResume(
        result.files.single.path!,
        accessToken,
      );

      setState(() {
        _analysis = analysis;
        _isUploading = false;
      });

      // Navigate to results screen
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ResumeResultsScreen(analysis: analysis),
        ),
      );
    } catch (e) {
      setState(() => _isUploading = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Upload failed: $e')),
      );
    }
  }
}
```

---

## Dependencies

Add to `pubspec.yaml`:

```yaml
dependencies:
  dio: ^5.0.0
  file_picker: ^6.0.0
  url_launcher: ^6.0.0
```

---

## Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `candidate_name` | String | Extracted from resume first line |
| `candidate_email` | String | Extracted via regex |
| `candidate_phone` | String | Extracted via regex |
| `candidate_level` | String | "Fresher", "Intermediate", or "Experienced" |
| `predicted_field` | String | "Data Science", "Web Development", "Android Development", "IOS Development", "UI-UX Development", or "NA" |
| `resume_score` | Integer | 0-100 based on sections |
| `detected_skills` | List | Skills found in resume |
| `recommended_skills` | List | Suggested skills to add |
| `recommended_courses` | List | Online courses with links |
| `score_breakdown` | List | Detailed feedback |

---

## Testing Tips

1. **Test with Postman first** to verify API
2. **Android Emulator**: Use `10.0.2.2:8000`
3. **Physical Device**: Use your local IP `192.168.x.x:8000`
4. **Handle errors** with try-catch blocks
5. **Show loading** during upload (5-10 seconds)

---

## Quick Start Checklist

- [ ] Add dependencies to `pubspec.yaml`
- [ ] Create data models (`ResumeAnalysis`, `Course`, `GeminiResponse`)
- [ ] Create `ResumeService` class
- [ ] Update base URL for your environment
- [ ] Implement file picker
- [ ] Add upload functionality
- [ ] Display results in UI
- [ ] Test with sample PDF resume
