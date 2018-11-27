# Lost in Space and Time
## When Plagiarism is a Good Thing

Sr. Design Project – Medical Device Requirements

Lispat is built to convert documents from their common pdf/docx format to txt,
processes the documents information, performs similarity checks, and builds
a learning model for text classification and prediction all in order to capture
the original information, in a manner that preserves and increases its value,
accessibility and usefulness.

## How to Run

### DOCKER

Install docker from  https://www.docker.com/get-started


Why docker ?

* Easy, deployable, manageable, lightweight, and portable.


Docker ensures that any one can pull the image for Lispat and run it on any OS that has docker supported.

It's easy to distribute, we have a public registry to pull the image from. To get the latest code docker image pull from `jbrummet/lispat`

Once docker is install you can pull the image from the repo with

```
docker pull jbrummet/lispat:0.1.0
```


If you are wanting to build the image from the repo please do the following

```
git clone thisrepo

cd lispat_app

docker build . -t lispat

```

*note*: this does take a minute to build, please be patient. You would need to install all the dependencies on your OS anyways.

now you can run the containerized application with to train data.

`docker run -it --name lispat_container jbrummet/lispat:0.1.0 --path=/path/to/file --train`

to run a file already in the container please use `./assets/pdfs/test/testfile.pdf or ./assets/pdfs/test/test/*`

to get names of test files to run
```
docker start lispat_container
docker exec -it lispat_container /bin/bash
> ls
> cd lispat/assets/pdfs
> ls
 ```

where docker_id comes from `docker images`

If your docker image is already built and you want to modify and run the same container again please follow the following commands.

`docker update --cpu-shares 512 -m 4G --memory-swap 5G lispat_container`

`docker start lispat_container`

`docker exec -it lispat_container lispat --path=./path/to/docs  --train`


If you want to create the container from the docker image run.

`docker rm lispat_container`

`docker run -it --name lispat_container jbrummet/lispat:0.1.0 --path=/path/to/file  --train`

Once you have the data trained you can now commit the image to a new name and mount a volume to it to the document you want to compare with.

```
docker ps -a
docker commit <lispat_container_id> lispat_trained
docker run -it -v local/path/to/file.pdf:local/path/to/file.pdf --name lispat_trained_container lispat_trained --path=local/path/to/file.pdf --compare
```

You will now see the container using the trained data that was saved from the previous data.
If you plan on using documents in the *assets* folder, there is no need for a -v mount.  


Feel free to keep the docker image, you can remove it by

`docker rmi --force <docker_id>`

---

### LOCALLY

#### Requirements

* brew cask install xquartz
* brew install poppler antiword unrtf tesseract swig
* pip install textract

#### NLTK

in terminal run `python`

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

clone the repo and run.

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

Dependencies and package issues are possible with the requirements of the application.
Should use the docker container above all else for easier application use.
