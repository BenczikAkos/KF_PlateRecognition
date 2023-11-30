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
    pattern = r'([AEIOU]{2}[A-Za-z]{2,3})-\d{3}|([A-Z0-9]*[A-Z]{3})-\d{3}|([A-Z]{2,}) ?(\d{2}-\d{2})|([A-Z]*[A-Z])-(\d{7})|0(T\d+)-(\d+)|(0*[A-Z]*0*[A-Z]*0*)-(\d{3})|HI([A-Z]{3,4})\d{3}'

    def repl_func(m):
            if m.group(1):  # Matched the vowel condition
                part = m.group(1)
                if len(part) == 4:  # Four-letter case
                    return f"{part[:2]} {part[2:]}-{m.group(0).split('-')[1]}"
                elif len(part) == 5:  # Five-letter case
                    return f"{part[:2]} {part[3:]}-{m.group(0).split('-')[1]}"
            elif m.group(2):  # Matched the basic pattern (ABC-123)
                return m.group(2)[-3:] + '-' + m.group(0).split('-')[1]
            elif m.group(3):  # Matched the new case (two letters, two numbers, '-', two numbers) MA 23-53
                return f"{m.group(3)[-2:]} {m.group(4)}"
            elif m.group(5):  # Matched the 1 letter pattern - P-1234567
                return f"P-{m.group(6)}"
            elif m.group(7):  # Matched the '0T00-63' pattern
                return f"OT {m.group(7)[1:]}-{m.group(8)}"
            elif m.group(9):  # Matched the 'HA0E-447' pattern
                return m.group(9).replace('0', 'O')[-3:] + '-' + m.group(10)
            elif m.group(11):  # Matched the HI pattern
                part = m.group(11)
                digits = m.string[m.end(11):m.end(11)+3]
                if len(part) == 3:
                    # If there are 3 letters, add a '-'
                    replacement = part + '-' + digits
                elif len(part) == 4:
                    # If there are 4 letters, replace the last letter with '-'
                    replacement = part[:3] + '-' + digits
                return replacement
            
            
    return re.sub(pattern, repl_func, s)

# Examples
#print(clean_string("-HIDFY.253 "))  # Output: 'DFY-253'
#print(clean_string(" AHRD_623-"))   # Output: 'HRD-623'
#print(clean_string("AAGHU-686)"))  # Output: 'AA HU-686'
#print(clean_string("AAFV-653"))   # Output: 'AA FV-653'
#print(clean_string("MA06-89"))  # Output: 'MA 06-89'
#print(clean_string("HAMA51-25")) # Output: 'MA 51-25'
#print(clean_string("HP-1234567")) # Output: 'P-1234567'
#print(clean_string("0T00-12")) # Output: 'OT 00-12'
#print(clean_string("HA0E-447")) # Output: 'AOE-447'
#print(clean_string("HIGDHK447")) # Output: 'GDH-447'
