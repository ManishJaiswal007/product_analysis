
# Product Analysis
This project computes diffrent report project wise, currently supported reports are :-
- most time consuming query project wise1
- usage per project wise
- total number of query success and faulure (can be used for show success rate)

## Installation Requirement
To run this project below are required
    
- Python - 3.8 and above
- Spark 3.2.2
- pytest
- Java

 
To build docker image, run below command

```bash
sudo docker build -t product-analysis-image:latest .
```

## Appendix
To configure, use config.json file in config folder

| Parameter     |  Description                                        |
| :------------ |  :------------------------------------------------- |
| `time_window` |  define time window to calculate usage product_wise |
| `agg_col`     |  Column used for aggreation of usage                |


## Deployment

To deploy this project run

```bash
sudo docker run -v $PWD:/app/output/  product-analysis-image
```

**Note**: output of various report will be under report folder, it will be created in current folder.


## Future Development
- Handle Diffrent Exceptions
- Add Data quality checks
- Add multiple logger.

**Note**
- Current solution is builded on spark (Batch-processing) thus with few config changes it can be scaled up easily to handle heavy loads. In addition to spark, as this project produce a docker image it can be used with kubernates to scale up/down too.
- For making it more efficient pipe line we can include kafka as message que system to make whole pipeline more stable and robust. 

## Authors
- Manish Jaiswal
