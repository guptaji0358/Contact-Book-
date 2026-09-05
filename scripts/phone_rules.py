COUNTRY_CODES = [
    "+61 Australia", "+880 Bangladesh", "+55 Brazil",
    "+86 China", "+33 France", "+49 Germany",
    "+91 India", "+62 Indonesia", "+39 Italy",
    "+81 Japan", "+60 Malaysia", "+52 Mexico",
    "+31 Netherlands", "+64 New Zealand", "+92 Pakistan",
    "+7 Russia", "+966 Saudi Arabia", "+65 Singapore",
    "+27 South Africa", "+82 South Korea", "+34 Spain",
    "+94 Sri Lanka", "+971 UAE", "+44 United Kingdom",
    "+1 USA / Canada"
]

DIGIT_RULES = {
    "+91": 10,
    "+1": 10,
    "+44": 10,
    "+61": 9,
    "+880": 10,
    "+55": 11,
    "+86": 11,
    "+33": 9,
    "+49": 10,
    "+62": 10,
    "+39": 10,
    "+60": 9,
    "+52": 10,
    "+31": 9,
    "+64": 9,
    "+92": 10,
    "+7": 10,
    "+966": 9,
    "+65": 8,
    "+27": 9,
    "+82": 10,
    "+34": 9,
    "+94": 9,
    "+971": 9
}


def validate_phone(code, digits, parent, QMessageBox):
    if code == "+81":
        if len(digits) < 9 or len(digits) > 10:
            QMessageBox.warning(parent, "Invalid Phone Number", "Japan numbers must be 9-10 digits.")
            return False

    if code in DIGIT_RULES:
        required = DIGIT_RULES[code]
        if len(digits) != required:
            QMessageBox.warning(parent, "Invalid Phone Number", f"{code} numbers must contain {required} digits.")
            return False

    return True
