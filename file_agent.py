# This code was wrtitten to create a File Assistant agent that interacts with a local MCP server
# Terminal only application to test the agent functionality

import os
import sys
import json
import asyncio
from dotenv import load_dotenv, find_dotenv
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    set_tracing_disabled,
)
from agents.mcp import (
    MCPServerStreamableHttp,
    MCPServerStreamableHttpParams,
    create_static_tool_filter,
    ToolFilterContext
)


_: bool = load_dotenv(find_dotenv())


set_tracing_disabled(disabled=True)  # Disable tracing for this example

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

# 1. Which LLM Service?
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", openai_client=external_client
)


async def main():

    MCP_SERVER_URL = (
        "http://localhost:8000/mcp/"  
    )

    
    mcp_params = MCPServerStreamableHttpParams(url=MCP_SERVER_URL)
   
    async with MCPServerStreamableHttp(
        params=mcp_params,
        name="mcp_server_file_assistant",
    ) as mcp_file_server:

        file_agent: Agent = Agent(
            name="File Assistant",
            instructions="""
            You are a File Assistant with access to these tools: read_file, search_file, write_file.

            Rules:
            1. If the user asks for multiple tasks (like search + summarize), ALWAYS create a plan first.
            2. Execute tools step by step in the order of the plan.
            3. After each tool call, show its result before moving to the next.
            4. When summarizing, ALWAYS use `read_file` (even if you already have a snippet from search_file).
            5. Never answer directly until ALL requested steps are completed.
            6. Summarization must be done by the LLM, based on the `read_file` result.
            """,

            model=llm_model,
            mcp_servers=[mcp_file_server],
        )

        query = sys.argv[1] if len(sys.argv) > 1 else input("Enter query: ")
        
        stream = Runner.run_streamed(file_agent, query)

        async for event in stream.stream_events():
            if event.type == "run_item_stream_event":
                if event.name == "tool_called":
                    print(f"🔧 Tool called: {event.item.raw_item.name}")
                elif event.name == "tool_output":
                    try:
                        output_data = json.loads(event.item.output)
                        print(f"📄 Tool output: {output_data.get('text', '<no text found>')}")
                    except json.JSONDecodeError:
                        print(f"📄 Tool output (raw): {event.item.output}")
                elif event.name == "message_output_created":
                    print(f"🤖 Assistant: {event.item.raw_item.content[0].text}")





asyncio.run(main())



