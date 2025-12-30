import { Card } from "@/components/ui/card";

export default function Results() {
  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <h1 className="text-2xl font-bold">AI Assessment Results</h1>

      <Card className="p-6">
        <h3 className="text-lg font-semibold">Student: John Doe</h3>
        <p className="mt-2">Score: 87%</p>
        <p className="text-muted-foreground mt-1">
          Feedback: Good structure, minor issues.
        </p>
      </Card>
    </div>
  );
}