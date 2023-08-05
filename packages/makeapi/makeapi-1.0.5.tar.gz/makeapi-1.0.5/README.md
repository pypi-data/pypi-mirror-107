# makeapi

[![Downloads](https://pepy.tech/badge/makeapi)](https://pepy.tech/project/makeapi)

A small package, that allows you to make an API.

## Example

```py
import makeapi

app = MakeAPI("localhost", 8000) # localhost is your local computer

@app.get("/main")
def main(request : makeapi.Request):
    return makeapi.PlainResponse("Hello!")
    
app.run()    

# Go to http://localhost:8000/main in your browser and you should see Hello!
```

## Example with POST request

```py
import makeapi

app = MakeAPI("localhost", 8000)

@app.post("/main")
def params_route(request : makeapi.Request):
    params = request.json
    return JsonResponse(params)    

app.run()

# Make post request and include json data to http://localhost:8000/main and it should show your json data
```

Enjoy!
