Additional sources can be specified for the docker container.
These sources should be placed in `/etc/debpic/sources.list.d/`, their suffix should be `.sources` and they should conform to deb822 format.

By default debpic will use `/etc/debpic/sources.list.d/default.sources` if it exists. If the `-s/--sources` argument is supplied (e.g `debpic -s unstable`) then debpic will select `/etc/debpic/sources.list.d/unstable.sources` if it exists.

An example deb822 sources:  
(Note: The leading space before each line in the pgp key is necessary)
```
Enabled: Yes
Types: deb
URIs: http://mypackage.com/Tools/Debian11/
Suites: ./
Signed-By:
 -----BEGIN PGP PUBLIC KEY BLOCK-----
 .
 
 xo0EZVtLEQEEAMbNhZ7gHs5NpPTV0ptP3IskNFdK5dNK8TvOk2lEFRMfFa0UROr5
 HJhUjNsxSd9yhBcygQOaxYw994QZdpiikw3zNscj6M8OMuSEvHTqiWB80YQZFzYZ
 WznPyM9Pxt8mprm/Qvj2iTJa8I+cxfFA2+sGxR+9rnMdo79KkiNnuSONABEBAAHN
 IXNkYXNkIChhc2Rhc2QpIDxzYWRhc2RAYXNkc2EuY29tPsKtBBMBCgAXBQJlW0sR
 AhsvAwsJBwMVCggCHgECF4AACgkQnPv56vxHv6aanAQAgCMlq9IbHmrcxKmqh04G
 P2xf7lII2RK8heEmmaiWHwBqYvej+LQzCNBsumeU3xX113RmqcAWXgi1enQLpDeC
 eMdJYrz1qgGs5eOgfOgwDI4DT9++Wqhkbd7z9PxyHEHABfKYBgwOtxWV5vgzKm6r
 U/RQEGtez8NN2O63aEd7Tw7OjQRlW0sRAQQA9qHH11VASw2jhmeCMWfj8IFBpqY/
 pl7E9z6gPLKg7ivbqLcIolZsQeosUaVukAcLAT7z7hv9rgFdzjsU8rxK4Jd7ODNx
 p518cvV5e7JgrpsxWsj4P7muitkOvt0r9cHvLOtH/RXpgkFjqjf86Ww3icgt5Ve7
 7FtTJeJ7/0+IsaUAEQEAAcLAgwQYAQoADwUCZVtLEQUJDwmcAAIbLgCoCRCc+/nq
 /Ee/pp0gBBkBCgAGBQJlW0sRAAoJEHxR3NDh0Gx1bAEEAJkqDHPJai3hoEzfbZw8
 ieHq5YGxB5M7y7gvXFW1CdPLSjzyZvPt0c0qL0B3CI+Mb7qSvHYZldv+oMFppKM/
 IKckzit2asLwhgPx3lBAAqfHJGPDVjXQP8Ab8wY/1ZT3KhHoWM9nhikMfGfpP6bj
 fTC7TbzMRNbb3HY/Z7M2Ytg8QFcD+wQQBpchv+BTJ+7SWXipMqDtrc0+LZz7fj5M
 FmR/MM/lK0kqYvxhGQ338LxgHtLpl9QEb7xlZ9SV/aDu41Qdpd6ZMmcMgWQW4SJt
 jDyDvxNge+0gVhRV75++TivIPTa6IddSKwzjJZwCjS2A7tV5X/oDSGlH2JrX6c8A
 umERn63Xzo0EZVtLEQEEAKxXjXapQ1IBgGoVwIoXbUjB5WT8H5WrmqnBgs+var+M
 CTfZppToDHIA/XtM5e1Q65Ed0wx5KORF76e8FZf96Yuu8bSflYYdLAiEryiPg7yA
 fwmvXwxqc1VunwhvssgWh3iz/XYR/PFy0iCv1+A7G6oU1R+Z5uAqhwmwvW2i/SLj
 ABEBAAHCwIMEGAEKAA8FAmVbSxEFCQ8JnAACGy4AqAkQnPv56vxHv6adIAQZAQoA
 BgUCZVtLEQAKCRDB4TYgVFUM5m8eBACF92lpQyxkAsXazfeunLsZJFgNDAwaGt/M
 qwiJsq55cIe8RhClcQht6++OGx4/NBCxhV65J2S6gefp4ar4CYCTQ4aVkZro/zHg
 sSVO48rvV+n7BzGBDbdBwJOQpv6DN6TXn/CqfE+XbkEcdht5lI2skRiQudgxwUzJ
 6ej9gFJ4JXqFA/94LvVIYHZ022nXcTwy1Q8PIkrnvBmwr5UtQDUe3QwacG/SiB4V
 WmGB+3B5FC0c55lR5/ANHcnQjEc9Ksi4N/pajAWMaMp7cUCc7jK4xSJ+f5VFhkwD
 fE9fqzZmyIqlDZIQlHWEZwUucQEaySfR5+ajXyOXMPQxX2gONlU3/HpbYA==
 =a74y
-----END PGP PUBLIC KEY BLOCK-----

Enabled: Yes
Types: deb
URIs: http://repository.spotify.com
Suites: stable
Components: non-free
Signed-By:
 -----BEGIN PGP PUBLIC KEY BLOCK-----
 .
 mQINBGF5YIABEACnop+0P287u+2dzExoGpe109KHHd1eaj/ULDQZz0A47qJYaOld
 pGqsRq6EUbzrVxGaAsSDfCwlQ4hutP9uH0ekdIr+/te6pbrYYiUvAUthibbq0mm7
 zhpIa8saXLLyImygrPgZpfY3X8l4uWG33hMeU7OHOfReZzycfVxAzENlkomejP+W
 wvzliqz+TYWO7esh730hud0tFYzQjmRtL3UGIFI5sCJkR1NzMqHup/PW4BYM1zZu
 vXPGqyCLaoPV8WQz2Uq5DnX+wmTi2+s/42XbMGzyJVqXx8tjMBQlRHFpvjV1FfYc
 s7niQRnwz6wAZTitIgBYBPAPbGEIE2bi+Njur/z9ys3/Zp5CZOpKkF7TzW39tgvN
 ITq7oTO8DszCfVNrWARBOrWPy3NuAA9xvH1BWdZ7iaVP5UcAaHPG5rg3QGBGJ1HE
 UDYBDnr5GNlBvuv53MqwaThGRAwNyajO78JYuOFfz+DkvgJg9tMITThG3gpfek9Z
 TyHdN1/xZKQziMXNEgcx5CLJMoUCEMiAMKOB+Tng9HQzeCbOLTgugfzGrg2lRTnB
 Vy9o9SxuVBc5nCR1LbfpeDv+MVduYM6aZAFBHA0h8bc5svCMYHyyrfaigb75c/4q
 tg/Lg8GIhStw1za0bdxF8N6yPZvWztQfoQqTnTpldxLc4gkYjYE4IVKfowARAQAB
 tDdTcG90aWZ5IFB1YmxpYyBSZXBvc2l0b3J5IFNpZ25pbmcgS2V5IDx0dXhAc3Bv
 dGlmeS5jb20+iQJUBBMBCAA+FiEE+aIRl27WYvAOWTYeXjxF17MSxkMFAmF5YIAC
 GwMFCQJRQwAFCwkIBwIGFQoJCAsCBBYCAwECHgECF4AACgkQXjxF17MSxkOYbQ//
 VgFX2fJTUPAPR4oa79DJi0255lXhv6ZXDW/Yv6W4ycu1iIEXbDYNqBqhL1zwdphk
 Pg49LC0NkVWP3/n5WvbmJP7gfyl344ZPVeaz23ISFM8J9WlxuBonA/KSw7OCkf1+
 b+TxDb8An29hMAknwAQnLZGCoEroe3BPn9qmpbIBkkoRHFWCOAjdY98Arbq19s2k
 68wSeiGS+DcCvDOhnPxbf8M16cew/LDFpFAmbT7HhaFwN4VTLTa4gA3X9csGXMts
 jBqgk2NggoYu1ZF5P3Vt0HzqjaSlLgFe3c+HEZELPMES/zRtxO1VJv5cA9CjYu3c
 ldRlLdY35Y3CeEVzfqq6D8G1av1zpNDXjBk6zr9ZPeu1k5zOpxN008CshF82MZDd
 ymhbb/LMoY4OR1UwFPA8DwJGUE2Nb0PBrAKxpSQFuxM/iQsw1r362ZM6O3Kwyu3Y
 pCEKlbuYKKBnsBRwLY1KjhXh9ngqjxSoudwZSUtpRXp7O9SoFvUgdYsCRJuSrq/2
 qYkYgkXb9XaX1nh52tYPt50mNlceybVaKb5lDoBE6clWlBKasPAyLvjxV5RrBAKf
 adxHn0judK6HunANmZbMV4fkO7MhtyletK88dWKKgtLkVTSnoXz0xYe04LPUHDo+
 VhHeq7s/LpSTlMRs/WeB/Arue2+XuXfVEVdtDi7Mg/Q=
 =GrS9
 -----END PGP PUBLIC KEY BLOCK-----

```
