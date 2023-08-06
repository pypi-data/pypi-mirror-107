### bq_lookml_generator v.0.1.1

This automatic generator is buit over Josh Temples looker parser [https://github.com/joshtemple/lkml]. Building out lkml, it allows you to generate lookml from BigQuery metadata. 

## getting started

- make sure you are working in a venv.
- pip install lookml_gen

- config params 
    - run lookml_gen_init 
        - head to .lookml_gen and input your wh credentials
            - warehouse configs 
                - either input big_query or red_shift (current support warehouses) under warehouse_name
                - input schema name
                - input project name
            - security 
                - big_query 
                    - input your keyfile path
                - red_shift
                    - input you credentials


- input your warehouse schema target in here lookml/bq_lookml_gen/warehouse_target.py
- type lookml_gen into terminal and watch the base explore generate... 

## troubleshooting 

- run pip install -r requirements.txt if you are running into dependency issues
- you can run bq_lookml_gen.py from terminal if needed

## to update

twine upload

    --skip-existing dist/*

## to develop

- add new features to setup tools using: python setup.py develop


rebuild the wheel 

    python setup.py sdist bdist_wheel

    pip install -e /Users/lewisbaker/Documents/GitHub/kaplan_data_warehouse/lookml/lookml_gen/lookml_gen.py

pip freeze > requirements.txt

cat requirements.txt

