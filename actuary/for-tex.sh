#!/bin/sh

for t in hoken*.tex; do
    sed -f prob-ans.sed $t > nc/$t;
done

