import re

def markdown_to_chunks(filename, chunk_size=4000):
    """
    Splits a Markdown file into chunks with a maximum token size.

    Parameters:
    - filename: The path to the Markdown file.
    - chunk_size: Maximum token count for each chunk. Default is 4000, considering GPT-4's limits.
    """
    # Tokenize the Markdown by paragraphs to avoid breaking in the middle of a paragraph
    paragraph_separator = "\n\n"  # Markdown paragraph break
    chunks = []
    current_chunk = ""

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()
        paragraphs = re.split(paragraph_separator, text)

    for paragraph in paragraphs:
        # Simulate adding this paragraph to the current chunk
        test_chunk = f"{current_chunk}{paragraph_separator}{paragraph}".strip()
        # Check if the test chunk exceeds the chunk size
        if len(test_chunk.split()) > chunk_size:
            # Current chunk is full, save it and start a new one
            chunks.append(current_chunk)
            current_chunk = paragraph
        else:
            # Add the paragraph to the current chunk
            current_chunk = test_chunk

    # Don't forget to add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def save_markdown_chunks(filename, chunks):
    # Save chunks to files
    for i, chunk in enumerate(chunks):
        chunk_filename = f"{filename}_chunk_{i+1}.md"
        with open(chunk_filename, "w", encoding="utf-8") as chunk_file:
            chunk_file.write(chunk)
        print(f"Chunk {i+1} saved to {chunk_filename}")


if __name__ == "__main__":
    # Example usage
    markdown_file_path = "SPDMSpecification.md"  # Replace with your Markdown file path
    chunks = markdown_to_chunks(markdown_file_path)
    save_markdown_chunks(markdown_file_path, chunks)

