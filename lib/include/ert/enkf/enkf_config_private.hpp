/*
   Copyright (C) 2011  Equinor ASA, Norway.

   The file 'enkf_config_private.h' is part of ERT - Ensemble based Reservoir Tool.

   ERT is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   ERT is distributed in the hope that it will be useful, but WITHOUT ANY
   WARRANTY; without even the implied warranty of MERCHANTABILITY or
   FITNESS FOR A PARTICULAR PURPOSE.

   See the GNU General Public License at <http://www.gnu.org/licenses/gpl.html>
   for more details.
*/

struct enkf_config_struct {
  int  		    ens_size;
  hash_type        *config_hash;
  hash_type        *obs_hash;
  bool              endian_swap;
  path_fmt_type    *run_path;
  int               Nwells;
  char            **well_list;
};
