1. start prefect server   
    ```prefect server start``` local prefect server   
    ```prefect orion start``` local prefect orion server?   
    ```prefect cloud login``` use cloud instead
2. create prefect project (should be the first thing to deploy a workflow)   
    ```prefect project init```
3. start worker   
    ```prefect work-pool create my-pool``` create a work pool    
    ```prefect worker start -p my-pool -t process``` process for the model's binary file 
4. start deployment   
    ```prefect deploy {path of python file}:{name of main flow} -n '{name of deployment}' -p {name of work pool}```   
    ```prefect deploy --all``` create all deployments on deployment.yml   
    ```prefect deployment run {flow_name/deployment_name}```
5. edit deployment.yml   
    In video 3.5, 
    * add name of deployment
    * add entrypoint ({path to python file on local machine/ github}/{flow name}) 
    * add workpool name
6. set schedult for deployment    
    ```prefect deployment set-schedule {flow_name/deployment_name} --interval {120 (seconds-default)}```   

##### etc
* ```git remote -v```    
* port 4200 for prefect server
* in video 3.5, adding artifact markdown on orchestrate_s3.py 
* ```prefect profile ls``` list all profiles
* ```prefect profile use {name of profile}``` 
* ```prefect block register -m {name of module}``` list registered blocks of the module