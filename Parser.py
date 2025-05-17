import os
from Queue import Queue
from pypdf import PdfReader

class Parser:
    def __init__(self, root):
        self.documents = {}
        self.root = root

    def traverse(self):
        for _, _, files in os.walk(self.root):
            for filename in files:
                if not filename.endswith('.pdf'):
                    continue
                
                document = os.path.join(self.root, filename)
                reader = PdfReader(document)
                self.documents[document] = (len(reader.pages), reader)

    def get_document(self, document, limit = 10**18):
        print(f"Reading document {document}...")
        cnt_pages, reader = self.documents[document]
        for i in range(min(cnt_pages, limit)):
            print(reader.pages[i].extract_text())

    def get_abstract(self, document):
        return self.get_page_by_tokens(document, ['Resumen', 'Abstract', 'abstract', 'resumen'])

    def get_introduction(self, document):
        return self.get_page_by_tokens(document, ['Introducción', 'Introduction', 'introduction', 'introducción'])
    
    def get_page_by_tokens(self, document, tokens):
        cnt_pages, reader = self.documents[document]
        for i in range(cnt_pages):
            text = str(reader.pages[i].extract_text())
            for token in tokens:
                if text.startswith(token):
                    return text
        return 'Tokens not found'