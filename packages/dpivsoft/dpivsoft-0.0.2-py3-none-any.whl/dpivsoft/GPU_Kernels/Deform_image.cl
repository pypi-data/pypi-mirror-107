// Deform image

KERNEL void Deform_image(GLOBAL_MEM float2 *subImg,
GLOBAL_MEM float *img,
GLOBAL_MEM int *box_origin_x,
GLOBAL_MEM int *box_origin_y,
GLOBAL_MEM float *i_frac,
GLOBAL_MEM float *j_frac,
GLOBAL_MEM int *i_index,
GLOBAL_MEM int *j_index,
GLOBAL_MEM int *data)
{
    int width = data[0];
    int box_size_x = data[1];
    int box_size_y = data[2];
    int no_boxes_x = data[3];
    int no_boxes_y = data[4];
    int i = get_global_id(0);

    int pos = i/(box_size_y*box_size_x);
    int pos2 = i%(box_size_y*box_size_x);

    subImg[i].x = (1-j_frac[i])*(1-i_frac[i])*img[j_index[i]*width+i_index[i]]
        +(1-j_frac[i])*(i_frac[i])*img[(j_index[i])*width+i_index[i]+1]
        +(j_frac[i])*(1-i_frac[i])*img[(j_index[i]+1)*width+i_index[i]]
        +(j_frac[i])*(i_frac[i])*img[(j_index[i]+1)*width+i_index[i]+1];
}

