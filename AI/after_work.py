import re

def clean_string(string):
    string = string.replace('.', '-')
    string = string.replace('_', '-')
    string = string.replace(':', '-')
    string = re.sub(r'[^A-Z0-9\s-]', '', string)
    string = re.sub(r'^[\s-]+|[\s-]+$', '', string)

    string = modify_string(string)
    return string

def modify_string(s):
    pattern = r'([AEIOU]{2}[A-Za-z]{2,3})-\d{3}|([A-Z]{3,})-\d{3}|([A-Z]{2,})(\d{2}-\d{2})'

    def repl_func(m):
            if m.group(1):  # Matched the vowel condition
                part = m.group(1)
                if len(part) == 4:  # Four-letter case
                    return f"{part[:2]} {part[2:]}-{m.group(0).split('-')[1]}"
                elif len(part) == 5:  # Five-letter case
                    return f"{part[:2]} {part[3:]}-{m.group(0).split('-')[1]}"
            elif m.group(2):  # Matched the first pattern
                return m.group(2)[-3:] + '-' + m.group(0).split('-')[1]
            elif m.group(3):  # Matched the new case (two letters, two numbers, '-', two numbers)
                return f"{m.group(3)[-2:]} {m.group(4)}"
            
    return re.sub(pattern, repl_func, s)

# Examples
#print(clean_string("-HIDFY.253 "))  # Output: 'DFY-253'
#print(clean_string(" AHRD_623-"))   # Output: 'HRD-623'
#print(clean_string("AAGHU-686)"))  # Output: 'AA HU-686'
#print(clean_string("AAFV-653"))   # Output: 'AA FV-653'
#print(clean_string("MA06-89"))  # Output: 'MA 06-89'
#print(clean_string("HAMA51-25")) # Output: 'MA 51-25'
