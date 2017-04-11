=== The problem ===
The Diplomatic Menu is encoded in the EXE and does not
scale with the resolution. It made the menu nearly unuseable for
high resolutions.

=== The solution ===
Hook in at the drawing methods of the menu and increase the
values with reflect the dimenions of the drawed elements.

This modification superseeds tests/GetSaveOverHttp.
and also uses BTS_Wrapper.exe to load the dll at startup.

