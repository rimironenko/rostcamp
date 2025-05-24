from app.prompt_router import route_prompt

def test_route_prompt():
    prompt = "Hello, world!"
    result = route_prompt(prompt)
    assert result == "You said: Hello, world!"

def test_route_prompt_empty():
    prompt = ""
    result = route_prompt(prompt)
    assert result == "You said: "
