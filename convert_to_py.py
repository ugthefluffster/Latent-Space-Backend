import json
import os
from datetime import datetime

def convert_ipynb_to_py():
    """Converts server.ipynb to a timestamped .py file."""

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    py_filepath = f"server-{timestamp}.py"  # Timestamped filename
    ipynb_filepath = "server.ipynb"

    try:
        with open(ipynb_filepath, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {ipynb_filepath}")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {ipynb_filepath}")
        return

    with open(py_filepath, 'w', encoding='utf-8') as outfile:
        cell_num = 1
        for cell in notebook['cells']:
            outfile.write(f"# Cell {cell_num}\n")
            cell_num += 1

            if cell['cell_type'] == 'code':
                for line in cell['source']:
                    if line.startswith("!pip"):
                        outfile.write("# " + line.rstrip() + "\n")
                    else:
                        outfile.write(line.rstrip() + "\n")
                outfile.write("\n")  # Add newline between code cells

            elif cell['cell_type'] == 'markdown':
                for line in cell['source']:
                    outfile.write("# " + line.rstrip() + "\n")
                outfile.write("\n")

            elif cell['cell_type'] == 'raw':
                outfile.write("# Raw Cell (not converted)\n\n")

    print(f"Successfully converted {ipynb_filepath} to {py_filepath}")



if __name__ == "__main__":
    convert_ipynb_to_py()