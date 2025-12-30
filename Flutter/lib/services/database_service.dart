import "package:sqflite/sqflite.dart";
import "package:path/path.dart";
import "../models/analysis_result.dart";
import "package:path_provider/path_provider.dart";
import "dart:io";

class DatabaseService {
  static final DatabaseService _instance = DatabaseService._internal();
  factory DatabaseService() => _instance;
  DatabaseService._internal();

  Database? _db;

  Future<Database> get db async {
    if (_db != null) return _db!;
    final documentsDirectory = await getApplicationDocumentsDirectory();
    final path = join(documentsDirectory.path, "btec.db");
    _db = await openDatabase(path, version: 1, onCreate: (db, v) async {
      await db.execute('''
        CREATE TABLE submissions(
          id TEXT PRIMARY KEY,
          input TEXT,
          verdict TEXT,
          scores TEXT,
          timestamp TEXT
        )
      ''');
    });
    return _db!;
  }

  Future<void> saveSubmission(AnalysisResult result) async {
    final database = await db;
    await database.insert("submissions", {
      "id": result.id,
      "input": result.input,
      "verdict": result.verdict,
      "scores": result.scores.toString(),
      "timestamp": result.timestamp.toIso8601String(),
    }, conflictAlgorithm: ConflictAlgorithm.replace);
  }
}
