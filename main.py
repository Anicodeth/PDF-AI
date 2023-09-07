import google.generativeai as palm
import PyPDF2
 

#amount of pages to substract from the total
sub = 10
def read_pdf_file(file_path):
    text = ""
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages) - sub):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def save_summary_to_file(summary, output_file):
    with open(output_file, 'w') as file:
        file.write(summary)


rtf_file_path = 'file.pdf'
extracted_text = read_pdf_file(rtf_file_path)


palm.configure(api_key="AIzaSyBgwIEIym1m5ea6tY6xhCWeEGCjW2KfmgY")

defaults = {
  'model': 'models/text-bison-001',
  'temperature': 1,
  'candidate_count': 1,
  'top_k': 40,
  'top_p': 0.95,
  'max_output_tokens': 1024,
  'stop_sequences': [],
  'safety_settings': [{"category":"HARM_CATEGORY_DEROGATORY","threshold":4},{"category":"HARM_CATEGORY_TOXICITY","threshold":4},{"category":"HARM_CATEGORY_VIOLENCE","threshold":4},{"category":"HARM_CATEGORY_SEXUAL","threshold":4},{"category":"HARM_CATEGORY_MEDICAL","threshold":4},{"category":"HARM_CATEGORY_DANGEROUS","threshold":4}],
}
prompt = f"""Condense the following text and return a summary, found in quotes, '{extracted_text}'"""

response = palm.generate_text(
  **defaults,
  prompt=prompt
)

save_summary_to_file(str(response.candidates[0]['output']), 'summary.txt')
print(response.candidates[0]['output'])