from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from decouple import config
import chainlit as cl

key=config("GEMINI_API_KEY")
base_url=config("base_url")
gemini_client=AsyncOpenAI(api_key=key,base_url=base_url)

Model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=gemini_client
)
configuration = RunConfig(
    model=Model,
    model_provider=gemini_client,
    tracing_disabled=True
)
agent=Agent(
        name="Kaif shamim",
        instructions="you are my helpfull assistant.",
        model=Model
    )

@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])
    await cl.Message(content="Hello, how can I help you today?").send()

@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("history")
    history.append({"role": "user", "content": message.content})
    result = await Runner.run(
        agent,
        input=history,
        run_config=configuration
    )
    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)
    await cl.Message(content=result.final_output).send()       
