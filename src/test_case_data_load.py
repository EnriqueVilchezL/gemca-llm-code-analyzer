import json
from cwes import cwe_list
import random
import re

def remove_comments(code):
    pattern = r"""
        //.*?$           # single-line comments
        |                # or
        /\*.*?\*/        # multi-line comments
    """
    return re.sub(pattern, '', code, flags=re.DOTALL | re.MULTILINE | re.VERBOSE)

def format_sarif_and_src(sarif_data, src_data):
    formatted_data = []

    # Only accepted cases
    if sarif_data.get("properties", {}).get("status", "") != "deprecated":
        # Format the SARIF and source data into a dictionary
        for run in sarif_data.get("runs", []):
            for result in run.get("results", []):
                
                rule_id = result.get("ruleId", "Unknown")
                
                for location in result.get("locations", []):
                    data = {
                        "Weakness": "Unknown",
                        "File": "Unknown",
                        "Line": "Unknown",
                        "Source": "Unknown"
                    }
                    physical_location = location.get("physicalLocation", {})
                    artifact_location = physical_location.get("artifactLocation", {})
                    uri = artifact_location.get("uri", "")
                    
                    if uri and rule_id in cwe_list:
                        source_lines = src_data.splitlines()
                        start_line = int(physical_location.get("region", {}).get("startLine", 0))

                        data["File"] = uri
                        data["Weakness"] = rule_id
                        data["Line"] = remove_comments(source_lines[start_line - 1].strip() if start_line - 1 <= len(source_lines) else "Unknown")
                        data["Source"] = remove_comments(src_data)
                        formatted_data.append(data)

    return formatted_data

def read_all_test_cases(base_dir, max_dirs=100):
    count = 0
    test_cases = []
    subdirs = [d for d in base_dir.iterdir() if d.is_dir()]
    random.shuffle(subdirs)  # Shuffle the list for randomness

    for subdir in subdirs:
        sarif_data = {}
        src_data = ""
        # Look for sarif file
        sarif_files = list(subdir.glob("*.sarif"))
        for sarif_file in sarif_files:
            with open(sarif_file, "r") as f:
                sarif_data = json.load(f)

        # Look for source files
        src_files = list(subdir.glob("src/*.*"))

        print(f"Found {len(src_files)} source files in {subdir.name}")
        if len(src_files) > 1:
            print(f"Too many source files found in {subdir.name}, skipping...")
            continue

        for src_file in src_files:
            with open(src_file, "r") as f:
                src_data = f.read()

        formatted_data = format_sarif_and_src(sarif_data, src_data)
        if len(formatted_data) == 0 or any(v == "Unknown" for v in sarif_data.values()):
            continue
        else:
            test_cases.extend(formatted_data)
            print(f"Processed {sarif_file.name} and {src_file.name}") # type: ignore
            count += 1
            if count >= max_dirs:
                return test_cases
    return test_cases