from fastmcp import FastMCP
from evaluator import send_code_to_llm

mcp = FastMCP("GEMCA MCP")

@mcp.tool
def evaluate_code(code: str) -> str:
    """
    Evaluates the given code based on CWE weaknesses and IEC/ISO 5055 standards using an LLM.
    ## Parameters
    - code: The source code to be evaluated.
    ## Returns
    - A detailed evaluation report from the LLM.
    """
    response = send_code_to_llm(code)
    return response

if __name__ == "__main__":
    mcp.run()