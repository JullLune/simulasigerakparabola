<div align="center">

# 🏹 Gerak Parabola

### *Projectile Motion — calculated, visualized, understood.*

<p>
  <a href="https://lnzmu01pyhost.pythonanywhere.com/">
    <img src="https://img.shields.io/badge/Live%20Demo-Open%20App-e88eae?style=for-the-badge&logo=rocket&logoColor=white" alt="Live Demo">
  </a>
  <img src="https://img.shields.io/badge/Python-Flask-0A0812?style=for-the-badge&logo=python&logoColor=white" alt="Python Flask">
  <img src="https://img.shields.io/badge/Chart.js-Visualization-A39BB5?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Chart.js">
</p>

<p>
  A small web-based physics project for calculating and visualizing<br>
  <b>ideal projectile motion</b> using Python, Flask, and interactive web technologies.
</p>

<br>

**[ ✦ OPEN LIVE DEMO ✦ ](https://lnzmu01pyhost.pythonanywhere.com/)**

</div>

---

## ◌ Overview

**Gerak Parabola** is an interactive projectile-motion simulator.

Enter the initial velocity, launch angle, and gravitational acceleration — the application calculates the important physical quantities and draws the projectile trajectory directly in the browser.

The project is intentionally simple in its physics model, but polished in presentation:

> **Physics → Algorithm → Calculation → Visualization**

The backend performs the projectile-motion calculations and trajectory generation, while the frontend presents the results through an aesthetic interactive interface.

---

## ✦ What It Calculates

| Quantity | Formula | Unit |
|---|---|---:|
| Horizontal velocity | `vx = v₀ cos(θ)` | m/s |
| Vertical velocity | `vy = v₀ sin(θ)` | m/s |
| Time to peak | `t_peak = vy / g` | s |
| Maximum height | `h_max = vy² / (2g)` | m |
| Total flight time | `t_total = 2vy / g` | s |
| Horizontal range | `R = vx × t_total` | m |
| Horizontal position | `x(t) = vx × t` | m |
| Vertical position | `y(t) = vy × t − ½gt²` | m |

### Model assumptions

- Air resistance is ignored.
- Gravitational acceleration is constant.
- The projectile starts at `y = 0`.
- The launch angle is between `0°` and `90°`.
- The simulation uses an ideal 2D projectile-motion model.

---

## ✧ Features

**Interactive input**

Enter:

```text
v₀  → initial velocity
θ   → launch angle
g   → gravitational acceleration
```

**Automatic validation**

The application checks that:

```text
v₀ > 0
g  > 0
0° < θ < 90°
```

Invalid values are rejected with a readable error message before calculation.

**Trajectory visualization**

The generated trajectory is plotted interactively in the browser, with important locations such as the starting point, peak, and landing point highlighted.

**Preset simulations**

Quick presets are included for common configurations, including Earth-like and Moon-like gravity.

---

## 🌑 Design Direction

The interface follows an **editorial / aesthetic** visual language:

```text
plum · midnight · cream
soft gradients
serif display typography
monospace numerical data
subtle motion
minimal borders
```

The goal is to make a technical physics calculator feel more like a small digital science publication than a plain form.

---

## 🛠 Tech Stack

### Backend

- 🐍 **Python**
- 🌶 **Flask**
- `math`

### Frontend

- HTML5
- Tailwind CSS
- JavaScript
- Chart.js

### Deployment

- ☁️ PythonAnywhere

---

## 🚀 Live Demo

Try the deployed application:

### **[lnzmu01pyhost.pythonanywhere.com](https://lnzmu01pyhost.pythonanywhere.com/)**

No installation required — just open the website and enter the simulation parameters.

---

## 💻 Run Locally

Clone the repository:

```bash
git clone https://github.com/your-username/gerak-parabola.git
cd gerak-parabola
```

Install the dependency:

```bash
pip install flask
```

Run the application:

```bash
python app.py
```

Then open the local Flask address shown in the terminal.

> The current application is designed as a compact single-file Flask web app, with the backend logic and HTML template contained in the Python file.

---

## 📁 Project Structure

```text
gerak-parabola/
│
├── app.py
├── README.md
└── assets/
```

---

## 🧠 How It Works

```text
        INPUT
          │
          ▼
   Validate parameters
          │
          ▼
   Convert θ → radians
          │
          ▼
   Calculate vx and vy
          │
          ▼
 ┌─────────────────────┐
 │ t_peak              │
 │ h_max               │
 │ t_total             │
 │ range               │
 └─────────────────────┘
          │
          ▼
   Generate trajectory
          │
          ▼
    Render Chart.js
          │
          ▼
        OUTPUT
```

In other words:

> **The equations stay classical. The interface doesn't have to.**

---

## 🌌 Example

For:

```text
v₀ = 20 m/s
θ  = 45°
g  = 9.8 m/s²
```

the simulator calculates the velocity components, peak time, maximum height, total flight time, horizontal range, and the complete `(x, y)` trajectory.

---

## ✦ Project Identity

```text
Physics · Programming · Simulation
```

Designed and developed by:

### **Rajwa Rifa Rabbani**
`lnzmu`

---

<div align="center">

### *Same equations. Bigger horizons.* 🪐

**[ ✦ Live Demo ✦ ](https://lnzmu01pyhost.pythonanywhere.com/)**

</div>
