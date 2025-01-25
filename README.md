# Rebellious Calculator

A unique visualization tool that demonstrates the transition from order to chaos through a simple numerical system. This interactive application shows how complex patterns can emerge from basic rules, illustrating concepts from chaos theory and complex systems.

## Features

- **Three Distinct Phases:**
  1. Orderly Phase (First 5 presses)
  2. Standard Chaos (Presses 6-100)
  3. Growing Chaos (After press 100)

- **Interactive Controls:**
  - Adjustable simulation speed
  - Start/Stop functionality
  - Toggleable chaos mode
  - Real-time visualization

- **Visual Feedback:**
  - Dynamic plotting of results
  - Real-time total tracking
  - Progress updates

## How It Works

The calculator follows a progression from predictable behavior to chaos:

1. **Orderly Phase:**
   - Odd presses: Add 1
   - Even presses: Subtract 1
   - Perfectly predictable pattern

2. **Standard Chaos:**
   - Random operations between +1, -1, +2, -2
   - Equal probability distribution
   - Introduction of unpredictability

3. **Growing Chaos:**
   - Chaos level gradually increases
   - New operations (+3, -3) become possible
   - Increasing probability of extreme values
   - Maximum chaos at 500 presses

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/rebellious-calculator.git
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

## Requirements

- Python 3.x
- tkinter
- matplotlib
- numpy

## Mathematical & Philosophical Background

The application demonstrates several key concepts:

- Emergence of complexity from simple rules
- Transition between order and chaos
- Random walk properties
- Statistical behavior patterns
- Chaos theory principles

For a deeper understanding, explore the "Deep Analysis" section in the application.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

