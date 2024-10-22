import azure.functions as func
from openai import OpenAI
import logging


#{"model": "gpt-3.5-turbo", "prompt": "Write a story about an alien and a human astronaut", "max_tokens": 100, "temperature": 1}
#{"model": "dall-e-3", "prompt": "una maquina de helados de chocolate","size": "1024x1024" ,"quality": "standard","n": 1, "max_tokens": 100, "temperature": 1}
secret_key = "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"


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="firstfunctionapi")
def firstfunctionapi(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

@app.route(route="completionAPI", auth_level=func.AuthLevel.ANONYMOUS)
def completionAPI(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    client = OpenAI(
        api_key=secret_key
    )

    req_body = req.get_json()

    completion = client.chat.completions.create(
         model=req_body["model"],
         messages=[
             {"role": "system", "content": "You are a helpful assistant."},
             {"role": "user", "content": req_body["prompt"]}
        ],
        max_tokens=req_body["max_tokens"],
        temperature=req_body["temperature"]
        )
    return func.HttpResponse(completion.choices[0].message.content, status_code=200)

@app.route(route="imagefunction", auth_level=func.AuthLevel.ANONYMOUS)
def imagefunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    client = OpenAI(
    api_key=secret_key
    )

    req_body = req.get_json()

    completion = client.images.generate(
        model=req_body["model"],
        prompt = req_body["prompt"],
        size=req_body["size"],
        quality = req_body["quality"],
        n = req_body["n"]
        )

    return func.HttpResponse(completion.data[0].url, status_code=200)