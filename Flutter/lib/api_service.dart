
Future<Map<String, dynamic>> analyzeFile({
  String? filePath,
  Uint8List? fileBytes,
  String? fileName,
}) async {
  final url = Uri.parse("$baseUrl/analyze");
  var request = http.MultipartRequest("POST", url);

  if (kIsWeb) {
    if (fileBytes == null || fileName == null) {
      throw Exception("يجب تمرير fileBytes و fileName عند العمل على الويب");
    }
    request.files.add(http.MultipartFile.fromBytes(
      "file",
      fileBytes,
      filename: fileName,
    ));
  } else {
    if (filePath == null) {
      throw Exception("يجب تمرير filePath عند العمل على الموبايل");
    }
    request.files.add(await http.MultipartFile.fromPath("file", filePath));
  }

  var response = await request.send();
  var responseBody = await response.stream.bytesToString();

  return {
    "statusCode": response.statusCode,
    "body": responseBody,
  };
}
