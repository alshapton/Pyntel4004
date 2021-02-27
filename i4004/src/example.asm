/ Example program
        org     rom
        ldm     7
        xch     9
        fim     rp0     173
        jms     lbl
        fin     2
        jms     lbl
        jcn     ICT   lbl
        add     9 
        end
/ Sub-routine
lbl,    ldm     6
        fin     3
        bbl     6