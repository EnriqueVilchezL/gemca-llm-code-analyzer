from test_case_data_load import read_all_test_cases
from test_core import check_response
from core import send_code_to_llm, parse_response_to_dataframe
from dotenv import load_dotenv

from test_configuration import CSHARP_TEST_DIR, PHP_TEST_DIR, CSHARP_RESULTS_DIR, PHP_RESULTS_DIR, JAVA_TEST_DIR, JAVA_RESULTS_DIR
import time
import pandas as pd
import os

PATHS = {
    "csharp": [CSHARP_TEST_DIR, CSHARP_RESULTS_DIR],
    "php": [PHP_TEST_DIR, PHP_RESULTS_DIR],
    "java": [JAVA_TEST_DIR, JAVA_RESULTS_DIR]
}

if __name__ == "__main__":
    load_dotenv("./.env")
    # Set display options for Pandas DataFrame
    pd.set_option('display.max_columns', None)
    DATASET = os.getenv("DATASET")
    base_path, results_path = PATHS[DATASET]

    iterations = int(os.getenv("ITERATIONS", 1))
    TOTAL_TEST_CASES = int(os.getenv("TOTAL_TEST_CASES", 100))
    iterations_list = []
    total_test_cases_list = []
    hit_test_cases_list = []
    accuracy_list = []


    for iter in range(0, iterations):
        total_test_cases = TOTAL_TEST_CASES
        test_cases = read_all_test_cases(base_path, max_dirs=100)
        hit_test_cases = 0
        
        llm_code_list = []
        result_list = []
        result_type_list = []
        test_case_line_list = []
        test_case_weakness_list = []
        test_case_file_list = []
        test_case_code_list = []
        llm_complete_responses = []

        for test_case in test_cases:
            code_combined = "File name: File 1\n" + test_case["Source"]

            response = send_code_to_llm(code_combined, verbose=False)
            response_df = parse_response_to_dataframe(response)
            hit, llm_code, result, result_type = check_response(response_df, test_case)

            if hit:
                hit_test_cases += 1

            llm_code_list.append(llm_code)
            result_list.append(result)
            result_type_list.append(result_type)
            test_case_line_list.append(test_case["Line"])
            test_case_weakness_list.append(test_case["Weakness"])
            test_case_file_list.append(test_case["File"])
            test_case_code_list.append(test_case["Source"])
            llm_complete_responses.append(response)

            time.sleep(5)

        # Create a DataFrame with the results
        results_df = pd.DataFrame({
            "Test Case Weakness": test_case_weakness_list,
            "Test Case File": test_case_file_list,
            "Test Case Code": test_case_code_list,
            "Test Case Line": test_case_line_list,
            "Result": result_list,
            "Result Type": result_type_list,
            "LLM Code": llm_code_list,
            "LLM Complete Response": llm_complete_responses
        })

        results_df.to_csv(str(results_path / f"test_cases_iter_{iter}_results.csv"), index=False)

        iterations_list.append(iter + 1)
        total_test_cases_list.append(total_test_cases)
        hit_test_cases_list.append(hit_test_cases)
        accuracy_list.append(hit_test_cases / total_test_cases * 100)

        print(f"Iteration {iter + 1}: {hit_test_cases} out of {total_test_cases} test cases hit. Accuracy: {hit_test_cases / total_test_cases * 100:.2f}%")

    # Create a DataFrame with the results
    results_df = pd.DataFrame({
        "Iteration": iterations_list,
        "Total Test Cases": total_test_cases_list,
        "Hit Test Cases": hit_test_cases_list,
        "Accuracy": accuracy_list
    })
    # Save the results to a CSV file
    results_df.to_csv(str(results_path / "test_cases_results_general.csv"), index=False)
