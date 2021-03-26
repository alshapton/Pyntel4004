/ Example program
        org     rom
        ldm     2
        inc     16
        nop
        fim     rp0     180
        src     rp0
lbl,    ldm     15
        wrm
        wr0
        wmp
        end
c2,     12