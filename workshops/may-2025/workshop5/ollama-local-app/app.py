import ollama


response = ollama.generate(model='gemma3:4b',
                           prompt='what is a qubit?')
print(response['response'])