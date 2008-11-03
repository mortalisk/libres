#ifndef __GEN_DATA_CONFIG_H__
#define __GEN_DATA_CONFIG_H__
#ifdef __cplusplus
extern "C" {
#endif
#include <ecl_util.h>
#include <enkf_macros.h>
#include <gen_common.h>
typedef struct gen_data_config_struct gen_data_config_type; 

void    	        gen_data_config_get_ecl_file(const gen_data_config_type * , int , char ** , char ** );
void                    gen_data_config_get_obs_file(const gen_data_config_type *, int , char ** , char **);
void    	        gen_data_config_free(gen_data_config_type * );
gen_data_config_type  * gen_data_config_fscanf_alloc(const char * );
bool                    gen_data_config_obs_on(const gen_data_config_type * , int );
bool                    gen_data_config_is_active(const gen_data_config_type *  , int );
void                    gen_data_config_assert_metadata(gen_data_config_type * , int  , int , ecl_type_enum , const char * );
void                    gen_data_config_deactivate_metadata(gen_data_config_type *);
const bool            * gen_data_config_get_iactive(const gen_data_config_type * );
int                     gen_data_config_get_data_size(const gen_data_config_type * );
void                    gen_data_config_set_obs_size(gen_data_config_type * , int);
void                    gen_data_config_fload_iactive(gen_data_config_type * ,  FILE * , const char * ,gen_data_file_type  , int);
void                    gen_data_config_read_local_map(gen_data_config_type *, int);
void                    gen_data_config_change_iactive(gen_data_config_type *, int);
void                    gen_data_config_fload_local_data(FILE *, gen_data_config_type *);
bool                    gen_data_config_get_local_active(gen_data_config_type *, int);
void                    gen_data_config_realloc_local(gen_data_config_type *, int);
bool                    gen_data_config_fload_local_step_active(int);
int                     gen_data_config_get_num_local_updates(gen_data_config_type *);
void                    gen_data_config_set_local_step(gen_data_config_type *,int);
int                     gen_data_config_get_local_step(gen_data_config_type *);
int                   * gen_data_config_get_param_index_i(const gen_data_config_type *,int);
int                   * gen_data_config_get_param_index_j(const gen_data_config_type *,int);
int                   * gen_data_config_get_param_index_k(const gen_data_config_type *,int);
int                     gen_data_config_get_num_param(const gen_data_config_type *,int);

VOID_FREE_HEADER(gen_data_config)
GET_ACTIVE_SIZE_HEADER(gen_data);
GET_ACTIVE_LIST_HEADER(gen_data);

#ifdef __cplusplus
}
#endif
#endif
