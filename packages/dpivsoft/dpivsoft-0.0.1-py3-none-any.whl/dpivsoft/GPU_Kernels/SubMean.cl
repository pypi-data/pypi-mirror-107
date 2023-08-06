//Obtain mean value of each sub-image box

KERNEL void SubMean(GLOBAL_MEM float *gamma,
GLOBAL_MEM float2 *subImg,
GLOBAL_MEM int *data)
{
    int box_size_x = data[1];
    int box_size_y = data[2];
    int temp = 0;
    int idx;

    int pos = get_global_id(0);

    for (int j=0; j<box_size_y; j++)
    {
        for (int i=0; i<box_size_x; i++)
        {
            idx = pos*box_size_y*box_size_x+box_size_x*j+i;
            temp = temp+subImg[idx].x;
        }
    }
    gamma[pos] = temp/(box_size_y*box_size_x);
}
