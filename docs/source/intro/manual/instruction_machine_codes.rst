.. _instruction_machine_codes:

Instruction Machine Codes
=========================


.. include:: ../../global.rst
In order to help the programmer examine memory when debugging programs, this list provides the assembly language instruction represented by each of the 256 possible instruction code bytes.
Where an instruction occupies two bytes, only the first (code) byte is given.

.. list-table:: Instruction Machine Codes
   :header-rows: 1

   * - Decimal
     - Octal
     - Hex
     - Mnemonic
     - Parameter
     - Comment
   * - 0
     - 0
     - 0
     - :ref:`NOP <hardware-machine-nop>`
     - 
     - 
   * - 1
     - 1
     - 1
     - Not Used 
     - 
     - 
   * - 2
     - 2
     - 2
     - Not Used 
     - 
     - 
   * - 3
     - 3
     - 3
     - Not Used 
     - 
     - 
   * - 4
     - 4
     - 4
     - Not Used 
     - 
     - 
   * - 5
     - 5
     - 5
     - Not Used 
     - 
     - 
   * - 6
     - 6
     - 6
     - Not Used 
     - 
     - 
   * - 7
     - 7
     - 7
     - Not Used 
     - 
     - 
   * - 8
     - 10
     - 8
     - Not Used 
     - 
     - 
   * - 9
     - 11
     - 9
     - Not Used 
     - 
     - 
   * - 10
     - 12
     - A
     - Not Used 
     - 
     - 
   * - 11
     - 13
     - B
     - Not Used 
     - 
     - 
   * - 12
     - 14
     - C
     - Not Used 
     - 
     - 
   * - 13
     - 15
     - D
     - Not Used 
     - 
     - 
   * - 14
     - 16
     - E
     - Not Used 
     - 
     - 
   * - 15
     - 17
     - F
     - Not Used 
     - 
     - 
   * - 16
     - 20
     - 10
     - :ref:`JCN <hardware-machine-jcn>`
     - 0
     - CN=0
   * - 17
     - 21
     - 11
     - :ref:`JCN <hardware-machine-jcn>`
     - 1
     - CN=1
   * - 18
     - 22
     - 12
     - :ref:`JCN <hardware-machine-jcn>`
     - 2
     - CN=2
   * - 19
     - 23
     - 13
     - :ref:`JCN <hardware-machine-jcn>`
     - 3
     - CN=3
   * - 20
     - 24
     - 14
     - :ref:`JCN <hardware-machine-jcn>`
     - 4
     - CN=4
   * - 21
     - 25
     - 15
     - :ref:`JCN <hardware-machine-jcn>`
     - 5
     - CN=5
   * - 22
     - 26
     - 16
     - :ref:`JCN <hardware-machine-jcn>`
     - 6
     - CN=6
   * - 23
     - 27
     - 17
     - :ref:`JCN <hardware-machine-jcn>`
     - 7
     - CN=7
   * - 24
     - 30
     - 18
     - :ref:`JCN <hardware-machine-jcn>`
     - 8
     - CN=8
   * - 25
     - 31
     - 19
     - :ref:`JCN <hardware-machine-jcn>`
     - 9
     - CN=9
   * - 26
     - 32
     - 1A
     - :ref:`JCN <hardware-machine-jcn>`
     - 10
     - CN=10
   * - 27
     - 33
     - 1B
     - :ref:`JCN <hardware-machine-jcn>`
     - 11
     - CN=11
   * - 28
     - 34
     - 1C
     - :ref:`JCN <hardware-machine-jcn>`
     - 12
     - CN=12
   * - 29
     - 35
     - 1D
     - :ref:`JCN <hardware-machine-jcn>`
     - 13
     - CN=13
   * - 30
     - 36
     - 1E
     - :ref:`JCN <hardware-machine-jcn>`
     - 14
     - CN=14
   * - 31
     - 37
     - 1F
     - :ref:`JCN <hardware-machine-jcn>`
     - 15
     - CN=15
   * - 32
     - 40
     - 20
     - :ref:`FIM <hardware-machine-fim>`
     - 0P
     - 
   * - 33
     - 41
     - 21
     - :ref:`SRC <hardware-machine-src>`
     - 0
     - 
   * - 34
     - 42
     - 22
     - :ref:`FIM <hardware-machine-fim>`
     - 1P
     - 
   * - 35
     - 43
     - 23
     - :ref:`SRC <hardware-machine-src>`
     - 1
     - 
   * - 36
     - 44
     - 24
     - :ref:`FIM <hardware-machine-fim>`
     - 2P
     - 
   * - 37
     - 45
     - 25
     - :ref:`SRC <hardware-machine-src>`
     - 2
     - 
   * - 38
     - 46
     - 26
     - :ref:`FIM <hardware-machine-fim>`
     - 3P
     - 
   * - 39
     - 47
     - 27
     - :ref:`SRC <hardware-machine-src>`
     - 3
     - 
   * - 40
     - 50
     - 28
     - :ref:`FIM <hardware-machine-fim>`
     - 4P
     - 
   * - 41
     - 51
     - 29
     - :ref:`SRC <hardware-machine-src>`
     - 4
     - 
   * - 42
     - 52
     - 2A
     - :ref:`FIM <hardware-machine-fim>`
     - 5P
     - 
   * - 43
     - 53
     - 2B
     - :ref:`SRC <hardware-machine-src>`
     - 5
     - 
   * - 44
     - 54
     - 2C
     - :ref:`FIM <hardware-machine-fim>`
     - 6P
     - 
   * - 45
     - 55
     - 2D
     - :ref:`SRC <hardware-machine-src>`
     - 6
     - 
   * - 46
     - 56
     - 2E
     - :ref:`FIM <hardware-machine-fim>`
     - 7P
     - 
   * - 47
     - 57
     - 2F
     - :ref:`SRC <hardware-machine-src>`
     - 7
     - 
   * - 48
     - 60
     - 30
     - :ref:`FIN <hardware-machine-fin>`
     - 0
     - 
   * - 49
     - 61
     - 31
     - :ref:`JIN <hardware-machine-jin>`
     - 0
     - 
   * - 50
     - 62
     - 32
     - :ref:`FIN <hardware-machine-fin>`
     - 1
     - 
   * - 51
     - 63
     - 33
     - :ref:`JIN <hardware-machine-jin>`
     - 1
     - 
   * - 52
     - 64
     - 34
     - :ref:`FIN <hardware-machine-fin>`
     - 2
     - 
   * - 53
     - 65
     - 35
     - :ref:`JIN <hardware-machine-jin>`
     - 2
     - 
   * - 54
     - 66
     - 36
     - :ref:`FIN <hardware-machine-fin>`
     - 3
     - 
   * - 55
     - 67
     - 37
     - :ref:`JIN <hardware-machine-jin>`
     - 3
     - 
   * - 56
     - 70
     - 38
     - :ref:`FIN <hardware-machine-fin>`
     - 4
     - 
   * - 57
     - 71
     - 39
     - :ref:`JIN <hardware-machine-jin>`
     - 4
     - 
   * - 58
     - 72
     - 3A
     - :ref:`FIN <hardware-machine-fin>`
     - 5
     - 
   * - 59
     - 73
     - 3B
     - :ref:`JIN <hardware-machine-jin>`
     - 5
     - 
   * - 60
     - 74
     - 3C
     - :ref:`FIN <hardware-machine-fin>`
     - 6
     - 
   * - 61
     - 75
     - 3D
     - :ref:`JIN <hardware-machine-jin>`
     - 6
     - 
   * - 62
     - 76
     - 3E
     - :ref:`FIN <hardware-machine-fin>`
     - 7
     - 
   * - 63
     - 77
     - 3F
     - :ref:`JIN <hardware-machine-jin>`
     - 7
     - 
   * - 64
     - 100
     - 40
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 65
     - 101
     - 41
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 66
     - 102
     - 42
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 67
     - 103
     - 43
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 68
     - 104
     - 44
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 69
     - 105
     - 45
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 70
     - 106
     - 46
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 71
     - 107
     - 47
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 72
     - 110
     - 48
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 73
     - 111
     - 49
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 74
     - 112
     - 4A
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 75
     - 113
     - 4B
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 76
     - 114
     - 4C
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 77
     - 115
     - 4D
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 78
     - 116
     - 4E
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 79
     - 117
     - 4F
     - :ref:`JUN <hardware-machine-jun>`
     - 
     - |psi|
   * - 80
     - 120
     - 50
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 81
     - 121
     - 51
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 82
     - 122
     - 52
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 83
     - 123
     - 53
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 84
     - 124
     - 54
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 85
     - 125
     - 55
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 86
     - 126
     - 56
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 87
     - 127
     - 57
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 88
     - 130
     - 58
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 89
     - 131
     - 59
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 90
     - 132
     - 5A
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 91
     - 133
     - 5B
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 92
     - 134
     - 5C
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 93
     - 135
     - 5D
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 94
     - 136
     - 5E
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 95
     - 137
     - 5F
     - :ref:`JMS <hardware-machine-jms>`
     - 
     - |psi|
   * - 96
     - 140
     - 60
     - :ref:`INC <hardware-machine-inc>`
     - 0
     - 
   * - 97
     - 141
     - 61
     - :ref:`INC <hardware-machine-inc>`
     - 1
     - 
   * - 98
     - 142
     - 62
     - :ref:`INC <hardware-machine-inc>`
     - 2
     - 
   * - 99
     - 143
     - 63
     - :ref:`INC <hardware-machine-inc>`
     - 3
     - 
   * - 100
     - 144
     - 64
     - :ref:`INC <hardware-machine-inc>`
     - 4
     - 
   * - 101
     - 145
     - 65
     - :ref:`INC <hardware-machine-inc>`
     - 5
     - 
   * - 102
     - 146
     - 66
     - :ref:`INC <hardware-machine-inc>`
     - 6
     - 
   * - 103
     - 147
     - 67
     - :ref:`INC <hardware-machine-inc>`
     - 7
     - 
   * - 104
     - 150
     - 68
     - :ref:`INC <hardware-machine-inc>`
     - 8
     - 
   * - 105
     - 151
     - 69
     - :ref:`INC <hardware-machine-inc>`
     - 9
     - 
   * - 106
     - 152
     - 6A
     - :ref:`INC <hardware-machine-inc>`
     - 10
     - 
   * - 107
     - 153
     - 6B
     - :ref:`INC <hardware-machine-inc>`
     - 11
     - 
   * - 108
     - 154
     - 6C
     - :ref:`INC <hardware-machine-inc>`
     - 12
     - 
   * - 109
     - 155
     - 6D
     - :ref:`INC <hardware-machine-inc>`
     - 13
     - 
   * - 110
     - 156
     - 6E
     - :ref:`INC <hardware-machine-inc>`
     - 14
     - 
   * - 111
     - 157
     - 6F
     - :ref:`INC <hardware-machine-inc>`
     - 15
     - 
   * - 112
     - 160
     - 70
     - :ref:`ISZ <hardware-machine-isz>`
     - 0
     - 
   * - 113
     - 161
     - 71
     - :ref:`ISZ <hardware-machine-isz>`
     - 1
     - 
   * - 114
     - 162
     - 72
     - :ref:`ISZ <hardware-machine-isz>`
     - 2
     - 
   * - 115
     - 163
     - 73
     - :ref:`ISZ <hardware-machine-isz>`
     - 3
     - 
   * - 116
     - 164
     - 74
     - :ref:`ISZ <hardware-machine-isz>`
     - 4
     - 
   * - 117
     - 165
     - 75
     - :ref:`ISZ <hardware-machine-isz>`
     - 5
     - 
   * - 118
     - 166
     - 76
     - :ref:`ISZ <hardware-machine-isz>`
     - 6
     - 
   * - 119
     - 167
     - 77
     - :ref:`ISZ <hardware-machine-isz>`
     - 7
     - 
   * - 120
     - 170
     - 78
     - :ref:`ISZ <hardware-machine-isz>`
     - 8
     - 
   * - 121
     - 171
     - 79
     - :ref:`ISZ <hardware-machine-isz>`
     - 9
     - 
   * - 122
     - 172
     - 7A
     - :ref:`ISZ <hardware-machine-isz>`
     - 10
     - 
   * - 123
     - 173
     - 7B
     - :ref:`ISZ <hardware-machine-isz>`
     - 11
     - 
   * - 124
     - 174
     - 7C
     - :ref:`ISZ <hardware-machine-isz>`
     - 12
     - 
   * - 125
     - 175
     - 7D
     - :ref:`ISZ <hardware-machine-isz>`
     - 13
     - 
   * - 126
     - 176
     - 7E
     - :ref:`ISZ <hardware-machine-isz>`
     - 14
     - 
   * - 127
     - 177
     - 7F
     - :ref:`ISZ <hardware-machine-isz>`
     - 15
     - 
   * - 128
     - 200
     - 80
     - :ref:`ADD <hardware-machine-add>`
     - 0
     - 
   * - 129
     - 201
     - 81
     - :ref:`ADD <hardware-machine-add>`
     - 1
     - 
   * - 130
     - 202
     - 82
     - :ref:`ADD <hardware-machine-add>`
     - 2
     - 
   * - 131
     - 203
     - 83
     - :ref:`ADD <hardware-machine-add>`
     - 3
     - 
   * - 132
     - 204
     - 84
     - :ref:`ADD <hardware-machine-add>`
     - 4
     - 
   * - 133
     - 205
     - 85
     - :ref:`ADD <hardware-machine-add>`
     - 5
     - 
   * - 134
     - 206
     - 86
     - :ref:`ADD <hardware-machine-add>`
     - 6
     - 
   * - 135
     - 207
     - 87
     - :ref:`ADD <hardware-machine-add>`
     - 7
     - 
   * - 136
     - 210
     - 88
     - :ref:`ADD <hardware-machine-add>`
     - 8
     - 
   * - 137
     - 211
     - 89
     - :ref:`ADD <hardware-machine-add>`
     - 9
     - 
   * - 138
     - 212
     - 8A
     - :ref:`ADD <hardware-machine-add>`
     - 10
     - 
   * - 139
     - 213
     - 8B
     - :ref:`ADD <hardware-machine-add>`
     - 11
     - 
   * - 140
     - 214
     - 8C
     - :ref:`ADD <hardware-machine-add>`
     - 12
     - 
   * - 141
     - 215
     - 8D
     - :ref:`ADD <hardware-machine-add>`
     - 13
     - 
   * - 142
     - 216
     - 8E
     - :ref:`ADD <hardware-machine-add>`
     - 14
     - 
   * - 143
     - 217
     - 8F
     - :ref:`ADD <hardware-machine-add>`
     - 15
     - 
   * - 144
     - 220
     - 90
     - :ref:`SUB <hardware-machine-sub>`
     - 0
     - 
   * - 145
     - 221
     - 91
     - :ref:`SUB <hardware-machine-sub>`
     - 1
     - 
   * - 146
     - 222
     - 92
     - :ref:`SUB <hardware-machine-sub>`
     - 2
     - 
   * - 147
     - 223
     - 93
     - :ref:`SUB <hardware-machine-sub>`
     - 3
     - 
   * - 148
     - 224
     - 94
     - :ref:`SUB <hardware-machine-sub>`
     - 4
     - 
   * - 149
     - 225
     - 95
     - :ref:`SUB <hardware-machine-sub>`
     - 5
     - 
   * - 150
     - 226
     - 96
     - :ref:`SUB <hardware-machine-sub>`
     - 6
     - 
   * - 151
     - 227
     - 97
     - :ref:`SUB <hardware-machine-sub>`
     - 7
     - 
   * - 152
     - 230
     - 98
     - :ref:`SUB <hardware-machine-sub>`
     - 8
     - 
   * - 153
     - 231
     - 99
     - :ref:`SUB <hardware-machine-sub>`
     - 9
     - 
   * - 154
     - 232
     - 9A
     - :ref:`SUB <hardware-machine-sub>`
     - 10
     - 
   * - 155
     - 233
     - 9B
     - :ref:`SUB <hardware-machine-sub>`
     - 11
     - 
   * - 156
     - 234
     - 9C
     - :ref:`SUB <hardware-machine-sub>`
     - 12
     - 
   * - 157
     - 235
     - 9D
     - :ref:`SUB <hardware-machine-sub>`
     - 13
     - 
   * - 158
     - 236
     - 9E
     - :ref:`SUB <hardware-machine-sub>`
     - 14
     - 
   * - 159
     - 237
     - 9F
     - :ref:`SUB <hardware-machine-sub>`
     - 15
     - 
   * - 160
     - 240
     - A0
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 161
     - 241
     - A1
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 162
     - 242
     - A2
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 163
     - 243
     - A3
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 164
     - 244
     - A4
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 165
     - 245
     - A5
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 166
     - 246
     - A6
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 167
     - 247
     - A7
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 168
     - 250
     - A8
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 169
     - 251
     - A9
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 170
     - 252
     - AA
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 171
     - 253
     - AB
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 172
     - 254
     - AC
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 173
     - 255
     - AD
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 174
     - 256
     - AE
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 175
     - 257
     - AF
     - :ref:`LD  <hardware-machine-ld>`
     - 
     - 
   * - 176
     - 260
     - B0
     - :ref:`XCH <hardware-machine-xch>`
     - 0
     - 
   * - 177
     - 261
     - B1
     - :ref:`XCH <hardware-machine-xch>`
     - 1
     - 
   * - 178
     - 262
     - B2
     - :ref:`XCH <hardware-machine-xch>`
     - 2
     - 
   * - 179
     - 263
     - B3
     - :ref:`XCH <hardware-machine-xch>`
     - 3
     - 
   * - 180
     - 264
     - B4
     - :ref:`XCH <hardware-machine-xch>`
     - 4
     - 
   * - 181
     - 265
     - B5
     - :ref:`XCH <hardware-machine-xch>`
     - 5
     - 
   * - 182
     - 266
     - B6
     - :ref:`XCH <hardware-machine-xch>`
     - 6
     - 
   * - 183
     - 267
     - B7
     - :ref:`XCH <hardware-machine-xch>`
     - 7
     - 
   * - 184
     - 270
     - B8
     - :ref:`XCH <hardware-machine-xch>`
     - 8
     - 
   * - 185
     - 271
     - B9
     - :ref:`XCH <hardware-machine-xch>`
     - 9
     - 
   * - 186
     - 272
     - BA
     - :ref:`XCH <hardware-machine-xch>`
     - 10
     - 
   * - 187
     - 273
     - BB
     - :ref:`XCH <hardware-machine-xch>`
     - 11
     - 
   * - 188
     - 274
     - BC
     - :ref:`XCH <hardware-machine-xch>`
     - 12
     - 
   * - 189
     - 275
     - BD
     - :ref:`XCH <hardware-machine-xch>`
     - 13
     - 
   * - 190
     - 276
     - BE
     - :ref:`XCH <hardware-machine-xch>`
     - 14
     - 
   * - 191
     - 277
     - BF
     - :ref:`XCH <hardware-machine-xch>`
     - 15
     - 
   * - 192
     - 300
     - C0
     - :ref:`BBL <hardware-machine-bbl>`
     - 0
     - 
   * - 193
     - 301
     - C1
     - :ref:`BBL <hardware-machine-bbl>`
     - 1
     - 
   * - 194
     - 302
     - C2
     - :ref:`BBL <hardware-machine-bbl>`
     - 2
     - 
   * - 195
     - 303
     - C3
     - :ref:`BBL <hardware-machine-bbl>`
     - 3
     - 
   * - 196
     - 304
     - C4
     - :ref:`BBL <hardware-machine-bbl>`
     - 4
     - 
   * - 197
     - 305
     - C5
     - :ref:`BBL <hardware-machine-bbl>`
     - 5
     - 
   * - 198
     - 306
     - C6
     - :ref:`BBL <hardware-machine-bbl>`
     - 6
     - 
   * - 199
     - 307
     - C7
     - :ref:`BBL <hardware-machine-bbl>`
     - 7
     - 
   * - 200
     - 310
     - C8
     - :ref:`BBL <hardware-machine-bbl>`
     - 8
     - 
   * - 201
     - 311
     - C9
     - :ref:`BBL <hardware-machine-bbl>`
     - 9
     - 
   * - 202
     - 312
     - CA
     - :ref:`BBL <hardware-machine-bbl>`
     - 10
     - 
   * - 203
     - 313
     - CB
     - :ref:`BBL <hardware-machine-bbl>`
     - 11
     - 
   * - 204
     - 314
     - CC
     - :ref:`BBL <hardware-machine-bbl>`
     - 12
     - 
   * - 205
     - 315
     - CD
     - :ref:`BBL <hardware-machine-bbl>`
     - 13
     - 
   * - 206
     - 316
     - CE
     - :ref:`BBL <hardware-machine-bbl>`
     - 14
     - 
   * - 207
     - 317
     - CF
     - :ref:`BBL <hardware-machine-bbl>`
     - 15
     - 
   * - 208
     - 320
     - D0
     - :ref:`LDM <hardware-machine-ldm>`
     - 0
     - 
   * - 209
     - 321
     - D1
     - :ref:`LDM <hardware-machine-ldm>`
     - 1
     - 
   * - 210
     - 322
     - D2
     - :ref:`LDM <hardware-machine-ldm>`
     - 2
     - 
   * - 211
     - 323
     - D3
     - :ref:`LDM <hardware-machine-ldm>`
     - 3
     - 
   * - 212
     - 324
     - D4
     - :ref:`LDM <hardware-machine-ldm>`
     - 4
     - 
   * - 213
     - 325
     - D5
     - :ref:`LDM <hardware-machine-ldm>`
     - 5
     - 
   * - 214
     - 326
     - D6
     - :ref:`LDM <hardware-machine-ldm>`
     - 6
     - 
   * - 215
     - 327
     - D7
     - :ref:`LDM <hardware-machine-ldm>`
     - 7
     - 
   * - 216
     - 330
     - D8
     - :ref:`LDM <hardware-machine-ldm>`
     - 8
     - 
   * - 217
     - 331
     - D9
     - :ref:`LDM <hardware-machine-ldm>`
     - 9
     - 
   * - 218
     - 332
     - DA
     - :ref:`LDM <hardware-machine-ldm>`
     - 10
     - 
   * - 219
     - 333
     - DB
     - :ref:`LDM <hardware-machine-ldm>`
     - 11
     - 
   * - 220
     - 334
     - DC
     - :ref:`LDM <hardware-machine-ldm>`
     - 12
     - 
   * - 221
     - 335
     - DD
     - :ref:`LDM <hardware-machine-ldm>`
     - 13
     - 
   * - 222
     - 336
     - DE
     - :ref:`LDM <hardware-machine-ldm>`
     - 14
     - 
   * - 223
     - 337
     - DF
     - :ref:`LDM <hardware-machine-ldm>`
     - 15
     - 
   * - 224
     - 340
     - E0
     - :ref:`WRM <hardware-machine-wrm>`
     - 
     - 
   * - 225
     - 341
     - E1
     - :ref:`WMP <hardware-machine-wmp>`
     - 
     - 
   * - 226
     - 342
     - E2
     - :ref:`WRR <hardware-machine-wrr>`
     - 
     - 
   * - 227
     - 343
     - E3
     - :ref:`WPM <hardware-machine-wpm>`
     - 
     - 
   * - 228
     - 344
     - E4
     - :ref:`WR0 <hardware-machine-wrn>`
     - 
     - 
   * - 229
     - 345
     - E5
     - :ref:`WR1 <hardware-machine-wrn>`
     - 
     - 
   * - 230
     - 346
     - E6
     - :ref:`WR2 <hardware-machine-wrn>`
     - 
     - 
   * - 231
     - 347
     - E7
     - :ref:`WR3 <hardware-machine-wrn>`
     - 
     - 
   * - 232
     - 350
     - E8
     - :ref:`SBM <hardware-machine-sbm>`
     - 
     - 
   * - 233
     - 351
     - E9
     - :ref:`RDM <hardware-machine-rdm>`
     - 
     - 
   * - 234
     - 352
     - EA
     - :ref:`RDR <hardware-machine-rdr>`
     - 
     - 
   * - 235
     - 353
     - EB
     - :ref:`ADM <hardware-machine-adm>`
     - 
     - 
   * - 236
     - 354
     - EC
     - :ref:`RD0 <hardware-machine-rdn>`
     - 
     - 
   * - 237
     - 355
     - ED
     - :ref:`RD1 <hardware-machine-rdn>`
     - 
     - 
   * - 238
     - 356
     - EE
     - :ref:`RD2 <hardware-machine-rdn>`
     - 
     - 
   * - 239
     - 357
     - EF
     - :ref:`RD3 <hardware-machine-rdn>`
     - 
     - 
   * - 240
     - 360
     - F0
     - :ref:`CLB <hardware-machine-clb>`
     - 
     - 
   * - 241
     - 361
     - F1
     - :ref:`CLC <hardware-machine-clc>`
     - 
     - 
   * - 242
     - 362
     - F2
     - :ref:`IAC <hardware-machine-iac>`
     - 
     - 
   * - 243
     - 363
     - F3
     - :ref:`CMC <hardware-machine-cmc>`
     - 
     - 
   * - 244
     - 364
     - F4
     - :ref:`CMA <hardware-machine-cma>`
     - 
     - 
   * - 245
     - 365
     - F5
     - :ref:`RAL <hardware-machine-ral>`
     - 
     - 
   * - 246
     - 366
     - F6
     - :ref:`RAR <hardware-machine-rar>`
     - 
     - 
   * - 247
     - 367
     - F7
     - :ref:`TCC <hardware-machine-tcc>`
     - 
     - 
   * - 248
     - 370
     - F8
     - :ref:`DAC <hardware-machine-dac>`
     - 
     - 
   * - 249
     - 371
     - F9
     - :ref:`TCS <hardware-machine-tcs>`
     - 
     - 
   * - 250
     - 372
     - FA
     - :ref:`STC <hardware-machine-stc>`
     - 
     - 
   * - 251
     - 373
     - FB
     - :ref:`DAA <hardware-machine-daa>`
     - 
     - 
   * - 252
     - 374
     - FC
     - :ref:`KBP <hardware-machine-kbp>`
     - 
     - 
   * - 253
     - 375
     - FD
     - :ref:`DCL <hardware-machine-dcl>`
     - 
     - 
   * - 254
     - 376
     - FE
     - Not Used 
     - 
     - 
   * - 255
     - 377
     - FF
     - Not Used 
     - 
     - 

|br|

 |psi| Second hexadecimal digit is part of the jump address.

