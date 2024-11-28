import sys
from termcolor import colored

def print_progress_bar(session, total_sessions, max_length, max_length_session, args):
	"""Prints a progress bar with color transitions and max length reached."""
	progress = (session + 1) / total_sessions
	progress_percent = int(progress * 100)
	progress_color = (
		"\033[34m" if progress_percent < 33 else  # Deep blue
		"\033[36m" if progress_percent < 66 else  # Cyan
		"\033[32m"  # Green
	)
	objective = args.objective
	max_color = (
		"\033[31m" if max_length < objective / 2 else  # Red
		"\033[33m" if max_length < objective else  # Yellow
		"\033[93m"  # Gold
	)

	# Format the progress bar and maximum length
	bar_length = 30
	filled_length = int(bar_length * progress)
	bar = f"{progress_color}{'█' * filled_length}{'░' * (bar_length - filled_length)}\033[0m"
	max_info = f"Max Length: {max_color}{max_length}\033[0m (Session {max_length_session})"

	# Display progress bar and overwrite previous line
	sys.stdout.write(f"\r[{bar}] {progress_percent}% - {max_info}")
	sys.stdout.flush()
