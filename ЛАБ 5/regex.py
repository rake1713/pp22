import re

def match_a_followed_by_b(s):
    return bool(re.fullmatch(r'a*b*', s))

def match_a_followed_by_2_or_3_b(s):
    return bool(re.fullmatch(r'ab{2,3}', s))

def find_lowercase_sequences(s):
    return re.findall(r'\b[a-z]+_[a-z]+\b', s)

def find_capital_followed_by_lowercase(s):
    return re.findall(r'\b[A-Z][a-z]+\b', s)

def match_a_followed_by_anything_ending_in_b(s):
    return bool(re.fullmatch(r'a.*b', s))

def replace_spaces_commas_dots(s):
    return re.sub(r'[ ,.]', ':', s)

def snake_to_camel(s):
    return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), s)

def split_by_uppercase(s):
    return re.findall(r'[A-Z][^A-Z]*', s)

def insert_spaces_before_capitals(s):
    return re.sub(r'(?<!^)([A-Z])', r' \1', s)

def camel_to_snake(s):
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', s).lower()


print(match_a_followed_by_b("aaabbb"))  
print(match_a_followed_by_2_or_3_b("abb")) 
print(match_a_followed_by_2_or_3_b("abbbb")) 
print(find_lowercase_sequences("hello_world test_example python_code"))  
print(find_capital_followed_by_lowercase("Hello World Python Code"))  
print(match_a_followed_by_anything_ending_in_b("axxxb"))  
print(replace_spaces_commas_dots("Hello, world. This is a test")) 
print(snake_to_camel("hello_world_test"))  
print(split_by_uppercase("HelloWorldPythonCode"))  
print(insert_spaces_before_capitals("HelloWorldPython")) 
print(camel_to_snake("HelloWorldPython"))


