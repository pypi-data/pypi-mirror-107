**Logger4py**  

**_Custom logging module_**  

**Usage**  

> install package 
```
pip install logger4py
```

> How to use logger4py  

```
from logger4py import Logger  
log = Logger.get_logger('my_module')
# 'my_module' is the name of the logger object got from the logger4py.json file in 'loggers' section  

log.debug('this is a debug message')  
log.info('this is an info message')  
log.error('this is an error message')  
log.warning('this is a warning message')
```


**Demo**    

```
2021-05-20T00:06:20.736	DEBUG	35692	44080	test_log	this is a debug message      
2021-05-20T00:06:20.736	INFO	35692	44080	test_log	this is an info message    
2021-05-20T00:06:20.736	ERROR	35692	44080	test_log	this is an error message    
2021-05-20T00:06:20.736	WARNING	35692	44080	test_log	this is a warning message    
2021-05-20T10:13:09.552	DEBUG	42864	43524	test_log	this is a debug message    
2021-05-20T10:13:09.552	INFO	42864	43524	test_log	this is an info message    
2021-05-20T10:13:09.552	ERROR	42864	43524	test_log	this is an error message    
2021-05-20T10:13:09.553	WARNING	42864	43524	test_log	this is a warning message
```
  

**Configuration file**  
1. Default configuration file path:

> module directory/logger4py.json

```
.\<your virtual environment>\Lib\site-packages\logger4py\logger4py.json
```
In my test environment :

```
C:\Users\mahmoud.aouinti\Desktop\test\env\Lib\site-packages\logger4py\logger4py.json
```
 
2. Default Configuration file content:

```
{
  "version": 1,
  "disable_existing_loggers": false,
  "formatters": {
    "simple": {
      "datefmt": "%Y-%m-%dT%H:%M:%S",
      "format": "%(asctime)s.%(msecs)03d\t%(levelname)s\t%(thread)d\t%(process)d\t%(module)s\t%(message)s"
      
    },
    "simple_message": {
      "datefmt": "%Y-%m-%dT%H:%M:%S",
      "format": "%(message)s"
      
    }
  },

  "handlers": {
    "console": {
      "class": "logging.StreamHandler",
      "level": "DEBUG",
      "formatter": "simple",
      "stream": "ext://sys.stdout"
    },

    "info_file_handler": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "DEBUG",
      "formatter": "simple",
      "filename": "info.log",
      "maxBytes": 10485760,
      "backupCount": 20,
      "encoding": "utf8"
    },

    "error_file_handler": {
      "class": "logging.handlers.RotatingFileHandler",
      "level": "INFO",
      "formatter": "simple",
      "filename": "errors.log",
      "maxBytes": 10485760,
      "backupCount": 20,
      "encoding": "utf8"
    }
  },

  "loggers": {
     "my_module": {
        "level": "DEBUG",
        "handlers": ["info_file_handler"],
        "propagate": false
      }
    },

  "root": {
    "level": "ERROR",
    "handlers": ["console", "info_file_handler", "error_file_handler"]
  }
}

```



