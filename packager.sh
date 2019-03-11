#!/bin/bash

# Just a script to package the solution into the format I need.

ROLL='p2csn17017'
INPF='test.py'
OUTF='subnet.py'

rm -rf $ROLL
rm $ROLL.tar

mkdir $ROLL/1 -p
cp $INPF $ROLL/1/$OUTF

tar -cf ./$ROLL.tar $ROLL

rm -rf $ROLL

echo 'Done!'
