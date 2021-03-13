/ Example program
        org     rom
        ldm     4
        dcl
        fim     rp0     180
        jun     last
        xch     9
        pin     1
        src     6
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