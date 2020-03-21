The library supoorts the following file formats so far. The development process is persistent to expand the number of supported formats.


.. jupyter-execute::
   :hide-code:

   import geoextent.lib.extent as geoextent
   import subprocess

   # (1) Download showcase file and extract geoextent data
   subprocess.run('mkdir showcase_csv', shell=True)
   subprocess.run('wget -P showcase_csv https://sandbox.zenodo.org/record/256820/files/cities_NL.csv', shell=True)

   geoextent.fromFile('showcase_csv/cities_NL.csv', True, True)

.. jupyter-execute::
   :hide-code:
   :hide-output:

   # (2) Remove downloaded showcase file
   subprocess.run(["rm", "-rf", "showcase_csv"])  #Hello
