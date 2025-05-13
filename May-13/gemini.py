#api key
key = 'xxxxxxxxxxx'
import google.generativeai as genai
genai.configure(api_key= key)
model = genai.GenerativeModel("gemini-1.5-flash")

#text generation
def generate_text(prompt):
    return model.generate_content(prompt)

response = model.generate_content('Advanced RAG')

# Access the first candidate's text
print(response.candidates[0].content.parts[0].text)