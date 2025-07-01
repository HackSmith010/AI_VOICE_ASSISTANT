import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe ,JobContext,WorkerOptions,cli,llm,AgentSession
from livekit.plugins import openai,silero

load_dotenv()

async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContent().append(
        role = "system",
        text = (
            "You are a voice assistant created by Livekit. Your Interface with users will ne voice."
            "You should use short and concise responses, and avoiding usage of unpronounable puntuation."   
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm = openai.LLM.with_ollama(
            model="llama3.1:latest",
            base_url="http://localhost:11434/v1",         
        ),
        tts=openai.TTS(),
        chat_ctx = initial_ctx,
    )
    session.start(ctx.room)
    
    await asyncio.sleep(1)
    await session.say("Hey, how can I help you today!",allow_interruptions=True)
    

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))