import React from "react";
type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary"|"outline"|"ghost" };
export const Button: React.FC<Props> = ({ variant="primary", children, ...p }) => {
  const base = "px-4 py-2 rounded-lg font-semibold";
  const cls = variant==="primary" ? "bg-blue-600 text-white" : variant==="outline" ? "border border-white/10 text-white" : "text-white/90";
  return <button className={base + " " + cls} {...p}>{children}</button>;
};
export default Button;
