import gradio as gr
from core import save_uploaded_zip, evaluate_zip, parse_response_to_dataframe
from styler import style_dataframe


def process_zip_and_display(zip_file) -> gr.Dataframe:
    """
    Processes the uploaded ZIP file, evaluates it using the LLM,
    parses the response, and returns a styled DataFrame.
    """
    if not zip_file:
        return gr.update(value=[], headers=[])

    tmp_path = save_uploaded_zip(zip_file)
    llm_response = evaluate_zip(tmp_path)

    # Defensive fallback
    if isinstance(llm_response, list):
        return gr.update(value=llm_response, headers=["Error"])

    parsed_df = parse_response_to_dataframe(llm_response)
    styled_df = style_dataframe(parsed_df)
    return styled_df


def clear_inputs():
    """
    Clears the uploaded ZIP file and resets the DataFrame output.
    Sends a dummy row to reset scroll/width behavior.
    """
    headers = ["Type", "Weakness", "Severity", "File", "Code", "Justification"]
    dummy = [[""] * len(headers)]
    return None, gr.update(value=dummy, headers=headers)


with gr.Blocks() as demo:
    gr.Markdown("# Source Code LLM ISO 5055 Evaluation 🤖")
    gr.Markdown(
        "### Upload a ZIP file containing source code for analysis based on ISO/IEC 5055:2021 using an LLM."
    )
    gr.Markdown(
        "The evaluation will identify weaknesses in the code and provide detailed feedback."
    )
    gr.Markdown(
        " The supported languages are: Python, Java, C, C++, JavaScript, TypeScript, Go, Ruby, PHP, Swift, Kotlin, Rust."
    )

    # File upload
    zip_input = gr.File(label="Upload ZIP File", file_types=[".zip"])

    # Action buttons in a row below the input
    with gr.Row():
        upload_btn = gr.Button("Upload & Evaluate", variant="primary")
        clear_btn = gr.Button("Clear")

    # Output DataFrame
    df_output = gr.Dataframe(
        label="LLM Evaluation Results",
        interactive=False,
        headers=["Type", "Weakness", "Severity", "File", "Code", "Justification"],
        value=[],
    )

    # Upload button event
    upload_btn.click(fn=process_zip_and_display, inputs=zip_input, outputs=df_output)

    # Clear button event
    clear_btn.click(fn=clear_inputs, inputs=[], outputs=[zip_input, df_output])

demo.launch(share=True)
