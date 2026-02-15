import ollama
response = ollama.chat(model='deepseek-coder:6.7b', messages=[
  {'role': 'user', 'content': 'Is the APK Omen connection working?'},
])
print(response['message']['content'])
