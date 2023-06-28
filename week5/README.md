# ml service on production
there are many things to check when a ml model is deployed on production to maintain its performance.
- service health
- model performance
- data quality and integrity
- data and concept drift
- performance by segment
- model bias/ fairness
- outliers
- model explainability

#### model performance
use a set of metrics to evaluate the model performance (ranking metric, mae, rmse, log loss, precision/ recall,  etc).   
#### data quality and integrity
about missing values or error in data.
#### data and concept drift
compare data distribution on training set and new data when the model is on production.    
if it is different, can assume that the model will not perform as it did on training set.
#### performance by segment
if data is more diverse, can segment the data to train a model for each segment.
#### model bias/ fairness
data is sensitive such as animal data, healthcare data, financial data
#### outliers
if the segments from above have high error individually, can remove it from the training set or wait for review.

# Batch vs Online 
how to monitor the model performance on production?    
* add ml metric to service health monitoring
    - Prometheus: pull ml metrics from production service
    - Grafana: visualize the metrics
* build an ml-focused dashboard 
    - visualisation tools such as Grafana, Tableau, PowerBI, Looker

### Batch
#### Data Quality
Compare data distribution between reference (training set?) and current batch data    

### Non-Batch
#### Data Quality
create a window function to compare data distribution for each window

#### monitoring scheme
![picture from ml ops zoomcamp course -video 5.1](https://github.com/ChungWasawat/dtc_mlops_course/tree/main/week5/img)