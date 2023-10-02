import openai
import os

with open("userapikey.txt") as f:
    userapikey = f.read()

openai.api_key = userapikey

with open("genscript.txt") as f:
    structure = f.read()

user_input = input("What would you like to check for: ")

prompts = ["write a file that checks for" + user_input + "in the same format as what is show below: " + structure]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": f"You are a helpful assistant that generates YAML configurations. Your task is to {prompts}"}]
)

generated_yaml = response.choices[0].message["content"].strip()

if not os.path.isfile("checks.yml"):
    open("checks.yml", "x")

with open("checks.yml","w") as f:
    outputwrite = f.write(generated_yaml)

print(generated_yaml)
