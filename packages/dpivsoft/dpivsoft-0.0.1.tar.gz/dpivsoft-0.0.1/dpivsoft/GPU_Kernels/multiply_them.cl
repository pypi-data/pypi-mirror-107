//multiplication Kernel
KERNEL void multiply_them(
    GLOBAL_MEM ${ctype} *dest,
    GLOBAL_MEM ${ctype} *a,
    GLOBAL_MEM ${ctype} *b)
{
  const SIZE_T i = get_global_id(0);
  dest[i] = ${mul}(a[i], b[i]);
}
