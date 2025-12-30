import { Card } from "@/components/ui/card";

export default function Dashboard() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 animate-in fade-in duration-300">
      <Card className="p-6">
        <h3 className="text-lg font-semibold">Total Students</h3>
        <p className="text-3xl font-bold mt-2">128</p>
      </Card>

      <Card className="p-6">
        <h3 className="text-lg font-semibold">AI Assessments</h3>
        <p className="text-3xl font-bold mt-2">342</p>
      </Card>

      <Card className="p-6">
        <h3 className="text-lg font-semibold">Pending Reviews</h3>
        <p className="text-3xl font-bold mt-2">17</p>
      </Card>
    </div>
  );
}