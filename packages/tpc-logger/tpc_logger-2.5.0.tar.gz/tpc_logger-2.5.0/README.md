# tpc_logger

Default python logger. Manage the logger in the console (INFO level) and also create a file activity.log with DEBUG level. File size is 10 mo maximum.

## How to use
First import 
```
    from tpc_logger import log
```
Then log from 4 differents level. Can log multi var
```
    log.debug("")
    log.info("ok",myvar,anrray,adict,"Noproblem","#éà@ Utf-8|Encode")
    log.warning("")
    log.error("")
```
