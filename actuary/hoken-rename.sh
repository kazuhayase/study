#!/bin/bash
for f in hoken*.tex hoken*.pdf; do
 t=${f#hoken}
 n=seiho$t
 #echo $f
 #echo $t
 #echo $n
 git mv $f $n
done
