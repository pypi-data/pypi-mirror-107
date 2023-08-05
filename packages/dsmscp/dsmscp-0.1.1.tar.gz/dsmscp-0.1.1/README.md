# dsmscp
## installation
```
pip install dsmscp
```
## run the application
by passing a config file
```
python3 -m dsmscp -c [config file].ini
```
or by passing params in command line
```
python3 -m dsmscp -H host:port
```
replace host by the host url and port by the host port
## config file structure
```
[GLOBAL]
loglevel=info
host=host:port
```