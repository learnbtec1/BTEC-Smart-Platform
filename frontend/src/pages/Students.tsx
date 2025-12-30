export default function Students() {
  const students = [
    { name: "John Doe", id: "STU-001" },
    { name: "Sarah Smith", id: "STU-002" },
    { name: "Michael Brown", id: "STU-003" },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <h1 className="text-2xl font-bold">Students</h1>

      <div className="border rounded-lg p-4">
        <table className="w-full">
          <thead>
            <tr className="text-left border-b">
              <th className="py-2">Name</th>
              <th className="py-2">ID</th>
            </tr>
          </thead>

          <tbody>
            {students.map((s) => (
              <tr key={s.id} className="border-b">
                <td className="py-2">{s.name}</td>
                <td className="py-2">{s.id}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}