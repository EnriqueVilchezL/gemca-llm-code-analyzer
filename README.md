# 🧠 LLM ISO/IEC 5055 Code Evaluator

This project leverages a Large Language Model (LLM) — specifically Google Gemini — to analyze the quality of source code projects against the **ISO/IEC 5055:2021** standard, which defines measures for software code quality across four key aspects: **Reliability, Performance Efficiency, Security**, and **Maintainability**.

The evaluation is entirely LLM-driven, enabling intelligent, context-aware code assessment with just a ZIP upload.

---

## 📖 Description of the System

The system consists of a Gradio web interface that accepts a ZIP file containing a codebase (e.g., Python files). Once uploaded:

1. The ZIP file is unpacked and all source files with allowed extensions (only source code files) are extracted.
2.	A PDF file containing evaluation criteria inspired by ISO/IEC 5055:2021 may optionally be provided by the user. This file can be used to inform the LLM’s analysis but must not contain copyrighted content unless you have appropriate licensing.

⚠️ This project does not include or distribute the official ISO/IEC 5055:2021 standard. To obtain a licensed copy, visit the official [ISO](https://www.iso.org/obp/ui/en/#iso:std:iso-iec:5055:ed-1:v1:en) website.

Alternatively, you may create your own summary or ruleset that aligns with the four quality dimensions (Reliability, Performance Efficiency, Security, Maintainability).

3. The code files are also **concatenated and sent to the LLM**, along with the standard.
4. The LLM is prompted with a carefully constructed system message and asked to:
   - Analyze the codebase based on the ISO 5055 guidelines.
   - Identify weaknesses (e.g., referencing CWEs where appropriate).
   - Justify findings.

The LLM is expected to return a JSON array of findings, which is then parsed and displayed in a tabular interface within the app.

---

## 🚀 Installation

This project uses **[uv](https://github.com/astral-sh/uv)**, a fast Python package manager, to handle dependencies and virtual environments.

> Requirements:
> - Python 3.12+
> - `uv`: Install with `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/EnriqueVilchezL/gemca-llm-code-analyzer.git
   cd gemca-llm-code-analyzer
   ```

2. **Install dependencies using `uv`:**

   ```bash
   uv sync
   ```

3. **Set up the environment**

    Create a .env file and add your Google API key:

    ```bash
    API_KEY=your_google_gemini_api_key
    ```

4. **Add the main resource**

    In the directory named `resources`, place some files with the standard rules. We can't provide the full standard for copyright reasons, but you can buy it from [ISO](https://www.iso.org/obp/ui/en/#iso:std:iso-iec:5055:ed-1:v1:en) or get a summarized version.


5. **Run the app**

    You can run the app with the `uv` command:
    ```bash
    uv run app.py
    ```
    This will launch a local Gradio web interface in your browser where you can upload your ZIP project for analysis.

## ✅ Supported programming languages for code analysis

The following languages are currently supported:

- 🐍 Python (`.py`)
- 💠 C# (`.cs`)
- 🔧 C (`.c`, `.h`)
- ➕➕ C++ (`.cpp`, `.hpp`, `.cc`, `.hh`)
- ☕ Java (`.java`)
- 🌐 JavaScript (`.js`)
- 🌀 TypeScript (`.ts`)
- 🐹 Go (`.go`)
- 🦀 Rust (`.rs`)
- 🧬 Kotlin (`.kt`, `.kts`)
- 🍏 Swift (`.swift`)
- 🐘 PHP (`.php`)
- 💎 Ruby (`.rb`)

---

## 💡 Notes
- The LLM must return a valid JSON list of dictionaries. If not, the UI will throw an error. Same case if the Gemini API can't take any more requests.
- If provided, a user-supplied file containing summary rules or evaluation criteria inspired by ISO/IEC 5055 is passed into the LLM along with the extracted code files. The official ISO standard is not included or redistributed by this project.
- If you have access to a more powerful LLM or API key you can modify the model name in the code.

---

## License

This project is under the MIT License, see [LICENSE](LICENSE)