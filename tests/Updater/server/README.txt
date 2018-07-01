=== Example layout for mod locations on your webserver. ===

Just create a folder with the mod name and put
updates.html + desired updates archives into this subfolder.


Notes:
– Local testing is easy if you simply starts a webserver with python, i.e.
  'python -m SimpleHTTPServer' or python3 -m http.server'

– Add update_info.json into your update zips to define some meta
  information. Currently, you...
  • can define a popup text, which will be displayed after the update,
  • add a list of (deprecated) files which should be removed.
