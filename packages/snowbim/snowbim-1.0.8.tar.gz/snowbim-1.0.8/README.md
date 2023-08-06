# snowbim
This is to do something awesome between snowflake database and Power BI tabular model file (.bim).

We make use of [dbt (data build tool)'s profile](https://docs.getdbt.com/dbt-cli/configure-your-profile) to configure the Snowflake connection.

Those are:
* Refresh tables (key: name)
* Refresh table's columns (key: name)
* Refresh table's partitions (key: name)

Supported Models:
* Compatibility Level: 1550
* Default Power BI Data Source Version: powerBI_V3

Installation:
```
python -m pip install snowbim --upgrade

# dependencies
python -m pip install snowflake-connector-python[pandas]
```


Virtual enviroment:
```
python -m venv env
```

Activate virtual env:
```
Windows: 	.\env\Scripts\activate
Linux:		source env/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

