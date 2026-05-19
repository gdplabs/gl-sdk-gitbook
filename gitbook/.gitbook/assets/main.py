import asyncio


from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from gllm_core.constants import EventLevel
from gllm_core.event import EventEmitter
from gllm_core.event.handler import ConsoleEventHandler, StreamEventHandler


from pipeline import e2e_pipeline


app = FastAPI()


async def run_pipeline(state: dict, config: dict):
   event_emitter: EventEmitter = state.get("event_emitter")


   try:
       await event_emitter.emit("Starting pipeline")
       await e2e_pipeline.invoke(state, config)
   except Exception as error:
       await event_emitter.emit(str(error))
   finally:
       await event_emitter.emit("Finished pipeline")
       await event_emitter.close()




@app.post("/stream")
async def add_message(request: Request):
   body = await request.json()
   user_query = body.get("user_query")
   top_k = body.get("top_k")
   debug = body.get("debug", False)
   event_level = EventLevel.DEBUG if debug else EventLevel.INFO


   stream_handler = StreamEventHandler()
   console_handler = ConsoleEventHandler()
   event_emitter = EventEmitter([stream_handler, console_handler], event_level)
   state = {"user_query": user_query, "event_emitter": event_emitter}
   config = {"top_k": top_k}


   asyncio.create_task(run_pipeline(state, config))
   return StreamingResponse(stream_handler.stream())