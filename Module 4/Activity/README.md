## Learning Activity 1: Working with DataFrame and Functions in PySpark

1. [Download Traffic Crash Dataset](1.Download_Dataset/README.md)

2. [Initialize File structure](2.Initialize/README.md)
   
3. [Install Pyspark](3.Install_Pyspark/README.md)

In Jupyter Notebook, using PySpark, perform the following:

- ## Create SparkSession 
Use the following code:
```python
#import necessary packages
from pyspark.sql import SparkSession

#create spark context
sqlCtx = SparkSession.builder.getOrCreate()
```
instead of : 
```python
from pyspark.sql import SQLContext
from pyspark import SparkContext

#create spark context
sc = SparkContext.getOrCreate()
sqlCtx = SQLContext(sc)
```
### What is SparkSession
SparkSession is an entry point to underlying Spark functionality in order to programmatically create Spark RDD, DataFrame and DataSet. It’s object “spark” is default available in spark-shell and it can be created programmatically using SparkSession builder pattern.

### What is SQLContext
Spark SQLContext is defined in org.apache.spark.sql package since 1.0 and is deprecated in 2.0 and replaced with SparkSession. SQLContext contains several useful functions of Spark SQL to work with structured data (columns & rows) and it is an entry point to Spark SQL.


- ## Load the data from the csv files into DataFrames.

### Step 1:
Run the following code to load data from csv files:
```python
crashes = sqlCtx.read.option('header','true').csv('data/Traffic_Crashes_-_Crashes.csv')
vehicles = sqlCtx.read.option('header','true').csv('data/Traffic_Crashes_-_Vehicles.csv')
peoples = sqlCtx.read.option('header','true').csv('data/Traffic_Crashes_-_People.csv')
```  
`sqlCtx.read` is  a function to read from csv file.

`.option('header', 'true')` is an option means csv file headers are already defined in the file.

`.csv('data/Traffic...')` is file path you created in Initialize part. 

- ## Find the ratio of number of crashes where the person involved was using cell phone to that where the person was not using the cell phone.

### Step 1:
Following code will show the Cause of the accident, grouped by "DRIVER_ACTION" and count number. 
```python
peoples.groupby(peoples.DRIVER_ACTION).count().orderBy("count").show(truncate=False)
```
Press `Shift + Enter` you have to see following table:
```jupyter
+---------------------------------+-----+
|DRIVER_ACTION                    |count|
+---------------------------------+-----+
|EMERGENCY VEHICLE ON CALL        |3    |
|TEXTING                          |3    |
|CELL PHONE USE OTHER THAN TEXTING|5    |
|EVADING POLICE VEHICLE           |5    |
|OVERCORRECTED                    |7    |
|IMPROPER PARKING                 |16   |
|WRONG WAY/SIDE                   |21   |
|TOO FAST FOR CONDITIONS          |49   |
|IMPROPER LANE CHANGE             |69   |
|DISREGARDED CONTROL DEVICES      |73   |
|IMPROPER TURN                    |92   |
|IMPROPER PASSING                 |99   |
|IMPROPER BACKING                 |125  |
|null                             |176  |
|FOLLOWED TOO CLOSELY             |184  |
|OTHER                            |241  |
|FAILED TO YIELD                  |291  |
|NONE                             |1073 |
|UNKNOWN                          |1507 |
+---------------------------------+-----+
```

### Step 2:
The following code will group the accidents by "DRIVER_ACTION" filtered by actions that cell phone envolved: "CELL PHONE USE OTHER THAN TEXTING" and "TEXTING"

```python
phone = peoples.groupby(peoples.DRIVER_ACTION).count().filter((peoples.DRIVER_ACTION == 'CELL PHONE USE OTHER THAN TEXTING') | (peoples.DRIVER_ACTION == 'TEXTING'))
phone.show(truncate=False)
phone_crashes = phone.groupBy().sum('count').collect()[0][0]
print("crashes that occurs because of phone : ", phone_crashes)
```

```jupyter
+---------------------------------+-----+
|DRIVER_ACTION                    |count|
+---------------------------------+-----+
|CELL PHONE USE OTHER THAN TEXTING|5    |
|TEXTING                          |3    |
+---------------------------------+-----+

crashes that occurs because of phone :  8
```

### Step 3:
The following code will group the accidents by "DRIVER_ACTION" filtered by actions that cell phone has not envolved:
```python
no_phone = peoples.where((peoples.DRIVER_ACTION != "UNKNOWN") & (peoples.DRIVER_ACTION != "NONE") & (peoples.DRIVER_ACTION != "OTHER"))\
.groupby("DRIVER_ACTION").count().filter((peoples.DRIVER_ACTION != 'CELL PHONE USE OTHER THAN TEXTING') & (peoples.DRIVER_ACTION != 'TEXTING'))

no_phone.show(truncate=False)
no_phone_crashes = no_phone.groupBy().sum('count').collect()[0][0]
print("crashes that occurs because of other : ", no_phone_crashes)
```
```jupyter
+---------------------------+-----+
|DRIVER_ACTION              |count|
+---------------------------+-----+
|EVADING POLICE VEHICLE     |5    |
|FOLLOWED TOO CLOSELY       |184  |
|IMPROPER LANE CHANGE       |69   |
|IMPROPER PARKING           |16   |
|TOO FAST FOR CONDITIONS    |49   |
|DISREGARDED CONTROL DEVICES|73   |
|IMPROPER TURN              |92   |
|IMPROPER BACKING           |125  |
|OVERCORRECTED              |7    |
|WRONG WAY/SIDE             |21   |
|IMPROPER PASSING           |99   |
|FAILED TO YIELD            |291  |
|EMERGENCY VEHICLE ON CALL  |3    |
+---------------------------+-----+

crashes that occurs because of other :  1034
​
```

### Step 3: 
print out the ratio of numbers found in previous steps : 
```python
print("ratio: ", f"{phone_crashes}/{no_phone_crashes} =", 100 * phone_crashes/no_phone_crashes)
```
```jupyter
ratio:  8/1034 = 0.7736943907156673
```

- ##Find which three Age groups were involved with highest number of crashes.

```python
from pyspark.sql.types import IntegerType

age = peoples.where((peoples.AGE > 0)).groupby(peoples.AGE.cast(IntegerType())).count().orderBy("count", ascending=False).limit(3)
age.show(120, truncate=False)
```
```jupyter
+----------------+-----+
|CAST(AGE AS INT)|count|
+----------------+-----+
|30              |78   |
|25              |77   |
|28              |76   |
+----------------+-----+
```

- ##Find which month of the year has the highest crashes.
```python
month = crashes.select((crashes.CRASH_MONTH).cast(IntegerType()))\
                    .groupby("CRASH_MONTH")\
                    .count()\
                    .orderBy("count", ascending=False).limit(1)
month.show(truncate=False)
```
```jupyter
+-----------+-----+
|CRASH_MONTH|count|
+-----------+-----+
|5          |1195 |
+-----------+-----+
```
- ##Find which day of the week has the least crashes.
```python
df = crashes.select((crashes.CRASH_DAY_OF_WEEK).cast(IntegerType()))\
                    .groupby("CRASH_DAY_OF_WEEK")\
                    .count()\
                    .orderBy("count", ascending=True)
df.show(truncate=False)
```
```jupyter
+-----------------+-----+
|CRASH_DAY_OF_WEEK|count|
+-----------------+-----+
|null             |1    |
|6                |148  |
|5                |229  |
|2                |236  |
|1                |274  |
|7                |285  |
|3                |577  |
|4                |594  |
+-----------------+-----+
```





APA Reference:

Sullivan, D. (2019). Jupyter Notebook and PySpark configuration and basic operation using DataFrames. Retrieved from https://www.linkedin.com/learning/introduction-to-spark-sql-and-dataframes/apache-spark-sql-and-data-analysis?u=56744473.
