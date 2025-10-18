from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP(name="file-reader", stateless_http=True)


@mcp.tool()
def read_file(path: str) -> str:
    """
    Reads a file and returns its contents.
    """
    if not os.path.exists(path):
        return f"Error: File '{path}' not found."
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def search_file(path: str, keyword: str) -> list[str] | str:
    """
    Searches for a keyword in the file and returns matching lines.
    """
    if not os.path.exists(path):
        return [f"Error: File '{path}' not found."]
    try:
        results = []
        with open(path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                if keyword.lower() in line.lower():
                    results.append(f"Line {line_num}: {line.strip()}")
        return results or [f"No matches found for '{keyword}'."]
    except Exception as e:
        return [f"Error searching file: {str(e)}"]
    

@mcp.tool()
def write_file(path: str, content: str, mode: str = "w") -> str:
    """
    Writes content to a file.
    mode = "w" (overwrite) or "a" (append).
    """
    try:
        with open(path, mode, encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to '{path}' (mode={mode})."
    except Exception as e:
        return f"Error writing file: {str(e)}"
   


mcp_app = mcp.streamable_http_app()

if __name__ == "__main__":
    import uvicorn
    # Use host 0.0.0.0 so it works locally AND on Render
    uvicorn.run(mcp_app, host="0.0.0.0", port=int(os.getenv("MCP_PORT", 9000)))
