//Obtaien index to deform image in next kernel

KERNEL void Deform_index(GLOBAL_MEM float *i_frac_1,

GLOBAL_MEM float *i_frac_2,
GLOBAL_MEM float *j_frac_1,
GLOBAL_MEM float *j_frac_2,
GLOBAL_MEM int *box_origin_x,
GLOBAL_MEM int *box_origin_y,
GLOBAL_MEM int *i_index_1,
GLOBAL_MEM int *i_index_2,
GLOBAL_MEM int *j_index_1,
GLOBAL_MEM int *j_index_2,
GLOBAL_MEM float *u_index,
GLOBAL_MEM float *v_index,
GLOBAL_MEM float *u,
GLOBAL_MEM float *v,
GLOBAL_MEM float *du_dx,
GLOBAL_MEM float *du_dy,
GLOBAL_MEM float *dv_dx,
GLOBAL_MEM float *dv_dy,
GLOBAL_MEM int *data)

{
    float temp;

    int box_size_x = data[1];
    int box_size_y = data[2];

    int pos = get_global_id(0);
    int pos1 = pos / (box_size_y * box_size_x);
    int pos2 = pos % (box_size_y * box_size_x);

    int i_matrix = pos2 % box_size_x;
    int j_matrix = pos2 / box_size_x;

    int i_index = box_origin_x[pos1] + i_matrix;
    int j_index = box_origin_y[pos1] + j_matrix;

    u_index[pos] = u[pos1] + du_dx[pos1]*(i_matrix-box_size_x/2) + du_dy[pos1]*(j_matrix-box_size_y/2);
    v_index[pos] = v[pos1] + dv_dx[pos1]*(i_matrix-box_size_x/2) + dv_dy[pos1]*(j_matrix-box_size_y/2);

    temp = (i_index - u_index[pos]/2);
    i_frac_1[pos] = temp-(int)temp;
    i_index_1[pos] = (int)temp;

    temp = (i_index + u_index[pos]/2);
    i_frac_2[pos] = temp-(int)temp;
    i_index_2[pos] = (int)temp;

    temp =(j_index - v_index[pos]/2);
    j_frac_1[pos] = temp-(int)temp;
    j_index_1[pos] = (int)temp;

    temp = (j_index + v_index[pos]/2);
    j_frac_2[pos] = temp-(int)temp;
    j_index_2[pos] = (int)temp;
}
