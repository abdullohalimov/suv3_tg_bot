async def check_phone(phone):
    if phone.isdigit():
        return True
    else:
        return False