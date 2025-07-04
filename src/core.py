import os
import json
import re
import logging
import tempfile
import shutil

import PyPDF2
import pandas as pd
from dotenv import load_dotenv
from zip_processor import ZipFileProcessor
from llm_evaluator import GenAIEvaluator
from system_prompt import SYSTEM_PROMPT
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Constants
RESOURCES_PATH = "resources/"

SUPPORTED_EXTENSIONS = [
    ".py",  # Python
    ".cs",  # C#
    ".c",  # C
    ".h",  # C Header
    ".cpp",  # C++
    ".hpp",  # C++ Header
    ".cc",  # C++
    ".hh",  # C++ Header
    ".java",  # Java
    ".js",  # JavaScript
    ".ts",  # TypeScript
    ".go",  # Go
    ".rs",  # Rust
    ".kt",  # Kotlin
    ".kts",  # Kotlin Script
    ".swift",  # Swift
    ".php",  # PHP
    ".rb",  # Ruby
]

DEFAULT_OUTPUT_ROW = {
    "Type": "None",
    "Weakness": "None",
    "Description": "None",
    "Severity": "None",
    "File": "None",
    "Code": "None",
    "Justification": "None",
}


def extract_standard_text() -> str:
    """
    Extracts text from all PDF files in the 'resources/' directory.

    Returns:
        str: The combined text content from all PDF files.
    """
    combined_text = ""

    for filename in os.listdir(RESOURCES_PATH):
        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(RESOURCES_PATH, filename)

        try:
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = "".join(page.extract_text() or "" for page in reader.pages)
                combined_text += f"\n\n# {filename}\n{text}"
        except Exception as e:
            logger.warning(f"Failed to extract text from {filename}: {e}")

    return combined_text

# Preloaded standard text
STANDARD_TEXT = extract_standard_text()


def save_uploaded_zip(gradio_file) -> str:
    """
    Saves a Gradio file object to a temporary ZIP file.

    Args:
        gradio_file: Uploaded file object from Gradio.

    Returns:
        str: Path to the saved temporary ZIP file.
    """
    temp_path = tempfile.NamedTemporaryFile(suffix=".zip", delete=False).name
    shutil.copy(gradio_file.name, temp_path)
    return temp_path

def send_code_to_llm(code: str, verbose: bool = True) -> str:
    """
    Sends source code to an LLM for evaluation.

    Args:
        code (str): Source code to evaluate.
        verbose (bool): Whether to print processing info (default True).

    Returns:
        str: Raw response from the LLM.
    """
    if verbose:
        logger.info("Sending code to LLM for evaluation...")

    # llm = LLMEvaluator(
    #     model=ChatGoogleGenerativeAI(
    #         api_key=os.getenv("API_KEY"),
    #         model="gemini-2.0-flash",
    #     ),
    #     system_prompt=SYSTEM_PROMPT,
    # )

    # payload = {"standard": STANDARD_TEXT, "code_snippet": code}
    # response = llm.evaluate(payload)

    llm = GenAIEvaluator(
        model=genai.GenerativeModel("gemini-2.0-flash"),
        system_prompt=SYSTEM_PROMPT,
    )
    payload = {"standard": STANDARD_TEXT, "code_snippet": code}
    response = llm.evaluate(input_variables=payload)
    
    if verbose:
        logger.info(f"LLM response: {response}")

    return response

def evaluate_zip(zip_path: str, verbose: bool = True) -> str:
    """
    Evaluates source code files in a ZIP archive using an LLM.

    Args:
        zip_path (str): Path to the ZIP archive.
        verbose (bool): Whether to print processing info (default True).

    Returns:
        str: Raw response from the LLM.
    """
    zip_processor = ZipFileProcessor(zip_file_path=zip_path, logger=logger)
    code_files = zip_processor.get_all_files(
        allowed_extensions=SUPPORTED_EXTENSIONS, verbose=verbose
    )

    if not code_files:
        return json.dumps([{"Error": "No source code files found."}])

    code_combined = "\n".join(str(code_files))

    response = send_code_to_llm(code_combined, verbose)
    return response


def parse_json(s):
    """
    Attempts to extract and parse JSON array or object from a text blob.
    """
    try:
        # Extract the first JSON array or object
        match = re.search(r"(\{.*\}|\[.*\])", s, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        else:
            raise ValueError("No JSON object or array found in response.")
    except Exception as e:
        logger.error(f"Failed to parse JSON: {e}")
        raise ValueError(f"Invalid JSON format: {e}") from e
        return None
    

def parse_xml(s: str) -> list:
    """
    Parses an XML string into a dictionary.

    Args:
        s (str): XML string to parse.

    Returns:
        dict: Parsed XML as a dictionary.
    """
    # Extract all <Issue>...</Issue> blocks
    issues = re.findall(r"<Issue>(.*?)</Issue>", s, re.DOTALL)
    parsed_issues = []

    for issue in issues:
        parsed = {}
        fields = DEFAULT_OUTPUT_ROW.keys()
        for field in fields:
            # Match content between opening and closing tags for each field
            match = re.search(rf"<{field}>(.*?)</{field}>", issue, re.DOTALL)
            if match:
                parsed[field] = (match.group(1).strip()
                    .replace("&amp;", "&")
                    .replace("&lt;", "<")
                    .replace("&gt;", ">")
                    .replace("&quot;", '"')
                    .replace("&apos;", "'"))
                
            else:
                parsed[field] = None

        parsed_issues.append(parsed)

    return parsed_issues
    
def parse_response_to_dataframe(response: str) -> pd.DataFrame:
    """
    Parses the LLM's JSON response into a Pandas DataFrame.

    Args:
        response (str): Raw JSON response from the LLM.

    Returns:
        pd.DataFrame: Parsed DataFrame or fallback error information.
    """
    try:
        parsed = parse_xml(response)

        if len(parsed) == 0:
            # If no issues found, return an empty DataFrame
            return pd.DataFrame([DEFAULT_OUTPUT_ROW])
        else:
            # Create a DataFrame from the parsed issues
            return pd.DataFrame(parsed)

    except Exception as e:
        logger.error(f"Failed to parse LLM response: {e}")
        raise ValueError(f"Invalid response format: {e}") from e
        return pd.DataFrame([{"Error": str(e), "Raw response": response}])
