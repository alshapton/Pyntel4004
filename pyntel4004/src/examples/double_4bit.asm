/ Double i.e. multiple by 2 - a 4 bit digit
/ inputs : r0 = 4 bit digit
/ outputs: rp7 = 8 bit digit (r0 *2)
        org     rom
        clb
        ldm     15
        ral
        xch     8
        jcn     2    oflow
        ldm     1
        jun     noflow
oflow,  ldm     1
        xch     9
noflow, nop
        end