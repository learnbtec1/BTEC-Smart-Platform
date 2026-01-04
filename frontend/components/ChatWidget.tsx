import React, { useState } from "react";
export const ChatWidget: React.FC = () => {
  const [open, setOpen] = useState(false);
  return (
    <div style={{position:"fixed", bottom:20, left:20}}>
      {!open && <button onClick={()=>setOpen(true)} style={{borderRadius:999,padding:12,background:"#2563EB",color:"#fff"}}>ق</button>}
      {open && (
        <div style={{width:320,background:"#071022",borderRadius:12,padding:12}}>
          <div style={{display:"flex",justifyContent:"space-between"}}><strong>مساعد قيتاغورس</strong><button onClick={()=>setOpen(false)}>✕</button></div>
          <div style={{height:200,overflow:"auto",marginTop:8}}>ابدأ المحادثة...</div>
        </div>
      )}
    </div>
  );
};
export default ChatWidget;
