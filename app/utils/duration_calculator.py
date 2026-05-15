# duration_calculator.py
# This file calculates how long a user was in a session (their attendance duration).
# For example: if a user checked in at 8:00 AM and checked out at 10:30 AM,
# this will tell you they attended for 2 hours and 30 minutes.

from datetime import datetime


def calculate_duration(start_time, end_time):
    """
    Calculate the time difference between check-in and check-out.

    Parameters:
        start_time - when the user checked in (a datetime object)
        end_time   - when the user checked out (a datetime object)

    Returns a dictionary like:
        {
            "hours": 2,
            "minutes": 30,
            "seconds": 0,
            "total_minutes": 150,
            "formatted": "2h 30m 0s"
        }
    Returns None if either time is missing or the end is before the start.
    """
    if not start_time or not end_time:
        return None

    # Find the difference between the two times
    difference = end_time - start_time

    # Convert the difference to total seconds
    total_seconds = int(difference.total_seconds())

    # If end time is before start time, something went wrong
    if total_seconds < 0:
        return None

    # Break total seconds into hours, minutes, and remaining seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return {
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "total_minutes": total_seconds // 60,
        "formatted": f"{hours}h {minutes}m {seconds}s"
    }


def get_current_utc_time():
    """
    Returns the current time in UTC.
    We use UTC so all times are consistent no matter where the server is.
    """
    return datetime.utcnow()


def format_datetime(dt):
    """
    Turn a datetime object into a readable string.
    Example output: "2026-05-12 08:30:00"
    """
    if not dt:
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S")