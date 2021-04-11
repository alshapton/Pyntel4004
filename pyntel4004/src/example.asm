/ Example program
/        org     rom
/        ldm     2
/        inc     1
/        nop
/        fim     rp0     180
/        src     rp0
/lbl,    ldm     15
/        wrm
/        wr0
/        wmp
/        end
/c2,     12
        fim 0p 224 
        src 0p
        ldm 1
        wrr
        jms com
        ld      2
        wpm
        ld      3 
        wpm
        fim 0p 224 
        src 0p
        clb
        wrr
        bbl 0
com,    fim 0p 0
        src 0p
        rd1
        xch 10
        rd2
        xch 11
        rd0
        fim 0
        src 0p
        wrr
        src 5p 
        bbl 0
fch,    jms com
        wpm
        fim 0p  224 
        src 0p 
        rdr
        xch 2
        inc 0
        rdr
        xch 3
        bbl 0
