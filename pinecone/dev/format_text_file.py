def add_newlines_to_text(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # Replace periods followed by a space with a period followed by a newline
            modified_content = content.replace('. ', '.\n')

        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        print(f"Processed file saved to {output_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    input_path = 'chapter17.txt'  # Specify the path to your input file
    output_path = 'chapter17_new.txt'  # Specify the path where you want to save the output file
    add_newlines_to_text(input_path, output_path)