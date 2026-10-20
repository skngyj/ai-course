import datetime

def calculate_fee(entry: str, exit: str) -> dict:
    """
    Calculates the parking duration and fee based on entry and exit times.
    """
    # 1. Check for empty input
    if not entry or not exit:
        return {"status": "error", "message": "입력값이 비어 있습니다."}

    # 2. Parse and validate time format
    try:
        # datetime.strptime validates both format (HH:MM) and value range (00:00-23:59)
        entry_dt = datetime.datetime.strptime(entry, "%H:%M")
        exit_dt = datetime.datetime.strptime(exit, "%H:%M")
    except ValueError:
        return {"status": "error", "message": "잘못된 시간 형식입니다. (HH:MM)"}

    # 3. Check if entry and exit times are the same
    if entry_dt == exit_dt:
        return {"status": "error", "message": "입차와 출차 시간이 동일할 수 없습니다."}

    # 4. Calculate duration in minutes
    entry_minutes = entry_dt.hour * 60 + entry_dt.minute
    exit_minutes = exit_dt.hour * 60 + exit_dt.minute
    
    duration_min = exit_minutes - entry_minutes

    # 5. Handle midnight crossing (if exit < entry, assume next day)
    if duration_min < 0:
        duration_min += 24 * 60

    # 6. Calculate fee
    # - 30 mins free
    # - After 30 mins: 500 KRW per 10 mins (with rounding up)
    fee = 0
    if duration_min > 30:
        excess_min = duration_min - 30
        # Ceiling division for 10-minute intervals: (excess_min + 9) // 10
        intervals = (excess_min + 9) // 10
        fee = intervals * 500

    # 7. Cap the fee at 20,000 KRW
    if fee > 20000:
        fee = 20000

    # 8. Prepare display time ("H시간 M분")
    hours = duration_min // 60
    minutes = duration_min % 60
    display_time = f"{hours}시간 {minutes}분"

    return {
        "status": "success",
        "duration_min": duration_min,
        "display_time": display_time,
        "fee": fee
    }