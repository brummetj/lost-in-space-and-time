# lost-in-space-and-time
Senior Design NLP processing and comparisons on regulatory filing documents. 

## How to Run

### DOCKER

Install docker from  https://www.docker.com/get-started


Why docker ?

* Easy, deployable, manageable, lightweight, and portable. 


Docker ensures that any one can pull the image for Lispat and run it on any OS that has docker supported. 

It's easy to distribute, we have a public registry to pull the image from. To get the latest code docker image pull from `jbrummet/lispat`

Once docker is install you can pull the image from the repo with

`docker pull jbrummet/lispat`

*note*: this does take a minute to build, please be patient. You would need to install all the dependencies on your OS anyways.

now you can run the containerized application with

`docker run -it -rm --name lispat_container -v path/to/file:path/to/file lispat --path=/path/to/file [--compare] [--train]`

note: 
* train and compare are required but not ran at the same time. 
* each path/to/file should be the same path in the command.

to run a file already in the container please use `./assets/pdfs/test/testfile.pdf or ./assets/pdfs/test/test/*`

to get names of test files to run 
```
docker start lispat_container
docker exec -it lispat_container /bin/bash
> ls 
> cd lispat/assets/pdfs
> ls
 ```

Feel free to keep the docker image, you can remove it by

`docker rmi --force <docker_id>`

where docker_id comes from `docker images`

If your docker image is already built and you want to run it again please follow the following commands.

`docker update --cpu-shares 512 -m 4G --memory-swap 5G lispat_container`

`docker start lispat_container`

`docker exec -it lispat_container lispat --path=./path/to/docs [--compare] [--train]`

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

clone the repo and run.

`pip install -e path/to/lispat`


lispat should be now installed into the OS under your pip env.


you can now run the following commands to both train data and compare submitted documents.


`lispat -h`
* help commands

`lispat --path=path/to/docs --train`
* upload data of previously submitted documents that are passed by the FDA

`lispat --path=path/todocs --compare`
* upload a submitted document to compare with documents that are already passed by the FDA


Dependencies and package issues are possible with the requirements of the application. 
Should use the docker container above all else for easier application use. 



