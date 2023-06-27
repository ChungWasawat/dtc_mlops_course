# Hands-on    
* Install `pipenv`  
```pip install pipenv```   
* Install the depencencies    
```pipenv install scikit-learn==1.0.2 flask gunicorn --python=3.9```   
```pipenv install --dev requests```    
1. scikit-learn: machine learning library
2. flask: web service
3. gunicorn: web server (deployment environment)
4. Providing the --dev argument will put the dependency in a special [dev-packages] location   
* Enter the pipenv virtual environment   
```pipenv shell```
* Activate the virtual environment   
```. {<path>/activate}```    
* gunicorn command    
```gunicorn --bind={0.0.0.0/9696} {function_name}:{app_name}```    
* deploy??    
```pipenv install --deploy --system```    
1. tell Pipenv to install a Pipfile’s contents into its parent system with the --system flag
2. --deploy will make sure your packages are properly locked in Pipfile.lock since it will check the hashes   

## jupyter notebook to script
```jupyter nbconvert --to script {notebook_name}.ipynb```   

## Docker
```docker run -it --rm -p 9696:9696  ride-duration-prediction-service:v1``` 
* -it: interactive mode
* --rm: remove the image after it stops
* -p: port mapping    
[setup code](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/04-deployment/web-service)    
    
```docker ps```      
list all running containers      
```docker kill {container_id}```    
kill a container
#### Publishing the image to dockerhub    
```docker build -t mlops-zoomcamp-model:v1 .```   
```docker tag mlops-zoomcamp-model:v1 svizor/zoomcamp-model:mlops-3.10.0-slim```   
```docker push svizor/zoomcamp-model:mlops-3.10.0-slim```   

#### optional
[setup on cloud with AWS Elastic Beanstalk](https://github.com/alexeygrigorev/mlbookcamp-code/blob/master/course-zoomcamp/05-deployment/07-aws-eb.md)    
[kubertenes 1](https://github.com/alexeygrigorev/mlbookcamp-code/blob/master/course-zoomcamp/10-kubernetes/05-kubernetes-intro.md)    
[kubertenes 2](https://github.com/alexeygrigorev/mlbookcamp-code/blob/master/course-zoomcamp/10-kubernetes/06-kubernetes-simple-service.md)    
# Lesson
When it comes to deployment, should know it is offline/batch (model can be waited for a while) or online (model is needed to run all the time).
### online deployment
* web service: model response to http request to make prediction
    * ride duration prediction 
* stream processing: listen to a stream of data
    * content recommendation (youtube)

### virtual environment from pipenv
When activating the environment, only installed packages can be used    
example: the above command, that installs scikit-learn, doesn't install `requests` package so python files with that package can't be run    

#### pipfile and pipfile.lock
pipfile: list of packages    
pipfile.lock: list of packages with more details (avoiding the risks of automatically upgrading packages that depend upon each other and breaking your project dependency tree)


### docker instruction
COPY ["file1", "file2"(optional), "dest directory"]    
WORKDIR: set the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions    
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0/9696", "predict:app"]: tell docker to run this command when the container starts    
EXPOSE 9696: tell docker to open this port 9696     

### scikit-learn pipeline
no need to store a model and a preprocessing model separately, just store in the pipeline    

### tracking server
if it is down, we can access the model directly from a storage on cloud without run id from tracking server    

### os and system
#### os
```os.getenv("variable_name", "default_value")```    
#### system
* sys package: let command line arguments passed to a Python script    
* set `sys.argv[1]` as the first argument on command line    
can use `argparse ` ??
### AWS file system
if folder name has space in it
* for http url, it thinks space is the same as `+`
* in command line, it is needed `""` to wrap the folder name
* `s3fs` is used to allow pandas to read and write on s3