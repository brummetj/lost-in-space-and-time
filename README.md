# Lost in Space and Time
## When Plagiarism is a Good Thing

Sr. Design Project – Medical Device Requirements

Lispat is built to convert documents from their common pdf/docx format to txt,
processes the documents information, performs similarity checks, and builds
a learning model for text classification and prediction all in order to capture
the original information, in a manner that preserves and increases its value,
accessibility and usefulness.

## Requirements

* brew cask install xquartz
* brew install poppler antiword unrtf tesseract swig
* pip install textract

## NLTK

run terminal run `python`

then run the following to download NLTK.

```
 >>> import nltk`
 >>> nltk.download()
```

nlkt downloader will show up. Download all.

## PDF DECRYPTION

Due to some pdfs having restrictions to their content ```qpdf``` was used in
order to remove these restrictions.

Link: https://github.com/qpdf/qpdf

## How to Run

`pip install -e path/to/lispat`


lispat should be now installed into the OS under your pip env.


You can now run the following commands to both train data and compare submitted
documents:

* NOTE:
* The path must be to a directory containing files of these formats:
- .pdf
- .docx
- .doc
- .txt

`lispat -h`
* help commands

`lispat --path=path/to/docs --convert`
* Coverts any .pdf, .doc, .docx file to .txt format for future analysis
* Files are stored inside /usr/local/var/lispat/<format>\_data/

`lispat --path=path/to/docs --train`
* Upload data of previously submitted documents that are passed by the FDA


`lispat --path=path/todocs --compare`
* upload a submitted document to compare with documents that are already passed by the FDA
