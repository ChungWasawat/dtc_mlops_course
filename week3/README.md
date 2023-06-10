1. start prefect server   
    ```prefect server start``` local prefect server   
    ```prefect orion start``` local prefect orion server?   
    ```prefect cloud login``` use cloud instead
2. create prefect project (should be the first thing to deploy a workflow)   
    ```prefect project init```
3. start worker   
    ```prefect worker start -p my-pool -t process```
4. start deployment   
    ```prefect deploy {path of python file}:{name of main flow} -n '{name of deployment}' -p {name of work pool}```   
    ```prefect deployment run ```

##### etc
```git remote -v``` 