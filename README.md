# Test demo

## xml-zip generator

## Usage

```bash
pip install -r requirements.txt
python main.py --mode generate
python main.py --mode parse

# For help:
python main.py -h
```

Assignment:

Implement python-app which should do following:

1. Creates 50 zip-archives with 100 generated xml file in each with structure:
```xml
<root>
  <var name='id' value='<unique random string value>'/>
  <var name='level' value='<random integer in range from 1 to 100'/>
  <objects>
    <object name='<random string value>'/>
    <object name='<random string value>'/>
    …
  </objects>
</root>
```
In `objects` tag random count `object` tag in range from 1 to 10.

2. Process a directory with generated zip files, parse nested xml-files and created two csv-files:

    First: id, level - for each xml-file.
    Second: id, object_name - for each 'object' tag in each xml-file (1-10 row per xml).

For second part mandatory use multicore processors resources.
 
