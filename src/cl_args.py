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
		choices=["on", "off"],
		default="on",
		help="Enable or disable the display (default: on).",
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
		choices=range(3, 101),  # Ensures grid size is >= 3
		metavar="[3-100]",
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
		default=0.01,
		metavar="[0.0-1.0]",
		help="Learning rate for the agent (default: 0.01). Must be between 0.0 and 1.0.",
	)
	parser.add_argument(
		"--agent-discount-factor",
		type=float,
		default=0.99,
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

	args = parser.parse_args()

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

	return args
