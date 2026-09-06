export type Llengua = 'ca' | 'es' | 'mixt';
// Paraules gramaticals pròpies de cada llengua (no compartides). Les contraccions amb apòstrof (l’, d’, s’…)
// i lletres com ç, à, è compten per al valencià; ñ, ¿ i ¡ per al castellà. Els poemes curts es decidixen així.
const CA = new Set('les els dels als amb és són això aquest aquesta aquests aquestes molt vaig hi ho també però perquè doncs sempre meua meu seua seu nostre nostra tots res ens em et us qui què on jo ell ella nosaltres vosaltres ells elles aquell aquella mateix mateixa quan mentre després abans dins fora damunt baix ací allí així cap fins ja encara sols només bé mal més menys molts moltes poc poca tan tant tanta vegada vegades any anys dia dies casa poble xiquet xiquets mare pare germà germans avi àvia agüelo agüela'.split(' '));
const ES = new Set('los las con también pero es son esto este esta estos estas muy ya hay siempre nuestro nuestra todos nada nos me te os quien qué donde yo él ella nosotros vosotros ellos ellas aquel aquella mismo misma cuando mientras después antes dentro fuera encima abajo aquí allí así hacia hasta todavía solo sólo bien mal más menos muchos muchas poco poca tan tanto tanta vez veces año años día días casa pueblo niño niños madre padre hermano hermanos abuelo abuela'.split(' '));
export function llengua(text: string): Llengua {
  const t = text.toLowerCase();
  let ca = 0, es = 0;
  for (const w of t.replace(/[^a-zà-ü’' ]/g, ' ').split(/\s+/)) {
    if (CA.has(w) && !ES.has(w)) ca++;
    else if (ES.has(w) && !CA.has(w)) es++;
  }
  ca += (t.match(/\b[ldsmtn]’/g) ?? []).length + (t.match(/[çàèò]/g) ?? []).length * 0.5;
  es += (t.match(/[ñ¿¡]/g) ?? []).length;
  const tot = ca + es;
  if (tot === 0) return 'mixt';
  const r = ca / tot;
  return r > 0.75 ? 'ca' : r < 0.25 ? 'es' : 'mixt';
}
