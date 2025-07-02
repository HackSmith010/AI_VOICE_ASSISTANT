import asyncio
import os
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, AgentSession, llm
from livekit.plugins import openai, silero

load_dotenv()

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    chat_ctx = llm.ChatContent().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice-based. "
            "Use short and concise responses, and avoid unpronounceable punctuation."
        ),
    )

    my_llm = openai.LLM.with_ollama(
        model="llama3.1:latest",
        base_url="http://localhost:11434/v1",
        chat_ctx=chat_ctx,  
    )

    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(api_key=os.getenv("OPENAI_API_KEY")),
        llm=my_llm,
        tts=openai.TTS(api_key=os.getenv("OPENAI_API_KEY")),
    )

    session.start(ctx.room)

    await asyncio.sleep(1)
    await session.say("Hey, how can I help you today!", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
