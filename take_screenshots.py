"""Take screenshots of schooldashboard.uk app for marketing website."""
import os
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:3000"
EMAIL = "monitor.admin@abraxor.com"
PASSWORD = "testpass123"
OUT = "/home/wasim/projects/schooldashboard-website/screenshots"

BP_SEED_JS = r"""() => {
  // Stop the page's own renderGrid from clobbering our injection
  if (typeof window.renderGrid === 'function') {
    window.renderGrid = function() {};
  }
  const grid = document.getElementById('bp-grid');
  if (!grid) return;
  // Clear the grid (it may contain a "no plan" message)
  grid.innerHTML = '';
  const firstNames = ['Alex','Jordan','Sam','Taylor','Morgan','Casey','Riley','Jamie','Drew','Quinn','Avery','Skyler','Reese','Cameron','Hayden','Parker','Rowan','Sage','Emery','Finley','Blake','Harper','Aiden','Mia','Noah','Zara','Eli','Iris','Owen','Maya'];
  const lastNames  = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Wilson','Moore','Taylor','Anderson','Thomas','Jackson','White','Harris','Martin','Thompson','Clark','Lewis','Patel','Chen','Khan','Singh','Wright','Kelly','Hughes','Wood','Bell','Ward'];
  const colours = ['#2563eb','#0ea5e9','#14b8a6','#22c55e','#84cc16','#eab308','#f97316','#ef4444','#ec4899','#a855f7','#6366f1','#0891b2','#16a34a','#dc2626','#d97706','#7c3aed','#0f766e','#be123c','#9333ea','#1d4ed8'];
  grid.style.gridTemplateColumns = 'repeat(6, 1fr)';
  grid.innerHTML = '';
  const rows = 5, cols = 6;
  let n = 0;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      // Leave a couple of seats empty for realism
      if ((r === 1 && c === 3) || (r === 3 && c === 0)) {
        const empty = document.createElement('div');
        empty.className = 'bp-tile bp-empty';
        grid.appendChild(empty);
        continue;
      }
      const first = firstNames[n % firstNames.length];
      const last = lastNames[(n * 7) % lastNames.length];
      const colour = colours[n % colours.length];
      const initials = (first[0] + last[0]).toUpperCase();
      const tile = document.createElement('div');
      tile.className = 'bp-tile';
      tile.innerHTML = `
        <div class="bp-avatar" style="background:${colour}">${initials}</div>
        <div style="font-size:0.85rem;font-weight:600;color:#1f2937">${first} ${last[0]}.</div>
      `;
      grid.appendChild(tile);
      n++;
    }
  }
  // Update header bits — replace "No seating plan" with a friendly status, set BP/Merits counts
  document.querySelectorAll('.bp-bar').forEach(bar => {
    bar.querySelectorAll('span, div').forEach(el => {
      if (/no seating plan/i.test(el.textContent)) {
        el.textContent = '28 pupils seated';
        el.style.color = '#475569';
      }
    });
  });
  // Tweak the right-hand "Recent activity" panel to show a couple of example entries
  const activityCards = document.querySelectorAll('.bp-card, .activity-card, [class*="activity"]');
  // Best-effort: find a card titled RECENT ACTIVITY and append example items
  document.querySelectorAll('div').forEach(d => {
    const heading = d.querySelector(':scope > *');
    if (heading && /recent activity/i.test(heading.textContent || '')) {
      // Find empty placeholder text in this card
      d.querySelectorAll('em, i, .muted, .empty').forEach(el => el.remove());
      [...d.childNodes].forEach(n => {
        if (n.nodeType === 3 && /no events yet/i.test(n.textContent)) n.textContent = '';
      });
      const items = [
        ['Drew M.', 'Merit', '+1', '#166534', '#dcfce7'],
        ['Quinn B.', 'BP', '-1', '#991b1b', '#fee2e2'],
        ['Casey H.', 'Merit', '+1', '#166534', '#dcfce7'],
      ];
      items.forEach(([who, kind, val, fg, bg]) => {
        const row = document.createElement('div');
        row.style.cssText = 'display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-top:1px solid #f1f5f9;font-size:0.9rem;color:#334155';
        row.innerHTML = `<span>${who}</span><span style="display:inline-flex;gap:8px;align-items:center"><span style="background:${bg};color:${fg};padding:2px 8px;border-radius:999px;font-weight:600;font-size:0.78rem">${kind} ${val}</span><span style="color:#94a3b8;font-size:0.78rem">just now</span></span>`;
        d.appendChild(row);
      });
    }
  });
}"""

SP_SEED_JS = r"""() => {
  const grid = document.getElementById('sp-grid');
  const pool = document.getElementById('sp-pool');
  if (!grid) return;
  const firstNames = ['Alex','Jordan','Sam','Taylor','Morgan','Casey','Riley','Jamie','Drew','Quinn','Avery','Skyler','Reese','Cameron','Hayden','Parker','Rowan','Sage','Emery','Finley','Blake','Harper','Aiden','Mia','Noah','Zara','Eli','Iris','Owen','Maya','Leo','Nora','Theo','Ava','Ezra','Lily'];
  const lastNames  = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Wilson','Moore','Taylor','Anderson','Thomas','Jackson','White','Harris','Martin','Thompson','Clark','Lewis','Patel','Chen','Khan','Singh','Wright','Kelly','Hughes','Wood','Bell','Ward'];
  const rows = 5, cols = 6;
  let n = 0;
  grid.innerHTML = '';
  for (let r = 0; r < rows; r++) {
    const row = document.createElement('div');
    row.className = 'sp-row';
    const tiles = document.createElement('div');
    tiles.className = 'sp-row-tiles';
    tiles.style.gridTemplateColumns = `repeat(${cols}, 1fr)`;
    for (let c = 0; c < cols; c++) {
      const empty = (r === 2 && c === 4);
      const tile = document.createElement('div');
      if (empty) {
        tile.className = 'sp-tile sp-empty';
      } else {
        const first = firstNames[n % firstNames.length];
        const last = lastNames[(n * 7) % lastNames.length];
        tile.className = 'sp-tile sp-occupied';
        tile.style.cssText = 'padding:14px 8px;text-align:center;background:#fff;border:1px solid #e5e7eb;border-radius:10px';
        tile.innerHTML = `<div style="font-weight:600;font-size:0.92rem;color:#1f2937">${last}, ${first}</div>`;
        n++;
      }
      tiles.appendChild(tile);
    }
    row.appendChild(tiles);
    grid.appendChild(row);
  }
  if (pool) {
    pool.innerHTML = '';
    // Add a few unseated pupils
    for (let i = 0; i < 4; i++) {
      const first = firstNames[(n + i) % firstNames.length];
      const last = lastNames[((n + i) * 7) % lastNames.length];
      const chip = document.createElement('div');
      chip.style.cssText = 'padding:8px 10px;background:#fff;border:1px solid #e5e7eb;border-radius:8px;margin-bottom:6px;font-size:0.9rem;color:#1f2937';
      chip.textContent = `${last}, ${first}`;
      pool.appendChild(chip);
    }
    const count = document.getElementById('sp-unseated-count');
    if (count) count.textContent = '4';
  }
}"""

PAGES = [
    ("dashboard", "/"),
    ("detentions", "/teachers/detentions"),
    ("new_detention", "/teachers/new_detention"),
    ("behaviour_points", "/behaviour-points"),
    ("seating_plans", "/seating-plans"),
    ("warnings", "/warnings"),
    ("analytics", "/admin/analytics"),
    ("students", "/admin/students"),
    ("teachers", "/admin/teachers"),
    ("surveys", "/admin/surveys"),
]

def main():
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()

        # Login
        page.goto(f"{BASE}/session/new")
        page.fill('#email_address', EMAIL)
        page.fill('#password', PASSWORD)
        page.click('input.login-button')
        page.wait_for_load_state("networkidle")
        print(f"Logged in, URL: {page.url}")

        if False:  # disabled — logging in as KES admin directly
            pass
        # Impersonate KES admin — submit form directly (KES is the school with admins)
        if "/schools" in page.url:
            forms_info = page.evaluate("""() => {
              return [...document.querySelectorAll('form')].map((f, i) => ({
                idx: i,
                action: f.action,
                hasOpenAdmin: !!f.querySelector('button, input[type=submit]')?.innerText?.includes('Open as admin') ||
                              [...f.querySelectorAll('button')].some(b => b.innerText.includes('Open as admin'))
              }));
            }""")
            print("Forms:", forms_info[:5])
            # Find form that POSTs to /schools/<id>/impersonate with role=admin
            page.evaluate("""() => {
              // Find impersonate form where the button text mentions admin
              for (const f of document.querySelectorAll('form[action*="/impersonate"]')) {
                const txt = f.innerText || '';
                if (txt.includes('Open as admin')) { f.submit(); return; }
              }
            }""")
            page.wait_for_load_state("networkidle", timeout=15000)
            print(f"After impersonate, URL: {page.url}")

        for name, path in PAGES:
            try:
                page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=15000)
                page.wait_for_timeout(1000)
                # Inject seating dummies for the relevant pages BEFORE anonymisation
                if name == "behaviour_points":
                    page.evaluate(BP_SEED_JS)
                    page.wait_for_timeout(300)
                elif name == "seating_plans":
                    page.evaluate(SP_SEED_JS)
                    page.wait_for_timeout(300)
                # Replace school header logo with a banner that matches the header navy
                page.evaluate(r"""() => {
                  const headerColor = '#003366';
                  const svg = `data:image/svg+xml;utf8,${encodeURIComponent(`
                    <svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 200' preserveAspectRatio='xMidYMid slice'>
                      <rect width='1200' height='200' fill='${headerColor}'/>
                      <text x='600' y='118' text-anchor='middle'
                            font-family='Inter, Helvetica, Arial, sans-serif'
                            font-size='52' font-weight='700' fill='#ffffff'
                            letter-spacing='-0.5'>Oakland High</text>
                    </svg>
                  `)}`;
                  document.querySelectorAll('#logo img').forEach(img => {
                    img.src = svg;
                    img.style.height = '160px';
                    img.style.background = headerColor;
                  });
                  // Rename "Admin Test School" -> "Oakland High" anywhere it appears
                  (function walk(n){
                    if (n.nodeType === 3) {
                      n.textContent = n.textContent.replace(/Admin Test School/g, 'Oakland High');
                    } else if (n.nodeType === 1 && !['SCRIPT','STYLE'].includes(n.tagName)) {
                      n.childNodes.forEach(walk);
                    }
                  })(document.body);
                }""")
                # Anonymise visible PII via JS
                page.evaluate("""() => {
                  const firstNames = ['Alex','Jordan','Sam','Taylor','Morgan','Casey','Riley','Jamie','Drew','Quinn','Avery','Skyler','Reese','Cameron','Hayden','Parker','Rowan','Sage','Emery','Finley'];
                  const lastNames  = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Wilson','Moore','Taylor','Anderson','Thomas','Jackson','White','Harris','Martin','Thompson','Clark','Lewis'];
                  const used = new Map();
                  let nameI = 0;
                  function fakeName(orig) {
                    if (used.has(orig)) return used.get(orig);
                    const f = firstNames[nameI % firstNames.length];
                    const l = lastNames[(nameI*7) % lastNames.length];
                    nameI++;
                    const v = `${f} ${l}`;
                    used.set(orig, v);
                    return v;
                  }
                  const emailMap = new Map();
                  let emailI = 0;
                  function fakeEmail(orig) {
                    if (emailMap.has(orig)) return emailMap.get(orig);
                    emailI++;
                    const v = `student${emailI}@school.example`;
                    emailMap.set(orig, v);
                    return v;
                  }

                  // Replace real school name
                  function walk(node) {
                    if (node.nodeType === 3) {
                      let t = node.textContent;
                      // Anonymise KES references
                      t = t.replace(/King Edward VI/gi, 'Example Academy');
                      t = t.replace(/\\bKES\\b/g, 'Example Academy');
                      t = t.replace(/@kes\\.net/gi, '@school.example');
                      t = t.replace(/@abraxor\\.com/gi, '@school.example');
                      // Replace any email
                      t = t.replace(/[\\w.\\-+]+@[\\w.\\-]+\\.[a-z]{2,}/gi, m => fakeEmail(m.toLowerCase()));
                      // Replace any phone-like
                      t = t.replace(/\\b07\\d{9}\\b/g, '07700 900000');
                      // Anonymise KES house/VTG names ("Dyson 4" -> "Room 4", etc.)
                      t = t.replace(/\\b(Dyson|Fitzmaurice|Spender|Warneford)\\s+(\\d+)\\b/g, 'Room $2');
                      t = t.replace(/\\b(Dyson|Fitzmaurice|Spender|Warneford)\\b/g, 'Room');
                      // Replace inline "Lastname, Firstname" patterns
                      t = t.replace(/\\b([A-Z][a-z'\\-]{2,}), ([A-Z][a-z'\\-]{2,})\\b/g, (m, last, first) => {
                        const fn = fakeName(m);
                        const [ff, fl] = fn.split(' ');
                        return `${fl}, ${ff}`;
                      });
                      node.textContent = t;
                    } else if (node.nodeType === 1) {
                      // Tags to skip
                      if (['SCRIPT','STYLE'].includes(node.tagName)) return;
                      node.childNodes.forEach(walk);
                    }
                  }
                  walk(document.body);

                  // Anonymise <option> text (Cover Teacher dropdowns etc.)
                  document.querySelectorAll('option').forEach(o => {
                    const t = (o.textContent || '').trim();
                    if (/^[A-Z][a-z'\\-]+( [A-Z][a-z'\\-]+){1,2}$/.test(t)) {
                      o.textContent = fakeName(t);
                    }
                  });
                  // Replace anchors that link to student records
                  const STUDENT_HREF = /(students|pupils|user|teacher)s?\\/\\d+/;
                  document.querySelectorAll('a').forEach(a => {
                    const txt = a.innerText.trim();
                    const href = a.getAttribute('href') || '';
                    if (STUDENT_HREF.test(href) && /^[A-Z][a-z\\'-]+( [A-Z][a-z\\'-]+){1,2}$/.test(txt)) {
                      a.innerText = fakeName(txt);
                    }
                  });
                  // Replace bare text nodes that look like "Firstname Lastname" or "Lastname, Firstname"
                  document.querySelectorAll('td, strong, li, .student-name, .student-link, .seat-card, .student-chip, .unseated-student').forEach(el => {
                    el.childNodes.forEach(n => {
                      if (n.nodeType === 3) {
                        const t = n.textContent.trim();
                        // "Lastname, Firstname"
                        const m = t.match(/^([A-Z][a-z\\'-]+), ([A-Z][a-z\\'-]+)$/);
                        if (m) {
                          const fn = fakeName(t);
                          const [first, last] = fn.split(' ');
                          n.textContent = n.textContent.replace(t, `${last}, ${first}`);
                        } else if (/^[A-Z][a-z\\'-]+( [A-Z][a-z\\'-]+){1,2}$/.test(t)) {
                          n.textContent = n.textContent.replace(t, fakeName(t));
                        }
                      }
                    });
                  });
                  // Older catch-all from before
                  document.querySelectorAll('td, strong').forEach(el => {
                    el.childNodes.forEach(n => {
                      if (n.nodeType === 3) {
                        const t = n.textContent.trim();
                        if (/^[A-Z][a-z\\'-]+( [A-Z][a-z\\'-]+){1,2}$/.test(t)) {
                          n.textContent = n.textContent.replace(t, fakeName(t));
                        }
                      }
                    });
                  });
                  // Replace any "First Last" patterns in cells next to student emails
                  document.querySelectorAll('td, div, span, strong').forEach(el => {
                    // pattern: two capitalised words = name, leave alone unless looks like real student.
                  });
                }""")
                page.screenshot(path=f"{OUT}/{name}.png", full_page=True)
                print(f"  ✓ {name} -> {path}")
            except Exception as e:
                print(f"  ✗ {name}: {e}")

        browser.close()

if __name__ == "__main__":
    main()
