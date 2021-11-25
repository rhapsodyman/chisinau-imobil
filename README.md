### Chisinau imobil parser

Gathers information from two of the most popular Chisinau real estate websites: http://www.proimobil.md/ and https://accesimobil.md/



#### Configuration
Is done using ```config.json``` file

* outputType - specifies file output type - can be ```csv``` or ```excel```
* category - can only be ```apartment```
* minPrice - min price to include
* maxPrice - max price to include
* apartmentType - array, accepted values are:  [```"new"```, ```"old"```]
* apartmentState - array, accepted values are: [```"euro"```, ```"living"```, ```"white"```]
* rooms - array, accepted values are: [```"1"```, ```"2"```, ```"3"```, ```"4"```]
* offerType - array, accepted values are: [```"sale"```,```"rent"```]


#### Execution
1. run ```pip install -r requirements.txt``` in your terminal
2. execute ```parse_accessimobil.py``` or ```parse_proimobil.py```files
3. reports will be generated in the ```output``` folder