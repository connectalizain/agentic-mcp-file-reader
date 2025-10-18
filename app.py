import chainlit as cl
import os
import json
import asyncio
from dotenv import load_dotenv, find_dotenv
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_disabled,
)
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from openai.types.responses import ResponseTextDeltaEvent


_: bool = load_dotenv(find_dotenv())
set_tracing_disabled(disabled=True)

# --- LLM Setup ---
gemini_api_key = os.getenv("GEMINI_API_KEY", "")
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash", openai_client=external_client
)

# --- MCP Server ---
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:9000/mcp/")

async def create_agent(): 
    """Initialize the File Assistant agent"""
    mcp_params = MCPServerStreamableHttpParams(url=MCP_SERVER_URL)

    mcp_file_server = MCPServerStreamableHttp(
        params=mcp_params, name="mcp_server_file_assistant"
    )

    # ✅ Connect to MCP server before passing to Agent
    await mcp_file_server.connect()

    file_agent = Agent(
        name="File Assistant",
        instructions="""
        You are a File Assistant with access to tools: read_file, search_file, write_file.

        Rules:
        1. Always plan before executing multiple tasks.
        2. Use tools step-by-step and display results.
        3. Summarize only after reading files fully.
        4. Don’t respond until all steps are complete.
        """,
        model=llm_model,
        mcp_servers=[mcp_file_server],
    )

    return file_agent, mcp_file_server


@cl.on_chat_start
async def on_chat_start():
    """Initialize agent and store in user session"""
    agent, mcp_server = await create_agent()
    cl.user_session.set("agent", agent)
    cl.user_session.set("mcp_server", mcp_server)

    await cl.Message( content="👋 Hi! I’m your Smart File Assistant.\n\n"
                "You can ask me things like:\n"
                "- 'Search the word future in test.txt and summarize'\n"
                "- 'Summarize test.txt in 50 words'\n"
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    """Handle user input with streaming and tool call notifications"""
    agent: Agent = cl.user_session.get("agent")

    # Start a message to stream tokens with 🤖 Assistant 
    msg = cl.Message(content="🤖 Assistant: ")
    await msg.send()

    stream = Runner.run_streamed(agent, message.content)

    try:
        async for event in stream.stream_events():
            #  Stream model tokens
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                await msg.stream_token(event.data.delta)

            #  Notify when a tool is called
            elif event.type == "run_item_stream_event" and event.name == "tool_called":
                await cl.Message(content=f"🔧 Tool called: {event.item.raw_item.name}").send()

    finally:
        # Ensure the spinner stops and message finalizes
        await msg.update()

    
@cl.on_chat_end
async def on_chat_end():
    """Gracefully disconnect MCP server when user leaves the chat"""
    mcp_server = cl.user_session.get("mcp_server")

    if mcp_server:
        try:
            await mcp_server.disconnect()
            print("🛑 MCP connection closed.")
        except Exception as e:
            print(f"⚠️ Error closing MCP connection: {e}")

