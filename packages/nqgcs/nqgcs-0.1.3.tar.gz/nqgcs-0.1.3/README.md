# NQGCS

This package offers a pleasant interface to Google Cloud Storage. 

Usage: 

# Create an NQGCS object 

```python
form nqgcs import NQGCS

nqgcs = NQGCS(json_key_path="your json key to gcs")
```        

The json key above is not needed on Appengine. 
The json key is also not needed if you use: 

```commandline
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```

in the shell. 

# Access GCS

## Upload a file

```python
with open("myfile", "r") as f:
    nqgcs.upload("bucket name", "file name", f, type="text/plain")
```

## Write a string to GCS

```python
nqgcs.write("bucket name", "file name", "my content string", type="text/plain")
```

## Read a string from GCS

```python
s = nqgcs.read("bucket name", "file name")
```

## Download a file from GCS

```python
nqgcs.download("bucket name", "file name")
```

## Delete a file, list files

```python
nqgcs.delete("bucket name", "file name")

for f in nqgcs.listfiles("bucket_name", maximum=200):
    print("The file name is:", f)
```
