```pipenv install --dev deepdiff```  

```
    docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID="Test123" \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \ 
    -e AWS_DEFAULT_REGION="eu-west-1" \ 
    -v $(pwd)/model:/app/model \ 
    stream-model-duration:v2
```     
```PS1="> "``` -remove showing path in terminal    
```set -e``` -find one non-zero error code, terminate the script     
```echo $?``` -show error code of previous command -0=successful


# documentation
* [localstack](https://github.com/localstack)