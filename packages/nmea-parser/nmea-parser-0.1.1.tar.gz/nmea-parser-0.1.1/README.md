# NMEA Parser

A library used to decode NMEA data streams from GNSS receivers. Capable of parsing a text file
containing NMEA data or reading from a serial port real time.

This library is currently in Beta and is subject to change any time.

## Dependencies

PySerial is the only dependency. See `requirements.txt`.

## Usage

See www.bek.sh/nmea-parser for a manual.

## Changelog

* 0.1.1 (2021-05-24)
	- Improve safety of file handling in input stream module
	- Bug fixes in type checking
	- Fix absolute imports in project
	- Small fixes to documentation

* 0.1.0 (2021-05-20):
    - Inital release
