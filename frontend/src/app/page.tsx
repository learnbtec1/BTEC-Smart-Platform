import Link from 'next/link';

export default function Home() {
  return (
    <div style={{ padding: "50px", fontFamily: "sans-serif", textAlign: "center" }}>
      <h1>مرحباً بك في نظام BTEC Nexus</h1>
      <p>الصفحة الرئيسية تعمل الآن بنجاح.</p>
      
      <div style={{ marginTop: "20px" }}>
        {/* رابط ينقلك لصفحة التقييمات التي وجدتها سابقاً */}
        <Link href="/assessments" style={{ color: "blue", textDecoration: "underline" }}>
          الذهاب إلى صفحة التقييمات (Assessments)
        </Link>
      </div>
    </div>
  );
}