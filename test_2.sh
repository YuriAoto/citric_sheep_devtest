#!/bin/sh
#
# Tests for config_2.txt
#
#
python make_demand 1 2024-07-01T00:00:00.000000 # mon 00
python make_demand 2 2024-07-01T01:00:00.000000 # mon 01
python make_demand 1 2024-07-01T02:00:00.000000 # mon 02
python make_demand 2 2024-07-01T03:00:00.000000 # mon 03
python make_demand 3 2024-07-01T05:00:00.000000 # mon 05
python make_demand 1 2024-07-01T06:00:00.000000 # mon 06
python make_demand 2 2024-07-01T06:10:00.000000 # mon 06
python make_demand 1 2024-07-01T08:00:00.000000 # mon 08
python make_demand 1 2024-07-02T00:00:00.000000 # tue 00
python make_demand 3 2024-07-02T01:00:00.000000 # tue 01
python make_demand 1 2024-07-02T02:00:00.000000 # tue 02
python make_demand 1 2024-07-02T03:00:00.000000 # tue 03
python make_demand 2 2024-07-02T05:00:00.000000 # tue 05
python make_demand 1 2024-07-02T06:00:00.000000 # tue 06
python make_demand 3 2024-07-02T06:10:00.000000 # tue 06
python make_demand 2 2024-07-02T08:00:00.000000 # tue 08
python make_demand 1 2024-07-03T00:00:00.000000 # wed 00
python make_demand 2 2024-07-03T01:00:00.000000 # wed 01
python make_demand 1 2024-07-03T02:00:00.000000 # wed 02
python make_demand 2 2024-07-03T03:00:00.000000 # wed 03
python make_demand 2 2024-07-03T05:00:00.000000 # wed 05
python make_demand 1 2024-07-03T06:00:00.000000 # wed 06
python make_demand 3 2024-07-03T06:10:00.000000 # wed 06
python make_demand 1 2024-07-03T08:00:00.000000 # wed 08
sleep 10
python make_demand predict 2024-07-08T01:00:00.000000 # mon 01
python make_demand predict 2024-07-08T06:00:00.000000 # mon 06
python make_demand predict 2024-07-09T01:00:00.000000 # tue 01
python make_demand predict 2024-07-09T06:00:00.000000 # tue 06
python make_demand predict 2024-07-10T06:00:00.000000 # wed 06

