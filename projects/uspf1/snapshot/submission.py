# %%
import os
import asyncio
from pathlib import Path
import aiofiles
import sys

# Set up base and output directories
base_directory = Path(
    "../civic-tech-dc/uspf1-fda-knowledge-graph/fda_2025_data_derived"
)
output_folder = Path("../civic-tech-dc/uspf1-fda-knowledge-graph/LLM_outputs")
output_folder.mkdir(parents=True, exist_ok=True)


# Async function to process a single file
async def process_file(file_path: Path, model="llama-3.3-70b-versatile"):
    try:
        async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
            prompt_content = await f.read()

        prompt = (
            "Here is a comment letter addressed to a docket from the FDA, "
            "I want to know what specific information is requested by the comment issuer "
            "and how it relates to the docket.\n"
            "Return this response as a table with the name of the commenter, the information requested, and the type of information needed.\n\n"
            + prompt_content[:12000]
        )

        # Run LLM call in a thread-safe way
        chat_completion = await asyncio.to_thread(
            client.chat.completions.create,
            messages=[{"role": "user", "content": prompt}],
            model=model,
        )

        output_text = chat_completion.choices[0].message.content

        # Save the result
        output_filename = output_folder / f"{file_path.name}_summary_output.txt"
        async with aiofiles.open(output_filename, "w", encoding="utf-8") as out_file:
            await out_file.write(output_text)

        print(f"✅ Saved: {output_filename}")

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")


# Async function to scan and queue all files
async def process_all_files():
    tasks = []
    for folder in sorted(base_directory.iterdir()):
        if not folder.is_dir():
            continue

        txt_dir = folder / "mirrulations/extracted_txt/comments_extracted_text/pypdf"
        if not txt_dir.exists():
            print(f"❌ Skipping missing: {txt_dir}")
            continue

        for file in txt_dir.glob("*.txt"):
            tasks.append(process_file(file))

    await asyncio.gather(*tasks)


# Run it in a Notebook or Script safely
async def run_async_main():
    await process_all_files()


# Entry point
if __name__ == "__main__":
    if "ipykernel" in sys.modules:
        # Jupyter / IPython
        await run_async_main()
    else:
        # Regular Python script
        asyncio.run(run_async_main())


def letter_classifier(text, model="llama-3.1-8b-instant"):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                        You are an assistant that determines if a given text is part of a letter. The input text is: {text}.
                        If the text is part of a letter, respond with only: yes
                        If the text is not part of a letter or you are unsure, respond with only: no
                        Note: If the text contains address information, consider it part of a letter.
                        The text may come from research papers, comments, or other non-letter documents.""",
            }
        ],
        model="llama-3.1-8b-instant",
    )

    # Assuming the response contains a list of keywords in the content
    answer = chat_completion.choices[0].message.content
    return answer


results = {}
files = r"../civic-tech-dc/uspf1-fda-knowledge-graph/FDA_2025_data_derived/FDA-2025--D-0507/mirrulations/extracted_txt/comments_extracted_text/pypdf/FDA-2025-D-0507-0007_attachment_1_extracted.txt"

for file in files:
    with open(file, "r") as f:
        text = f.read()
    text = text[:10000]
    answer = letter_classifier(text)
    file_name = os.path.basename(file)
    results[file_name] = answer
    time.sleep(0.3)
