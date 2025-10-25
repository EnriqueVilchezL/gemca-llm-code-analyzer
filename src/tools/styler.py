import pandas as pd
from pandas.io.formats.style import Styler

def style_dataframe(df: pd.DataFrame) -> Styler:
    """
    Applies custom styles to a DataFrame for better visual presentation in Gradio or notebooks.

    - Sets preformatted text layout for 'Code' and 'Justification' columns.
    - Applies bold styling to 'Weakness' and 'Code' columns.
    - Colors the 'Severity' column based on severity levels:
        - Critical: red
        - High: orange
        - Medium: yellow
        - Others: green
    - Styles the header with a subtle background color for each column.

    Args:
        df (pd.DataFrame): The DataFrame to be styled.

    Returns:
        Styler: A styled pandas Styler object ready for rendering.
    """
    severity_colors = {
        "Critical": "red",
        "High": "orange",
        "Medium": "yellow",
    }

    def color_severity(val: str) -> str:
        for level, color in severity_colors.items():
            if level in val:
                return f"color: {color};"
        return "color: green;"

    # Pre-format code and justification text
    styled = df.style.set_properties(
        subset=["Code", "Justification"],
        **{"white-space": "pre"}
    )

    # Bold certain columns
    styled = styled.set_properties(
        subset=["Weakness", "Code"],
        **{"font-weight": "bold"}
    )

    # Apply header styling
    styled = styled.set_table_styles([
        {
            "selector": f"th.col{i}",
            "props": [("background-color", "#f0f0f0")]
        } for i in range(len(df.columns))
    ])

    # Apply severity-based color mapping
    styled = styled.map(color_severity, subset=["Severity"])

    return styled