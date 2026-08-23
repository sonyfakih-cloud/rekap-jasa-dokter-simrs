import json, os

# Baris rinci per-kunjungan (tDetail/oDetail, ~443rb + ~328rb baris) membuat index.html
# jauh melewati batas ukuran file yang bisa dipublish (Artifact, 16MB) maupun dikirim sbg
# lampiran (SendUserFile, 30MB) -- dan kalau di-host di GitHub Pages PUBLIK, baris rinci
# ini berisi No RM & Nama Pasien yang TIDAK boleh ikut publik. Data rinci itu tetap ada
# lengkap di data_source/data_v5.json (dipakai oleh export_detail_excel.py utk membuat
# file .xlsx terpisah yg TIDAK di-commit ke git); di sini kita KELUARKAN dari dashboard
# interaktif supaya index.html tetap ringan & aman utk di-host publik.
INCLUDE_ROW_DETAIL = False

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.join(SCRIPT_DIR, '..')
DATA_PATH = os.path.join(REPO_ROOT, 'data_source', 'data_v5.json')
OUTPUT_PATH = os.path.join(REPO_ROOT, 'index.html')

data = json.load(open(DATA_PATH, encoding='utf-8'))
if not INCLUDE_ROW_DETAIL:
    data.pop('tDetail', None)
    data.pop('oDetail', None)
    data['dict'].pop('rm', None)
    data['dict'].pop('pasien', None)
    data['dict'].pop('no_penjualan', None)
data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

html = r"""<title>Rekam Jasa Dokter</title>
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  /* corporate SaaS palette: periwinkle-blue / mint-teal / amber / rose, white cards on a soft blue-lavender wash */
  --bg:#eef1fb;
  --bg-grad-1:#e9edfb;
  --bg-grad-2:#f5f7fd;
  --bg-grad-3:#ffffff;
  --dot-color:rgba(85,112,224,0.16);
  --surface:#ffffff;
  --surface-2:#f1f3fb;
  --surface-3:#e4e8f7;
  --border:#dde3f5;
  --text:#1c2541;
  --text-muted:#64708f;
  --text-faint:#97a1c2;
  --accent:#93a8f5;
  --accent-strong:#5570e0;
  --accent-soft:#eef1fd;
  --accent-soft-2:#dde4fb;
  --sage:#7ddfc0;
  --sage-strong:#16a480;
  --sage-soft:#e3f9f1;
  --yellow:#f7c876;
  --yellow-strong:#d99a2e;
  --yellow-soft:#fdf1dc;
  --warn:#f3a7c8;
  --warn-strong:#c85586;
  --warn-soft:#fceef5;
  --marquee-bg-1:#6f93b8;
  --marquee-bg-2:#45688c;
  --marquee-bg-3:#6f93b8;
  --marquee-text:#f6fafd;
  --marquee-shadow:rgba(20,35,55,0.4);
  --shadow: 0 1px 0 rgba(255,255,255,0.75) inset, 0 14px 28px -18px rgba(70,90,190,0.28), 0 2px 6px rgba(70,90,190,0.10);
  --shadow-inset: inset 0 2px 5px rgba(70,90,190,0.10), inset 0 -1px 0 rgba(255,255,255,0.65);
  --shadow-pressed: 0 1px 0 rgba(255,255,255,0.5) inset, 0 8px 16px -10px rgba(60,80,180,0.35), 0 2px 4px rgba(60,80,180,0.20);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#10152a; --bg-grad-1:#12172c; --bg-grad-2:#0f1326; --bg-grad-3:#0d1022; --dot-color:rgba(147,168,245,0.14);
    --surface:#171d38; --surface-2:#1e2545; --surface-3:#272f57; --border:#333d6c;
    --text:#e7ebfa; --text-muted:#aab2d6; --text-faint:#7982ac;
    --accent:#93a8f5; --accent-strong:#b7c5fa; --accent-soft:#23294a; --accent-soft-2:#2c3358;
    --sage:#6fdcb9; --sage-strong:#9df0d2; --sage-soft:#173a2f;
    --yellow:#f0c169; --yellow-strong:#f6d795; --yellow-soft:#3a2d16;
    --warn:#f2a0c5; --warn-strong:#f7bcda; --warn-soft:#3a1f2e;
    --marquee-bg-1:#3c5876; --marquee-bg-2:#233850; --marquee-bg-3:#3c5876; --marquee-text:#e7eef7; --marquee-shadow:rgba(0,0,0,0.5);
    --shadow: 0 1px 0 rgba(255,255,255,0.05) inset, 0 12px 24px -14px rgba(0,0,0,0.55), 0 3px 6px rgba(0,0,0,0.35);
    --shadow-inset: inset 0 2px 5px rgba(0,0,0,0.4), inset 0 -1px 0 rgba(255,255,255,0.04);
    --shadow-pressed: 0 1px 0 rgba(255,255,255,0.08) inset, 0 8px 16px -8px rgba(0,0,0,0.55), 0 2px 4px rgba(0,0,0,0.4);
  }
}
:root[data-theme="dark"]{
  --bg:#10152a; --bg-grad-1:#12172c; --bg-grad-2:#0f1326; --bg-grad-3:#0d1022; --dot-color:rgba(147,168,245,0.14);
  --surface:#171d38; --surface-2:#1e2545; --surface-3:#272f57; --border:#333d6c;
  --text:#e7ebfa; --text-muted:#aab2d6; --text-faint:#7982ac;
  --accent:#93a8f5; --accent-strong:#b7c5fa; --accent-soft:#23294a; --accent-soft-2:#2c3358;
  --sage:#6fdcb9; --sage-strong:#9df0d2; --sage-soft:#173a2f;
  --yellow:#f0c169; --yellow-strong:#f6d795; --yellow-soft:#3a2d16;
  --warn:#f2a0c5; --warn-strong:#f7bcda; --warn-soft:#3a1f2e;
  --marquee-bg-1:#3c5876; --marquee-bg-2:#233850; --marquee-bg-3:#3c5876; --marquee-text:#e7eef7; --marquee-shadow:rgba(0,0,0,0.5);
  --shadow: 0 1px 0 rgba(255,255,255,0.08) inset, 0 12px 24px -14px rgba(0,0,0,0.55), 0 3px 6px rgba(0,0,0,0.35);
  --shadow-inset: inset 0 2px 5px rgba(0,0,0,0.4), inset 0 -1px 0 rgba(255,255,255,0.04);
  --shadow-pressed: 0 1px 0 rgba(255,255,255,0.08) inset, 0 8px 16px -8px rgba(0,0,0,0.55), 0 2px 4px rgba(0,0,0,0.4);
}
*{box-sizing:border-box;}
html,body{margin:0;padding:0;}
body{
  background-color:var(--bg);
  background-image:
    radial-gradient(900px 520px at 100% -8%, rgba(147,168,245,0.22), transparent 60%),
    linear-gradient(150deg, var(--bg-grad-1) 0%, var(--bg-grad-2) 55%, var(--bg-grad-3) 100%);
  background-attachment:fixed;
  color:var(--text);
  font-family:"Public Sans", -apple-system, "Segoe UI", sans-serif;
  font-size:14px; line-height:1.45; -webkit-font-smoothing:antialiased;
  position:relative;
}
body::before{
  content:''; position:fixed; top:0; right:0; width:400px; height:400px;
  background-image:radial-gradient(var(--dot-color) 1.6px, transparent 1.6px);
  background-size:22px 22px;
  -webkit-mask-image:radial-gradient(circle at 100% 0%, black 0%, transparent 65%);
  mask-image:radial-gradient(circle at 100% 0%, black 0%, transparent 65%);
  pointer-events:none; z-index:0;
}
.mono{ font-family:"IBM Plex Mono", ui-monospace, monospace; font-variant-numeric: tabular-nums; }

.page{ position:relative; z-index:1; max-width:1180px; margin:0 auto; padding:22px 28px 60px; }
@media (max-width: 620px){ .page{ padding:16px 14px 40px; } }

@keyframes fade-slide-in{ from{ opacity:0; transform:translateY(10px); } to{ opacity:1; transform:translateY(0); } }
@keyframes soft-glow-pulse{
  0%, 100% { box-shadow:var(--shadow-pressed), 0 0 0 0 rgba(85,112,224,0.35); }
  50% { box-shadow:var(--shadow-pressed), 0 0 0 7px rgba(85,112,224,0); }
}

/* ---------- Copyright marquee (single line, soft sweep, steel blue) ---------- */
.marquee-bar{
  position:relative; z-index:1; width:100%; height:30px; overflow:hidden;
  background:linear-gradient(90deg, var(--marquee-bg-1) 0%, var(--marquee-bg-2) 50%, var(--marquee-bg-3) 100%);
  border-bottom:1px solid var(--marquee-bg-2);
  box-shadow:inset 0 2px 5px rgba(0,0,0,0.18), inset 0 -1px 0 rgba(255,255,255,0.08), 0 2px 8px -2px var(--marquee-shadow);
}
.marquee-text{
  position:absolute; top:50%; left:0%;
  transform:translate(-100%, -50%);
  white-space:nowrap; pointer-events:none;
  font-family:"IBM Plex Mono", ui-monospace, monospace;
  font-size:11px; font-weight:600; letter-spacing:0.08em; text-transform:uppercase;
  color:var(--marquee-text);
  text-shadow:0 1px 2px var(--marquee-shadow);
  animation:marquee-sweep 18s cubic-bezier(0.42,0,0.58,1) infinite;
  will-change:left, transform, opacity;
}
@keyframes marquee-sweep{
  0%   { left:0%;   transform:translate(-100%, -50%); opacity:0; }
  6%   { opacity:0.85; }
  50%  { opacity:0.85; }
  94%  { opacity:0.85; }
  100% { left:100%; transform:translate(0%, -50%); opacity:0; }
}
@media (prefers-reduced-motion: reduce){
  .marquee-bar{ height:auto; padding:7px 0; display:flex; align-items:center; justify-content:center; }
  .marquee-text{ position:static; left:auto; transform:none; animation:none; opacity:0.85; }
}

/* ---------- Header ---------- */
.app-header{ display:flex; align-items:flex-start; justify-content:space-between; gap:16px; margin-bottom:16px; }
.brand .eyebrow{ font-size:11px; letter-spacing:0.08em; text-transform:uppercase; color:var(--accent); font-weight:700; }
.brand h1{ font-size:22px; margin:2px 0 0; font-weight:800; letter-spacing:-0.01em; text-shadow:0 1px 0 rgba(255,255,255,0.6); }
.brand p{ margin:4px 0 0; font-size:12.5px; color:var(--text-muted); }

.theme-toggle{
  display:inline-flex; align-items:center; gap:3px; border:1px solid var(--border);
  background:linear-gradient(180deg, var(--surface-2), var(--surface-3));
  box-shadow:var(--shadow-inset);
  border-radius:999px; padding:3px; flex-shrink:0;
}
.theme-toggle button{
  border:none; background:none; cursor:pointer; padding:6px 8px; border-radius:999px; display:flex;
  align-items:center; justify-content:center; color:var(--text-faint);
  transition:transform .15s ease, box-shadow .15s ease, background .15s ease;
}
.theme-toggle button svg{ width:14px; height:14px; }
.theme-toggle button.active{
  background:linear-gradient(180deg, var(--surface), var(--surface-2)); color:var(--accent-strong);
  box-shadow:0 1px 0 rgba(255,255,255,0.6) inset, 0 3px 6px -2px rgba(70,90,190,0.25); transform:translateY(-1px);
}

.header-actions{ display:flex; align-items:center; gap:10px; flex-shrink:0; flex-wrap:wrap; }
.logout-btn{
  display:inline-flex; align-items:center; gap:6px; border:1px solid var(--border); font-family:inherit;
  background:linear-gradient(180deg, var(--surface), var(--surface-2)); color:var(--text-muted);
  border-radius:999px; padding:8px 14px; font-size:12px; font-weight:700; cursor:pointer;
  box-shadow:var(--shadow-inset); transition:color .15s ease, box-shadow .15s ease, transform .15s ease;
}
.logout-btn:hover{ color:var(--warn-strong); box-shadow:0 1px 0 rgba(255,255,255,0.6) inset, 0 3px 6px -2px rgba(200,85,134,0.3); transform:translateY(-1px); }
.logout-btn svg{ width:14px; height:14px; }

/* ---------- Tab bar ---------- */
.tab-bar{ display:flex; gap:10px; margin-bottom:18px; flex-wrap:wrap; }
.tab-btn{
  display:inline-flex; align-items:center; gap:10px;
  border:1px solid var(--border); color:var(--text-muted); font-family:inherit;
  background:linear-gradient(180deg, var(--surface), var(--surface-2));
  box-shadow:var(--shadow);
  font-size:12.5px; font-weight:700; padding:8px 18px 8px 8px; border-radius:999px; cursor:pointer;
  transition:transform .15s ease, box-shadow .15s ease, color .15s ease;
}
.tab-btn:hover{ color:var(--text); transform:translateY(-2px); }
.tab-btn.active{
  background:linear-gradient(180deg, var(--accent) 0%, var(--accent-strong) 100%);
  color:#fff; border-color:var(--accent-strong);
  box-shadow:var(--shadow-pressed);
  transform:translateY(-1px);
  animation:soft-glow-pulse 2.6s ease-in-out infinite;
}
@media (prefers-reduced-motion: reduce){ .tab-btn.active{ animation:none; } }

.tab-icon{
  width:28px; height:28px; flex-shrink:0; border-radius:9px;
  display:flex; align-items:center; justify-content:center;
  background:linear-gradient(155deg, var(--accent-soft) 0%, var(--accent-soft-2) 100%);
  color:var(--accent-strong);
  box-shadow:0 1px 0 rgba(255,255,255,0.7) inset, 0 3px 7px -3px rgba(70,90,190,0.4);
  transition:transform .4s cubic-bezier(0.34,1.56,0.64,1), background .25s ease, color .25s ease, box-shadow .25s ease;
  transform-style:preserve-3d; perspective:200px;
}
.tab-icon svg{ width:15px; height:15px; }
.tab-btn:hover .tab-icon{ transform:translateY(-1px) rotateY(20deg) scale(1.08); }
.tab-btn.active .tab-icon{
  background:linear-gradient(155deg, rgba(255,255,255,0.4), rgba(255,255,255,0.06));
  color:#fff;
  box-shadow:0 1px 0 rgba(255,255,255,0.55) inset, 0 4px 10px -3px rgba(25,35,100,0.55);
  animation:icon-pop .55s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes icon-pop{
  0%{ transform:scale(0.4) rotate(-30deg); opacity:0.3; }
  55%{ transform:scale(1.18) rotate(8deg); opacity:1; }
  100%{ transform:scale(1) rotate(0deg); }
}
@media (prefers-reduced-motion: reduce){
  .tab-icon{ transition:none; animation:none; }
  .tab-btn.active .tab-icon{ animation:none; }
  .tab-btn:hover .tab-icon{ transform:none; }
}

/* ---------- Control panel ---------- */
.control-panel{
  background:linear-gradient(165deg, var(--surface) 0%, var(--surface-2) 100%);
  border:1px solid var(--border); border-radius:14px; padding:16px 18px;
  box-shadow:var(--shadow); margin-bottom:22px; display:flex; flex-direction:column; gap:12px;
}
.control-field{ display:flex; flex-direction:column; gap:5px; }
.control-field label{ font-size:10.5px; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-faint); font-weight:700; }

.primary-row{ display:grid; grid-template-columns: 1fr 1.4fr; gap:12px; }
@media (max-width:700px){ .primary-row{ grid-template-columns: 1fr; } }
.primary-row-single{ grid-template-columns: minmax(0, 420px); }

.select-primary{
  padding:11px 14px !important; border-radius:9px !important; border:1.5px solid var(--border) !important;
  font-size:15px !important; font-weight:600 !important;
}
.select-primary:focus{ border-color:var(--accent) !important; }

.filters-row{ display:grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap:12px; }

.select-input, .date-input{
  width:100%; padding:8px 10px; border-radius:8px; border:1px solid var(--border);
  background:linear-gradient(180deg, var(--surface-2), var(--surface-3));
  box-shadow:var(--shadow-inset);
  color:var(--text); font-family:inherit; font-size:12.5px; outline:none; cursor:pointer;
}
.select-input:focus, .date-input:focus{ border-color:var(--accent); }
.date-range{ display:flex; align-items:center; gap:6px; }
.date-range .date-input{ cursor:text; }
.date-range span{ color:var(--text-faint); font-size:11.5px; }

/* ---------- Main content ---------- */
.topline{ display:flex; align-items:baseline; justify-content:space-between; gap:16px; flex-wrap:wrap; margin-bottom:22px; }
.topline h2{ font-size:24px; margin:0; font-weight:800; letter-spacing:-0.01em; text-wrap:balance; }
.topline .role-pill{
  display:inline-flex; align-items:center; gap:6px; font-size:11.5px; font-weight:700;
  padding:3px 10px; border-radius:999px;
  background:linear-gradient(180deg, var(--accent-soft), var(--accent-soft-2)); color:var(--accent-strong);
  box-shadow:0 1px 0 rgba(255,255,255,0.6) inset, 0 2px 5px -2px rgba(85,112,224,0.35);
  text-transform:uppercase; letter-spacing:0.04em; margin-left:10px; vertical-align:middle;
}
.subline{ color:var(--text-muted); font-size:13px; margin-top:4px; }

.kpi-row{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:22px; }
@media (max-width:900px){ .kpi-row{ grid-template-columns:repeat(2,1fr); } }
@media (max-width:560px){ .kpi-row{ grid-template-columns:1fr; } }
.kpi{
  background:linear-gradient(160deg, var(--surface) 0%, var(--surface-2) 100%);
  border:1px solid var(--border); border-radius:12px; padding:14px 16px; box-shadow:var(--shadow);
  transition:transform .18s ease, box-shadow .18s ease;
  animation:fade-slide-in .45s ease both;
}
.kpi:hover{ transform:translateY(-2px); box-shadow:var(--shadow), 0 0 0 1px var(--accent-soft-2); }
.kpi .k-label{ font-size:11px; text-transform:uppercase; letter-spacing:0.06em; color:var(--text-faint); font-weight:700; }
.kpi .k-value{ font-size:20px; font-weight:700; margin-top:6px; }
.kpi .k-value.accent{ color:var(--accent-strong); }

.section{ margin-bottom:26px; }
.section-head{ display:flex; align-items:baseline; justify-content:space-between; margin-bottom:10px; gap:12px; flex-wrap:wrap; }
.section-head h3{ font-size:14.5px; margin:0; font-weight:700; }
.section-head .count-tag{ font-size:11.5px; color:var(--text-faint); }

.jasa-grid{ display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }
@media (max-width:700px){ .jasa-grid{ grid-template-columns:1fr; } }
.jasa-card{
  background:linear-gradient(160deg, var(--surface) 0%, var(--surface-2) 100%);
  border:1px solid var(--border); border-radius:10px; padding:12px 14px; display:flex; flex-direction:column; gap:8px;
  box-shadow:var(--shadow);
  animation:fade-slide-in .45s ease both;
}
.jasa-card .j-label{ font-size:11.5px; color:var(--text-muted); font-weight:600; }
.jasa-card .j-value{ font-size:15.5px; font-weight:700; }
.j-bar-track{ height:7px; border-radius:999px; background:var(--surface-3); box-shadow:var(--shadow-inset); overflow:hidden; }
.j-bar-fill{
  height:100%; border-radius:999px;
  background:linear-gradient(180deg, var(--accent-soft-2) 0%, var(--accent) 45%, var(--accent-strong) 100%);
  box-shadow:0 1px 0 rgba(255,255,255,0.4) inset;
}
/* per-jasa color differentiation across the soft palette */
.jasa-card[data-jasa="japel"] .j-bar-fill{ background:linear-gradient(180deg, var(--accent-soft-2) 0%, var(--accent) 45%, var(--accent-strong) 100%); }
.jasa-card[data-jasa="japel"] .j-value{ color:var(--accent-strong); }
.jasa-card[data-jasa="j_sarrs"] .j-bar-fill{ background:linear-gradient(180deg, var(--sage-soft) 0%, var(--sage) 45%, var(--sage-strong) 100%); }
.jasa-card[data-jasa="j_sarrs"] .j-value{ color:var(--sage-strong); }
.jasa-card[data-jasa="operator"] .j-bar-fill{ background:linear-gradient(180deg, var(--yellow-soft) 0%, var(--yellow) 45%, var(--yellow-strong) 100%); }
.jasa-card[data-jasa="operator"] .j-value{ color:var(--yellow-strong); }
.jasa-card[data-jasa="anestesi"] .j-bar-fill{ background:linear-gradient(180deg, var(--warn-soft) 0%, var(--warn) 45%, var(--warn-strong) 100%); }
.jasa-card[data-jasa="anestesi"] .j-value{ color:var(--warn-strong); }
.jasa-card[data-jasa="team"] .j-bar-fill{ background:linear-gradient(135deg, var(--sage) 0%, var(--accent) 55%, var(--accent-strong) 100%); }
.jasa-card[data-jasa="team"] .j-value{ color:var(--accent-strong); }

.tables-grid{ display:grid; grid-template-columns:1.4fr 1fr; gap:16px; align-items:start; }
@media (max-width:980px){ .tables-grid{ grid-template-columns:1fr; } }

.spec-doctor-card{ padding:20px 0; border-top:1px solid var(--border); }
.spec-doctor-card:first-child{ padding-top:4px; border-top:none; }
.spec-doctor-head{ display:flex; align-items:baseline; justify-content:space-between; gap:12px; margin-bottom:12px; flex-wrap:wrap; }
.spec-doctor-head h4{ margin:0; font-size:14.5px; font-weight:700; color:var(--text); }

.panel{
  background:linear-gradient(160deg, var(--surface) 0%, var(--surface-2) 100%);
  border:1px solid var(--border); border-radius:12px; overflow:hidden; box-shadow:var(--shadow); display:flex; flex-direction:column;
  animation:fade-slide-in .5s ease both;
}
.panel-head{ padding:12px 14px 10px; border-bottom:1px solid var(--border); }
.panel-head h4{ margin:0 0 8px; font-size:13px; font-weight:700; display:flex; align-items:center; gap:6px; flex-wrap:wrap; }
.panel-head h4 .dot{
  width:8px; height:8px; border-radius:50%; display:inline-block;
  background:radial-gradient(circle at 30% 30%, var(--accent-soft-2), var(--accent) 55%, var(--accent-strong));
  box-shadow:0 1px 2px rgba(0,0,0,0.2);
}
.mini-search{
  width:100%; padding:6px 9px; border-radius:7px; border:1px solid var(--border);
  background:linear-gradient(180deg, var(--surface-2), var(--surface-3)); box-shadow:var(--shadow-inset);
  color:var(--text); font-size:12px; font-family:inherit; outline:none;
}
.mini-search:focus{ border-color:var(--accent); }

.scroll-body{ max-height:400px; overflow-y:auto; }
.table-wrap{ overflow-x:auto; }
table{ width:100%; border-collapse:collapse; font-size:12.5px; }
thead th{
  position:sticky; top:0; background:linear-gradient(180deg, var(--surface) 0%, var(--surface-2) 100%);
  text-align:left; font-size:10.5px; text-transform:uppercase;
  letter-spacing:0.04em; color:var(--text-faint); font-weight:700; padding:8px 10px; border-bottom:1px solid var(--border);
  cursor:pointer; user-select:none; white-space:nowrap; transition:color .15s ease;
}
thead th:hover{ color:var(--accent-strong); }
thead th .arrow{ font-size:9px; margin-left:3px; opacity:0.6; }
tbody td{ padding:7px 10px; border-bottom:1px solid var(--border); vertical-align:top; }
tbody tr:last-child td{ border-bottom:none; }
tbody tr:hover{ background:var(--surface-2); }
td.num, th.num{ text-align:right; font-family:"IBM Plex Mono", monospace; font-variant-numeric: tabular-nums; white-space:nowrap; }
.name-cell{ max-width:260px; }
.subklas-cell{ color:var(--text-muted); font-size:11.5px; white-space:nowrap; }
.anes-cell{ white-space:nowrap; }
.anes-badge{
  display:inline-flex; align-items:center; gap:5px; padding:3px 8px; border-radius:999px;
  background:linear-gradient(180deg, var(--warn-soft) 0%, rgba(200,85,134,0.14) 100%);
  border:1px solid rgba(200,85,134,0.28); color:var(--warn-strong);
  font-size:11px; font-weight:600; white-space:nowrap;
}
.anes-badge::before{
  content:''; width:6px; height:6px; border-radius:50%; flex:none;
  background:radial-gradient(circle at 30% 30%, var(--warn-soft), var(--warn) 55%, var(--warn-strong));
}
.anes-none{ color:var(--text-faint); }
.empty-row td{ text-align:center; color:var(--text-faint); padding:18px; font-style:italic; }

.panel-toolbar{
  display:flex; align-items:center; gap:10px; flex-wrap:wrap;
  padding:12px 14px 10px; border-bottom:1px solid var(--border);
}
.panel-toolbar .mini-search{ flex:1; min-width:200px; }
.export-btn{
  display:inline-flex; align-items:center; gap:6px; padding:7px 14px; border-radius:8px; border:none;
  background:linear-gradient(180deg, var(--accent) 0%, var(--accent-strong) 100%); color:#fff;
  font-family:inherit; font-size:12px; font-weight:700; cursor:pointer; white-space:nowrap;
  box-shadow:0 2px 6px -2px rgba(70,90,190,0.5), 0 1px 0 rgba(255,255,255,0.25) inset;
  transition:transform .15s ease, box-shadow .15s ease;
}
.export-btn:hover{ transform:translateY(-1px); box-shadow:0 4px 10px -3px rgba(70,90,190,0.6), 0 1px 0 rgba(255,255,255,0.25) inset; }
.export-btn:active{ transform:translateY(0); }
.export-btn svg{ width:13px; height:13px; flex:none; }
.pager{
  display:flex; align-items:center; justify-content:space-between; gap:10px; flex-wrap:wrap;
  padding:10px 14px; border-top:1px solid var(--border); font-size:11.5px; color:var(--text-muted);
}
.pager-nav{ display:flex; gap:6px; }
.pager-btn{
  border:1px solid var(--border); background:linear-gradient(180deg, var(--surface-2), var(--surface-3));
  color:var(--text); border-radius:6px; padding:5px 10px; cursor:pointer; font-family:inherit; font-size:11.5px;
}
.pager-btn:disabled{ opacity:0.4; cursor:not-allowed; }
.pager-btn:not(:disabled):hover{ border-color:var(--accent); color:var(--accent-strong); }
.delta-up{ color:var(--sage-strong); }
.delta-down{ color:var(--warn-strong); }

/* ---------- Charts ---------- */
.rank-chart{
  display:flex; flex-direction:column; gap:10px;
  background:linear-gradient(165deg, var(--surface) 0%, var(--surface-2) 100%);
  border:1px solid var(--border); border-radius:14px; padding:18px 20px; box-shadow:var(--shadow);
  animation:fade-slide-in .5s ease both;
}
.rank-row{ display:grid; grid-template-columns: 220px 1fr 120px; align-items:center; gap:10px; }
@media (max-width:700px){ .rank-row{ grid-template-columns: 130px 1fr 90px; } }
.rank-name{ font-size:12.5px; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.rank-track{ height:15px; background:var(--surface-3); border-radius:999px; box-shadow:var(--shadow-inset); overflow:hidden; }
.rank-fill{
  position:relative; height:100%; border-radius:999px; overflow:hidden;
  background:linear-gradient(180deg, var(--accent-soft-2) 0%, var(--accent) 48%, var(--accent-strong) 100%);
  box-shadow:0 2px 6px -2px rgba(85,112,224,0.42);
}
.rank-fill::after{
  content:''; position:absolute; top:0; left:0; right:0; height:45%;
  background:linear-gradient(180deg, rgba(255,255,255,0.6), rgba(255,255,255,0));
}
.rank-value{ font-size:11.5px; text-align:right; white-space:nowrap; }
.rank-row:first-child .rank-name{ color:var(--accent-strong); }

.trend-chart-wrap{
  background:linear-gradient(165deg, var(--surface) 0%, var(--surface-2) 100%);
  border:1px solid var(--border); border-radius:14px; padding:16px 18px 8px;
  box-shadow:var(--shadow); animation:fade-slide-in .5s ease both;
}
.trend-svg{ width:100%; height:auto; display:block; overflow:visible; }
.trend-grid-line{ stroke:var(--border); stroke-width:1; stroke-dasharray:3 4; }
.trend-axis-label{ font-family:"IBM Plex Mono", monospace; font-size:9.5px; fill:var(--text-faint); }
.trend-value-label{ font-family:"IBM Plex Mono", monospace; font-size:10.5px; font-weight:700; fill:var(--text); }
.trend-month-label{ font-family:"Public Sans", sans-serif; font-size:10.5px; fill:var(--text-faint); }
.trend-delta{ font-family:"Public Sans", sans-serif; font-size:10px; font-weight:700; }
.trend-delta-up{ fill:var(--sage-strong); }
.trend-delta-down{ fill:var(--warn-strong); }
.trend-empty{ text-align:center; color:var(--text-faint); font-style:italic; padding:30px; }

/* ---------- Grafik Batang: Poin per Tindakan (menu Perbandingan Spesialisasi) ---------- */
.bar2d-chart-wrap{
  background:linear-gradient(165deg, var(--surface) 0%, var(--surface-2) 100%);
  border:1px solid var(--border); border-radius:14px; padding:18px 20px 10px;
  box-shadow:var(--shadow); animation:fade-slide-in .5s ease both; overflow-x:auto;
}
.bar2d-svg{ display:block; max-width:none; }
.bar2d-item{ cursor:default; }
.bar2d-name-label{ font-family:"Public Sans", sans-serif; font-size:10px; fill:var(--text-muted); }
.bar2d-value-label{ font-family:"IBM Plex Mono", monospace; font-size:11px; font-weight:700; fill:var(--text); }
.bar2d-empty{ text-align:center; color:var(--text-faint); font-style:italic; padding:30px; }
.bar2d-legend{ display:flex; flex-wrap:wrap; justify-content:center; gap:16px; padding:2px 0 14px; }
.bar2d-legend-item{ display:inline-flex; align-items:center; gap:6px; font-size:11.5px; color:var(--text-muted); font-weight:600; }
.bar2d-legend-swatch{ width:11px; height:11px; border-radius:3px; display:inline-block; box-shadow:0 1px 0 rgba(255,255,255,0.4) inset; }

.footnote{ margin-top:26px; font-size:11.5px; color:var(--text-faint); border-top:1px solid var(--border); padding-top:14px; }
.footnote code{ font-family:"IBM Plex Mono", monospace; background:var(--surface-2); padding:1px 5px; border-radius:4px; }

::-webkit-scrollbar{ width:9px; height:9px; }
::-webkit-scrollbar-thumb{ background:var(--surface-3); border-radius:6px; }
::-webkit-scrollbar-track{ background:transparent; }

@media (prefers-reduced-motion: no-preference){
  .j-bar-fill, .month-bar, .rank-fill{ transition: width 0.4s ease, height 0.4s ease; }
}
@media (prefers-reduced-motion: reduce){
  .kpi, .jasa-card, .panel, .rank-chart, .trend-chart-wrap{ animation:none; }
}

/* ---------- Auth gate ---------- */
.auth-gate{
  position:fixed; inset:0; z-index:9999; display:flex; align-items:center; justify-content:center;
  padding:24px; background:
    radial-gradient(circle at 18% 22%, var(--dot-color) 0, transparent 45%),
    linear-gradient(160deg, var(--bg-grad-1) 0%, var(--bg-grad-2) 55%, var(--bg-grad-3) 100%);
}
.auth-card{
  width:100%; max-width:360px; background:var(--surface); border:1px solid var(--border);
  border-radius:16px; padding:30px 28px 26px; box-shadow:var(--shadow);
  animation:fade-slide-in .4s ease both;
}
.auth-card .eyebrow{ display:block; font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase; color:var(--accent-strong); margin-bottom:6px; }
.auth-card h2{ margin:0 0 4px; font-size:19px; font-weight:800; color:var(--text); }
.auth-card p.auth-sub{ margin:0 0 20px; font-size:12.5px; color:var(--text-muted); line-height:1.5; }
.auth-field{ margin-bottom:14px; }
.auth-field label{ display:block; font-size:11.5px; font-weight:600; color:var(--text-muted); margin-bottom:6px; }
.auth-field input{
  width:100%; box-sizing:border-box; font:inherit; font-size:15px; letter-spacing:.02em;
  padding:11px 13px; border-radius:10px; border:1px solid var(--border); background:var(--surface-2);
  color:var(--text); box-shadow:var(--shadow-inset);
}
.auth-field input:focus{ outline:2px solid var(--accent); outline-offset:1px; }
.auth-code-input{ font-family:"IBM Plex Mono", monospace; letter-spacing:.35em; text-align:center; font-size:19px !important; }
.auth-submit{
  width:100%; margin-top:4px; padding:11px 14px; border-radius:10px; border:none; cursor:pointer;
  font:inherit; font-size:14px; font-weight:700; color:#fff;
  background:linear-gradient(180deg, var(--accent) 0%, var(--accent-strong) 100%);
  box-shadow:0 8px 18px -10px rgba(85,112,224,0.55);
}
.auth-submit:active{ box-shadow:var(--shadow-pressed); }
.auth-error{ min-height:16px; margin-top:10px; font-size:12px; font-weight:600; color:var(--warn-strong); }
.auth-back{ display:inline-block; margin-top:2px; font-size:12px; color:var(--text-muted); cursor:pointer; text-decoration:underline; background:none; border:none; padding:0; font:inherit; }
.auth-foot{ margin-top:18px; padding-top:14px; border-top:1px solid var(--border); font-size:10.5px; color:var(--text-faint); line-height:1.5; }
.auth-step{ display:none; }
.auth-step.active{ display:block; }
</style>

<div class="auth-gate" id="authGate">
  <div class="auth-card">
    <span class="eyebrow">SIMRS &middot; Remunerasi</span>
    <h2>Akses Terbatas</h2>
    <p class="auth-sub">Dashboard Rekam Jasa Dokter &mdash; masukkan kata sandi, lalu kode dari Google Authenticator.</p>

    <div class="auth-step active" id="authStepPw">
      <form id="authFormPw">
        <div class="auth-field">
          <label for="authPw">Kata Sandi</label>
          <input type="password" id="authPw" autocomplete="off" autocapitalize="off" spellcheck="false" />
        </div>
        <button type="submit" class="auth-submit">Lanjut</button>
        <div class="auth-error" id="authErrPw"></div>
      </form>
    </div>

    <div class="auth-step" id="authStepOtp">
      <form id="authFormOtp">
        <div class="auth-field">
          <label for="authOtp">Kode Google Authenticator (6 digit)</label>
          <input type="text" id="authOtp" class="auth-code-input" inputmode="numeric" pattern="[0-9]*" maxlength="6" autocomplete="off" />
        </div>
        <button type="submit" class="auth-submit">Masuk</button>
        <div class="auth-error" id="authErrOtp"></div>
      </form>
      <button type="button" class="auth-back" id="authBack">&larr; kembali</button>
    </div>

    <div class="auth-foot">Akses diingat di perangkat ini selama 24 jam.</div>
  </div>
</div>

<script>
(function(){
  var PW_HASH = 'e31fd44d519aedeb824ebebe477480707f045189866b22960839b062b87952f4';
  var TOTP_SECRET_B32 = 'MWNEX4WZRAACXG3OBSVVWBTXXKNUI3UO';
  var REMEMBER_MS = 24 * 60 * 60 * 1000;
  var REMEMBER_KEY = 'simrs_auth_until';

  function revealContent(){
    var mq = document.querySelector('.marquee-bar');
    var pg = document.querySelector('.page');
    if (mq) mq.style.display = '';
    if (pg) pg.style.display = '';
    var gate = document.getElementById('authGate');
    if (gate) gate.style.display = 'none';
    document.documentElement.style.overflow = '';
  }

  function isRemembered(){
    try {
      var until = parseInt(localStorage.getItem(REMEMBER_KEY) || '0', 10);
      return until > Date.now();
    } catch (e) { return false; }
  }

  function remember(){
    try { localStorage.setItem(REMEMBER_KEY, String(Date.now() + REMEMBER_MS)); } catch (e) {}
  }

  if (isRemembered()){
    // .marquee-bar / .page are declared further down in the HTML source (after this
    // script tag), so they don't exist in the DOM yet during synchronous parsing --
    // defer the reveal until the document has finished parsing.
    document.addEventListener('DOMContentLoaded', revealContent);
    return;
  }
  document.documentElement.style.overflow = 'hidden';

  async function sha256Hex(text){
    var enc = new TextEncoder().encode(text);
    var buf = await crypto.subtle.digest('SHA-256', enc);
    return Array.from(new Uint8Array(buf)).map(function(b){ return b.toString(16).padStart(2, '0'); }).join('');
  }

  function base32Decode(b32){
    var alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
    var clean = b32.toUpperCase().replace(/=+$/, '');
    var bits = '';
    for (var i = 0; i < clean.length; i++){
      var val = alphabet.indexOf(clean[i]);
      if (val === -1) continue;
      bits += val.toString(2).padStart(5, '0');
    }
    var bytes = [];
    for (var j = 0; j + 8 <= bits.length; j += 8){
      bytes.push(parseInt(bits.substring(j, j + 8), 2));
    }
    return new Uint8Array(bytes);
  }

  async function totpAt(unixSeconds){
    var key = await crypto.subtle.importKey('raw', base32Decode(TOTP_SECRET_B32), { name: 'HMAC', hash: 'SHA-1' }, false, ['sign']);
    var counter = Math.floor(unixSeconds / 30);
    var counterBuf = new ArrayBuffer(8);
    var view = new DataView(counterBuf);
    view.setUint32(0, Math.floor(counter / 0x100000000));
    view.setUint32(4, counter >>> 0);
    var sig = new Uint8Array(await crypto.subtle.sign('HMAC', key, counterBuf));
    var offset = sig[sig.length - 1] & 0x0f;
    var binCode = ((sig[offset] & 0x7f) << 24) | ((sig[offset + 1] & 0xff) << 16) | ((sig[offset + 2] & 0xff) << 8) | (sig[offset + 3] & 0xff);
    return String(binCode % 1000000).padStart(6, '0');
  }

  async function verifyTotp(code){
    var now = Math.floor(Date.now() / 1000);
    var candidates = [await totpAt(now), await totpAt(now - 30), await totpAt(now + 30)];
    return candidates.indexOf(code) !== -1;
  }

  var stepPw = document.getElementById('authStepPw');
  var stepOtp = document.getElementById('authStepOtp');
  var errPw = document.getElementById('authErrPw');
  var errOtp = document.getElementById('authErrOtp');

  document.getElementById('authFormPw').addEventListener('submit', function(e){
    e.preventDefault();
    var val = document.getElementById('authPw').value;
    errPw.textContent = '';
    sha256Hex(val).then(function(hash){
      if (hash === PW_HASH){
        stepPw.classList.remove('active');
        stepOtp.classList.add('active');
        document.getElementById('authOtp').focus();
      } else {
        errPw.textContent = 'Kata sandi salah.';
      }
    });
  });

  document.getElementById('authBack').addEventListener('click', function(){
    stepOtp.classList.remove('active');
    stepPw.classList.add('active');
    errOtp.textContent = '';
    document.getElementById('authPw').value = '';
    document.getElementById('authPw').focus();
  });

  document.getElementById('authFormOtp').addEventListener('submit', function(e){
    e.preventDefault();
    var code = document.getElementById('authOtp').value.trim();
    errOtp.textContent = '';
    verifyTotp(code).then(function(ok){
      if (ok){
        remember();
        revealContent();
      } else {
        errOtp.textContent = 'Kode tidak valid.';
      }
    });
  });
})();
</script>

<div class="marquee-bar" aria-hidden="true" style="display:none">
  <span class="marquee-text">Copyright &copy; 2026, Sony Fakih</span>
</div>

<div class="page" style="display:none">
  <div class="app-header">
    <div class="brand">
      <span class="eyebrow">SIMRS &middot; Remunerasi</span>
      <h1>Rekam Jasa Dokter</h1>
      <p>Gabungan TABEL IL ITL KRM N OB &amp; TABEL KRM OB &mdash; Januari&ndash;Juni 2026</p>
    </div>
    <div class="header-actions">
      <div class="theme-toggle" role="group" aria-label="Mode tampilan">
        <button type="button" id="themeLight" title="Mode terang" aria-label="Mode terang">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4.5"/><path d="M12 2.5v2.5M12 19v2.5M4.2 4.2l1.8 1.8M18 18l1.8 1.8M2.5 12H5M19 12h2.5M4.2 19.8L6 18M18 6l1.8-1.8"/></svg>
        </button>
        <button type="button" id="themeDark" title="Mode gelap" aria-label="Mode gelap">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8.5 8.5 0 1 1 9.5 4a6.7 6.7 0 0 0 10.5 10.5Z"/></svg>
        </button>
      </div>
      <button type="button" class="logout-btn" id="logoutBtn" title="Keluar dari dashboard">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="M16 17l5-5-5-5"/><path d="M21 12H9"/></svg>
        <span>Keluar</span>
      </button>
    </div>
  </div>

  <div class="tab-bar">
    <button type="button" class="tab-btn active" data-tab="dokter">
      <span class="tab-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="3.2"/><path d="M5.5 19.5c1.2-3.6 4-5.5 6.5-5.5s5.3 1.9 6.5 5.5"/></svg></span>
      <span class="tab-label">Data Dokter</span>
    </button>
    <button type="button" class="tab-btn" data-tab="spesialisasi">
      <span class="tab-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="8.5" r="2.6"/><path d="M4 19c.8-2.8 2.6-4.3 5-4.3s4.2 1.5 5 4.3"/><circle cx="17" cy="9" r="2.1"/><path d="M15.2 14.6c2 .2 3.3 1.5 3.9 3.6"/></svg></span>
      <span class="tab-label">Perbandingan Spesialisasi</span>
    </button>
  </div>

  <div class="control-panel">
    <div class="primary-row" data-tab-visible="dokter">
      <div class="control-field">
        <label for="specFilter">Spesialisasi</label>
        <select id="specFilter" class="select-input select-primary">
          <option value="">Semua Dokter</option>
        </select>
      </div>
      <div class="control-field">
        <label for="doctorSelect">Dokter Pelaksana</label>
        <select id="doctorSelect" class="select-input select-primary"></select>
      </div>
    </div>
    <div class="primary-row primary-row-single" data-tab-visible="spesialisasi" style="display:none;">
      <div class="control-field">
        <label for="specFilterCompare">Spesialisasi yang Dibandingkan</label>
        <select id="specFilterCompare" class="select-input select-primary"></select>
      </div>
    </div>
    <div class="filters-row">
      <div class="control-field">
        <label for="ksoFilter">Jenis KSO</label>
        <select id="ksoFilter" class="select-input">
          <option value="">Semua KSO</option>
        </select>
      </div>
      <div class="control-field">
        <label for="unitFilter">Unit Tindakan (Ruangan)</label>
        <select id="unitFilter" class="select-input">
          <option value="">Semua Unit</option>
        </select>
      </div>
      <div class="control-field" data-tab-visible="dokter,spesialisasi">
        <label>Rentang Tanggal</label>
        <div class="date-range">
          <input type="date" id="dateFrom" class="date-input" />
          <span>&ndash;</span>
          <input type="date" id="dateTo" class="date-input" />
        </div>
      </div>
      <div class="control-field" data-tab-visible="dokter">
        <label for="trendTindakanFilter">Tindakan (untuk Grafik Tren)</label>
        <select id="trendTindakanFilter" class="select-input">
          <option value="">Semua Tindakan</option>
        </select>
      </div>
      <div class="control-field" data-tab-visible="spesialisasi" style="display:none;">
        <label for="specTindakanFilter">Tindakan Unik (utk Perbandingan)</label>
        <select id="specTindakanFilter" class="select-input">
          <option value="">Semua Tindakan</option>
        </select>
      </div>
    </div>
  </div>

  <!-- ===================== TAB 1: DATA DOKTER ===================== -->
  <div class="tab-panel" data-tab-panel="dokter">
    <div class="topline">
      <div>
        <h2 id="personName">&mdash;<span class="role-pill" id="rolePill"></span></h2>
        <div class="subline" id="personSub"></div>
      </div>
    </div>

    <div class="kpi-row">
      <div class="kpi"><div class="k-label">Jenis Tindakan Unik</div><div class="k-value mono accent" id="kpiUnikTindakan">0</div></div>
      <div class="kpi"><div class="k-label">Baris Obat (KRM OB)</div><div class="k-value mono" id="kpiObat">0</div></div>
      <div class="kpi"><div class="k-label">Total Jasa (3 Komponen)</div><div class="k-value mono accent" id="kpiJasa">0</div></div>
    </div>

    <div class="section">
      <div class="section-head"><h3>Rincian Jasa</h3><span class="count-tag">Jaspel &middot; Jasa Operator &middot; Jasa Anestesi (dalam Poin)</span></div>
      <div class="jasa-grid" id="jasaGrid"></div>
    </div>

    <div class="section">
      <div class="section-head"><h3>Tren Poin Tindakan per Bulan</h3><span class="count-tag" id="trendContextTag"></span></div>
      <div class="trend-chart-wrap" id="trendChartWrap"></div>
    </div>

    <div class="section">
      <div class="section-head"><h3>Rincian per Kategori</h3></div>
      <div class="tables-grid">
        <div class="panel">
          <div class="panel-head">
            <h4><span class="dot"></span>Tindakan Dilaksanakan (Unik)<span class="count-tag" id="tindakanCountTag" style="font-weight:400;"></span></h4>
            <div style="font-size:10.5px; color:var(--text-faint); margin:-2px 0 4px;">Syarat: japel &gt; 0 atau operator &gt; 0 &middot; Dokter Anestesi hanya terisi utk Tindakan Medis Operatif</div>
            <input class="mini-search" data-target="tindakan" placeholder="Filter tindakan&hellip;" />
          </div>
          <div class="scroll-body"><table id="tbl-tindakan">
            <thead><tr>
              <th data-key="name" data-table="tindakan">Tindakan<span class="arrow"></span></th>
              <th data-key="subklas" data-table="tindakan">Sub-klasifikasi<span class="arrow"></span></th>
              <th data-key="anesName" data-table="tindakan">Dokter Anestesi<span class="arrow"></span></th>
              <th class="num" data-key="count" data-table="tindakan">Berapa Kali<span class="arrow"></span></th>
              <th class="num" data-key="point" data-table="tindakan">Poin<span class="arrow"></span></th>
            </tr></thead>
            <tbody></tbody>
          </table></div>
        </div>

        <div class="panel">
          <div class="panel-head">
            <h4><span class="dot"></span>Obat Diresepkan</h4>
            <input class="mini-search" data-target="obat" placeholder="Filter obat&hellip;" />
          </div>
          <div class="scroll-body"><table id="tbl-obat">
            <thead><tr>
              <th data-key="name" data-table="obat">Nama Obat<span class="arrow"></span></th>
              <th class="num" data-key="qty" data-table="obat">Qty<span class="arrow"></span></th>
              <th class="num" data-key="profit" data-table="obat">Profit<span class="arrow"></span></th>
            </tr></thead>
            <tbody></tbody>
          </table></div>
        </div>
      </div>
    </div>

    <div class="section" id="anesDerivedSection" style="display:none;">
      <div class="section-head"><h3>Tindakan Operatif sebagai Dokter Anestesi</h3><span class="count-tag" id="anesDerivedCountTag"></span></div>
      <div style="font-size:10.5px; color:var(--text-faint); margin:-8px 0 8px;">Seluruh Tindakan Medis Operatif (kolom BB) yang dianestesi oleh dokter ini, dikelompokkan berdasarkan dokter operator (bedah/obsgyn/orthopedi)</div>
      <div class="panel">
        <div class="table-wrap"><table id="tbl-anesderived">
          <thead><tr>
            <th data-key="operator" data-table="anesderived">Operator<span class="arrow"></span></th>
            <th data-key="name" data-table="anesderived">Tindakan<span class="arrow"></span></th>
            <th data-key="subklas" data-table="anesderived">Sub-klasifikasi<span class="arrow"></span></th>
            <th class="num" data-key="count" data-table="anesderived">Berapa Kali<span class="arrow"></span></th>
            <th class="num" data-key="biaya" data-table="anesderived">Biaya<span class="arrow"></span></th>
          </tr></thead>
          <tbody></tbody>
        </table></div>
      </div>
    </div>

  </div>

  <!-- ===================== TAB 2: PERBANDINGAN SPESIALISASI ===================== -->
  <div class="tab-panel" data-tab-panel="spesialisasi" style="display:none;">
    <div class="topline">
      <div>
        <h2 id="specCompareTitle">&mdash;</h2>
        <div class="subline" id="specCompareSub"></div>
      </div>
    </div>

    <div class="section">
      <div class="section-head"><h3>Peringkat Total Poin</h3></div>
      <div class="rank-chart" id="rankChart"></div>
    </div>

    <div class="section">
      <div class="section-head"><h3>Rincian per Dokter</h3><span class="count-tag">Klik judul kolom untuk mengurutkan</span></div>
      <div class="panel">
        <div class="table-wrap"><table id="tbl-speccompare">
          <thead><tr>
            <th data-key="name" data-table="speccompare">Dokter<span class="arrow"></span></th>
            <th class="num" data-key="n_tindakan_rows" data-table="speccompare">Baris Tindakan<span class="arrow"></span></th>
            <th class="num" data-key="n_unique_tindakan" data-table="speccompare">Tindakan Unik<span class="arrow"></span></th>
            <th class="num" data-key="n_operatif_cases" data-table="speccompare">Kasus Operatif<span class="arrow"></span></th>
            <th class="num" data-key="poin_japel" data-table="speccompare">Poin Jaspel<span class="arrow"></span></th>
            <th class="num" data-key="poin_operator" data-table="speccompare">Poin Jasa Operator<span class="arrow"></span></th>
            <th class="num" data-key="poin_anestesi" data-table="speccompare">Poin Jasa Anestesi<span class="arrow"></span></th>
            <th class="num" data-key="total_poin" data-table="speccompare">Total Poin<span class="arrow"></span></th>
          </tr></thead>
          <tbody></tbody>
        </table></div>
      </div>
    </div>

    <div class="section">
      <div class="section-head"><h3>Grafik Poin per Tindakan</h3><span class="count-tag" id="doctorPoinBarChartTag">Poin = (Japel+Operator)/1000 per tindakan, per dokter</span></div>
      <div class="bar2d-legend" id="doctorPoinBarChartLegend"></div>
      <div class="bar2d-chart-wrap" id="doctorPoinBarChartWrap"></div>
    </div>

    <div class="section">
      <div class="section-head"><h3>Tindakan Unik &amp; Obat per Dokter</h3><span class="count-tag">Sama seperti menu Data Dokter &middot; klik judul kolom utk mengurutkan</span></div>
      <div id="specDoctorDetailWrap"></div>
    </div>
  </div>

  <div class="footnote">
    Sumber: enam file bulanan TEMPLATE KSI (Januari&ndash;Juni 2026) di folder SIMRS, masing-masing sheet <code>TABEL IL ITL KRM N OB</code> (kolom <code>pelaksana</code>, <code>tindakan</code>, <code>subklasifikasi</code>, <code>KSO_nama</code>, <code>unit</code>, <code>tgl</code>, <code>japel</code>, <code>j_sarrs</code>, <code>operator</code>, <code>anestesi</code>, <code>team</code>) digabung dengan sheet <code>TABEL KRM OB</code> (kolom <code>Dokter</code>, <code>Nama Obat</code>, <code>KSO</code>, <code>Poli (Ruangan)</code>, <code>Tgl</code>) berdasarkan nama dokter yang sama. Tabel <strong>Tindakan Dilaksanakan (Unik)</strong> hanya menghitung baris dengan <code>japel &gt; 0</code> atau <code>operator &gt; 0</code>. Kolom <strong>Dokter Anestesi</strong> diambil dari kolom BB sheet <code>TABEL IL ITL KRM N OB</code>, khusus untuk baris dengan subklasifikasi <strong>Tindakan Medis Operatif</strong> (operator dokter bedah/obsgyn/tulang dengan anestesi dokter anestesi); metrik <strong>Kasus Operatif</strong> pada menu Perbandingan Spesialisasi menghitung jumlah baris tindakan pada subklasifikasi tersebut. Data rinci per-kunjungan/per-transaksi (No RM, Nama Pasien) utk seluruh dokter &amp; 6 bulan (&plusmn;443 ribu baris tindakan, &plusmn;328 ribu baris obat) tersedia sbg file Excel terpisah (<code>Tindakan_Rinci_SemuaDokter.xlsx</code> &amp; <code>Obat_Rinci_SemuaDokter.xlsx</code>) &mdash; tidak disematkan di dashboard interaktif ini krn ukurannya terlalu besar utk tetap ringan &amp; bisa dibuka via link. Menu <strong>Perbandingan Spesialisasi</strong> membandingkan seluruh dokter dalam satu spesialisasi yang sama, dgn filter KSO, Unit, rentang tanggal, dan Tindakan Unik (dibatasi pada baris <code>japel &gt; 0</code> atau <code>operator &gt; 0</code>, sama seperti menu Data Dokter) yang sama-sama berlaku di kedua menu. Klik judul kolom untuk mengurutkan.
  </div>
</div>

<script>
const DATA = __DATA_JSON__;

const fmtInt = n => Math.round(n).toLocaleString('id-ID');
const fmtRp = n => 'Rp ' + Math.round(n).toLocaleString('id-ID');
function fmtRpShort(v){
  const abs = Math.abs(v);
  if (abs >= 1e9) return (v/1e9).toFixed(2).replace(/\.00$/,'').replace(/0$/,'') + ' M';
  if (abs >= 1e6) return (v/1e6).toFixed(1).replace(/\.0$/,'') + ' jt';
  if (abs >= 1e3) return (v/1e3).toFixed(0) + ' rb';
  return fmtInt(v);
}
// Alias generik (bukan Rupiah) -- dipakai utk memendekkan angka Poin di grafik tren.
const fmtNumShort = fmtRpShort;

const IND_MONTHS = ['Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September','Oktober','November','Desember'];
function monthLabel(m){ const parts = m.split('-'); return IND_MONTHS[parseInt(parts[1],10)-1] + ' ' + parts[0]; }
function monthShort(m){ return monthLabel(m).slice(0,3); }

function escapeHtml(s){
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

function safeGet(key){ try { return localStorage.getItem(key); } catch(e){ return null; } }
function safeSet(key, val){ try { localStorage.setItem(key, val); } catch(e){} }

// ---------- Theme ----------
function applyTheme(mode){
  document.documentElement.setAttribute('data-theme', mode);
  document.getElementById('themeLight').classList.toggle('active', mode === 'light');
  document.getElementById('themeDark').classList.toggle('active', mode === 'dark');
  safeSet('simrs-theme', mode);
}
applyTheme(safeGet('simrs-theme') === 'dark' ? 'dark' : 'light');
document.getElementById('themeLight').addEventListener('click', () => applyTheme('light'));
document.getElementById('themeDark').addEventListener('click', () => applyTheme('dark'));

// ---------- State ----------
let activeDocIdx = null;
let activeTab = 'dokter';
let lastSpecCompareRows = [];
let currentSort = {
  tindakan: {key:'count', dir:-1},
  obat: {key:'qty', dir:-1},
  speccompare: {key:'total_poin', dir:-1},
  anesderived: {key:'count', dir:-1},
};
const tableFilters = { tindakan:'', obat:'' };
// Sort/filter state per dokter utk tabel "Tindakan Unik & Obat per Dokter" di menu Perbandingan Spesialisasi
const specDoctorSort = new Map();
const specDoctorFilter = new Map();
function getSpecDoctorSort(idx, kind){
  const k = `${idx}:${kind}`;
  if (!specDoctorSort.has(k)) specDoctorSort.set(k, { key: kind === 'tindakan' ? 'biaya' : 'profit', dir: -1 });
  return specDoctorSort.get(k);
}

const specFilter = document.getElementById('specFilter');
const doctorSelect = document.getElementById('doctorSelect');
const specFilterCompare = document.getElementById('specFilterCompare');
const ksoFilter = document.getElementById('ksoFilter');
const unitFilter = document.getElementById('unitFilter');
const dateFrom = document.getElementById('dateFrom');
const dateTo = document.getElementById('dateTo');
const trendTindakanFilter = document.getElementById('trendTindakanFilter');
const specTindakanFilter = document.getElementById('specTindakanFilter');

const OTHER_SPEC = '__OTHER__';

// ---------- Populate filter dropdowns ----------
const specs = Array.from(new Set(DATA.people.filter(p => p.spec_label).map(p => p.spec_label))).sort((a,b)=>a.localeCompare(b));
specs.forEach(s => { const o = document.createElement('option'); o.value = s; o.textContent = s; specFilter.appendChild(o); });
{
  const o = document.createElement('option');
  o.value = OTHER_SPEC; o.textContent = 'Petugas Non-Dokter';
  specFilter.appendChild(o);
}

specs.forEach(s => { const o = document.createElement('option'); o.value = s; o.textContent = s; specFilterCompare.appendChild(o); });

DATA.dict.kso.slice().sort((a,b)=>a.localeCompare(b)).forEach(k => { const o = document.createElement('option'); o.value = k; o.textContent = k; ksoFilter.appendChild(o); });

// "Unit Tindakan (Ruangan)" hanya menampilkan unit yang benar-benar muncul pada baris yang
// memenuhi syarat Tindakan Dilaksanakan (Unik) (japel > 0 atau operator > 0) di SELURUH
// dokter -- konsisten dgn isi tabel Tindakan Dilaksanakan (Unik).
const qualifyingUnitIdx = new Set();
for (const r of DATA.tRows){
  const japel = r[7], operator = r[9];
  if (japel > 0 || operator > 0) qualifyingUnitIdx.add(r[4]);
}

DATA.dict.unit.map((name, idx) => ({ name, idx })).filter(u => u.name !== '(lainnya)' && qualifyingUnitIdx.has(u.idx)).sort((a,b)=>a.name.localeCompare(b.name)).forEach(u => {
  const o = document.createElement('option'); o.value = u.name; o.textContent = u.name; unitFilter.appendChild(o);
});

// "Tindakan (untuk Grafik Tren)" di-scope DINAMIS: hanya tindakan dgn japel>0 atau operator>0
// milik DOKTER YANG SEDANG AKTIF, dalam KSO/Unit/rentang tanggal yang sedang aktif juga --
// supaya tidak muncul nama tindakan yang sebenarnya tidak relevan/kosong utk konteks saat ini.
// Dipanggil ulang setiap kali dokter atau filter kso/unit/tanggal berubah (lihat renderAll()).
function populateTrendTindakanFilter(){
  if (activeDocIdx === null) return;
  const docIdx = activeDocIdx;
  const kso = ksoFilter.value, unit = unitFilter.value, from = dateFrom.value, to = dateTo.value;
  const qualifying = new Map();
  for (const r of DATA.tRows){
    if (r[0] !== docIdx) continue;
    const japel = r[7], operator = r[9];
    if (!(japel > 0 || operator > 0)) continue;
    const kIdx = r[3], uIdx = r[4], dtIdx = r[5];
    if (kso && DATA.dict.kso[kIdx] !== kso) continue;
    if (unit && DATA.dict.unit[uIdx] !== unit) continue;
    const dstr = DATA.dict.date[dtIdx];
    if (from && dstr < from) continue;
    if (to && dstr > to) continue;
    const tIdx = r[1];
    const name = DATA.dict.tindakan[tIdx];
    if (name !== '(lainnya)') qualifying.set(tIdx, name);
  }
  const prevValue = trendTindakanFilter.value;
  const options = Array.from(qualifying.entries()).map(([idx, name]) => ({ idx, name })).sort((a, b) => a.name.localeCompare(b.name));
  trendTindakanFilter.innerHTML = '<option value="">Semua Tindakan</option>' +
    options.map(o => `<option value="${o.idx}">${escapeHtml(o.name)}</option>`).join('');
  const stillValid = prevValue !== '' && options.some(o => String(o.idx) === prevValue);
  trendTindakanFilter.value = stillValid ? prevValue : '';
}

// "Tindakan Unik (utk Perbandingan)" di menu Perbandingan Spesialisasi: sama prinsipnya dgn
// populateTrendTindakanFilter(), tapi di-scope ke SELURUH dokter dlm spesialisasi yg sedang
// dibandingkan (specFilterCompare), bukan satu dokter aktif -- supaya bisa membandingkan
// dokter-dokter itu berdasarkan satu tindakan unik tertentu (japel>0 atau operator>0).
function populateSpecTindakanFilter(){
  const specValue = specFilterCompare.value;
  const kso = ksoFilter.value, unit = unitFilter.value, from = dateFrom.value, to = dateTo.value;
  const doctorIdxSet = new Set(
    DATA.people.map((p, idx) => ({ ...p, idx })).filter(p => p.is_doctor && p.spec_label === specValue).map(p => p.idx)
  );
  const qualifying = new Map();
  for (const r of DATA.tRows){
    if (!doctorIdxSet.has(r[0])) continue;
    const japel = r[7], operator = r[9];
    if (!(japel > 0 || operator > 0)) continue;
    const kIdx = r[3], uIdx = r[4], dtIdx = r[5];
    if (kso && DATA.dict.kso[kIdx] !== kso) continue;
    if (unit && DATA.dict.unit[uIdx] !== unit) continue;
    const dstr = DATA.dict.date[dtIdx];
    if (from && dstr < from) continue;
    if (to && dstr > to) continue;
    const tIdx = r[1];
    const name = DATA.dict.tindakan[tIdx];
    if (name !== '(lainnya)') qualifying.set(tIdx, name);
  }
  const prevValue = specTindakanFilter.value;
  const options = Array.from(qualifying.entries()).map(([idx, name]) => ({ idx, name })).sort((a, b) => a.name.localeCompare(b.name));
  specTindakanFilter.innerHTML = '<option value="">Semua Tindakan</option>' +
    options.map(o => `<option value="${o.idx}">${escapeHtml(o.name)}</option>`).join('');
  const stillValid = prevValue !== '' && options.some(o => String(o.idx) === prevValue);
  specTindakanFilter.value = stillValid ? prevValue : '';
}

// ---------- Dokter Anestesi -> Dokter Pelaksana name-matching (utk fitur "Tindakan Operatif sebagai Dokter Anestesi") ----------
function normName(s){ return (s||'').trim().toLowerCase().replace(/\s+/g,' '); }
const anesIdxByDocIdx = new Map();
DATA.people.forEach((p, idx) => {
  const ai = DATA.dict.dr_anestesi.findIndex(n => normName(n) === normName(p.name));
  if (ai >= 0) anesIdxByDocIdx.set(idx, ai);
});

const dateList = DATA.dict.date.slice().sort();
const minDate = dateList[0], maxDate = dateList[dateList.length - 1];
dateFrom.min = minDate; dateFrom.max = maxDate; dateFrom.value = minDate;
dateTo.min = minDate; dateTo.max = maxDate; dateTo.value = maxDate;

const months = DATA.months.slice();
specFilterCompare.value = specs[0] || '';

// ---------- Specialization -> Doctor cascading dropdowns (Tab 1 & 2) ----------
function peopleForSpec(specValue){
  if (specValue === OTHER_SPEC){
    return DATA.people.map((p, idx) => ({ ...p, idx })).filter(p => !p.is_doctor).sort((a,b)=>a.name.localeCompare(b.name));
  }
  return DATA.people.map((p, idx) => ({ ...p, idx }))
    .filter(p => p.is_doctor && (!specValue || p.spec_label === specValue))
    .sort((a,b)=>a.name.localeCompare(b.name));
}

function populateDoctorSelect(specValue, preferIdx){
  const list = peopleForSpec(specValue);
  doctorSelect.innerHTML = list.map(p => `<option value="${p.idx}">${escapeHtml(p.name)}</option>`).join('');
  let chosen = list.find(p => p.idx === preferIdx) ? preferIdx : (list[0] ? list[0].idx : null);
  if (chosen !== null){
    doctorSelect.value = String(chosen);
    activeDocIdx = chosen;
    renderActiveDoctorView();
  }
}

function renderActiveDoctorView(){
  renderAll();
}

specFilter.addEventListener('change', () => populateDoctorSelect(specFilter.value, activeDocIdx));
doctorSelect.addEventListener('change', () => {
  activeDocIdx = parseInt(doctorSelect.value, 10);
  renderActiveDoctorView();
});
specFilterCompare.addEventListener('change', renderSpecCompareView);

function renderActiveTabView(){
  if (activeTab === 'dokter') renderAll();
  else renderSpecCompareView();
}

// data filters trigger recompute of whichever tab is visible
[ksoFilter, unitFilter, dateFrom, dateTo].forEach(el => el.addEventListener('change', renderActiveTabView));
trendTindakanFilter.addEventListener('change', renderAll);
specTindakanFilter.addEventListener('change', renderSpecCompareView);

// ---------- Tab switching ----------
const tabButtons = document.querySelectorAll('.tab-btn');
function setActiveTab(tab){
  activeTab = tab;
  tabButtons.forEach(b => b.classList.toggle('active', b.dataset.tab === tab));
  document.querySelectorAll('[data-tab-panel]').forEach(p => { p.style.display = p.dataset.tabPanel === tab ? '' : 'none'; });
  document.querySelectorAll('[data-tab-visible]').forEach(el => {
    const tabs = el.dataset.tabVisible.split(',');
    el.style.display = tabs.includes(tab) ? '' : 'none';
  });
  renderActiveTabView();
}
tabButtons.forEach(b => b.addEventListener('click', () => setActiveTab(b.dataset.tab)));

// ---------- Core aggregation (pure function, reused by all 3 tabs) ----------
function computeAggregate(docIdx, kso, unit, from, to, tIdxFilter){
  if (tIdxFilter === undefined) tIdxFilter = null;
  let nTindakanRows = 0, biayaTotal = 0, nOperatifCases = 0;
  const jasa = { japel:0, j_sarrs:0, operator:0, anestesi:0, team:0 };
  const comboMap = new Map();
  const uniqueTind = new Set();

  for (const r of DATA.tRows){
    if (r[0] !== docIdx) continue;
    if (tIdxFilter !== null && r[1] !== tIdxFilter) continue;
    const kIdx = r[3], uIdx = r[4], dtIdx = r[5];
    if (kso && DATA.dict.kso[kIdx] !== kso) continue;
    if (unit && DATA.dict.unit[uIdx] !== unit) continue;
    const dstr = DATA.dict.date[dtIdx];
    if (from && dstr < from) continue;
    if (to && dstr > to) continue;

    const tIdx = r[1], sIdx = r[2];
    const cnt = r[6], japel = r[7], jsarrs = r[8], operator = r[9], anestesi = r[10], team = r[11], biaya = r[12];
    const anesIdx = r[13];

    nTindakanRows += cnt;
    jasa.japel += japel; jasa.j_sarrs += jsarrs; jasa.operator += operator; jasa.anestesi += anestesi; jasa.team += team;
    biayaTotal += biaya;

    const isOperatif = DATA.dict.subklas[sIdx] === 'TINDAKAN MEDIS OPERATIF';
    if (isOperatif) nOperatifCases += cnt;

    if (japel > 0 || operator > 0){
      const key = tIdx + '|' + sIdx + '|' + anesIdx;
      let c = comboMap.get(key);
      if (!c){
        c = {
          name: DATA.dict.tindakan[tIdx], subklas: DATA.dict.subklas[sIdx],
          anesName: anesIdx >= 0 ? DATA.dict.dr_anestesi[anesIdx] : null,
          count:0, biaya:0, japel:0, operator:0,
        };
        comboMap.set(key, c);
      }
      c.count += cnt; c.biaya += biaya; c.japel += japel; c.operator += operator;
      uniqueTind.add(tIdx);
    }
  }

  let nObatRows = 0;
  const obatMap = new Map();
  for (const r of DATA.oRows){
    if (r[0] !== docIdx) continue;
    const kIdx = r[2], uIdx = r[3], dtIdx = r[4];
    if (kso && DATA.dict.kso[kIdx] !== kso) continue;
    if (unit && DATA.dict.unit[uIdx] !== unit) continue;
    const dstr = DATA.dict.date[dtIdx];
    if (from && dstr < from) continue;
    if (to && dstr > to) continue;

    const oIdx = r[1], cnt = r[5], qty = r[6], profit = r[7];
    nObatRows += cnt;
    let c = obatMap.get(oIdx);
    if (!c){ c = { name: DATA.dict.obat[oIdx], count:0, qty:0, profit:0 }; obatMap.set(oIdx, c); }
    c.count += cnt; c.qty += qty; c.profit += profit;
  }

  return {
    n_tindakan_rows: nTindakanRows,
    n_obat_rows: nObatRows,
    biaya_total: biayaTotal,
    jasa,
    n_unique_tindakan: uniqueTind.size,
    n_operatif_cases: nOperatifCases,
    tindakan: Array.from(comboMap.values()),
    obat: Array.from(obatMap.values()),
  };
}

// Total Jasa (3 Komponen) dlm Poin = (Jaspel+Operator+Anestesi)/1000 -- Jasa Sarana & Jasa Tim tidak dihitung.
// Dipakai oleh KEDUA tab (Data Dokter & Perbandingan Spesialisasi) sejak 2026-08-23.
// totalJasa() (Rupiah, 5 komponen) & obatProfitTotal() dihapus 2026-08-23 stlh Perbandingan
// Spesialisasi jg dikonversi penuh ke Poin -- sudah tidak dipakai di manapun lagi.
function totalJasaPoin(d){ return (d.jasa.japel + d.jasa.operator + d.jasa.anestesi) / 1000; }

// ---------- Khusus dokter anestesi: turunan Tindakan Medis Operatif (kolom BB) yg dianestesi dokter ini ----------
function computeAnesDerived(docIdx, kso, unit, from, to){
  const anesIdx = anesIdxByDocIdx.get(docIdx);
  if (anesIdx === undefined) return null;
  const comboMap = new Map();
  let totalCases = 0, totalBiaya = 0;
  for (const r of DATA.tRows){
    if (r[13] !== anesIdx) continue;
    const kIdx = r[3], uIdx = r[4], dtIdx = r[5];
    if (kso && DATA.dict.kso[kIdx] !== kso) continue;
    if (unit && DATA.dict.unit[uIdx] !== unit) continue;
    const dstr = DATA.dict.date[dtIdx];
    if (from && dstr < from) continue;
    if (to && dstr > to) continue;

    const opDocIdx = r[0], tIdx = r[1], sIdx = r[2], cnt = r[6], biaya = r[12];
    const key = opDocIdx + '|' + tIdx + '|' + sIdx;
    let c = comboMap.get(key);
    if (!c){ c = { operator: DATA.people[opDocIdx].name, name: DATA.dict.tindakan[tIdx], subklas: DATA.dict.subklas[sIdx], count:0, biaya:0 }; comboMap.set(key, c); }
    c.count += cnt; c.biaya += biaya;
    totalCases += cnt; totalBiaya += biaya;
  }
  return { rows: Array.from(comboMap.values()), totalCases, totalBiaya };
}

function renderAnesDerivedTable(rows){
  const sort = currentSort.anesderived;
  const sorted = sortGeneric(rows, sort.key, sort.dir);
  const tbody = document.querySelector('#tbl-anesderived tbody');
  if (sorted.length === 0){
    tbody.innerHTML = `<tr class="empty-row"><td colspan="5">Tidak ada tindakan operatif dgn dokter ini sbg anestesi pada filter ini</td></tr>`;
  } else {
    tbody.innerHTML = sorted.map(r => `<tr>
      <td class="name-cell">${escapeHtml(r.operator)}</td>
      <td class="name-cell">${escapeHtml(r.name)}</td>
      <td class="subklas-cell">${escapeHtml(r.subklas)}</td>
      <td class="num mono">${fmtInt(r.count)}</td>
      <td class="num mono">${fmtRp(r.biaya)}</td>
    </tr>`).join('');
  }
  document.querySelectorAll('th[data-table="anesderived"]').forEach(th => {
    const arrow = th.querySelector('.arrow');
    arrow.textContent = th.dataset.key === sort.key ? (sort.dir === 1 ? '↑' : '↓') : '';
  });
}

function renderAnesDerivedSection(){
  const section = document.getElementById('anesDerivedSection');
  const derived = computeAnesDerived(activeDocIdx, ksoFilter.value, unitFilter.value, dateFrom.value, dateTo.value);
  if (!derived){ section.style.display = 'none'; return; }
  section.style.display = '';
  document.getElementById('anesDerivedCountTag').textContent = `${fmtInt(derived.totalCases)} kasus · ${fmtRp(derived.totalBiaya)}`;
  renderAnesDerivedTable(derived.rows);
}

// ======================================================================
// TAB 1: DATA DOKTER
// ======================================================================
function renderAll(){
  if (activeDocIdx === null) return;
  populateTrendTindakanFilter();
  const meta = DATA.people[activeDocIdx];
  const d = computeAggregate(activeDocIdx, ksoFilter.value, unitFilter.value, dateFrom.value, dateTo.value);

  document.getElementById('personName').innerHTML = escapeHtml(meta.name) + `<span class="role-pill">${meta.is_doctor ? 'Dokter Pelaksana' : 'Petugas Lain'}</span>`;
  document.getElementById('personSub').textContent = meta.is_doctor
    ? 'Tindakan yang dilaksanakan, sub-klasifikasi, obat, dan rincian jasa pelayanan sesuai filter aktif.'
    : 'Peran non-dokter (ditampilkan sebagai referensi pembanding).';

  document.getElementById('kpiUnikTindakan').textContent = fmtInt(d.n_unique_tindakan);
  document.getElementById('kpiObat').textContent = fmtInt(d.n_obat_rows);
  document.getElementById('kpiJasa').textContent = fmtInt(totalJasaPoin(d)) + ' Poin';
  document.getElementById('tindakanCountTag').textContent = `${fmtInt(d.n_unique_tindakan)} jenis unik (${fmtInt(d.tindakan.length)} kombinasi sub-klasifikasi) dari ${fmtInt(d.n_tindakan_rows)} baris`;

  // Jaspel/Jasa Operator/Jasa Anestesi ditampilkan dalam Poin (nilai/1000), bukan Rupiah.
  // Jasa Sarana & Jasa Tim sengaja tidak ditampilkan (bukan bagian dari Poin dokter).
  const jasaLabels = { japel:'Jaspel', operator:'Jasa Operator', anestesi:'Jasa Anestesi' };
  const maxJasa = Math.max(1, ...Object.keys(jasaLabels).map(k => d.jasa[k] || 0));
  const jasaGrid = document.getElementById('jasaGrid');
  jasaGrid.innerHTML = '';
  Object.keys(jasaLabels).forEach(k => {
    const v = d.jasa[k] || 0;
    const pct = Math.max(2, (v/maxJasa)*100);
    const card = document.createElement('div');
    card.className = 'jasa-card';
    card.setAttribute('data-jasa', k);
    card.innerHTML = `<div class="j-label">${jasaLabels[k]}</div><div class="j-value mono">${fmtInt(v/1000)} Poin</div><div class="j-bar-track"><div class="j-bar-fill" style="width:${pct}%"></div></div>`;
    jasaGrid.appendChild(card);
  });

  renderTable('tindakan', d.tindakan);
  renderTable('obat', d.obat);
  renderTrendSection();
  renderAnesDerivedSection();
}

// ---------- Tren Poin Tindakan per Bulan (garis, 3D) ----------
function fmtDateID(iso){ if (!iso) return '-'; const p = iso.split('-'); return `${p[2]}/${p[1]}/${p[0]}`; }

function buildTrendRows(){
  const docIdx = activeDocIdx;
  const kso = ksoFilter.value, unit = unitFilter.value;
  const tIdxSel = trendTindakanFilter.value === '' ? null : parseInt(trendTindakanFilter.value, 10);
  const from = dateFrom.value, to = dateTo.value;

  const activeMonths = months.filter(m => {
    const mStart = m + '-01', mEnd = m + '-31';
    return (!to || mStart <= to) && (!from || mEnd >= from);
  });

  const rows = activeMonths.map(m => {
    const mStart = m + '-01', mEnd = m + '-31';
    const effFrom = (from && from > mStart) ? from : mStart;
    const effTo = (to && to < mEnd) ? to : mEnd;
    let japelSum = 0, operatorSum = 0, count = 0;
    for (const r of DATA.tRows){
      if (r[0] !== docIdx) continue;
      if (tIdxSel !== null && r[1] !== tIdxSel) continue;
      const kIdx = r[3], uIdx = r[4], dtIdx = r[5];
      if (kso && DATA.dict.kso[kIdx] !== kso) continue;
      if (unit && DATA.dict.unit[uIdx] !== unit) continue;
      const dstr = DATA.dict.date[dtIdx];
      if (dstr < effFrom || dstr > effTo) continue;
      japelSum += r[7]; operatorSum += r[9]; count += r[6];
    }
    const poin = (japelSum + operatorSum) / 1000;
    return { month: m, poin, count };
  });

  rows.forEach((r, i) => {
    if (i === 0 || rows[i-1].poin === 0){ r.delta = null; }
    else { r.delta = (r.poin - rows[i-1].poin) / rows[i-1].poin * 100; }
  });
  return rows;
}

function renderTrendChart(rows){
  const wrap = document.getElementById('trendChartWrap');
  if (!rows.length){
    wrap.innerHTML = '<div class="trend-empty">Tidak ada data pada rentang tanggal ini</div>';
    return;
  }
  const n = rows.length;
  const maxVal = Math.max(1, ...rows.map(r => r.poin));
  const W = 900, H = 240, padL = 56, padR = 24, padT = 40, padB = 34;
  const plotW = W - padL - padR, plotH = H - padT - padB;
  const xFor = i => n === 1 ? padL + plotW/2 : padL + (plotW * i/(n-1));
  const yFor = v => padT + plotH - (v/maxVal)*plotH;
  const baseline = padT + plotH;

  const pts = rows.map((r,i) => ({ x: xFor(i), y: yFor(r.poin), r }));

  let gridSvg = '';
  for (let g = 0; g <= 4; g++){
    const gy = padT + plotH * g/4;
    const gv = maxVal * (1 - g/4);
    gridSvg += `<line x1="${padL}" y1="${gy.toFixed(1)}" x2="${W-padR}" y2="${gy.toFixed(1)}" class="trend-grid-line"/>`;
    gridSvg += `<text x="${padL-8}" y="${(gy+3).toFixed(1)}" text-anchor="end" class="trend-axis-label">${fmtNumShort(gv)}</text>`;
  }

  let linePath = '', areaPath = '';
  if (n >= 2){
    linePath = pts.map((p,i) => (i===0?'M':'L') + p.x.toFixed(1) + ' ' + p.y.toFixed(1)).join(' ');
    areaPath = linePath + ` L ${pts[n-1].x.toFixed(1)} ${baseline.toFixed(1)} L ${pts[0].x.toFixed(1)} ${baseline.toFixed(1)} Z`;
  }

  const pointsSvg = pts.map(p => {
    const r = p.r;
    const deltaSvg = r.delta === null ? ''
      : `<text x="${p.x.toFixed(1)}" y="${(p.y-30).toFixed(1)}" text-anchor="middle" class="trend-delta ${r.delta>=0?'trend-delta-up':'trend-delta-down'}">${r.delta>=0?'&#9650;':'&#9660;'} ${Math.abs(r.delta).toFixed(1)}%</text>`;
    return `
      <text x="${p.x.toFixed(1)}" y="${(p.y-14).toFixed(1)}" text-anchor="middle" class="trend-value-label">${fmtNumShort(r.poin)}</text>
      ${deltaSvg}
      <circle cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="9" fill="url(#trendPointGrad)" filter="url(#trendShadow)"/>
      <circle cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="3.2" fill="#fff" opacity="0.85"/>
      <text x="${p.x.toFixed(1)}" y="${(baseline+22).toFixed(1)}" text-anchor="middle" class="trend-month-label">${monthShort(r.month)}</text>`;
  }).join('');

  wrap.innerHTML = `<svg class="trend-svg" viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">
    <defs>
      <linearGradient id="trendAreaGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="var(--accent)" stop-opacity="0.4"/>
        <stop offset="100%" stop-color="var(--accent)" stop-opacity="0"/>
      </linearGradient>
      <radialGradient id="trendPointGrad" cx="35%" cy="30%" r="75%">
        <stop offset="0%" stop-color="#ffffff"/>
        <stop offset="45%" stop-color="var(--accent)"/>
        <stop offset="100%" stop-color="var(--accent-strong)"/>
      </radialGradient>
      <filter id="trendShadow" x="-60%" y="-60%" width="220%" height="220%">
        <feDropShadow dx="0" dy="3" stdDeviation="2.6" flood-color="var(--accent-strong)" flood-opacity="0.45"/>
      </filter>
      <filter id="trendLineShadow" x="-20%" y="-40%" width="140%" height="180%">
        <feDropShadow dx="0" dy="2" stdDeviation="2.2" flood-color="var(--accent-strong)" flood-opacity="0.35"/>
      </filter>
    </defs>
    ${gridSvg}
    ${n >= 2 ? `<path d="${areaPath}" fill="url(#trendAreaGrad)" stroke="none"/>` : ''}
    ${n >= 2 ? `<path d="${linePath}" fill="none" stroke="var(--accent-strong)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" filter="url(#trendLineShadow)"/>` : ''}
    ${pointsSvg}
  </svg>`;
}

function renderTrendSection(){
  const rows = buildTrendRows();
  renderTrendChart(rows);
  const kso = ksoFilter.value || 'Semua KSO';
  const unit = unitFilter.value || 'Semua Unit';
  const tName = trendTindakanFilter.value === '' ? 'Semua Tindakan' : trendTindakanFilter.options[trendTindakanFilter.selectedIndex].textContent;
  document.getElementById('trendContextTag').textContent = `${unit} · ${tName} · ${kso} · ${fmtDateID(dateFrom.value)}–${fmtDateID(dateTo.value)}`;
}

function getVal(row, key){
  if (key === 'point') return ((row.japel || 0) + (row.operator || 0)) / 1000;
  if (key === 'anesName') return row.anesName || '';
  return row[key];
}
function sortRows(rows, key, dir){
  return [...rows].sort((a,b) => {
    const va = getVal(a, key), vb = getVal(b, key);
    if (typeof va === 'string') return dir * va.localeCompare(vb);
    return dir * ((va||0) - (vb||0));
  });
}
const colCount = { tindakan: 5, obat: 3 };

function renderTable(kind, rows){
  const sort = currentSort[kind];
  let filtered = rows;
  const ft = tableFilters[kind].trim().toLowerCase();
  if (ft) filtered = rows.filter(r => r.name.toLowerCase().includes(ft) || (kind === 'tindakan' && ((r.subklas||'').toLowerCase().includes(ft) || (r.anesName||'').toLowerCase().includes(ft))));
  const sorted = sortRows(filtered, sort.key, sort.dir);
  const tbody = document.querySelector(`#tbl-${kind} tbody`);
  tbody.innerHTML = '';
  if (sorted.length === 0){
    tbody.innerHTML = `<tr class="empty-row"><td colspan="${colCount[kind]}">Tidak ada data</td></tr>`;
  } else {
    sorted.forEach(r => {
      const tr = document.createElement('tr');
      if (kind === 'tindakan'){
        const point = ((r.japel || 0) + (r.operator || 0)) / 1000;
        const subklas = r.subklas ? escapeHtml(r.subklas) : '&mdash;';
        const anesCell = r.anesName
          ? `<span class="anes-badge">${escapeHtml(r.anesName)}</span>`
          : `<span class="anes-none">&mdash;</span>`;
        tr.innerHTML = `<td class="name-cell">${escapeHtml(r.name)}</td><td class="subklas-cell">${subklas}</td><td class="anes-cell">${anesCell}</td><td class="num mono">${fmtInt(r.count)}</td><td class="num mono">${fmtInt(point)}</td>`;
      } else {
        tr.innerHTML = `<td class="name-cell">${escapeHtml(r.name)}</td><td class="num mono">${fmtInt(r.qty)}</td><td class="num mono">${fmtRp(r.profit)}</td>`;
      }
      tbody.appendChild(tr);
    });
  }
  document.querySelectorAll(`th[data-table="${kind}"]`).forEach(th => {
    const arrow = th.querySelector('.arrow');
    arrow.textContent = th.dataset.key === sort.key ? (sort.dir === 1 ? '↑' : '↓') : '';
  });
}

function sortGeneric(rows, key, dir){
  return [...rows].sort((a,b) => {
    const va = a[key], vb = b[key];
    if (va === null || va === undefined) return 1;
    if (vb === null || vb === undefined) return -1;
    if (typeof va === 'string') return dir * va.localeCompare(vb);
    return dir * (va - vb);
  });
}

// ======================================================================
// TAB 2: PERBANDINGAN SPESIALISASI (semua dokter, satu spesialisasi)
// ======================================================================
function buildSpecCompareRows(){
  const specValue = specFilterCompare.value;
  const kso = ksoFilter.value, unit = unitFilter.value;
  const from = dateFrom.value, to = dateTo.value;
  const tIdxSel = specTindakanFilter.value === '' ? null : parseInt(specTindakanFilter.value, 10);

  const doctors = DATA.people.map((p, idx) => ({ ...p, idx })).filter(p => p.is_doctor && p.spec_label === specValue);
  return doctors.map(p => {
    const d = computeAggregate(p.idx, kso, unit, from, to, tIdxSel);
    return {
      idx: p.idx,
      name: p.name,
      n_tindakan_rows: d.n_tindakan_rows,
      n_unique_tindakan: d.n_unique_tindakan,
      n_operatif_cases: d.n_operatif_cases,
      // Sejak 2026-08-23: menu Perbandingan Spesialisasi jg ditampilkan dlm Poin (bukan Rupiah),
      // konsisten dgn menu Data Dokter -- Jasa Sarana & Jasa Tim tdk lagi dihitung (sama spt totalJasaPoin()).
      poin_japel: d.jasa.japel / 1000,
      poin_operator: d.jasa.operator / 1000,
      poin_anestesi: d.jasa.anestesi / 1000,
      total_poin: totalJasaPoin(d),
      tindakan: d.tindakan,
      obat: d.obat,
    };
  });
}

function renderRankChart(rows){
  const sorted = [...rows].sort((a,b) => b.total_poin - a.total_poin);
  const max = Math.max(1, ...sorted.map(r => r.total_poin));
  const el = document.getElementById('rankChart');
  if (sorted.length === 0){
    el.innerHTML = `<div style="text-align:center; color:var(--text-faint); font-style:italic; padding:16px;">Tidak ada dokter pada spesialisasi ini</div>`;
    return;
  }
  el.innerHTML = sorted.map((r, i) => {
    const pct = Math.max(2, (r.total_poin / max) * 100);
    return `<div class="rank-row">
      <div class="rank-name" title="${escapeHtml(r.name)}">${i+1}. ${escapeHtml(r.name)}</div>
      <div class="rank-track"><div class="rank-fill" style="width:${pct}%"></div></div>
      <div class="rank-value mono">${fmtInt(r.total_poin)} Poin</div>
    </div>`;
  }).join('');
}

function renderSpecCompareTable(rows){
  const sort = currentSort.speccompare;
  const sorted = sortGeneric(rows, sort.key, sort.dir);
  const tbody = document.querySelector('#tbl-speccompare tbody');
  if (sorted.length === 0){
    tbody.innerHTML = `<tr class="empty-row"><td colspan="8">Tidak ada dokter pada spesialisasi ini</td></tr>`;
  } else {
    tbody.innerHTML = sorted.map(r => `<tr>
      <td class="name-cell">${escapeHtml(r.name)}</td>
      <td class="num mono">${fmtInt(r.n_tindakan_rows)}</td>
      <td class="num mono">${fmtInt(r.n_unique_tindakan)}</td>
      <td class="num mono">${fmtInt(r.n_operatif_cases)}</td>
      <td class="num mono">${fmtInt(r.poin_japel)}</td>
      <td class="num mono">${fmtInt(r.poin_operator)}</td>
      <td class="num mono">${fmtInt(r.poin_anestesi)}</td>
      <td class="num mono">${fmtInt(r.total_poin)}</td>
    </tr>`).join('');
  }
  document.querySelectorAll('th[data-table="speccompare"]').forEach(th => {
    const arrow = th.querySelector('.arrow');
    arrow.textContent = th.dataset.key === sort.key ? (sort.dir === 1 ? '↑' : '↓') : '';
  });
}

// ---------- Grafik Batang: Poin per Tindakan (menu Perbandingan Spesialisasi) ----------
// 2026-08-23: dirombak atas koreksi user -- SEBELUMNYA sempat dibuat batang 3D (front+top+side
// face) & memakai Total Poin per dokter; user minta grafiknya PERSIS spt referensi yg diberikan
// (batang FLAT 2D bergradasi, legenda berwarna di atas, kategori di sumbu-X, satu seri warna per
// item yg dibandingkan -- pola sama dgn contoh "Pendapatan vs Belanja per Tahun"), dan datanya
// harus Poin PER TINDAKAN (bukan total Poin keseluruhan dokter). Jadi: sumbu-X = nama tindakan
// (top N dgn Poin tertinggi gabungan semua dokter yg dibandingkan), satu seri warna per dokter,
// nilai = Poin tindakan tsb utk dokter itu = (Japel+Operator)/1000 -- sama persis dgn definisi
// kolom "Poin" di tabel "Tindakan Dilaksanakan (Unik)" (TIDAK memasukkan komponen Jasa Anestesi).
const TOP_N_TINDAKAN_CHART = 8;
const CHART_SERIES_PALETTE = [
  { top:'var(--accent-soft-2)', mid:'var(--accent)', bottom:'var(--accent-strong)' },
  { top:'var(--yellow-soft)', mid:'var(--yellow)', bottom:'var(--yellow-strong)' },
  { top:'var(--sage-soft)', mid:'var(--sage)', bottom:'var(--sage-strong)' },
  { top:'var(--warn-soft)', mid:'var(--warn)', bottom:'var(--warn-strong)' },
];

// Rect dgn sudut atas membulat & sudut bawah siku (baseline tetap rata) -- dipakai spy batang
// terlihat spt referensi (bar chart flat 2D bersudut atas membulat tipis), bukan kotak polos.
function roundedTopRectPath(x, y, w, h, r){
  if (h <= 0 || w <= 0) return '';
  const rr = Math.max(0, Math.min(r, w/2, h));
  if (rr <= 0.5) return `M${x.toFixed(1)},${y.toFixed(1)} h${w.toFixed(1)} v${h.toFixed(1)} h${(-w).toFixed(1)} Z`;
  return `M${x.toFixed(1)},${(y+rr).toFixed(1)} A${rr.toFixed(1)},${rr.toFixed(1)} 0 0 1 ${(x+rr).toFixed(1)},${y.toFixed(1)} L${(x+w-rr).toFixed(1)},${y.toFixed(1)} A${rr.toFixed(1)},${rr.toFixed(1)} 0 0 1 ${(x+w).toFixed(1)},${(y+rr).toFixed(1)} L${(x+w).toFixed(1)},${(y+h).toFixed(1)} L${x.toFixed(1)},${(y+h).toFixed(1)} Z`;
}

// Jumlahkan Poin ((Japel+Operator)/1000) per NAMA tindakan, digabung lintas kombinasi
// sub-klasifikasi/dokter-anestesi (sama spt cara tabel "Tindakan Dilaksanakan (Unik)" menghitung
// per baris, hanya di sini dijumlah per nama krn satu tindakan bisa py beberapa kombinasi).
function aggregateTindakanPoin(tindakanArr){
  const m = new Map();
  for (const c of tindakanArr){
    const poin = ((c.japel || 0) + (c.operator || 0)) / 1000;
    m.set(c.name, (m.get(c.name) || 0) + poin);
  }
  return m;
}

function renderDoctorPoinBarChart(rows){
  const wrap = document.getElementById('doctorPoinBarChartWrap');
  const legendWrap = document.getElementById('doctorPoinBarChartLegend');
  const tag = document.getElementById('doctorPoinBarChartTag');
  if (rows.length === 0){
    wrap.innerHTML = `<div class="bar2d-empty">Tidak ada dokter pada spesialisasi ini</div>`;
    if (legendWrap) legendWrap.innerHTML = '';
    if (tag) tag.textContent = 'Poin = (Japel+Operator)/1000 per tindakan, per dokter';
    return;
  }

  const perDoctor = rows.map(r => ({ name: r.name, map: aggregateTindakanPoin(r.tindakan) }));
  const totalByTindakan = new Map();
  perDoctor.forEach(pd => { pd.map.forEach((v, name) => totalByTindakan.set(name, (totalByTindakan.get(name) || 0) + v)); });
  const sortedNames = Array.from(totalByTindakan.keys())
    .filter(n => n !== '(lainnya)' && totalByTindakan.get(n) > 0)
    .sort((a, b) => totalByTindakan.get(b) - totalByTindakan.get(a));
  const shownNames = sortedNames.slice(0, TOP_N_TINDAKAN_CHART);
  const omitted = sortedNames.length - shownNames.length;

  if (legendWrap){
    legendWrap.innerHTML = perDoctor.map((pd, i) => {
      const c = CHART_SERIES_PALETTE[i % CHART_SERIES_PALETTE.length];
      return `<span class="bar2d-legend-item"><span class="bar2d-legend-swatch" style="background:${c.mid}"></span>${escapeHtml(pd.name)}</span>`;
    }).join('');
  }
  if (tag){
    tag.textContent = omitted > 0
      ? `${shownNames.length} dari ${sortedNames.length} tindakan (Poin tertinggi) · Poin = (Japel+Operator)/1000`
      : `Poin = (Japel+Operator)/1000 per tindakan, per dokter`;
  }

  if (shownNames.length === 0){
    wrap.innerHTML = `<div class="bar2d-empty">Tidak ada tindakan dgn Poin pada spesialisasi ini</div>`;
    return;
  }

  const nCat = shownNames.length, nSeries = perDoctor.length;
  const padL = 60, padR = 24, padT = 20, padB = 68;
  const groupGap = 32, barGap = 4;
  const barW = Math.min(42, Math.max(14, 220 / nSeries));
  const groupW = nSeries * barW + (nSeries - 1) * barGap;
  const slotW = groupW + groupGap;
  const plotW = nCat * slotW;
  const W = padL + plotW + padR, H = 300;
  const plotH = H - padT - padB;
  const baseline = padT + plotH;
  const maxVal = Math.max(1, ...shownNames.flatMap(name => perDoctor.map(pd => pd.map.get(name) || 0)));
  const maxChars = Math.max(10, Math.floor(slotW / 6));

  let gridSvg = '';
  for (let g = 0; g <= 4; g++){
    const gy = padT + plotH * g/4;
    const gv = maxVal * (1 - g/4);
    gridSvg += `<line x1="${padL}" y1="${gy.toFixed(1)}" x2="${(W-padR).toFixed(1)}" y2="${gy.toFixed(1)}" class="trend-grid-line"/>`;
    gridSvg += `<text x="${(padL-10).toFixed(1)}" y="${(gy+3).toFixed(1)}" text-anchor="end" class="trend-axis-label">${fmtInt(gv)}</text>`;
  }

  let barsSvg = '';
  shownNames.forEach((name, ci) => {
    const groupX0 = padL + ci*slotW + groupGap/2;
    const cx = groupX0 + groupW/2;
    perDoctor.forEach((pd, si) => {
      const val = pd.map.get(name) || 0;
      const x = groupX0 + si*(barW+barGap);
      const yTop = padT + plotH - (maxVal > 0 ? (val/maxVal)*plotH : 0);
      const h = baseline - yTop;
      const c = CHART_SERIES_PALETTE[si % CHART_SERIES_PALETTE.length];
      const gradId = `bar2dGrad_${ci}_${si}`;
      barsSvg += `<g class="bar2d-item">
        <title>${escapeHtml(pd.name)} — ${escapeHtml(name)}: ${fmtInt(val)} Poin</title>
        <defs><linearGradient id="${gradId}" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="${c.top}"/><stop offset="55%" stop-color="${c.mid}"/><stop offset="100%" stop-color="${c.bottom}"/>
        </linearGradient></defs>
        ${h > 0 ? `<path d="${roundedTopRectPath(x, yTop, barW, h, 4)}" fill="url(#${gradId})"/>` : ''}
        ${val > 0 ? `<text x="${(x+barW/2).toFixed(1)}" y="${(yTop-6).toFixed(1)}" text-anchor="middle" class="bar2d-value-label">${fmtInt(val)}</text>` : ''}
      </g>`;
    });
    const nameShort = name.length > maxChars ? name.slice(0, maxChars-1) + '…' : name;
    barsSvg += `<text x="${cx.toFixed(1)}" y="${(baseline+18).toFixed(1)}" text-anchor="middle" class="bar2d-name-label">${escapeHtml(nameShort)}</text>`;
  });

  wrap.innerHTML = `<svg class="bar2d-svg" width="${W.toFixed(0)}" height="${H}" viewBox="0 0 ${W.toFixed(0)} ${H}">
    ${gridSvg}
    <line x1="${padL}" y1="${baseline.toFixed(1)}" x2="${(W-padR).toFixed(1)}" y2="${baseline.toFixed(1)}" stroke="var(--border)" stroke-width="1.4"/>
    ${barsSvg}
  </svg>`;
}

// ---------- Rincian "Tindakan Unik" & "Obat" per dokter (sama struktur dgn menu Data Dokter) ----------
function renderSpecTindakanRows(items, sort, filterText){
  let filtered = items;
  const ft = (filterText || '').trim().toLowerCase();
  if (ft) filtered = items.filter(r => r.name.toLowerCase().includes(ft) || (r.subklas||'').toLowerCase().includes(ft) || (r.anesName||'').toLowerCase().includes(ft));
  const sorted = sortRows(filtered, sort.key, sort.dir);
  if (sorted.length === 0) return `<tr class="empty-row"><td colspan="5">Tidak ada data</td></tr>`;
  return sorted.map(r => {
    const point = ((r.japel || 0) + (r.operator || 0)) / 1000;
    const subklas = r.subklas ? escapeHtml(r.subklas) : '&mdash;';
    const anesCell = r.anesName
      ? `<span class="anes-badge">${escapeHtml(r.anesName)}</span>`
      : `<span class="anes-none">&mdash;</span>`;
    return `<tr><td class="name-cell">${escapeHtml(r.name)}</td><td class="subklas-cell">${subklas}</td><td class="anes-cell">${anesCell}</td><td class="num mono">${fmtInt(r.count)}</td><td class="num mono">${fmtInt(point)}</td></tr>`;
  }).join('');
}

function renderSpecObatRows(items, sort, filterText){
  let filtered = items;
  const ft = (filterText || '').trim().toLowerCase();
  if (ft) filtered = items.filter(r => r.name.toLowerCase().includes(ft));
  const sorted = sortRows(filtered, sort.key, sort.dir);
  if (sorted.length === 0) return `<tr class="empty-row"><td colspan="3">Tidak ada data</td></tr>`;
  return sorted.map(r => `<tr><td class="name-cell">${escapeHtml(r.name)}</td><td class="num mono">${fmtInt(r.qty)}</td><td class="num mono">${fmtRp(r.profit)}</td></tr>`).join('');
}

function updateSpecDoctorTable(idx, kind, itemsData){
  const table = document.querySelector(`table[data-spec-doctor="${idx}"][data-spec-kind="${kind}"]`);
  if (!table) return;
  const sort = getSpecDoctorSort(idx, kind);
  const filterText = specDoctorFilter.get(`${idx}:${kind}`) || '';
  table.querySelector('tbody').innerHTML = kind === 'tindakan'
    ? renderSpecTindakanRows(itemsData, sort, filterText)
    : renderSpecObatRows(itemsData, sort, filterText);
  table.querySelectorAll('th[data-key]').forEach(th => {
    const arrow = th.querySelector('.arrow');
    arrow.textContent = th.dataset.key === sort.key ? (sort.dir === 1 ? '↑' : '↓') : '';
  });
}

function renderSpecDoctorDetail(rows){
  const wrap = document.getElementById('specDoctorDetailWrap');
  if (rows.length === 0){
    wrap.innerHTML = `<div style="text-align:center; color:var(--text-faint); font-style:italic; padding:16px;">Tidak ada dokter pada spesialisasi ini</div>`;
    return;
  }
  const sorted = [...rows].sort((a,b) => b.total_poin - a.total_poin);
  wrap.innerHTML = sorted.map(r => {
    const tSort = getSpecDoctorSort(r.idx, 'tindakan');
    const oSort = getSpecDoctorSort(r.idx, 'obat');
    const tFilter = specDoctorFilter.get(`${r.idx}:tindakan`) || '';
    const oFilter = specDoctorFilter.get(`${r.idx}:obat`) || '';
    return `
    <div class="spec-doctor-card">
      <div class="spec-doctor-head">
        <h4>${escapeHtml(r.name)}</h4>
        <span class="count-tag">${fmtInt(r.n_unique_tindakan)} tindakan unik &middot; ${fmtInt(r.total_poin)} Poin total</span>
      </div>
      <div class="tables-grid">
        <div class="panel">
          <div class="panel-head">
            <h4><span class="dot"></span>Tindakan Dilaksanakan (Unik)</h4>
            <input class="mini-search" data-spec-doctor="${r.idx}" data-spec-kind="tindakan" placeholder="Filter tindakan&hellip;" value="${escapeHtml(tFilter)}" />
          </div>
          <div class="scroll-body"><table data-spec-doctor="${r.idx}" data-spec-kind="tindakan">
            <thead><tr>
              <th data-key="name">Tindakan<span class="arrow"></span></th>
              <th data-key="subklas">Sub-klasifikasi<span class="arrow"></span></th>
              <th data-key="anesName">Dokter Anestesi<span class="arrow"></span></th>
              <th class="num" data-key="count">Berapa Kali<span class="arrow"></span></th>
              <th class="num" data-key="point">Poin<span class="arrow"></span></th>
            </tr></thead>
            <tbody>${renderSpecTindakanRows(r.tindakan, tSort, tFilter)}</tbody>
          </table></div>
        </div>
        <div class="panel">
          <div class="panel-head">
            <h4><span class="dot"></span>Obat Diresepkan</h4>
            <input class="mini-search" data-spec-doctor="${r.idx}" data-spec-kind="obat" placeholder="Filter obat&hellip;" value="${escapeHtml(oFilter)}" />
          </div>
          <div class="scroll-body"><table data-spec-doctor="${r.idx}" data-spec-kind="obat">
            <thead><tr>
              <th data-key="name">Nama Obat<span class="arrow"></span></th>
              <th class="num" data-key="qty">Qty<span class="arrow"></span></th>
              <th class="num" data-key="profit">Profit<span class="arrow"></span></th>
            </tr></thead>
            <tbody>${renderSpecObatRows(r.obat, oSort, oFilter)}</tbody>
          </table></div>
        </div>
      </div>
    </div>`;
  }).join('');

  wrap.querySelectorAll('table[data-spec-doctor]').forEach(table => {
    const idx = table.dataset.specDoctor, kind = table.dataset.specKind;
    const sort = getSpecDoctorSort(idx, kind);
    table.querySelectorAll('th[data-key]').forEach(th => {
      const arrow = th.querySelector('.arrow');
      arrow.textContent = th.dataset.key === sort.key ? (sort.dir === 1 ? '↑' : '↓') : '';
    });
  });
}

// Event delegation: header-click sort & mini-search utk tabel per-dokter yg dibuat dinamis
// (tidak ada di DOM saat page load, jadi tidak bisa dipasangi listener statis spt tabel lain)
document.getElementById('specDoctorDetailWrap').addEventListener('click', (e) => {
  const th = e.target.closest('th[data-key]');
  if (!th) return;
  const table = th.closest('table[data-spec-doctor]');
  if (!table) return;
  const idx = table.dataset.specDoctor, kind = table.dataset.specKind;
  const sort = getSpecDoctorSort(idx, kind);
  const key = th.dataset.key;
  if (sort.key === key){ sort.dir *= -1; } else { sort.key = key; sort.dir = key === 'name' ? 1 : -1; }
  const row = lastSpecCompareRows.find(r => String(r.idx) === idx);
  if (row) updateSpecDoctorTable(idx, kind, kind === 'tindakan' ? row.tindakan : row.obat);
});
document.getElementById('specDoctorDetailWrap').addEventListener('input', (e) => {
  const inp = e.target.closest('input.mini-search[data-spec-doctor]');
  if (!inp) return;
  const idx = inp.dataset.specDoctor, kind = inp.dataset.specKind;
  specDoctorFilter.set(`${idx}:${kind}`, inp.value);
  const row = lastSpecCompareRows.find(r => String(r.idx) === idx);
  if (row) updateSpecDoctorTable(idx, kind, kind === 'tindakan' ? row.tindakan : row.obat);
});

function renderSpecCompareView(){
  populateSpecTindakanFilter();
  const specValue = specFilterCompare.value;
  const rows = buildSpecCompareRows();
  lastSpecCompareRows = rows;
  const kso = ksoFilter.value || 'Semua KSO';
  const unit = unitFilter.value || 'Semua Unit';
  const tName = specTindakanFilter.value === '' ? 'Semua Tindakan' : specTindakanFilter.options[specTindakanFilter.selectedIndex].textContent;
  document.getElementById('specCompareTitle').textContent = specValue || '—';
  document.getElementById('specCompareSub').textContent =
    `${rows.length} dokter · ${unit} · ${tName} · ${kso} · ${fmtDateID(dateFrom.value)}–${fmtDateID(dateTo.value)}`;
  renderRankChart(rows);
  renderSpecCompareTable(rows);
  renderDoctorPoinBarChart(rows);
  renderSpecDoctorDetail(rows);
}

// ---------- Column header sort clicks (shared across all tables) ----------
document.querySelectorAll('th[data-key]').forEach(th => {
  th.addEventListener('click', () => {
    const kind = th.dataset.table;
    const key = th.dataset.key;
    const sort = currentSort[kind];
    if (sort.key === key){ sort.dir *= -1; } else { sort.key = key; sort.dir = key === 'name' ? 1 : -1; }
    if (kind === 'tindakan' || kind === 'obat') renderAll();
    else if (kind === 'speccompare') renderSpecCompareView();
    else if (kind === 'anesderived') renderAnesDerivedSection();
  });
});

document.querySelectorAll('.mini-search').forEach(inp => {
  inp.addEventListener('input', () => {
    tableFilters[inp.dataset.target] = inp.value;
    renderAll();
  });
});

document.getElementById('logoutBtn').addEventListener('click', () => {
  try { localStorage.removeItem('simrs_auth_until'); } catch (e) {}
  location.reload();
});

// ---------- init ----------
populateDoctorSelect('', null);
</script>
"""

html = html.replace('__DATA_JSON__', data_json)

with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print('written', len(html), 'chars to', OUTPUT_PATH)
