import sys


def calculate_percentage(current, maximum):
    """
    Calculate the percentage value of current relative to maximum.

    Args:
    current (float): The current value.
    maximum (float): The maximum value.

    Returns:
    float: The percentage value.
    """
    if maximum == 0:
        raise ValueError("Maximum value cannot be zero.")
    return (current / maximum) * 100


def display_progress_bar(progress, length=50):
    """
    Display a progress bar using ASCII art.

    Parameters:
        progress (float): A number between 0 and 1 indicating the progress.
        length (int): Length of the progress bar.

    Returns:
        None
    """
    progress = progress / 100
    if not 0 <= progress <= 1:
        raise ValueError("Progress must be between 0 and 1.")

    # Calculate the number of characters to fill in the progress bar
    num_filled = int(length * progress)
    num_empty = length - num_filled

    # Build the progress bar string
    bar = '[' + '#' * num_filled + ' ' * num_empty + ']'

    # Display the progress bar
    sys.stdout.write('\r' + bar)