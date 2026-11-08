#!/bin/sh
# Wrap the artifact page (site.html) into a standalone index.html for any static host.
cd "$(dirname "$0")"
{
  printf '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  awk '/^<style>/{exit} {print}' site.html
  awk 'f||/^<style>/{f=1} f&&/^<\/style>/{print; exit} f{print}' site.html
  printf '</head>\n<body>\n'
  awk 'p{print} /^<\/style>/{p=1}' site.html
  printf '</body>\n</html>\n'
} > index.html
