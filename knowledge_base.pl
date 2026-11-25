% Факты с одним аргументом

% Персонажи
pony(twilight_sparkle).
pony(rainbow_dash).
pony(pinkie_pie).
pony(rarity).
pony(applejack).
pony(fluttershy).
pony(princess_celestia).
pony(princess_luna).
pony(starlight_glimmer).
pony(trixie).
pony(spike).
pony(discord).
pony(zecora).
pony(cheerilee).
pony(lyra_heartstrings).
pony(bon_bon).
pony(doctor_whooves).
pony(derpy_hooves).
pony(big_macintosh).
pony(apple_bloom).
pony(scootaloo).
pony(sweetie_belle).

% Виды существ в мире Эквестрии
creature_type(unicorn).
creature_type(pegasus).
creature_type(earth_pony).
creature_type(alicorn).
creature_type(dragon).
creature_type(draconequus).
creature_type(zebra).

% Шесть Стихий Гармонии
element(magic).
element(loyalty).
element(laughter).
element(generosity).
element(honesty).
element(kindness).


% Факты с двумя аргументами

% is_a(Pony, Type) — вид существа персонажа
is_a(twilight_sparkle, alicorn).
is_a(rainbow_dash, pegasus).
is_a(pinkie_pie, earth_pony).
is_a(rarity, unicorn).
is_a(applejack, earth_pony).
is_a(fluttershy, pegasus).
is_a(princess_celestia, alicorn).
is_a(princess_luna, alicorn).
is_a(starlight_glimmer, unicorn).
is_a(trixie, unicorn).
is_a(spike, dragon).
is_a(discord, draconequus).
is_a(zecora, zebra).
is_a(big_macintosh, earth_pony).
is_a(apple_bloom, earth_pony).
is_a(scootaloo, pegasus).
is_a(sweetie_belle, unicorn).
is_a(derpy_hooves, pegasus).
is_a(doctor_whooves, earth_pony).
is_a(cheerilee, earth_pony).
is_a(lyra_heartstrings, unicorn).
is_a(bon_bon, earth_pony).

% bears_element(Pony, Element) — носитель Стихии Гармонии
bears_element(twilight_sparkle, magic).
bears_element(rainbow_dash, loyalty).
bears_element(pinkie_pie, laughter).
bears_element(rarity, generosity).
bears_element(applejack, honesty).
bears_element(fluttershy, kindness).

% trait(Pony, Trait) — черты характера (у персонажа может быть несколько)
trait(twilight_sparkle, studious).
trait(twilight_sparkle, organized).
trait(twilight_sparkle, introverted).
trait(rainbow_dash, brave).
trait(rainbow_dash, competitive).
trait(rainbow_dash, loyal).
trait(pinkie_pie, cheerful).
trait(pinkie_pie, spontaneous).
trait(pinkie_pie, social).
trait(rarity, creative).
trait(rarity, elegant).
trait(rarity, dramatic).
trait(applejack, hardworking).
trait(applejack, honest).
trait(applejack, stubborn).
trait(fluttershy, shy).
trait(fluttershy, caring).
trait(fluttershy, gentle).
trait(starlight_glimmer, determined).
trait(starlight_glimmer, reformed).
trait(trixie, boastful).
trait(trixie, proud).
trait(discord, chaotic).
trait(discord, mischievous).

% loves(Pony, Activity) — любимое занятие персонажа
loves(twilight_sparkle, reading).
loves(twilight_sparkle, magic_study).
loves(rainbow_dash, flying).
loves(rainbow_dash, sports).
loves(pinkie_pie, parties).
loves(pinkie_pie, baking).
loves(rarity, fashion).
loves(rarity, gems).
loves(applejack, farming).
loves(applejack, rodeo).
loves(fluttershy, animals).
loves(fluttershy, nature).
loves(starlight_glimmer, magic_study).
loves(discord, chaos).

% home(Pony, Place) — место проживания
home(twilight_sparkle, ponyville).
home(rainbow_dash, ponyville).
home(pinkie_pie, ponyville).
home(rarity, ponyville).
home(applejack, sweet_apple_acres).
home(fluttershy, ponyville).
home(princess_celestia, canterlot).
home(princess_luna, canterlot).
home(starlight_glimmer, ponyville).
home(zecora, everfree_forest).


% Правила логического вывода

% can_use_magic(Pony)
% Пони умеет применять магию, если она единорог ИЛИ аликорн.
can_use_magic(Pony) :-
    pony(Pony),
    (is_a(Pony, unicorn) ; is_a(Pony, alicorn)).

% can_fly(Pony)
% Пони умеет летать, если она пегас ИЛИ аликорн.
can_fly(Pony) :-
    pony(Pony),
    (is_a(Pony, pegasus) ; is_a(Pony, alicorn)).

% main_six(Pony)
% Пони входит в Мейн Шесть, если несёт хотя бы одну Стихию Гармонии.
main_six(Pony) :-
    pony(Pony),
    bears_element(Pony, _).

% creative_pony(Pony)
% Пони творческая натура, если любит моду или выпечку ИЛИ обладает чертой creative.
creative_pony(Pony) :-
    pony(Pony),
    (loves(Pony, fashion) ; loves(Pony, baking) ; trait(Pony, creative)).

% studious_and_magical(Pony)
% Пони — книжный волшебник: умеет применять магию И любит читать или учиться.
studious_and_magical(Pony) :-
    can_use_magic(Pony),
    (loves(Pony, reading) ; loves(Pony, magic_study)).

% outdoor_pony(Pony)
% Пони уличного типа: любит природу/спорт/полёты/фермерство И не интроверт.
outdoor_pony(Pony) :-
    pony(Pony),
    (loves(Pony, farming) ; loves(Pony, sports) ; loves(Pony, flying) ; loves(Pony, nature)),
    \+ trait(Pony, introverted).

% similar_pony(Pony1, Pony2)
% Две разные пони похожи, если у них есть хотя бы одна общая черта характера.
similar_pony(Pony1, Pony2) :-
    pony(Pony1),
    pony(Pony2),
    Pony1 \= Pony2,
    trait(Pony1, Trait),
    trait(Pony2, Trait).
