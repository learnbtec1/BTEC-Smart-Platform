import React, { useState } from "react";
export const FileUpload: React.FC = () => {
  const [file, setFile] = useState<File|null>(null);
  async function submit(){
    if(!file) return;
    const fd = new FormData();
    fd.append("file", file);
    const res = await fetch("/api/v1/files/upload", { method:"POST", body: fd });
    if(!res.ok) alert("Upload failed");
  }
  return (
    <div style={{background:"#071022",padding:12,borderRadius:8}}>
      <input type="file" onChange={(e:any)=>setFile(e.target.files?.[0]||null)} />
      <button onClick={submit}>رفع</button>
    </div>
  );
};
export default FileUpload;
