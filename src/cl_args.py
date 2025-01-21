import argparse
import os


def parse_arguments():
	parser = argparse.ArgumentParser(
		description="Learn2Slither: A snake that learns how to behave in an environment through trial and error."
	)

	# General arguments
	parser.add_argument(
		"--sessions",
		type=int,
		default=10,
		help="Number of sessions to perform (default: 10).",
	)
	parser.add_argument(
		"--load",
		type=str,
		help="Filepath to load the model. Raises an error if the file does not exist.",
	)
	parser.add_argument(
		"--save",
		type=str,
		help="Filepath to save the model after training sessions.",
	)
	parser.add_argument(
		"--visual",
		choices=["terminal-only", "graphical-interface-only", "off"],
		default="terminal-only",
		help="Enable or disable the display (default: terminal-only).",
	)
	parser.add_argument(
		"--step-by-step",
		action="store_true",
		help="Enable step-by-step mode, waiting for user input at each step.",
	)
	parser.add_argument(
		"--test-mode",
		action="store_true",
		help="Turn on test mode (no learning, no model saving).",
	)

	# Environment-specific arguments
	parser.add_argument(
		"--grid-size",
		type=int,
		default=10,
		choices=range(3, 102),  # Ensures grid size is >= 3
		metavar="[3-101]",
		help="Size of the grid (default: 10). Minimum is 3.",
	)

	# Agent and Q-function arguments
	parser.add_argument(
		"--q-function",
		choices=["time-difference", "bellman"],
		default="time-difference",
		help="Choose Q-function update method: 'time-difference' (default) or 'bellman'.",
	)
	parser.add_argument(
		"--agent-epsilon",
		type=float,
		default=0.1,
		metavar="[0.0-1.0]",
		help="Epsilon-greedy exploration rate (default: 0.1). Must be between 0.0 and 1.0.",
	)
	parser.add_argument(
		"--agent-learning-rate",
		type=float,
		default=0.1,
		metavar="[0.0-1.0]",
		help="Learning rate for the agent (default: 0.01). Must be between 0.0 and 1.0.",
	)
	parser.add_argument(
		"--agent-discount-factor",
		type=float,
		default=0.9,
		metavar="[0.0-1.0]",
		help="Discount factor for future rewards (default: 0.99). Must be between 0.0 and 1.0.",
	)
	parser.add_argument(
		"--progress-bar",
		action="store_true",
		help="Print a progress bar during sessions."
	)
	parser.add_argument(
		"--objective",
		type=int,
		default=10,
		help="Objective snake length (must be > 3)."
	)
	parser.add_argument(
		"--epsilon-decay",
		nargs="+",
		help="Gradually modify epsilon. Use 'linear <start_value> <end_value>' or 'exponential <start_value> <end_value>'.",
	)
	parser.add_argument(
		"--progressive-grid-size",
		nargs="+",
		help="Modify the grid size over time. Use 'random <start_size> <end_size>' or 'logarithmic <start_size> <end_size>'.",
	)
	parser.add_argument(
		"--visual-speed",
		type=float,
		default=0.0,
		help="Delay in seconds between each step of visualization (default: 0.0, no delay).",
	)

	args = parser.parse_args()

	# Validate --sessions argument
	if args.sessions <= 0:
		parser.error(f"Can't perform less than 1 session: {args.sessions}")

	# Validate --load argument
	if args.load and not os.path.isfile(args.load):
		parser.error(f"The file '{args.load}' does not exist.")

	# Validate floats in [0.0, 1.0]
	for attr in ["agent_epsilon", "agent_learning_rate", "agent_discount_factor"]:
		value = getattr(args, attr)
		if not (0.0 <= value <= 1.0):
			parser.error(f"{attr.replace('_', '-')} must be between 0.0 and 1.0.")

	# Validate objective > 3
	if args.objective <= 3:
		parser.error(f"The objective only makes sense if over 3, set at {args.objective}")

	# Validate epsilon-decay
	if args.epsilon_decay:
		method, *values = args.epsilon_decay
		if method not in ["linear", "exponential"]:
			parser.error("Epsilon-decay must be 'linear' or 'exponential'.")
		if len(values) != 2:
			parser.error("Epsilon-decay requires <start_value> and <end_value>.")
		start_value, end_value = map(float, values)
		if not (0.0 <= start_value <= 1.0 and 0.0 <= end_value <= 1.0):
			parser.error("Epsilon values must be between 0.0 and 1.0.")

	# Validate progressive-grid-size
	if args.progressive_grid_size:
		method, *values = args.progressive_grid_size
		if method not in ["random", "logarithmic"]:
			parser.error("Progressive-grid-size must be 'random' or 'logarithmic'.")
		if len(values) != 2:
			parser.error("Progressive-grid-size requires <start_size> and <end_size>.")
		start_size, end_size = map(int, values)
		if not (3 <= start_size <= 100 and 3 <= end_size <= 100):
			parser.error("Grid size must be between 3 and 100.")

	return args
