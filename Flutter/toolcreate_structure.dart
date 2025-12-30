import 'dart:io';

void main() {
  final dirs = [
    'lib/models',
    'lib/screens',
    'lib/services',
    'lib/widgets',
    'lib/utils',
  ];

  for (var dir in dirs) {
    Directory(dir).createSync(recursive: true);
    print('Created: $dir');
  }

  File('lib/models/analysis_result.dart').writeAsStringSync('// AnalysisResult model');
  File('lib/services/api_service.dart').writeAsStringSync('// ApiService');
  File('lib/screens/analysis_screen.dart').writeAsStringSync('// AnalysisScreen');
  File('lib/screens/home_screen.dart').writeAsStringSync('// HomeScreen');

  print('All files created successfully!');
}