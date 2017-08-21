#!/bin/bash
sed -i -e 's|_static/|0static/|g' `find manual/ -type f`
mv manual/_static manual/0static
sed -i -e 's|_sources/|0sources/|g' `find manual/ -type f`
mv manual/_sources manual/0sources
