export default function Assignments() {
  const assignments = [
    { title: "Unit 1 – Business Environment", due: "2025-01-10" },
    { title: "Unit 2 – Marketing Essentials", due: "2025-01-15" },
    { title: "Unit 3 – Finance for Business", due: "2025-01-20" },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <h1 className="text-2xl font-bold">Assignments</h1>

      <div className="border rounded-lg p-4">
        <table className="w-full">
          <thead>
            <tr className="text-left border-b">
              <th className="py-2">Assignment</th>
              <th className="py-2">Due Date</th>
            </tr>
          </thead>

          <tbody>
            {assignments.map((a) => (
              <tr key={a.title} className="border-b">
                <td className="py-2">{a.title}</td>
                <td className="py-2">{a.due}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}