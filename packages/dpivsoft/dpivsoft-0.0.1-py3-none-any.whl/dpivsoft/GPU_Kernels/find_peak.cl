//Find Peak Kernel
KERNEL void find_peak(GLOBAL_MEM float *v,
GLOBAL_MEM float *u,
GLOBAL_MEM float2 *input,
GLOBAL_MEM float *u_index,
GLOBAL_MEM float *v_index,
GLOBAL_MEM int *data)
{
    int box_size_x = data[1];
    int box_size_y = data[2];
    int window_x = data[5];
    int window_y = data[6];
    float peak_noise = data[7];

    int ds_x = (box_size_x-window_x)/2;
    int ds_y = (box_size_y-window_y)/2;

    int idx, idx1, idrow, idcol, idrow1, idcol1;
    int lm = box_size_x/16;
    float temp = 0, temp1 = 0;
    float epsilon_x = 0, epsilon_y = 0;
    float fit_peak_00, fit_peak_01, fit_peak_02, fit_peak_10, fit_peak_11;
    float fit_peak_12, fit_peak_20, fit_peak_21, fit_peak_22;

    int pos = get_global_id(0);

    //Find first peak
    for (int j=ds_y; j<box_size_y-ds_y; j++)
    {
        for (int i=ds_x; i<box_size_x-ds_x; i++)
        {
            idx = pos*box_size_y*box_size_x+box_size_x*j+i;
            if(input[idx].x>temp)
            {
                temp = input[idx].x;
                idrow = j;
                idcol = i;
            }
        }
    }

    idx = pos*box_size_y*box_size_x+box_size_x*idrow+idcol;
    temp = (input[idx].x+input[idx+1].x+input[idx-1].x+input[idx+box_size_x].x+
           input[idx+box_size_x+1].x+input[idx+box_size_x-1].x+input[idx-box_size_x].x+
           input[idx-box_size_x+1].x+input[idx-box_size_x-1].x);

    //Find second peak
    for (int j=ds_y; j<box_size_y-ds_y; j++)
    {
        for (int i=ds_x; i<box_size_x-ds_x; i++)
        {
            idx1 = pos*box_size_y*box_size_x+box_size_x*j+i;
            if(input[idx1].x>temp1 && abs(i-idcol1)>lm && abs(j-idcol1)>lm )
            {
                temp1 = input[idx1].x;
                idrow1 = j;
                idcol1 = i;
            }
        }
    }

    idx1 = pos*box_size_y*box_size_x+box_size_x*idrow1+idcol1;
    temp1 = (input[idx1].x+input[idx1+1].x+input[idx1-1].x+input[idx1+box_size_x].x+
              input[idx1+box_size_x+1].x+input[idx1+box_size_x-1].x+input[idx1-box_size_x].x+
              input[idx1-box_size_x+1].x+input[idx1-box_size_x-1].x);

    if (temp1 > temp)
    {
        float aux = temp;
        temp = temp1;
        temp1 = aux;
        idrow = idrow1;
        idcol = idcol1;
        idx = idx1;
    }

    float box_size_f_x = box_size_x;
    float box_size_f_y = box_size_y;
    float lim = 0.001;

    //bias correction based on Westerweel
    fit_peak_00 = max(lim,(input[idx-box_size_x-1].x/
                 (1 - sqrt(pow((idrow-box_size_f_y/2-1)/box_size_y,2))))/
                 (1-sqrt(pow((idcol-box_size_f_x/2-1)/box_size_x,2))));
    fit_peak_01 = max(lim,(input[idx-box_size_x].x/
                 (1 - sqrt(pow((idrow-box_size_f_y/2-1)/box_size_y,2))))/
                 (1-sqrt(pow((idcol-box_size_f_x/2)/box_size_x,2))));
    fit_peak_02 = max(lim,(input[idx-box_size_x+1].x/
                 (1 - sqrt(pow((idrow-box_size_f_y/2-1)/box_size_y,2))))/
                 (1-sqrt(pow((idcol-box_size_f_x/2+1)/box_size_x,2))));
    fit_peak_10 = max(lim,(input[idx-1].x/
                  (1 - sqrt(pow((idrow-box_size_f_y/2)/box_size_y,2))))/
                  (1-sqrt(pow((idcol-box_size_f_x/2-1)/box_size_x,2))));
    fit_peak_11 = max(lim,(input[idx].x/
                  (1 - sqrt(pow((idrow-box_size_f_y/2)/box_size_y,2))))/
                  (1-sqrt(pow((idcol-box_size_f_x/2)/box_size_x,2))));
    fit_peak_12 = max(lim,(input[idx+1].x/
                  (1 - sqrt(pow((idrow-box_size_f_y/2)/box_size_y,2))))/
                  (1-sqrt(pow((idcol-box_size_f_x/2+1)/box_size_x,2))));
    fit_peak_20 = max(lim,(input[idx+box_size_x-1].x/
                  (1 - sqrt(pow((idrow-box_size_f_y/2+1)/box_size_y,2))))/
                  (1-sqrt(pow((idcol-box_size_f_x/2-1)/box_size_x,2))));
    fit_peak_21 = max(lim,(input[idx+box_size_x].x/
                  (1 - sqrt(pow((idrow-box_size_f_y/2+1)/box_size_y,2))))/
                  (1-sqrt(pow((idcol-box_size_f_x/2)/box_size_x,2))));
    fit_peak_22 = max(lim,(input[idx+box_size_x+1].x/
                  (1 - sqrt(pow((idrow-box_size_f_y/2+1)/box_size_y,2))))/
                  (1-sqrt(pow((idcol-box_size_f_x/2+1)/box_size_x,2))));

    //Check noise to peak ratio
    if (temp/temp1 < peak_noise){
        fit_peak_00 = lim;
        fit_peak_01 = lim;
        fit_peak_02 = lim;
        fit_peak_10 = lim;
        fit_peak_11 = lim;
        fit_peak_12 = lim;
        fit_peak_20 = lim;
        fit_peak_21 = lim;
        fit_peak_22 = lim;
    }

    //Sub-pixel accuracy with gaussian estimator
    if (fit_peak_11 < fit_peak_10 && fit_peak_11 < fit_peak_12)
    {
        epsilon_x = 0;
        idcol = box_size_y/2;
    }
    else
    {
        if (fit_peak_10 > 0 && fit_peak_11 > 0 && fit_peak_12 > 0 &&
                       (log(fit_peak_10)+log(fit_peak_12)-2*log(fit_peak_11)) != 0)
        {
            epsilon_x = (0.5*(log(fit_peak_10)-log(fit_peak_12))/(log(fit_peak_10)+
                log(fit_peak_12)-2*log(fit_peak_11)));
        }
        else
        {
            epsilon_x = 0;
        }
    }

    if (fit_peak_11 < fit_peak_01 && fit_peak_11 < fit_peak_21)
    {
        epsilon_y = 0;
        idrow = box_size_x/2;
    }
    else
    {
        if (fit_peak_01 > 0 && fit_peak_11 > 0 && fit_peak_21 > 0 &&
                        (log(fit_peak_01)+log(fit_peak_21)-2*log(fit_peak_11)) != 0)
        {
            epsilon_y = (0.5*(log(fit_peak_01)-log(fit_peak_21))/(log(fit_peak_01)+
                        log(fit_peak_21)-2*log(fit_peak_11)));
        }
        else
        {
            epsilon_y = 0;
        }
    }

    v[pos] = (v_index[pos*box_size_y*box_size_x+idrow*box_size_x+idcol] +
             idrow + epsilon_y - box_size_y/2);
    u[pos] = (u_index[pos*box_size_y*box_size_x+idrow*box_size_x+idcol] +
             idcol + epsilon_x - box_size_x/2);
}
