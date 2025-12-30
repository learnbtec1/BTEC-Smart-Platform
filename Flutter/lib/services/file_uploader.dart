import "package:file_picker/file_picker.dart";
import "package:dio/dio.dart";

class FileUploader {
  final Dio _dio = Dio();
  final String baseUrl = const String.fromEnvironment("API_BASE", defaultValue: "http://127.0.0.1:8000");

  Future<void> pickAndUploadFile() async {
    final result = await FilePicker.platform.pickFiles(type: FileType.custom, allowedExtensions: ["pdf","docx"]);
    if (result == null) return;
    final filePath = result.files.single.path!;
    final fileName = result.files.single.name;

    final formData = FormData.fromMap({
      "file": await MultipartFile.fromFile(filePath, filename: fileName),
    });

    final res = await _dio.post("\$baseUrl/api/v1/upload", data: formData);
    if (res.statusCode == 200 || res.statusCode == 201) {
      print("Upload success: \${res.data}");
    } else {
      throw Exception("Upload failed \${res.statusCode}");
    }
  }
}
import 'package:flutter/foundation.dart';

Future<void> pickAndUploadFile() async {
  final result = await FilePicker.platform.pickFiles(type: FileType.custom, allowedExtensions: ['pdf','docx']);
  if (result != null) {
    if (kIsWeb) {
      final fileBytes = result.files.single.bytes;
      final fileName = result.files.single.name;
      await ApiService().analyzeFile(fileBytes: fileBytes, fileName: fileName);
    } else {
      final filePath = result.files.single.path!;
      await ApiService().analyzeFile(filePath: filePath);
    }
  }
}
import 'package:flutter/foundation.dart';
import '../api_service.dart';

Future<void> pickAndUploadFile() async {
  final result = await FilePicker.platform.pickFiles(type: FileType.custom, allowedExtensions: ['pdf','docx']);
  if (result != null) {
    if (kIsWeb) {
      final fileBytes = result.files.single.bytes;
      final fileName = result.files.single.name;
      await ApiService().analyzeFile(fileBytes: fileBytes, fileName: fileName);
    } else {
      final filePath = result.files.single.path!;
      await ApiService().analyzeFile(filePath: filePath);
    }
  }
}
import 'package:flutter/foundation.dart';
import '../api_service.dart';

Future<void> pickAndUploadFile() async {
  final result = await FilePicker.platform.pickFiles(type: FileType.custom, allowedExtensions: ['pdf','docx']);
  if (result != null) {
    if (kIsWeb) {
      final fileBytes = result.files.single.bytes;
      final fileName = result.files.single.name;
      await ApiService().analyzeFile(fileBytes: fileBytes, fileName: fileName);
    } else {
      final filePath = result.files.single.path!;
      await ApiService().analyzeFile(filePath: filePath);
    }
  }
}
