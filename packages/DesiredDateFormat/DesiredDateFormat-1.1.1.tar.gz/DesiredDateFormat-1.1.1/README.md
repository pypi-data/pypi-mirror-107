# DesiredDateFormat
This module will convert date (the date which python library datetime module provides) into the desired date format.
User need to pass 2 arguments, the first argument will be the date and the second one is the desired date format which the user wants to receive output. 
#### user can pass python inbuilt datetime as the first argument for date and the the second argument will be the required format in which the user wants to receive output i.e [dd/mm/yy , mm/dd/yy, yy/mm/dd]
### for example: 
> import datetime
>
> import DesiredDateFormat.Convert as ddt
>
>ddt().convert(datetime.datetime.now(), "dd-mm-yy")
> 
> and the output would be same as above 
> 
>\>> output: 23-05-2021 (current date : 2021-05-23)
### for example:
> convert("2021/05/14","dd/mm/yy")(make sure that the first argument which is 2021/05/14 in the format yy/mm/dd i.e how the python datetime module provides the date)
> 
>\>> output would be : 14/05/2021

OR
>ddt().convert("2021-05-14","dd/mm/yy")
> 
>\>> output would be : 14/05/2021

OR


## Installation
  Run the following command to install:
  ```pip install DesiredDateFormat```


## Usage
```
import DesiredDateFormat.Convert as ddt
import datetime
ddt().convert(datetime.datetime.now(), "dd-mm-yy")
>> output: 23-05-2021 (current date : 2021-05-23) 
```
