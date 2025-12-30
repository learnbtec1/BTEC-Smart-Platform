import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api.dart';

class PlagiarismService {
  static Future<Map<String, dynamic>> checkPlagiarism({
    required String studentText,
    required List<String> referenceTexts,
    double threshold = 0.7,
  }) async {
    final url = Uri.parse("${ApiConfig.baseUrl}/plagiarism/check");

    final response = await http.post(
      url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({
        "student_text": studentText,
        "reference_texts": referenceTexts,
        "threshold": threshold,
      }),
    );

    return jsonDecode(response.body);
  }
}
