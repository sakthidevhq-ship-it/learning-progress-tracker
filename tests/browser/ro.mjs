import { connect, evaluate, size, nav, shot, click, check, sleep, errors, chrome } from './drive.mjs';
const visEd = () => evaluate(`[...document.querySelectorAll('.ed,#addBtn')].filter(e=>e.offsetParent!==null).length`);
try {
  await connect();
  for (const [label, url] of [['file', 'file://' + process.env.SITE + '/index.html'], ['pages-like', process.env.STATIC_BASE + 'index.html']]) {
    await size(390, 844, true);
    await nav(url + '#wb');
    check(await evaluate(`document.body.classList.contains('ro')`), `${label}: read-only mode`);
    check((await visEd()) === 0, `${label}: no edit buttons visible`);
    check((await evaluate(`document.querySelector('#t-wb').textContent`)).includes('Raft'), `${label}: shows the in-progress item`);
    await click('#t-wb .pc .ttl', 'Raft');
    check(await evaluate(`document.querySelector('#notesBox').readOnly && document.querySelector('.ck input').disabled`), `${label}: notes and checklist are read-only`);
    check((await visEd()) === 0, `${label}: item panel has no edit buttons`);
    await shot(`ro-${label}-item`);
    await evaluate(`closeItem()`);
    await evaluate(`document.dispatchEvent(new KeyboardEvent('keydown',{key:'a'}))`);
    check(!(await evaluate(`document.body.classList.contains('md')`)), `${label}: "a" does not open Add`);
    await nav(url + '#plan'); await shot(`ro-${label}-plan`);
  }
  const real = errors.filter(e => !/api\/items|favicon/.test(e));
  console.log('JS errors:', real.length ? real : 'none', `(ignored ${errors.length - real.length} expected 404 for /api/items)`);
  if (real.length) process.exitCode = 1;
} catch (e) { console.log('FAIL (crashed) ' + e.message, errors); process.exitCode = 1; } finally { chrome.kill(); }
