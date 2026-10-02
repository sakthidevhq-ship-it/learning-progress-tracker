import { readFileSync } from 'node:fs';
import { connect, evaluate, size, nav, shot, click, type, key, api, check, sleep, errors, chrome, BASE } from './drive.mjs';

const VAULT = (process.env.VAULT || '/tmp/lpt-browser/vault') + '/pages/';
const RAFT = 'Raft — In Search of an Understandable Consensus Algorithm';
const vis = sel => evaluate(`[...document.querySelectorAll(${JSON.stringify(sel)})].filter(e=>e.offsetParent!==null).length`);
const text = sel => evaluate(`(document.querySelector(${JSON.stringify(sel)})||{}).textContent||''`);
// click innerSel inside the first visible rowSel whose text contains rowText
async function clickIn(rowSel, rowText, innerSel) {
  const ok = await evaluate(`(() => { const row=[...document.querySelectorAll(${JSON.stringify(rowSel)})].find(e=>e.offsetParent!==null&&e.textContent.includes(${JSON.stringify(rowText)}));
    if(!row) return 'no row'; const el=row.querySelector(${JSON.stringify(innerSel)}); if(!el) return 'no inner'; row.scrollIntoView({block:'center'}); return 'ok'; })()`);
  if (ok !== 'ok') throw new Error(`${ok}: ${rowSel} "${rowText}" ${innerSel}`);
  const box = await evaluate(`(() => { const row=[...document.querySelectorAll(${JSON.stringify(rowSel)})].find(e=>e.offsetParent!==null&&e.textContent.includes(${JSON.stringify(rowText)}));
    const r=row.querySelector(${JSON.stringify(innerSel)}).getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2}; })()`);
  const { send } = await import('./drive.mjs');
  for (const t of ['mouseMoved', 'mousePressed', 'mouseReleased']) await send('Input.dispatchMouseEvent', { type: t, x: box.x, y: box.y, button: 'left', clickCount: 1 });
  await sleep(500);
}
const item = async t => (await api()).find(i => i.title.startsWith(t));

try {
  await connect();
  await size(1440, 950);
  await nav(BASE + '#wb');
  check(!(await evaluate(`document.body.classList.contains('ro')`)), 'served page is editable (not read-only)');
  check((await text('#t-wb')).includes('Nothing in progress'), 'fresh workbench shows the empty state');
  await shot('d-wb-empty');

  // Library: set a priority and plan for October
  await click('nav button', 'Library');
  check((await vis('#t-lib .item')) > 100, 'library lists every item');
  await clickIn('#t-lib .item', RAFT, '.pp');
  await clickIn('#t-lib .item', RAFT, '.pp');
  check((await item('Raft —')).prio === 'soon', 'priority chip cycles none → now → soon');
  await clickIn('#t-lib .item', RAFT, '.pls .btn');
  check((await item('Raft —')).planned === new Date().toISOString().slice(0, 7), '+ month plans it for this month');
  await shot('d-lib');

  // Plan: it's in Not started; pick it up there
  await click('nav button', 'Plan');
  check((await text('#t-plan')).includes('Not started'), 'plan shows the item under Not started');
  await clickIn('#t-plan .prow', RAFT, '.btn');
  check((await item('Raft —')).state === 'picked', 'Pick up from the plan');

  // Workbench card: +30m twice
  await click('nav button', 'Workbench');
  await clickIn('#t-wb .pc', RAFT, '.logbtn');
  await clickIn('#t-wb .pc', RAFT, '.logbtn');
  const today = new Date(); const iso = `${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,'0')}-${String(today.getDate()).padStart(2,'0')}`;
  check(JSON.stringify((await item('Raft —')).sessions) === JSON.stringify([{ d: iso, m: 60 }]), '+30m twice logs 1h today');
  check((await text('#t-wb')).includes('1h today'), 'card shows 1h today');

  // Open it: notes, checklist
  await click('#t-wb .pc .ttl', 'Raft');
  check(await evaluate(`document.body.classList.contains('dr')`), 'clicking the card opens the item');
  await click('#notesBox');
  await type('Read half of §5, stopped at 5.4.1');
  await sleep(1400);
  check((await item('Raft —')).notes === 'Read half of §5, stopped at 5.4.1', 'notes autosave');
  check((await text('#notesState')) === 'saved', 'notes show "saved"');
  await click('#newCheck');
  await type('Read §5 log replication\n');
  await type('Implement it in Rust\n');  // straight away, while the first save is in flight
  await sleep(500);
  check(JSON.stringify((await item('Raft —')).checks.map(c => c.t)) === JSON.stringify(['Read §5 log replication', 'Implement it in Rust']), 'two checklist items added with Enter, typed back to back');
  check(await evaluate(`document.activeElement && document.activeElement.id === 'newCheck'`), 'focus stays in the subtask box');
  await click('#drawer .ck span', 'Read §5');
  check((await item('Raft —')).checks[0].done === true, 'ticking a checklist item saves');
  await click('#drawer .tbtns .btn', '+30m');
  check((await item('Raft —')).sessions[0].m === 90, '+30m inside the item');
  await click('#drawer .tbtns .btn', '−30m');
  check((await item('Raft —')).sessions[0].m === 60, '−30m takes it back');
  await shot('d-item');
  const page = readFileSync(VAULT + RAFT + '.md', 'utf8');
  check(page.includes('## Notes\nRead half of §5, stopped at 5.4.1') && page.includes('## Checklist\n- [x] Read §5 log replication\n- [ ] Implement it in Rust') && page.includes(`## Time\n- ${iso} · 1h`), 'the markdown file has Notes, Checklist and Time');
  check(page.includes('state:: picked') && page.includes('my-priority:: soon'), 'the markdown file has state and priority');
  await key('Escape', 'Escape', 27);
  check(!(await evaluate(`document.body.classList.contains('dr')`)), 'Escape closes the item');

  // Capture: press a, two lines, Cmd+Enter
  await key('a', 'KeyA', 65);
  check(await evaluate(`document.body.classList.contains('md')`), '"a" opens Add');
  await type('https://example.com/event-loops');
  await evaluate(`document.querySelector('#addText').value += '\\nRead tokio internals'`);
  await click('#addPrio button', 'someday');
  await click('#addSave');
  await sleep(500);
  const unsorted = (await api()).filter(i => i.area === 'Unsorted');
  check(unsorted.length === 2 && unsorted.every(i => i.prio === 'someday' && i.enrich), 'Add saves both lines to Unsorted with priority');

  // Search
  await key('/', 'Slash', 191);
  await type('attention');
  await sleep(300);
  check((await vis('#t-lib .item')) >= 1 && (await vis('#t-lib .item')) < 10, 'search filters the library');
  await click('#t-lib .item .tt', 'Attention Is All You Need');
  await click('#drawer .btn', 'Pick up');
  await click('#drawer .btn', 'Done');
  check((await item('Attention Is All You Need')).state === 'done', 'pick up then Done from the item');
  await key('Escape', 'Escape', 27);
  await evaluate(`document.querySelector('#q').blur()`);

  // Put back and drop
  await evaluate(`clearQuery()`);
  await click('#t-lib .item .tt', 'Gossip Glomers');
  await click('#drawer .btn', 'Pick up');
  await click('#drawer .btn', 'Put back');
  const gg = await item('Gossip Glomers');
  check(gg.state === 'collected' && gg.planned, 'Put back: not started, still planned');
  await click('#drawer .btn', 'Pick up');
  await click('#drawer .btn', 'Drop');
  check((await item('Gossip Glomers')).state === 'dropped', 'Drop');
  await key('Escape', 'Escape', 27);

  // Reload keeps everything
  await nav(BASE + '#wb');
  check((await text('#t-wb')).includes('1h today') && (await text('#t-wb')).includes('Read half of §5'), 'reload shows saved time and latest note');
  await shot('d-wb');
  await click('nav button', 'Plan'); await shot('d-plan');
  check((await text('#t-plan')).includes('Done') && (await text('#t-plan')).includes('In progress'), 'plan shows In progress and Done');
  await click('nav button', 'Insights'); await shot('d-ins');
  check((await text('#t-ins')).includes('1h') && (await text('#t-ins')).includes('of your time went to'), 'insights reflect the logged hour');

  // Phone
  await size(390, 844, true);
  for (const t of ['wb', 'plan', 'lib', 'ins']) { await nav(BASE + '#' + t); await shot('p-' + t); }
  check((await vis('nav button')) === 4, 'phone: four tabs in the bottom bar');
  const navBox = await evaluate(`(() => { const r=document.querySelector('nav').getBoundingClientRect(); return r.bottom })()`);
  check(Math.abs(navBox - 844) < 2, 'phone: tab bar sits at the bottom');
  check(await evaluate(`document.documentElement.scrollWidth <= 391`), 'phone: no sideways scrolling');
  await nav(BASE + '#wb');
  await click('#t-wb .pc .ttl', 'Raft');
  await shot('p-item');
  await click('#drawer .tbtns .btn', '+30m');
  check((await item('Raft —')).sessions[0].m === 90, 'phone: +30m works inside the item');

  console.log('JS errors:', errors.length ? errors : 'none');
  if (errors.length) process.exitCode = 1;
} catch (e) {
  console.log('FAIL (crashed) ' + e.message);
  console.log('JS errors:', errors);
  process.exitCode = 1;
} finally {
  chrome.kill();
}
