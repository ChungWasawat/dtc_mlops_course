# Hands-on    
* Install `pipenv`  
```pip install pipenv```   
* Install the depencencies    
```pipenv install scikit-learn==1.0.2 flask gunicorn --python=3.9```   
```pipenv install --dev requests```    
1. scikit-learn: machine learning library
2. flask: web service
3. gunicorn: web server (deployment environment)
4. --dev: Install both develop and defaul` package categories from Pipfile    
* Enter the pipenv virtual environment   
```pipenv shell```
* Activate the virtual environment   
```. {<path>/activate}```    
* gunicorn command
```gunicorn --bind={0.0.0.0/9696} {function_name}:{app_name}```    

## Docker
[setup code](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/04-deployment/web-service)    
```docker run -it --rm -p 9696:9696  ride-duration-prediction-service:v1``` 
* -it: interactive mode
* --rm: remove the image after it stops
* -p: port mapping    
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

### docker instruction
COPY ["file1", "file2"(optional), "dest directory"]    
WORKDIR: set the working directory for any RUN, CMD, ENTRYPOINT, COPY and ADD instructions    
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0/9696", "predict:app"]: tell docker to run this command when the container starts    
EXPOSE 9696: tell docker to open this port 9696   