from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import markdown

# Load environment variables from .env
load_dotenv()

# Initialize the Gemini model
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Initialize FastAPI app
app = FastAPI()


SYSTEM_PROMPT = """
    You are an expert AI assistant, Please format your reponse in **markdown**, using
    --Heading (##)
    --Bullet Points
    --Bold/itallic text
    --Code blocks Example
"""

@app.get("/model", response_class=HTMLResponse)
async def query_model_root(prompt: str = Query(..., description="The prompt to send to Gemini")):
    try:
        # Run the model with the given prompt
        full_prompt = f"{SYSTEM_PROMPT.strip()}\n\n{prompt.strip()}"
        result = model.invoke(full_prompt)

        html_content = markdown.markdown(result.content) # type: ignore

        data = {
            "prompt" : prompt,
            "reponse_markdown" : result.content,
            "reponse_html" : html_content
        }
        
        # Return result content in a basic JSON format
        return JSONResponse( content=data)


    except Exception as e:
        return HTMLResponse(content=f"<h2>Error:</h2><p>{str(e)}</p>", status_code=500)


@app.get("/model_html", response_class=HTMLResponse)
async def query_model_html(prompt: str = Query(..., description="The prompt to send to Gemini")):
    try:
        # Run the model with the given prompt
        full_prompt = f"{SYSTEM_PROMPT.strip()}\n\n{prompt.strip()}"
        result = model.invoke(full_prompt)

        html_content = markdown.markdown(result.content) # type: ignore
        
        # Return result content in a basic HTML format
        return f"""
        <html>
            <head><title>Gemini Response</title></head>
            <body>
                <h2>Prompt:</h2>
                <p>{prompt}</p>
                <h2>Response:</h2>
                <p>{html_content}</p>
            </body>
        </html>
        """
    except Exception as e:
        return HTMLResponse(content=f"<h2>Error:</h2><p>{str(e)}</p>", status_code=500)  


@app.get("/", response_class=HTMLResponse)
async def query_model_msg():
    try :
        
        # Return result content in a basic HTML format
        data = {"message": "Hello from model deployment"}
        return JSONResponse( content= data)
    except Exception as e:
        return HTMLResponse(content=f"<h2>Error:</h2><p>{str(e)}</p>", status_code=500)

