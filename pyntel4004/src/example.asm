/ Example program
        org     rom
        ldm     14
        xch     9
        pin     1
        fim     rp0     173
        jms     lbl
        stc
        jcn     IC      lbl
/        isz     9       end 
        add     9 
end,    fin     2
        jun     last
/ Sub-routine
lbl,    ldm     6
        fin     3
        bbl     6
last,   end