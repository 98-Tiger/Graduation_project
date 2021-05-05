
PANOPLY

  panoply \PAN-uh-plee\, noun: 1. A splendid or impressive array. [...]


INTRODUCTION

  Panoply is a Java application that allows the user to make plots of data from netCDF, HDF,
  and GRIB datasets. Although its strength is in making longitude-latitude (map) plots, it
  can also make other types of georeferenced plots, including keograms and Hovmoeller diagrams;
  general 2D color contour plots; and line plots. Data arrays may be "sliced" from larger
  multidimensional arrays (aka, variables). A large selection of global map projections is
  available for lon-lat figures. Plot images may be saved to disk in bitmap graphic formats
  or in PDF.

  Panoply requires that a Java 9 (or later) Runtime Environment be installed on your computer.


DOWNLOADING

  The current version of Panoply, along with other information about the application, may
  always be found at
  https://www.giss.nasa.gov/tools/panoply/


INSTALLING AND RUNNING THE PANOPLY FOR WINDOWS PACKAGE

  The Panoply package for Windows comes as a zipped archive. You _must_ manually extract
  this archive. Some versions of Windows allow you to run programs from within a zipped
  archive without extraction. If you try this with Panoply, it won't work.

  The Panoply package for Windows should, after uncompression, include the following items:

  - Panoply.exe application.
  - Application code files in a folder (sub-directory) called "jars".
  - This README file.

  To run Panoply, double-click on the Panoply.exe application.


TROUBLE-SHOOTING

  You _must_ manually unzip the GProjector.zip archive file or else Panoply will not work.
  Do not simply open the zip file on your desktop and doubleclick on the Panoply.exe icon.

  The sub-directory called jars _must_ remain in the same directory as the Panoply.exe launcher.
  Also, any .jar files in that folder must remain there. If you move or remove the jars folder
  or any of its contents, Panoply will not work.

  The Panoply.exe Java launcher requires that certain keys/values regarding the Java installation
  have been set in the Windows Registry. However, some alternative Java distributions may not set
  these keys or else may require that you specifically enable them during installation. For
  example, if using the AdoptOpenJDK installer, you must enable the options for "Set JAVA_HOME
  variable" and "JavaSoft (Oracle) registry keys" in the Custom Setup panel.


OTHER DOCUMENTATION

  More details about Panoply are available at:

    https://www.giss.nasa.gov/tools/panoply/


COLOR TABLES AND CONTINENTS FILES

  Beginning with version 4, Panoply's "standard" selection of color tables and map overlays
  is built into the application. Additional color tables and map overlays may be opened for
  a single session or added to your favorites library for continued use. See the Panoply
  website for for such optional support files.


CONTACT

  Panoply was developed at the

  NASA Goddard Institute for Space Studies
  2880 Broadway, New York, NY 10025 USA

  Please send bug reports, etc., to Dr. Robert Schmunk at robert.b.schmunk@nasa.gov.


ACKNOWLEDGMENTS

  Panoply uses Java classes and libraries written by several third-party organizations. A
  complete list, with links to pertinent websites containing license information and source
  code, may be accessed via Panoply's Help menu or on the Panoply website.
