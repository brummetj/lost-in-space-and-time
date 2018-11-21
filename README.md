# lost-in-space-and-time
Senior Design for comparisons on regulatory filing documents. 

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

## How to Run

`pip install -e path/to/lispat`


lispat should be now installed into the OS under your pip env.


you can now run the following commands to both train data and compare submitted documents.


`lispat -h`
* help commands

`lispat --path=path/to/docs --train`
* upload data of previously submitted documents that are passed by the FDA

`lispat --path=path/todocs --compare`
* upload a submitted document to compare with documents that are already passed by the FDA





