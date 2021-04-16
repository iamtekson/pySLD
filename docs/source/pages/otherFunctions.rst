.. _additional-functions:

Some additional function
========================

.. code:: python

    from pysld.style import StyleSld
    sld = StyleSld (
        style_name='polygonStyle', 
        geom_type='polygon', 
        attribute_name='USE',
        color_palette='Spectral_r', 

        # Postgres connection parameters 
        dbname='postgres',
        user='postgres',
        password='admin',
        host='localhost',
        port='5432',
        schema='public',
    )

    sld.get_attribute_name(pg_table_name='postgres_table_name') # get the random attribute_name
    print(sld.attribute_name) # Print the random attribute name from ``get_attribute_name()`` function

    sld.get_values_from_pg() # Get and set the values from given ``pg_table_name`` table and ``attribute_name`` column
    print(sld.values) 

    


PostgreSQL functions
^^^^^^^^^^^^^^^^^^^^

Below is the example of some postgres functionalities,

.. code:: python

    from pysld.postgres import Pg 

    pg = Pg(dbname='dbname', user='postgres', password='admin', host='localhost', port=5432)
    
    pg.connect() # connect the postgresql 

    pg.set_postgres_schema('public') # set the schema to public

    pg.get_column_names(table='table_name') # get all the column names from "table_name" table

    pg.get_values_from_column(column='column_name', table='table_name', schema='public') # get the values from "column_name" column of "table_name" table

   

