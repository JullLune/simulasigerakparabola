"""
SIMULASI GERAK PARABOLA — FLASK WEB APP
========================================
Backend  : Flask (satu file)
Frontend : HTML + Tailwind CSS (CDN) + Chart.js
Design   : Editorial / aesthetic (serif · plum-midnight palette)
Credit   : by Rajwa Rifa Rabbani (lnzmu)
"""

from flask import Flask, render_template_string, request
import math


app = Flask(__name__)


# ─────────────────────────────────────────────────────────────
#  FISIKA
# ─────────────────────────────────────────────────────────────
def calculate_projectile(v0, theta_deg, g):
    """Menghitung seluruh parameter gerak parabola ideal."""
    theta_rad = math.radians(theta_deg)

    vx = v0 * math.cos(theta_rad)
    vy = v0 * math.sin(theta_rad)

    t_peak  = vy / g
    h_max   = vy ** 2 / (2 * g)
    t_total = 2 * vy / g
    range_x = vx * t_total

    return {
        "theta_rad": theta_rad,
        "vx":        vx,
        "vy":        vy,
        "t_peak":    t_peak,
        "h_max":     h_max,
        "t_total":   t_total,
        "range":     range_x,
    }


def generate_trajectory(v0, theta_deg, g, t_total, points=240):
    """Menghasilkan titik-titik lintasan (x, y) untuk chart."""
    theta_rad = math.radians(theta_deg)
    vx = v0 * math.cos(theta_rad)
    vy = v0 * math.sin(theta_rad)

    data = []
    for i in range(points):
        t = t_total * i / (points - 1)
        x = vx * t
        y = vy * t - 0.5 * g * t ** 2
        data.append({"x": round(x, 4), "y": round(y, 4)})
    return data


# ─────────────────────────────────────────────────────────────
#  TEMPLATE HTML
# ─────────────────────────────────────────────────────────────
TEMPLATE = r"""
<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Simulasi Gerak Parabola · lnzmu</title>

<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400;1,500;1,600;1,700&family=Outfit:wght@200;300;400;500;600&family=JetBrains+Mono:wght@300;400;500;600&display=swap" rel="stylesheet">

<script>
  tailwind.config = {
    theme: {
      extend: {
        fontFamily: {
          serif: ['Fraunces', 'Georgia', 'serif'],
          sans:  ['Outfit', 'system-ui', 'sans-serif'],
          mono:  ['JetBrains Mono', 'monospace'],
        },
        colors: {
          ink:    '#0A0812',
          plum:   '#140F1F',
          cream:  '#F5F1EA',
          mauve:  '#A39BB5',
          whisper:'#6E6780',
          rose:   '#E88EAE',
          blush:  '#F2A9C4',
          lilac:  '#B896FF',
          sky:    '#7DD3FC',
          honey:  '#F5C77E',
          mint:   '#8EE8C1',
        },
      },
    },
  };
</script>

<style>
  html, body { scroll-behavior: smooth; }
  body {
    font-feature-settings: "ss01", "cv11";
    background-color: #0A0812;
    color: #F5F1EA;
  }

  /* Fine grain texture overlay */
  body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 1;
    opacity: 0.035;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 220 220' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  }

  /* Serif display refinement */
  .display {
    font-family: 'Fraunces', serif;
    font-variation-settings: "SOFT" 40, "WONK" 0, "opsz" 144;
    letter-spacing: -0.02em;
    line-height: 1.02;
  }
  .display-italic {
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-variation-settings: "SOFT" 50, "WONK" 1, "opsz" 90;
  }

  /* Letter-spaced micro label */
  .micro {
    font-size: 10px;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    font-weight: 500;
  }

  /* Ambient aurora blobs */
  .aurora-1 {
    background: radial-gradient(circle,
      rgba(184,150,255,0.16) 0%,
      rgba(184,150,255,0.05) 40%,
      transparent 70%);
  }
  .aurora-2 {
    background: radial-gradient(circle,
      rgba(232,142,174,0.14) 0%,
      rgba(232,142,174,0.04) 45%,
      transparent 72%);
  }
  .aurora-3 {
    background: radial-gradient(circle,
      rgba(125,211,252,0.13) 0%,
      rgba(125,211,252,0.04) 45%,
      transparent 72%);
  }

  /* Underline field */
  .field {
    width: 100%;
    background: transparent;
    border: 0;
    border-bottom: 1px solid rgba(245,241,234,0.14);
    padding: 12px 4px 12px 0;
    color: #F5F1EA;
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    font-weight: 400;
    outline: none;
    transition: border-color .3s ease, color .3s ease;
    border-radius: 0;
  }
  .field::placeholder {
    color: rgba(163,155,181,0.35);
    font-weight: 300;
  }
  .field:focus {
    border-bottom-color: #E88EAE;
  }
  .field::-webkit-outer-spin-button,
  .field::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
  .field[type=number] { -moz-appearance: textfield; }

  /* Soft frame */
  .frame {
    background: linear-gradient(180deg, rgba(20,15,31,0.85) 0%, rgba(10,8,18,0.92) 100%);
    border: 1px solid rgba(245,241,234,0.07);
    border-radius: 32px;
    position: relative;
    overflow: hidden;
  }
  .frame::after {
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 32px;
    padding: 1px;
    background: linear-gradient(135deg,
      rgba(245,241,234,0.10) 0%,
      transparent 40%,
      transparent 60%,
      rgba(245,241,234,0.06) 100%);
    -webkit-mask: linear-gradient(#000 0 0) content-box,
                  linear-gradient(#000 0 0);
    -webkit-mask-composite: xor;
            mask-composite: exclude;
    pointer-events: none;
  }

  /* Ornament hairline */
  .ornament {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    color: rgba(163,155,181,0.55);
  }
  .ornament .line {
    height: 1px;
    width: 56px;
    background: linear-gradient(90deg,
      transparent,
      rgba(163,155,181,0.4),
      transparent);
  }

  /* Fade animations */
  @keyframes rise {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .rise    { animation: rise .9s cubic-bezier(.22,.8,.28,1) both; }
  .delay-1 { animation-delay: .06s; }
  .delay-2 { animation-delay: .14s; }
  .delay-3 { animation-delay: .22s; }
  .delay-4 { animation-delay: .30s; }
  .delay-5 { animation-delay: .38s; }
  .delay-6 { animation-delay: .46s; }

  /* Slow shimmer */
  @keyframes shimmer {
    0%,100% { opacity: .55; }
    50%     { opacity: 1; }
  }
  .shimmer { animation: shimmer 4s ease-in-out infinite; }

  /* CTA button — elegant, not loud */
  .cta {
    position: relative;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 15px 30px;
    border-radius: 999px;
    font-family: 'Outfit', sans-serif;
    font-weight: 500;
    font-size: 14px;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #0A0812;
    background: #F5F1EA;
    border: 1px solid #F5F1EA;
    transition: all .35s cubic-bezier(.22,.8,.28,1);
    cursor: pointer;
    width: 100%;
  }
  .cta:hover {
    background: transparent;
    color: #F5F1EA;
    letter-spacing: 0.18em;
    box-shadow: 0 0 0 1px rgba(245,241,234,0.25),
                0 0 40px -8px rgba(232,142,174,0.35);
  }
  .cta:active { transform: scale(0.985); }
  .cta .arrow {
    transition: transform .35s ease;
  }
  .cta:hover .arrow { transform: translateX(6px); }

  /* Credit badge — like a wax seal */
  .badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 8px 16px 8px 12px;
    border-radius: 999px;
    background: rgba(20,15,31,0.7);
    border: 1px solid rgba(245,241,234,0.09);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: all .3s ease;
    font-family: 'Outfit', sans-serif;
  }
  .badge:hover {
    border-color: rgba(232,142,174,0.35);
    background: rgba(20,15,31,0.9);
  }
  .badge .star {
    color: #E88EAE;
    font-size: 12px;
    line-height: 1;
  }

  /* Preset chips */
  .chip {
    padding: 7px 14px;
    border-radius: 999px;
    border: 1px solid rgba(245,241,234,0.09);
    background: transparent;
    color: #A39BB5;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.02em;
    transition: all .28s ease;
    cursor: pointer;
  }
  .chip:hover {
    border-color: rgba(232,142,174,0.5);
    color: #F5F1EA;
    background: rgba(232,142,174,0.06);
  }

  /* Editorial number block */
  .stat-num {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 300;
    font-size: 2.1rem;
    line-height: 1;
    color: #F5F1EA;
    letter-spacing: -0.02em;
  }
  @media (min-width: 768px) {
    .stat-num { font-size: 2.4rem; }
  }
  .stat-unit {
    font-family: 'Outfit', sans-serif;
    font-weight: 300;
    font-size: 12px;
    color: #6E6780;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-left: 6px;
  }

  /* Hairline */
  .hairline {
    height: 1px;
    background: linear-gradient(90deg,
      transparent,
      rgba(245,241,234,0.10) 20%,
      rgba(245,241,234,0.10) 80%,
      transparent);
  }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 8px; }
  ::-webkit-scrollbar-track { background: #0A0812; }
  ::-webkit-scrollbar-thumb {
    background: rgba(245,241,234,0.08);
    border-radius: 8px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: rgba(245,241,234,0.16);
  }
</style>
</head>

<body class="font-sans min-h-screen antialiased relative">

<!-- ── Ambient aurora ─────────────────────────────────── -->
<div class="fixed inset-0 overflow-hidden pointer-events-none z-0">
  <div class="absolute -top-52 -left-40 w-[720px] h-[720px] aurora-1 rounded-full blur-[100px]"></div>
  <div class="absolute top-[15%] -right-48 w-[680px] h-[680px] aurora-2 rounded-full blur-[110px]"></div>
  <div class="absolute -bottom-52 left-[10%] w-[700px] h-[700px] aurora-3 rounded-full blur-[120px]"></div>
</div>

<!-- ── Credit badge (floating) ─────────────────────────── -->
<div class="fixed top-6 right-6 z-30 rise delay-4">
  <div class="badge">
    <span class="star">✦</span>
    <span class="text-[11px] tracking-wide text-mauve">
      by <span class="text-cream font-medium">Rajwa Rifa Rabbani</span>
      <span class="mx-1 text-whisper">·</span>
      <span class="text-blush font-mono text-[10px]">lnzmu</span>
    </span>
  </div>
</div>

<main class="relative z-10 max-w-6xl mx-auto px-6 md:px-10 py-14 md:py-24">

  <!-- ═══ HERO ═══════════════════════════════════════════ -->
  <header class="text-center mb-16 md:mb-24 rise">

    <p class="micro text-mauve mb-6">Physics · Simulation · No. 01</p>

    <h1 class="display text-[clamp(2.6rem,7vw,5.6rem)] text-cream">
      Gerak
      <span class="display-italic text-blush">Parabola</span>
    </h1>

    <div class="ornament my-9">
      <span class="line"></span>
      <span class="text-[10px] shimmer">✦</span>
      <span class="line"></span>
    </div>

    <p class="max-w-xl mx-auto text-mauve text-[15px] md:text-base leading-[1.85] font-light">
      Sebuah studi kecil tentang gerak, gravitasi, dan busur yang membentuk lintasan.
      Masukkan nilainya, dan saksikan kurva itu terbentuk.
    </p>

  </header>

  <!-- ═══ ERROR ═══════════════════════════════════════════ -->
  {% if error %}
  <div class="mb-12 rise delay-1">
    <div class="frame px-6 py-5 flex items-start gap-4" style="border-left: 2px solid #E88EAE;">
      <span class="text-blush text-lg leading-none mt-0.5">✦</span>
      <div>
        <p class="micro text-blush mb-1">Input tidak sesuai</p>
        <p class="text-mauve text-sm font-light">{{ error }}</p>
      </div>
    </div>
  </div>
  {% endif %}

  <!-- ═══ SPLIT: FORM + CHART ════════════════════════════ -->
  <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 md:gap-10 mb-16">

    <!-- ── Form ─────────────────────────────────────── -->
    <section class="lg:col-span-4 rise delay-1">
      <div class="frame p-8 md:p-10 h-full">
        <p class="micro text-mauve mb-3">Parameter</p>
        <h2 class="display text-2xl md:text-3xl text-cream mb-10">
          Variabel <span class="display-italic text-lilac">masukan</span>
        </h2>

        <form method="POST" class="space-y-9" id="simForm">

          <div>
            <label class="flex items-baseline justify-between mb-3">
              <span class="micro text-mauve">Kecepatan awal</span>
              <span class="display-italic text-blush text-lg">v₀</span>
            </label>
            <div class="flex items-baseline gap-3">
              <input type="number" step="any" name="v0" id="v0" required
                     placeholder="20" value="{{ v0 }}" class="field">
              <span class="text-[11px] font-mono text-whisper whitespace-nowrap">m/s</span>
            </div>
          </div>

          <div>
            <label class="flex items-baseline justify-between mb-3">
              <span class="micro text-mauve">Sudut elevasi</span>
              <span class="display-italic text-lilac text-lg">θ</span>
            </label>
            <div class="flex items-baseline gap-3">
              <input type="number" step="any" name="theta" id="theta" required
                     placeholder="30" value="{{ theta }}" class="field">
              <span class="text-[11px] font-mono text-whisper whitespace-nowrap">derajat</span>
            </div>
          </div>

          <div>
            <label class="flex items-baseline justify-between mb-3">
              <span class="micro text-mauve">Gravitasi</span>
              <span class="display-italic text-sky text-lg">g</span>
            </label>
            <div class="flex items-baseline gap-3">
              <input type="number" step="any" name="g" id="g" required
                     placeholder="9.8" value="{{ g }}" class="field">
              <span class="text-[11px] font-mono text-whisper whitespace-nowrap">m/s²</span>
            </div>
          </div>

          <div class="pt-3">
            <button type="submit" class="cta">
              Hitung
              <span class="arrow">→</span>
            </button>
          </div>

        </form>

        <div class="mt-10 pt-8 border-t border-cream/[0.06]">
          <p class="micro text-whisper mb-4">Coba cepat</p>
          <div class="flex flex-wrap gap-2">
            <button type="button" data-preset="15,45,9.8"   class="chip">15 · 45°</button>
            <button type="button" data-preset="20,30,9.8"   class="chip">20 · 30°</button>
            <button type="button" data-preset="25,60,9.8"   class="chip">25 · 60°</button>
            <button type="button" data-preset="30,45,1.62"  class="chip">Bulan</button>
          </div>
        </div>
      </div>
    </section>

    <!-- ── Chart ────────────────────────────────────── -->
    <section class="lg:col-span-8 rise delay-2">
      <div class="frame p-6 md:p-8 h-full flex flex-col">

        <div class="flex items-end justify-between mb-6">
          <div>
            <p class="micro text-mauve mb-2">Visualisasi</p>
            <h2 class="display text-2xl md:text-3xl text-cream">
              Lintasan <span class="display-italic text-blush">proyektil</span>
            </h2>
          </div>
          <div class="hidden sm:flex items-center gap-5 text-[10px] tracking-widest uppercase text-whisper">
            <span class="flex items-center gap-2">
              <span class="w-1.5 h-1.5 rounded-full bg-mint"></span>Awal
            </span>
            <span class="flex items-center gap-2">
              <span class="w-1.5 h-1.5 rounded-full bg-honey"></span>Puncak
            </span>
            <span class="flex items-center gap-2">
              <span class="w-1.5 h-1.5 rounded-full bg-blush"></span>Jatuh
            </span>
          </div>
        </div>

        {% if result %}
        <div class="relative flex-1 min-h-[340px] md:min-h-[420px]">
          <canvas id="trajectoryChart"></canvas>
        </div>
        {% else %}
        <div class="flex-1 flex flex-col items-center justify-center text-center py-20 md:py-28 min-h-[340px]">
          <div class="display-italic text-6xl md:text-7xl text-mauve/25 mb-4">∿</div>
          <p class="text-mauve text-sm font-light max-w-xs leading-relaxed">
            Isi parameter di samping, dan kurva akan tergambar di sini.
          </p>
        </div>
        {% endif %}

      </div>
    </section>

  </div>

  <!-- ═══ HASIL ═══════════════════════════════════════════ -->
  {% if result %}
  <section class="rise delay-3 mb-16">

    <div class="flex items-center gap-5 mb-10">
      <span class="hairline flex-1"></span>
      <span class="micro text-mauve">Hasil</span>
      <span class="hairline flex-1"></span>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-3 gap-y-12 gap-x-8 md:gap-y-14 md:gap-x-12">

      {% set stats = [
        ('Komponen vx',      result.vx,      'm/s'),
        ('Komponen vy',      result.vy,      'm/s'),
        ('Waktu puncak',     result.t_peak,  's'),
        ('Tinggi maksimum',  result.h_max,   'm'),
        ('Waktu total',      result.t_total, 's'),
        ('Jangkauan',        result.range,   'm'),
      ] %}

      {% for label, value, unit in stats %}
      <div class="text-center rise delay-{{ loop.index }}">
        <p class="micro text-whisper mb-4">{{ label }}</p>
        <p class="stat-num">
          {{ "%.2f"|format(value) }}<span class="stat-unit">{{ unit }}</span>
        </p>
      </div>
      {% endfor %}

    </div>

  </section>

  <!-- ═══ DETAIL ══════════════════════════════════════════ -->
  <section class="rise delay-4 mb-20">
    <div class="frame p-8 md:p-10">

      <div class="flex items-center gap-5 mb-8">
        <span class="text-blush text-sm">✦</span>
        <span class="micro text-mauve">Detail perhitungan</span>
        <span class="hairline flex-1"></span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-x-16 gap-y-0">

        {% set details = [
          ('v₀',          '%.4f m/s'|format(v0)),
          ('θ',           '%.4f °'|format(theta)),
          ('g',           '%.4f m/s²'|format(g)),
          ('θ (radian)',  '%.4f rad'|format(result.theta_rad)),
          ('vx',          '%.4f m/s'|format(result.vx)),
          ('vy',          '%.4f m/s'|format(result.vy)),
          ('t puncak',    '%.4f s'|format(result.t_peak)),
          ('tinggi maks', '%.4f m'|format(result.h_max)),
          ('waktu total', '%.4f s'|format(result.t_total)),
          ('jangkauan',   '%.4f m'|format(result.range)),
        ] %}

        {% for label, value in details %}
        <div class="flex items-baseline justify-between py-3 border-b border-cream/[0.05]">
          <span class="font-serif italic text-mauve text-sm">{{ label }}</span>
          <span class="font-mono text-cream text-sm font-light">{{ value }}</span>
        </div>
        {% endfor %}

      </div>

      <div class="mt-10 pt-8 border-t border-cream/[0.05]">
        <p class="micro text-whisper mb-4">Persamaan</p>
        <div class="space-y-2 font-serif italic text-mauve text-base md:text-lg leading-relaxed">
          <p>x(t) <span class="text-whisper">=</span> v₀ · cos θ · t</p>
          <p>y(t) <span class="text-whisper">=</span> v₀ · sin θ · t <span class="text-whisper">−</span> ½ g t²</p>
        </div>
      </div>

    </div>
  </section>
  {% endif %}

  <!-- ═══ SIGNATURE ═══════════════════════════════════════ -->
  <footer class="rise delay-5 text-center pt-10 pb-6">

    <div class="ornament mb-8">
      <span class="line"></span>
      <span class="text-[10px] shimmer text-blush">✦</span>
      <span class="line"></span>
    </div>

    <p class="micro text-whisper mb-5">Disusun oleh</p>

    <h3 class="display text-3xl md:text-4xl text-cream mb-2">
      Rajwa Rifa Rabbani
    </h3>

    <p class="display-italic text-blush text-lg md:text-xl mb-8">
      — lnzmu —
    </p>

    <p class="text-whisper text-xs font-light tracking-wide max-w-md mx-auto leading-relaxed">
      Hambatan udara diabaikan · gravitasi konstan · titik awal pada y = 0
    </p>

  </footer>

</main>

<!-- ═══ SCRIPT ═══════════════════════════════════════════ -->
<script>
document.querySelectorAll('[data-preset]').forEach(btn => {
  btn.addEventListener('click', () => {
    const [v0, theta, g] = btn.dataset.preset.split(',');
    document.getElementById('v0').value    = v0;
    document.getElementById('theta').value = theta;
    document.getElementById('g').value     = g;
  });
});

{% if result %}
const trajectory = {{ trajectory|tojson }};
const peakX      = {{ result.vx * result.t_peak }};
const hMax       = {{ result.h_max }};
const rangeX     = {{ result.range }};

const canvas = document.getElementById('trajectoryChart');
const ctx    = canvas.getContext('2d');

function buildGradients() {
  const w = canvas.parentElement.clientWidth;
  const h = canvas.parentElement.clientHeight;

  const line = ctx.createLinearGradient(0, 0, w, 0);
  line.addColorStop(0.00, '#7DD3FC');
  line.addColorStop(0.50, '#B896FF');
  line.addColorStop(1.00, '#E88EAE');

  const fill = ctx.createLinearGradient(0, 0, 0, h);
  fill.addColorStop(0.00, 'rgba(184,150,255,0.22)');
  fill.addColorStop(0.55, 'rgba(232,142,174,0.07)');
  fill.addColorStop(1.00, 'rgba(232,142,174,0.00)');

  return { line, fill };
}

const { line: lineGrad, fill: fillGrad } = buildGradients();

const pathPoints = [
  { x: 0, y: 0 },
  ...trajectory.filter(p => p.x > 0 && p.x < rangeX),
  { x: rangeX, y: 0 },
];

new Chart(ctx, {
  type: 'line',
  data: {
    datasets: [
      {
        label: 'Lintasan',
        data: pathPoints,
        borderColor: lineGrad,
        backgroundColor: fillGrad,
        borderWidth: 2.4,
        fill: 'origin',
        tension: 0.42,
        pointRadius: 0,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: '#E88EAE',
        pointHoverBorderColor: '#F5F1EA',
        pointHoverBorderWidth: 1.5,
      },
      {
        label: 'Titik penting',
        data: [
          { x: 0,      y: 0 },
          { x: peakX,  y: hMax },
          { x: rangeX, y: 0 },
        ],
        backgroundColor: ['#8EE8C1', '#F5C77E', '#E88EAE'],
        borderColor: '#F5F1EA',
        borderWidth: 1.5,
        pointRadius: 7,
        pointHoverRadius: 9,
        showLine: false,
      },
    ],
  },
  options: {
    parsing: false,
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'nearest', intersect: false },
    animation: { duration: 1400, easing: 'easeOutQuart' },
    layout: { padding: { top: 20, right: 24, bottom: 4, left: 4 } },
    scales: {
      x: {
        type: 'linear',
        min: 0,
        grace: '4%',
        grid: { color: 'rgba(245,241,234,0.045)', drawBorder: false },
        border: { display: false },
        ticks: {
          color: '#6E6780',
          font: { family: 'JetBrains Mono', size: 10, weight: 300 },
          padding: 8,
        },
        title: {
          display: true,
          text: 'posisi horizontal · x (m)',
          color: '#6E6780',
          font: { family: 'Outfit', size: 10, weight: 300 },
          padding: { top: 8 },
        },
      },
      y: {
        type: 'linear',
        min: 0,
        grace: '6%',
        grid: { color: 'rgba(245,241,234,0.045)', drawBorder: false },
        border: { display: false },
        ticks: {
          color: '#6E6780',
          font: { family: 'JetBrains Mono', size: 10, weight: 300 },
          padding: 8,
        },
        title: {
          display: true,
          text: 'posisi vertikal · y (m)',
          color: '#6E6780',
          font: { family: 'Outfit', size: 10, weight: 300 },
          padding: { bottom: 8 },
        },
      },
    },
    plugins: {
      legend: { display: false },
      tooltip: {
        backgroundColor: 'rgba(10,8,18,0.96)',
        borderColor: 'rgba(245,241,234,0.12)',
        borderWidth: 1,
        titleColor: '#F5F1EA',
        bodyColor: '#A39BB5',
        padding: 14,
        cornerRadius: 12,
        displayColors: false,
        titleFont: { family: 'Fraunces', size: 11, style: 'italic' },
        bodyFont: { family: 'JetBrains Mono', size: 11 },
        callbacks: {
          title: () => 'titik lintasan',
          label: (item) => {
            const p = item.raw;
            return `x = ${p.x.toFixed(2)} m   ·   y = ${p.y.toFixed(2)} m`;
          },
        },
      },
    },
  },
});

let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    const chart = Chart.getChart('trajectoryChart');
    if (!chart) return;
    const { line, fill } = buildGradients();
    chart.data.datasets[0].borderColor = line;
    chart.data.datasets[0].backgroundColor = fill;
    chart.update('none');
  }, 200);
});
{% endif %}
</script>

</body>
</html>
"""


# ─────────────────────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    context = {
        "error":      None,
        "result":     None,
        "trajectory": None,
        "v0": "", "theta": "", "g": "",
    }

    if request.method == "POST":
        v0_raw    = request.form.get("v0", "").strip()
        theta_raw = request.form.get("theta", "").strip()
        g_raw     = request.form.get("g", "").strip()

        context["v0"]    = v0_raw
        context["theta"] = theta_raw
        context["g"]     = g_raw

        try:
            if not v0_raw or not theta_raw or not g_raw:
                raise ValueError("Semua kolom harus diisi.")

            v0    = float(v0_raw)
            theta = float(theta_raw)
            g     = float(g_raw)

            if v0 <= 0:
                raise ValueError("Kecepatan awal harus lebih besar dari nol.")
            if g <= 0:
                raise ValueError("Gravitasi harus lebih besar dari nol.")
            if not (0 < theta < 90):
                raise ValueError("Sudut elevasi harus di antara 0° dan 90°.")

            r    = calculate_projectile(v0, theta, g)
            traj = generate_trajectory(v0, theta, g, r["t_total"])

            context["result"]     = r
            context["trajectory"] = traj
            context["v0"]         = v0
            context["theta"]      = theta
            context["g"]          = g

        except ValueError as err:
            msg = str(err)
            if "could not convert" in msg or msg == "":
                msg = "Masukkan angka yang valid pada setiap kolom."
            context["error"] = msg

    return render_template_string(TEMPLATE, **context)


# ─────────────────────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
