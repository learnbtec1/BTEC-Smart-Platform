import React, { useState } from 'react';
import { Layout, Input, Button, Select, List, Card, Spin, message, Typography } from 'antd';
import { SendOutlined, DownloadOutlined, BookOutlined } from '@ant-design/icons';
import ReactMarkdown from 'react-markdown'; // تأكد من تثبيته: npm install react-markdown
import { askAssistant, downloadTemplate } from './api'; // استيراد الدوال من الملف السابق

const { Header, Content } = Layout;
const { Option } = Select;
const { Text } = Typography;

const ChatInterface = () => {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState([]); // سجل المحادثة
  const [loading, setLoading] = useState(false);
  
  // State للأزرار الجديدة
  const [level, setLevel] = useState('L2');
  const [major, setMajor] = useState('Business');

  // دالة الإرسال
  const handleSend = async () => {
    if (!question.trim()) return;

    const userMsg = { role: 'user', content: question };
    setMessages([...messages, userMsg]);
    setLoading(true);

    try {
      // إرسال البيانات للباكند
      const data = await askAssistant(question, level, major);
      
      const botMsg = { 
        role: 'bot', 
        content: data.msg, 
        sources: data.sources // استقبال المصادر
      };
      setMessages(prev => [...prev, botMsg]);
      setQuestion('');
    } catch (error) {
      message.error("عذراً، حدث خطأ في الاتصال بالسيرفر.");
    } finally {
      setLoading(false);
    }
  };

  // دالة زر التحميل
  const handleDownloadClick = async () => {
    try {
      message.loading({ content: 'جاري إنشاء ملف الوورد...', key: 'download' });
      await downloadTemplate(level, "1"); // رقم الوحدة افتراضي 1 حالياً
      message.success({ content: 'تم التحميل بنجاح!', key: 'download' });
    } catch (error) {
      message.error({ content: 'فشل التحميل', key: 'download' });
    }
  };

  return (
    <Layout style={{ height: '100vh', background: '#fff' }}>
      {/* 1. الشريط العلوي (Toolbar) */}
      <Header style={{ background: '#f0f2f5', padding: '0 20px', display: 'flex', alignItems: 'center', gap: '15px' }}>
        <Select value={level} onChange={setLevel} style={{ width: 120 }}>
          <Option value="L2">Level 2 (G10)</Option>
          <Option value="L3">Level 3 (G11/12)</Option>
        </Select>

        <Select value={major} onChange={setMajor} style={{ width: 120 }}>
          <Option value="Business">Business</Option>
          <Option value="IT">IT (Beta)</Option>
        </Select>

        <Button 
          type="primary" 
          icon={<DownloadOutlined />} 
          onClick={handleDownloadClick}
          style={{ marginLeft: 'auto' }}
        >
          تحميل نموذج الحل
        </Button>
      </Header>

      {/* 2. منطقة المحادثة */}
      <Content style={{ padding: '20px', overflowY: 'auto' }}>
        <List
          itemLayout="horizontal"
          dataSource={messages}
          renderItem={item => (
            <List.Item style={{ justifyContent: item.role === 'user' ? 'flex-end' : 'flex-start' }}>
              <Card 
                style={{ 
                  maxWidth: '80%', 
                  background: item.role === 'user' ? '#1890ff' : '#f5f5f5',
                  color: item.role === 'user' ? '#fff' : '#000'
                }}
              >
                {/* عرض النص باستخدام Markdown */}
                <ReactMarkdown>{item.content}</ReactMarkdown>

                {/* عرض المصادر إذا كانت رسالة بوت */}
                {item.role === 'bot' && item.sources && item.sources.length > 0 && (
                  <div style={{ marginTop: '10px', paddingTop: '10px', borderTop: '1px solid #d9d9d9' }}>
                    <Text type="secondary" style={{ fontSize: '12px' }}>
                      <BookOutlined /> المصادر:
                    </Text>
                    <ul style={{ fontSize: '11px', paddingRight: '20px', margin: '5px 0' }}>
                      {item.sources.map((src, idx) => (
                        <li key={idx}>{src}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </Card>
            </List.Item>
          )}
        />
        {loading && <Spin tip="جاري الكتابة..." style={{ marginTop: 20 }} />}
      </Content>

      {/* 3. صندوق الإدخال */}
      <div style={{ padding: '20px', borderTop: '1px solid #eee' }}>
        <Input.Search
          placeholder="اسأل عن أي معيار (مثال: P1 Unit 1)..."
          enterButton={<SendOutlined />}
          size="large"
          value={question}
          onChange={e => setQuestion(e.target.value)}
          onSearch={handleSend}
          loading={loading}
        />
      </div>
    </Layout>
  );
};

export default ChatInterface;