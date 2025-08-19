# Flappy AI (Pygame)

A simple **Flappy Bird–style** project built with Python and Pygame.  
Pipes spawn at random heights and slide left; the bird (a black circle) auto-flaps to survive as long as possible.

---

## 🎮 Features
- **Classic pipes** with fixed gap (default: 180 px)
- **Auto-flap logic** using a simple rule (no manual controls)
- **Score tracking** when passing pipes
- **Lightweight rendering** (rectangles + circle) for clarity

---

## ✅ Requirements
- Python 3.8+  
- Pygame 2.x

---

## 🛠️ Installation

1) Clone the repo:
```bash
git clone https://github.com/your-username/flappy-ai.git
cd flappy-ai
```

2) Install dependencies:
```bash
pip install pygame
```

---

## ▶️ Run
```bash
python flappy.py
```

---

## 📁 Project Structure (minimal)
```
.
├─ flappy.py          # main game file (your script)
├─ README.md          # this file
└─ LICENCE.md         # the MIT licence
```

---

## ⚙️ How It Works
- The **bird** starts at `x = 200`, `y = screen_height / 2`, radius = `player_size` (default 20).
- **Pipes** are `[x, gap_top, gap_bottom]` with `gap_bottom = gap_top + 180` (configurable).
- Every frame:
  - Pipes move left by 4 px and are drawn as two rectangles (top & bottom).
  - The game selects the **current pipe** (the first whose right edge is still ahead of the bird) for logic/collision.
  - The bird’s **momentum** makes it rise for a set distance when flapping, otherwise it falls.
  - Score increases over time and when pipes leave the screen to the left.

**Key constants in this version**
- Screen: `1100 × 700`
- Pipe width: `120`
- Pipe gap: `180`
- Bird radius: `20`
- Gravity step: `+8` px down when not flapping
- Flap step: `−12` px per frame while momentum is active

---

## 🧠 Notes on Logic (to help future you)
- Choose the **current pipe** *after* moving/drawing all pipes:
  - A pipe is “current” if `pipe_x + pipe_width > player_x`.
  - This prevents switching to the next pipe too early.
- For simple auto-flap behavior, compare the bird’s `y` with the **gap center** of the current pipe.

---

## 🚀 Ideas / Future Work
- Replace the rule with a small **neural net / genetic algorithm**
- Add **sprites**, parallax background, and **sound effects**

---

## 📜 License
MIT License — do whatever you like, attribution appreciated.
