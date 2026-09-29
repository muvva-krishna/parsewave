export function ResponseCard({ card }: { card:any }) {
  return <section style={{marginTop:24, border:"1px solid #ddd", borderRadius:16, padding:24}}>
    <div style={{fontSize:12, letterSpacing:1, textTransform:"uppercase"}}>{card.type}</div>
    <h2>{card.title}</h2>
    {card.answer && <p style={{whiteSpace:"pre-wrap"}}>{card.answer}</p>}
    {card.warnings?.map((x:string,i:number)=><p key={i}>⚠ {x}</p>)}
    {card.criteria?.map((x:any,i:number)=><div key={i} style={{padding:"12px 0", borderTop:"1px solid #eee"}}><b>{x.status}</b> {x.text}<div>{x.reason}</div></div>)}
  </section>;
}
