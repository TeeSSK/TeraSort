# TeraSort

## Description

Term-project for education, aim to solve the problem GigaSort.  
Before start running project, you should create folder like this:  
```
- data
  - input
      your input file
  - output
      your file for store output
```

## Run project via Python locally

There are two files are used as inputs as a `sys.argv`: one is an input file and the other is a file used to store the result. <br>

The command shown below is an example for running this project:

```
python gigaSort.py data/input/sort-rand-199999999.txt data/output/output.txt
```

## Run project via Docker

First, build docker image via `docker build -t $yourtagname .` and create docker container for running docker image. <br>
There are two file for mouting volume from host directory to directory inside the container. <br>
  1. `$(pwd)"/data/input` map to `/input`.
  2.  `$(pwd)"/data/output` map to `/output`.  
 
  and access as `sys.argv` behind powergrid (name of docker image).

### Example command is below:
```
docker run -v "$(pwd)"/data/input:/input -v "$(pwd)"/data/output:/output gigasort /input/sort-rand-199999999.txt /output/output.txt
```
