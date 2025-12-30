import "package:flutter/material.dart";
import "../services/api_service.dart";
import "../services/database_service.dart";
import "../services/file_uploader.dart";
import "../models/analysis_result.dart";
import "analysis_screen.dart";

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _textController = TextEditingController();
  bool _isAnalyzing = false;
  AnalysisResult? _result;

  Future<void> _analyzeText() async {
    if (_textController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text("???? ??? ???????")));
      return;
    }
    setState(() => _isAnalyzing = true);
    try {
      final submissionId =
          await ApiService.analyzeText(_textController.text.trim());
      final result = await ApiService.getResults(submissionId);
      await DatabaseService().saveSubmission(result);
      setState(() {
        _result = result;
        _isAnalyzing = false;
      });
      Navigator.push(context,
          MaterialPageRoute(builder: (_) => AnalysisScreen(result: result)));
    } catch (e) {
      setState(() => _isAnalyzing = false);
      ScaffoldMessenger.of(context)
          .showSnackBar(SnackBar(content: Text("??? ?? ???????: \$e")));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("???? BTEC ??????? ?????"),
        actions: [
          IconButton(
            icon: Icon(Icons.dashboard),
            onPressed: () => Navigator.pushNamed(context, "/dashboard"),
            tooltip: "???? ???? ??????",
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Expanded(
              child: TextField(
                controller: _textController,
                maxLines: null,
                expands: true,
                decoration: InputDecoration(
                  hintText: "???? ?? ?????? ???...",
                  border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(8.0)),
                  filled: true,
                  fillColor: Colors.white,
                ),
              ),
            ),
            SizedBox(height: 16),
            ElevatedButton(
              onPressed: _isAnalyzing ? null : _analyzeText,
              style: ElevatedButton.styleFrom(
                  padding: EdgeInsets.symmetric(vertical: 16),
                  backgroundColor: Color(0xFF0078ff)),
              child: _isAnalyzing
                  ? Row(mainAxisAlignment: MainAxisAlignment.center, children: [
                      SizedBox(
                          width: 18,
                          height: 18,
                          child: CircularProgressIndicator(
                              color: Colors.white, strokeWidth: 2)),
                      SizedBox(width: 10),
                      Text("???? ???????...")
                    ])
                  : Text("??? ???????"),
            ),
            SizedBox(height: 8),
            OutlinedButton.icon(
              onPressed: () => FileUploader().pickAndUploadFile(),
              icon: Icon(Icons.upload_file),
              label: Text("??? ??? PDF ?? DOCX"),
              style: OutlinedButton.styleFrom(
                  padding: EdgeInsets.symmetric(vertical: 16),
                  side: BorderSide(color: Color(0xFF0078ff))),
            ),
          ],
        ),
      ),
    );
  }
}
