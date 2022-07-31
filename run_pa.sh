spark-submit \
    --master local[1] \
    --name spark-pi \
    --conf spark.executor.instances=1 \
    local:///app/task.py
