% 1.1 Проверка: является ли twilight_sparkle персонажем (pony)?
% Ожидаемый ответ: true.
?- pony(twilight_sparkle).

% 1.2 Проверка типа существа: является ли rainbow_dash пегасом?
% Ожидаемый ответ: true.
?- is_a(rainbow_dash, pegasus).

% 1.3 Поиск: какую Стихию несёт fluttershy?
% Ожидаемый ответ: Element = kindness.
?- bears_element(fluttershy, Element).

% 1.4 Поиск: где живёт applejack?
% Ожидаемый ответ: Place = sweet_apple_acres.
?- home(applejack, Place).

% 1.5 Поиск: все черты характера pinkie_pie.
% Ожидаемый ответ: T = cheerful ; T = spontaneous ; T = social.
?- trait(pinkie_pie, T).

% 2.1 Конъюнкция (И): найти всех персонажей-пегасов (is_a + pony).
% Ожидаемый ответ: rainbow_dash, fluttershy, scootaloo, derpy_hooves.
?- pony(X), is_a(X, pegasus).

% 2.2 Отрицание (НЕ \+): пони, у которых НЕТ Стихии Гармонии.
% Ожидаемый ответ: все персонажи кроме Мейн Шести.
?- pony(X), \+ bears_element(X, _).

% 2.3 Дизъюнкция (ИЛИ): пони, которые любят читать ИЛИ изучать магию.
% Ожидаемый ответ: twilight_sparkle (дважды), starlight_glimmer.
?- pony(X), (loves(X, reading) ; loves(X, magic_study)).

% 2.4 Конъюнкция: персонажи, которые одновременно смелые И верные.
% Ожидаемый ответ: rainbow_dash.
?- pony(X), trait(X, brave), trait(X, loyal).

% 3.1 Найти все пары (Pony, Element): кто несёт какую Стихию?
% Ожидаемый ответ: 6 пар для Мейн Шести.
?- bears_element(Pony, Element).

% 3.2 Найти всех жителей Понивилля (ponyville).
% Ожидаемый ответ: twilight_sparkle, rainbow_dash, pinkie_pie, rarity, fluttershy, starlight_glimmer.
?- home(Pony, ponyville).

% 3.3 Найти всех единорогов, которые любят изучать магию.
% Ожидаемый ответ: starlight_glimmer. (twilight — аликорн, не единорог)
?- is_a(Pony, unicorn), loves(Pony, magic_study).

% 3.4 Найти всех персонажей с чертой "caring".
% Ожидаемый ответ: fluttershy.
?- trait(Pony, caring).

% 4.1 Правило can_use_magic/1: кто умеет применять магию?
% Ожидаемый ответ: twilight_sparkle, rarity, princess_celestia, princess_luna, starlight_glimmer, trixie, sweetie_belle, lyra_heartstrings.
?- can_use_magic(X).

% 4.2 Правило can_fly/1: кто умеет летать?
% Ожидаемый ответ: все пегасы и аликорны.
?- can_fly(X).

% 4.3 Правило main_six/1: кто входит в Мейн Шесть?
% Ожидаемый ответ: twilight_sparkle, rainbow_dash, pinkie_pie, rarity, applejack, fluttershy.
?- main_six(X).

% 4.4 Правило outdoor_pony/1: «уличные» пони (не интроверты).
% Ожидаемый ответ: rainbow_dash, applejack, fluttershy.
?- outdoor_pony(X).

% 4.5 Правило creative_pony/1: творческие пони.
% Ожидаемый ответ: pinkie_pie (baking), rarity (fashion, creative).
?- creative_pony(X).

% 4.6 Правило studious_and_magical/1: книжные волшебники.
% Ожидаемый ответ: twilight_sparkle, starlight_glimmer.
?- studious_and_magical(X).

% 4.7 Правило similar_pony/2: на кого похожа rainbow_dash?
% Ожидаемый ответ: все персонажи с совпадающей чертой (brave, competitive, loyal).
?- similar_pony(rainbow_dash, X).

