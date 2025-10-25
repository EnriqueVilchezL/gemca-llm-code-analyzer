import difflib

def fuzzy_substring_match(substring, string, threshold=0.8):
    """
    Checks if any substring of 'string' (of length equal to 'substring') 
    has a similarity score above 'threshold' with 'substring'.
    Returns True if such a match is found, else False.
    """
    n = len(substring)
    if n == 0:
        return False
    
    if n > len(string):
        # Exchange the values if substring is longer than string
        temporal_substring = substring
        substring = string
        string = temporal_substring
        n = len(substring)

    for i in range(len(string) - n + 1):
        window = string[i:i+n]
        similarity = difflib.SequenceMatcher(None, substring, window).ratio()
        if similarity >= threshold:
            return True
    return False

# Check te response
def check_response(response_df, test_case) -> tuple[bool, str]:
    """
    Checks if the response DataFrame contains the expected vulnerability and source code.
    Args:
        response_df (pd.DataFrame): DataFrame containing the LLM's response.
        test_case (dict): Dictionary containing the test case data.
    Returns:
        bool: True if the response matches the test case, False otherwise.
    """
    vulnerability_symbol = "Weakness"
    value = test_case[vulnerability_symbol]

    # Use .str.startswith for partial match, or == for exact match
    matches = response_df[vulnerability_symbol].str.startswith(value)
    matching_indices = response_df.index[matches].tolist()

    for idx in matching_indices:
        code = response_df.iloc[idx, response_df.columns.get_loc("Code")]

        test_line = test_case["Line"].strip()
        code_lines = [code_line.strip() for code_line in code.splitlines()]

        # Use difflib to find the best match
        match_found = False
        for code_line in code_lines:
            match_found = fuzzy_substring_match(test_line, code_line, 0.8)
            if match_found:
                break

        if match_found:
            print(f"Hit CWE: {value} in file {test_case['File']}")
            return True, code
        else:
            print(f"Failed to accert CWE: {value} in file {test_case['File']}. Code does not match.")
            print(f"Code: {code}")
            print(f"Test Case Line: {test_case['Line']}")
            return False, code

    print(f"Failed to accert CWE: {value} in file {test_case['File']}. No matching CWE found.")
    return False, ""
