#!/usr/bin/env perl

$latex  = "uplatex -halt-on-error -interaction=nonstopmode -file-line-error --synctex=1 %O %S";
$bibtex = 'upbibtex %O %S';
$biber = 'biber --bblencoding=utf8 -u -U --output_safechars %O %S';
$makeindex = 'upmendex %O -o %D %S';
$dvipdf = 'dvipdfmx %O -o %D %S';

$pdf_mode = 3;
$max_repeat = 5;
