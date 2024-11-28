
# Snake AI Training Results

This document contains details and results for each trained model of the Snake AI, including commands to reproduce them.

## Baseline Model
- **Training Sessions**: 10,000
- **Q-function**: Temporal Difference (TD)
- **Epsilon**: 0.1 (Static)
- **Learning Rate**: Default
- **Discount Factor**: Default
- **Max Length Reached**: 6 (Session 4253)
- **Command**:
  ```bash
  ./snake --save /Users/lgreau/goinfre/models/baseline.txt --sessions 10000 --progress-bar --visual off
  ```

---

## Model: 20k Linear Decay Epsilon (TD)
- **Training Sessions**: 20,000
- **Q-function**: Temporal Difference (TD)
- **Epsilon**: Linearly decays to 0.01
- **Learning Rate**: 0.05
- **Discount Factor**: Default
- **Max Length Reached**: 6 (Session 4162)
- **Command**:
  ```bash
  ./snake --save /Users/lgreau/goinfre/models/20k_lindec0.01_td.txt --sessions 20000 --progress-bar --visual off --agent-learning-rate 0.05 --agent-epsilon 0.01
  ```

---

## Model: 15k Bellman
- **Training Sessions**: 15,000
- **Q-function**: Bellman
- **Epsilon**: Static 0.1
- **Learning Rate**: N/A (Bellman doesn't use it)
- **Discount Factor**: 0.95
- **Max Length Reached**: 6 (Session 10800)
- **Command**:
  ```bash
  ./snake --save /Users/lgreau/goinfre/models/15k_bellman.txt --progress-bar --visual off --sessions 15000 --q-function bellman --agent-discount-factor 0.95
  ```

---

## Model: 25k Exponential Decay Epsilon (Bellman)
- **Training Sessions**: 25,000
- **Q-function**: Bellman
- **Epsilon**: Exponential Decay (to 0.01)
- **Learning Rate**: N/A
- **Discount Factor**: Default
- **Max Length Reached**: 7 (Session 18661)
- **Command**:
  ```bash
  ./snake --save /Users/lgreau/goinfre/models/25k_expdec0.01_bellman.txt --progress-bar --visual off --sessions 25000 --q-function bellman
  ```

---

## Model: 5k Aggressive Exploration (TD)
- **Training Sessions**: 5,000
- **Q-function**: Temporal Difference (TD)
- **Epsilon**: Static 0.9
- **Learning Rate**: 0.2
- **Discount Factor**: 0.85
- **Max Length Reached**: 6 (Session 3962)
- **Command**:
  ```bash
  ./snake --save /Users/lgreau/goinfre/models/5k_td.txt --progress-bar --visual off --sessions 5000 --agent-epsilon 0.9 --agent-learning-rate 0.2 --agent-discount-factor 0.85
  ```

---

## Model: 30k Linear Decay Epsilon (TD)
- **Training Sessions**: 30,000
- **Q-function**: Temporal Difference (TD)
- **Epsilon**: 0.05 (Static)
- **Learning Rate**: 0.05
- **Discount Factor**: 0.95
- **Max Length Reached**: 6 (Session 4093)
- **Command**:
  ```bash
  ./snake --save /Users/lgreau/goinfre/models/30k_lindec0.05_td.txt --progress-bar --visual off --sessions 30000 --agent-epsilon 0.05 --agent-learning-rate 0.05 --agent-discount-factor 0.95
  ```

---

## Model: 50k Bellman (Long-Term Planning)
- **Training Sessions**: 50,000
- **Q-function**: Bellman
- **Epsilon**: Static 0.1
- **Learning Rate**: N/A
- **Discount Factor**: 0.99
- **Max Length Reached**: 6 (Session 1122)
- **Command**:
  ```bash
  ./snake --save /Users/lgreau/goinfre/models/50k_bellman.txt --progress-bar --visual off --sessions 50000 --agent-discount-factor 0.99
  ```
