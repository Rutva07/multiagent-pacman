# 🧠 Multi-Agent Pacman AI

This project implements intelligent agents for the classic **Pacman** game using **multi-agent search algorithms** including **Minimax**, **Alpha-Beta Pruning**, and **Expectimax**. Agents are also equipped with customized evaluation functions to perform competitively against ghosts in a variety of game layouts.

---

## 🎮 Project Overview

This is a course project where we design decision-making agents in adversarial and stochastic environments. The main focus is on implementing and comparing different AI strategies in the Pacman world, where Pacman must navigate the maze, avoid ghosts, and collect food.

---

## 🔍 Features Implemented

### ✅ Reflex Agent
- A basic agent that evaluates state-action pairs based on proximity to food and ghosts.
- Custom evaluation logic written to improve survival and food collection.

### ✅ Minimax Agent
- Implements the **Minimax algorithm** to simulate adversarial decision-making between Pacman and ghosts.
- Searches to configurable depth.

### ✅ Alpha-Beta Pruning
- Optimized version of Minimax using **Alpha-Beta Pruning** to reduce computation.
- Same output quality as Minimax, but significantly faster.

### ✅ Expectimax Agent
- Models ghosts as probabilistic agents using **Expectimax**.
- Better suited for dealing with random ghost behavior (non-adversarial).

### ✅ Advanced Evaluation Function
- Custom function to evaluate game states rather than actions.
- Factors include food distance, ghost proximity, scared timers, remaining capsules, etc.
- Allows agents to play efficiently even with limited search depth.

---

## 🧪 Testing and Autograder

The project includes an **autograder** that checks correctness, efficiency, and performance for each agent type.

**Usage:**
```bash
python autograder.py -q q1  # Test Reflex Agent
python autograder.py -q q2  # Test Minimax Agent
python autograder.py -q q3  # Test Alpha-Beta Agent
python autograder.py -q q4  # Test Expectimax Agent
python autograder.py -q q5  # Test Better Evaluation Function
Use --no-graphics for faster execution:
