import "dart:convert";
import "package:http/http.dart" as http;
import "../models/analysis_result.dart";

class ApiService {
  static const String baseUrl = String.fromEnvironment("API_BASE", defaultValue: "http://127.0.0.1:8000");

  static Future<String> analyzeText(String text) async {
    final url = Uri.parse("\$baseUrl/api/v1/evaluate");
    final res = await http.post(url,
      headers: {"Content-Type": "application/json"},
      body: jsonEncode({"input": text}),
    );
    if (res.statusCode == 200 || res.statusCode == 201) {
      final data = jsonDecode(res.body);
      return data["submission_id"] ?? data["id"] ?? "";
    }
    throw Exception("Server error \${res.statusCode}: \${res.body}");
  }

  static Future<AnalysisResult> getResults(String submissionId) async {
    final url = Uri.parse("\$baseUrl/api/v1/results/\$submissionId");
    final res = await http.get(url);
    if (res.statusCode == 200) {
      final data = jsonDecode(res.body);
      return AnalysisResult.fromJson(data);
    }
    throw Exception("Failed to fetch results \${res.statusCode}");
  }
}
