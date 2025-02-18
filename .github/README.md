# OMSI Configuration Exporter 

This add-on for Blender is effectively a port of part of the original add-on created for Blender versions 2.68-2.79b by [Fabian S. (faaabiii)](https://forum.omnibussimulator.de/forum/index.php?thread/29488-blender-addon-omsi-konfigurationsdateien-exporter-v1-2-neu-passengercabinexporte/) and originally uploaded to the official OMSI forum. 

## Features

*(Items ~~struck out~~ are not implemented as of the current release version)*

- Import of Path config files
  - Provides raw path data only
  - One-way paths and Head Clearance `set_roomheight` data are not imported
- Export of Path Configurations
  - Allows for one-way path configuration through the use of ~~sharp~~ bevel marking on path segments 
  - ~~Allows for Head Clearance data using the bevel bevel marking on path segments~~
  - ~~Allows for step sound group allocation through vertex groups~~
    - ~~Step sound groups must be manually defined after the fact~~
- Export of Passenger Cabin (seat and standing position) Configurations
  - Allows for driver seat definition, through the use of ~~sharp~~ crease marking on the driver's position 
  - Allows the randomisation of rotation of standee locations if only a single vertex is defined as a passenger point
  - ~~Allows the definition of money points, change points and stamper and ticketprinter locations~~

## Releases

Releases can be found in the [releases](https://github.com/jem-suu/io_scene_omsipath/releases) tab, or on the sidebar on the right hand side
 
## License

This blender plugin is released under the GPLv2 license, as per the original plugin.
