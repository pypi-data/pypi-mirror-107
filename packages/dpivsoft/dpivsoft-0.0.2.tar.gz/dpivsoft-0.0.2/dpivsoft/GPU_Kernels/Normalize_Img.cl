//Normalize and center in 0 the subimages

KERNEL void Normalize(GLOBAL_MEM float2 *subImg,
GLOBAL_MEM float *gamma,
GLOBAL_MEM int *data)
{
    int box_size_x = data[1];
    int box_size_y = data[2];

    int i = get_global_id(0);
    int pos = i/(box_size_x*box_size_y);

    subImg[i].x = subImg[i].x - subImg[i].x / gamma[pos];
 }
