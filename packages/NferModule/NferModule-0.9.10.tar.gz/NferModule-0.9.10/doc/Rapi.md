R Interface
=============================================================================
To load the R language interface, setwd() to the base directory of the project
and run:

```R
> source("R/nfer.R")
```

This will load the library and instantiate some R wrapper functions.

To initialize a specification that can be applied to a dataframe of events, use
the Rnfer function.  This function takes three parameters: the path to an nfer
specification file, the path to a log file (optional), and the log level (optional).

```R
> handle <- Rnfer("examples/specs/ssps.nfer")
```

This can then be applied to a dataframe containing events.  There should be two 
columns, the first of which is a character type containing the event names, and 
the second of which is a numeric type containing the event timestamps.

Currently the R wrappers will automatically convert factor columns to character 
columns.  The R API does not presently support data maps, but support should be
added soon.

```R
> df <- read.table("examples/logs/ssps.events", sep="|", header=FALSE)
> intervals <- RnferApply(handle, df)
> summary(intervals)
     name               start                end           
 Length:19342       Min.   :8.238e+05   Min.   :1.080e+09  
 Class :character   1st Qu.:2.452e+13   1st Qu.:2.455e+13  
 Mode  :character   Median :4.023e+13   Median :4.024e+13  
                    Mean   :4.460e+13   Mean   :4.462e+13  
                    3rd Qu.:6.589e+13   3rd Qu.:6.592e+13  
                    Max.   :9.335e+13   Max.   :9.335e+13  
```

The learner can also be used from R using the RnferLearn function.
The function takes a single parameter which is a data frame of events.  
There should be two columns, the first of which is a character type
containing the event names, and the second of which is a numeric type 
containing the event timestamps.  RnferLearn also has the same two optional
arguments as Rnfer which are the log file and log level.

The handle returned from RnferLearn can then be applied to a trace using RnferApply 
just like if it had been loaded from a specification file.

```R
> df <- read.table("examples/logs/ssps.events", sep="|", header=FALSE)
> learned <- RnferLearn(df)
> intervals <- RnferApply(learned, df)
> summary(intervals)
     name               start                end           
 Length:4864        Min.   :8.238e+05   Min.   :1.080e+09  
 Class :character   1st Qu.:2.289e+13   1st Qu.:2.290e+13  
 Mode  :character   Median :3.948e+13   Median :3.948e+13  
                    Mean   :4.475e+13   Mean   :4.475e+13  
                    3rd Qu.:6.771e+13   3rd Qu.:6.772e+13  
                    Max.   :9.335e+13   Max.   :9.335e+13  
```

