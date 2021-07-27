; Example program
.target  "4004"
.setting "OutputTxtValueFormat" , "{0:x02}"
.setting "OutputTxtValueSeparator" , ","
	ldm     2
        inc     1
        nop
        fim     0,     180
        src     0
Lbl     ldm     15
        wrm
        wr0
        wmp
lb2     bbl  1
