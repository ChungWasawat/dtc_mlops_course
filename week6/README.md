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
```aws --endpoint-url=http://localhost:4566 s3 mb s3://nyc-duration```     
```aws --endpoint-url=http://localhost:4566 s3 ls```     
```aws --endpoint-url=http://localhost:4566 s3 ls nyc-duration/in/ --summarize```     

###### set global var
```
export INPUT_FILE_PATTERN="s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
export OUTPUT_FILE_PATTERN="s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
```
`./directory/run.sh` run script     
# document
* [localstack](https://github.com/localstack/localstack)
* [localstack -docker compose configuration](https://docs.localstack.cloud/getting-started/installation/#docker-compose)