
# 💸 Money Rain Game

**Money Rain** is a 2D arcade-style avoidance and collection game built using Python and Pygame. The objective is simple: collect as much falling money as possible across different lanes while dodging police obstacles to stay alive and achieve the highest score!

---

## 🎮 Game Features

* **Dynamic Gameplay:** Collect falling money items to increase your score (+10 points per cash item).
* **Challenging Obstacles:** Avoid police items! Hitting police cars/obstacles decreases your score (-10 points) and removes one heart (life).
* **Life Recovery System:** Recover lost hearts by maintaining high scores (+1 heart restored for every 500-point milestone maintained without crashing).
* **Speed Levels:** The game speed automatically scales up based on your current score:
  * **Score < 150:** Level 3 (Normal)
  * **Score 150 - 299:** Level 4 (Fast)
  * **Score 300 - 499:** Level 5 (Faster)
  * **Score ≥ 500:** Level 6 (Maximum Speed)
* **Animated Background:** Features smooth dynamic frame-based road animation.

---

## 🕹️ Controls

| Key / Control | Action |
| :--- | :--- |
| **`Left Arrow` / `A`** | Move Player Left |
| **`Right Arrow` / `D`** | Move Player Right |
| **`P`** | Pause Game Prompt |
| **`ESC`** | Exit Game Prompt |

---

## 🚀 Requirements & Installation

### Prerequisites
Make sure you have **Python 3.x** and **Pygame** installed on your system.

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/DipDay/moneyRain.git](https://github.com/DipDay/moneyRain.git)
   cd moneyRain



2. **Install required dependencies:**
```bash
pip install pygame

```


3. **Run the game:**
```bash
python main.py

```



---

## 📁 Project Structure

```text
moneyRain/
├── final_road/        # Background animation frames (.jpg)
├── logo.png           # Window icon image
├── money.png          # Collectible money sprite
├── police.png         # Police obstacle sprite
├── heart.png          # Life status sprite
├── user1.png          # Player sprite (Full health - 3 hearts)
├── user2.png          # Player sprite (Damaged - 2 hearts)
├── user3.png          # Player sprite (Critical - 1 heart)
├── label.png          # Score background banner
├── main.py            # Main game entry point and logic
└── README.md          # Project documentation

```

---

## 📝 Refactoring & Maintainability

This repository contains code refactored for **PEP 8 style guidelines**, enhanced readability, structured modular functions, and optimized input event handling while keeping all original assets and core mechanics intact.
