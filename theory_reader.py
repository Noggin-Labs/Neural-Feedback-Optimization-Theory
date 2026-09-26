from pypdf import PdfReader

# Extract text to understand the Neural Feedback Optimization Theory
reader = PdfReader('/main/Neural_Feedback_Optimization_Theory__NFOT_.pdf')
theory_text = "".join([page.extract_text() for page in reader.pages])
print("Theory extracted. I will now apply this paper into the repository.")
