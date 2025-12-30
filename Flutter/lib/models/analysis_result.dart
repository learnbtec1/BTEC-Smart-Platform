class AnalysisResult {
  final String id;
  final String input;
  final Map<String, dynamic> scores;
  final String verdict;
  final DateTime timestamp;

  AnalysisResult({
    required this.id,
    required this.input,
    required this.scores,
    required this.verdict,
    required this.timestamp,
  });

  factory AnalysisResult.fromJson(Map<String, dynamic> json) {
    return AnalysisResult(
      id: json["id"]?.toString() ?? "",
      input: json["input"] ?? "",
      scores: Map<String, dynamic>.from(json["scores"] ?? {}),
      verdict: json["verdict"] ?? "",
      timestamp: DateTime.parse(json["timestamp"] ?? DateTime.now().toIso8601String()),
    );
  }

  Map<String, dynamic> toJson() => {
    "id": id,
    "input": input,
    "scores": scores,
    "verdict": verdict,
    "timestamp": timestamp.toIso8601String(),
  };
}
