"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP
import os

# Create an MCP server
mcp = FastMCP("AI for Sticky Note")

NOTES_FILE = "/Users/naveenrai/Learning/notes.txt"


def ensure_file():
    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "w") as notes_file:
            notes_file.write("")


@mcp.tool()
def add_note(message: str) -> str:
    """
    Append a new note in the sticky not file
    :param message: The note content to be added
    :return: str: Confirmation messages indicating the note was saved.
    """
    ensure_file()
    with open(NOTES_FILE, "a") as notes_file:
        notes_file.write(message+"\n")
    return "Notes Saved!"


@mcp.tool()
def get_all_notes() -> list:
    """
    Return the list of all the notes saved so far
    :return: List of all the notes saved
    """
    ensure_file()
    with open(NOTES_FILE, "r") as notes_file_read:
        return notes_file_read.readlines()


@mcp.resource("notes://latest")
def get_latest_notes() -> str:
    """
    Get the latest notes added in the notes.
    :return: str: return the latest notes fetched
    """
    ensure_file()
    with open(NOTES_FILE, "r") as notes_file:
        lines = notes_file.readlines()
    return lines[-1].strip() if lines else "No notes found"


@mcp.prompt()
def note_summary_prompt() -> str:
    """
    Generate a prompt asking the AI to summarize all the current notes
    :return: str: Return the summary
    """
    ensure_file()
    with open(NOTES_FILE, "r") as notes_file:
        lines = notes_file.readlines()
    return f"Provide summary of the notes {lines}"