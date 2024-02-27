# AI_spele
### Papildu prasības programmatūrai
Spēles sākumā spēles programmatūra gadījuma ceļā saģenerē 5 skaitļus diapazonā no 10000 līdz
20000, bet tādus, kas sākotnēji dalās gan ar 3, gan ar 2. Cilvēks-spēlētājs izvēlas, ar kuru no
saģenerētajiem skaitļiem viņš vēlas sākt spēli.

### Spēles apraksts
Spēles sākumā ir dots cilvēka-spēlētāja izvēlētais skaitlis. Abiem spēlētājiem ir 0 punktu. Turklāt
spēlē tiek izmantota spēles banka, kura sākotnēji ir vienāda ar 0. Spēlētāji izdara gājienus pēc kārtas,
katrā gājienā dalot pašreizējā brīdī esošu skaitli ar 2 vai 3. Skaitli ir iespējams sadalīt tikai tajā
gadījumā, ja rezultātā veidojas vesels skaitlis. Ja tiek veikta dalīšana ar 2, tad pretinieka punktu
skaitam tiek pieskaitīti 2 punkti. Ja tiek veikta dalīšana ar 3, tad paša spēlētāja punktu skaitam tiek
pieskaitīti 3 punkti. Savukārt, ja tiek iegūts skaitlis, kas beidzas ar 0 vai 5, tad bankai tiek pieskaitīts 1
punkts. Spēle beidzas, kā tikko ir iegūts skaitlis, kas ir mazāks vai vienāds ar 10. Spēlētājs, pēc kura
gājiena spēle beidzas, iztukšo banku, saviem punktiem pieskaitot bankas punktus. Ja spēlētāju
punktu skaits ir vienāds, tad rezultāts ir neizšķirts. Pretējā gadījumā uzvar spēlētājs, kam ir vairāk
punktu.
