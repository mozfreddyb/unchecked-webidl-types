# unchecked-webidl-types

This script parses one or multiple WebIDL files to find usage of
lax type definitions. Functions and constructors that take object
parameters might do some unintended things with e.g., opaque objects.
To find those we go through  all functions and constructors that
take parameters of type object. The script will also go through all
custom defined types and take them into account as well.