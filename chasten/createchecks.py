import argparse
import openai
import os
from cryptography.fernet import Fernet


user_api_key = None
fernet = None
genscript = """
checks:
  - name: "A human-readable name for the check, describing its purpose or objective. For example, 'Class Definition' or 'Function Naming Convention'."
    code: "A short, unique identifier or code that distinguishes the check from others. This code is often used for reference or automation."
    id: "A unique identifier or tag that provides additional context to the check. It may include information such as the check's category or origin. For instance, 'C001' could represent a 'Code Quality' category."
    pattern: "An XPath expression specifying the exact code pattern or element that the check aims to locate within the source code. This expression serves as the search criteria for the check's evaluation."
    count:
      min: "The minimum number of times the specified pattern is expected to appear in the source code. It establishes the lower limit for the check's results, ensuring compliance or a minimum level of occurrence."
      max: "The maximum number of times the specified pattern is expected to appear in the source code. It defines an upper limit for the check's results, helping to identify potential issues or excessive occurrences."

Example:

  - name: "class-definition"
    code: "CDF"
    id: "C001"
    pattern: './/ClassDef'
    count:
      min: 1
      max: 50
  - name: "all-function-definition"
    code: "AFD"
    id: "F001"
    pattern: './/FunctionDef'
    count:
      min: 1
      max: 200
  - name: "non-test-function-definition"
    code: "NTF"
    id: "F002"
    pattern: './/FunctionDef[not(contains(@name, "test_"))]'
    count:
      min: 40
      max: 70
  - name: "single-nested-if"
    code: "SNI"
    id: "CL001"
    pattern: './/FunctionDef/body//If'
    count:
      min: 1
      max: 100
  - name: "double-nested-if"
    code: "DNI"
    id: "CL002"
    pattern: './/FunctionDef/body//If[ancestor::If and not(parent::orelse)]'
    count:
      min: 1
      max: 15

"""

API_KEY_FILE = "userapikey.txt"

def generate_key():
    return Fernet.generate_key()

def encrypt_key(api_key, key):
    fernet = Fernet(key)
    return fernet.encrypt(api_key.encode()).decode()

def decrypt_key(encrypted_key, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_key.encode()).decode()

def is_valid_api_key(api_key):
    try:
        openai.api_key = api_key
        openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Test message"}]
        )
        return True
    except openai.error.OpenAIError:
        return False

def get_user_api_key():
    global user_api_key, fernet
    while True:
        user_api_key = input("Enter your API key: ")
        if is_valid_api_key(user_api_key):
            key = generate_key()
            encrypted_key = encrypt_key(user_api_key, key)
            with open(API_KEY_FILE, "w") as f:
                f.write(key.decode() + "\n" + encrypted_key)
            break
        else:
            print("Invalid API key. Please enter a valid API key.")

def load_user_api_key():
    global user_api_key, fernet
    if os.path.isfile(API_KEY_FILE):
        with open(API_KEY_FILE, "r") as f:
            lines = f.read().strip().split("\n")
            if len(lines) == 2:
                key = lines[0].encode()
                encrypted_key = lines[1]
                user_api_key = decrypt_key(encrypted_key, key)

def generate_yaml_config():

    if user_api_key is None or not is_valid_api_key(user_api_key):
        print("Please run '--get-api-key' and provide a valid API key first.")
        return

    try:
        openai.api_key = user_api_key
        
        user_input = input("What would you like to check for: ")
        
        prompts = ["write a file that checks for" + user_input + "in the same format as what is shown below: " + genscript]
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": f"You are a helpful assistant that generates YAML configurations. Your task is to {prompts}"}]
        )
        
        generated_yaml = response.choices[0].message["content"].strip()
        
        if not os.path.isfile("checks.yml"):
            open("checks.yml", "x")
        
        with open("checks.yml", "w") as f:
            outputwrite = f.write(generated_yaml)
        
        print(generated_yaml)
    
    except openai.error.OpenAIError:
        print("Error: There was an issue with the API key. Make sure you input your API key correctly.")

def main():
    parser = argparse.ArgumentParser(description="CLI for OpenAI YAML Generation")
    parser.add_argument('--get-api-key', action='store_true', help='Get and store the API key')
    parser.add_argument('--generate-yaml', action='store_true', help='Generate YAML configuration')
    args = parser.parse_args()

    if args.get_api_key:
        get_user_api_key()
    elif args.generate_yaml:
        load_user_api_key()
        generate_yaml_config()
    else:
        load_user_api_key()
        print("Please specify a valid command.")

if __name__ == "__main__":
    main()
