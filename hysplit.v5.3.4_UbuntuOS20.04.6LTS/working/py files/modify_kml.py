import re
import sys

def modify_kml_opacity(input_path, output_path):
    try:
        with open(input_path, 'r', encoding='utf-8') as file:
            kml_content = file.read()

        # This pattern now allows optional spaces within the <color> tag:
        color_pattern = re.compile(r'(<color>\s*)C8([0-9A-Fa-f]{6})(\s*</color>)')

        # Replace 'C8' with '40'. Using \g<1>, \g<2>, etc. ensures that the digits are not
        # confused with the backreference syntax.
        replacement = r'\g<1>40\g<2>\g<3>'
        modified_content = color_pattern.sub(replacement, kml_content)

        # Remove stray backtick characters if any exist
        modified_content = modified_content.replace("`", "")

        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)

        print(f"✅ Opacity modification complete. File saved at: {output_path}")

    except FileNotFoundError:
        print(f"❌ Error: The file '{input_path}' was not found.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python modify_kml.py <input_kml_path> <output_kml_path>")
        sys.exit(1)

    input_kml = sys.argv[1]
    output_kml = sys.argv[2]

    modify_kml_opacity(input_kml, output_kml)