from datetime import datetime


def calculate_duration(start_time, end_time):
    """
    Returns a dict with hours, minutes, seconds, total_minutes, and formatted string.
    Returns None if times are missing or end is before start.
    """
    if not start_time or not end_time:
        return None

    total_seconds = int((end_time - start_time).total_seconds())

    if total_seconds < 0:
        return None

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
    """Returns the current UTC time."""
    return datetime.utcnow()


def format_datetime(dt):
    """Formats a datetime to a readable string like '2026-05-12 08:30:00'."""
    if not dt:
        return None
    return dt.strftime("%Y-%m-%d %H:%M:%S")
