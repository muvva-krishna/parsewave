export function ActivityFeed({ activities }: { activities: Array<{label:string;detail?:string}> }) {
  return <div style={{marginTop:24}}><h3>Agent activity</h3>{activities.map((a,i)=><div key={i}>✓ {a.label}{a.detail ? ` — ${a.detail}` : ""}</div>)}</div>;
}
