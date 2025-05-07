#!/usr/bin/env bash

find ./screenshots -not -name "*-small.png" \
 -type f \
 -execdir sh -c 'magick $0 -resize '25%' "${0%.*}-small.png"' {} \;