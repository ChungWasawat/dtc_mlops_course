# Hands-on    
* Install `pipenv`  
```pip install pipenv```   
* Install the depencencies    
```pipenv install scikit-learn==1.0.2 flask gunicorn --python=3.9```   
1. scikit-learn: machine learning library
2. flask: web service
3. gunicorn: web server (deployment environment)    
* Enter the pipenv virtual environment   
```pipenv shell```
* Activate the virtual environment   
```. {<path>/activate}```


# Lesson
    When it comes to deployment, should know it is offline/batch (model can be waited for a while) or online (model is needed to run all the time).
### online deployment
* web service: model response to http request to make prediction
    * ride duration prediction 
* stream processing: listen to a stream of data
    * content recommendation (youtube)