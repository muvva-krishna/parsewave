"use client";
import { useState } from "react";
import { ActivityFeed } from "../components/ActivityFeed";
import { ResponseCard } from "../components/ResponseCard";

export default function Home() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  async function ask() {
    setLoading(true);
    const r = await fetch("http://localhost:8000/api/v1/ask", {method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({query})});
    const data = await r.json(); setResult(data); setLoading(false);
  }

  return <main style={{maxWidth:960, margin:"0 auto", padding:48}}>
    <h1>Clinical Evidence Agent</h1>
    <p>Evidence-first clinical workflows with typed agent outputs.</p>
    <textarea value={query} onChange={e=>setQuery(e.target.value)} placeholder="Ask a clinical question..." rows={5} style={{width:"100%", padding:16}} />
    <button onClick={ask} disabled={loading || query.length<3} style={{marginTop:12, padding:"10px 16px"}}>{loading?"Working…":"Ask"}</button>
    {result && <><ActivityFeed activities={result.activities}/><ResponseCard card={result.card}/></>}
  </main>;
}
