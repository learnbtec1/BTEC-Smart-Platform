import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function Upload() {
  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      <h1 className="text-2xl font-bold">Upload Assignment</h1>

      <Input type="file" />
      <Button>Upload</Button>
    </div>
  );
}