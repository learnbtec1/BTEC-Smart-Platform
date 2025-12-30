import "package:flutter/material.dart";
import "../models/analysis_result.dart";

class AnalysisScreen extends StatelessWidget {
  final AnalysisResult result;
  const AnalysisScreen({super.key, required this.result});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("????? ???????")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("ID: \${result.id}",
                style: TextStyle(fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            Text("Input:", style: TextStyle(fontWeight: FontWeight.bold)),
            Text(result.input),
            SizedBox(height: 12),
            Text("Verdict: \${result.verdict}",
                style: TextStyle(color: Colors.blue)),
            SizedBox(height: 12),
            Text("Scores:", style: TextStyle(fontWeight: FontWeight.bold)),
            Expanded(
              child: ListView(
                children: result.scores.entries
                    .map((e) => ListTile(
                        title: Text(e.key), trailing: Text(e.value.toString())))
                    .toList(),
              ),
            ),
            Text("Timestamp: \${result.timestamp.toIso8601String()}"),
          ],
        ),
      ),
    );
  }
}
