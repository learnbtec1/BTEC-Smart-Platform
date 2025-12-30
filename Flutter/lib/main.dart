import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'منصة Flutter',
      theme: ThemeData(primarySwatch: Colors.blue, fontFamily: 'Cairo'),
      home: HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  final List<String> items = [
    'الصفحة الأولى',
    'الصفحة الثانية',
    'الصفحة الثالثة',
    'الصفحة الرابعة',
  ];

HomePage({super.key});


  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('القائمة الرئيسية'),
        centerTitle: true,
      ),
      body: ListView.builder(
        itemCount: items.length,
        itemBuilder: (context, index) {
          return Card(
            margin: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: ListTile(
              leading: Icon(Icons.star, color: Colors.blue),
              title: Text(items[index]),
              trailing: Icon(Icons.arrow_forward_ios),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => DetailPage(title: items[index]),
                  ),
                );
              },
            ),
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('تم الضغط على الزر بنجاح!')),
          );
        },
        child: Icon(Icons.add),
      ),
    );
  }
}

class DetailPage extends StatelessWidget {
  final String title;

  const DetailPage({super.key, required this.title});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(title)),
      body: Center(
        child: Text(
          'أنت الآن في صفحة: $title',
          style: TextStyle(fontSize: 20),
        ),
      ),
    );
  }
}
