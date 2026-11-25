import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

try:
    from pyswip import Prolog
    PYSWIP_AVAILABLE = True
except Exception:
    PYSWIP_AVAILABLE = False


class PrologEngine:
    def __init__(self, pl_path: str):
        self.pl_path = Path(pl_path)
        if not self.pl_path.exists():
            raise FileNotFoundError(f"Файл БЗ не найден: {self.pl_path}")

        self.use_pyswip = False
        if PYSWIP_AVAILABLE:
            try:
                self.prolog = Prolog()
                normalized_path = str(self.pl_path.resolve()).replace("\\", "/")
                self.prolog.consult(normalized_path)
                self.use_pyswip = True
            except Exception as e:
                print(f"[Prolog] Ошибка подключения pyswip: {e}. Переключение на встроенный парсер.")
                self.use_pyswip = False
        else:
            print("[Prolog] Библиотека pyswip недоступна. Использование встроенного парсера.")

        if not self.use_pyswip:
            self._load_fallback_kb()

    def _load_fallback_kb(self):
        self.facts: Dict[str, List[Tuple[str, ...]]] = {}
        text = self.pl_path.read_text(encoding="utf-8")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("%") or ":-" in line:
                continue
            m = re.match(r"^([a-z_][a-z0-9_]*)\((.*?)\)\.\s*$", line)
            if m:
                pred = m.group(1)
                raw_args = m.group(2)
                args = tuple(a.strip() for a in raw_args.split(",") if a.strip())
                self.facts.setdefault(pred, []).append(args)

    def query_prolog(self, query_str: str) -> List[Dict[str, Any]]:
        if self.use_pyswip:
            try:
                return list(self.prolog.query(query_str))
            except Exception as e:
                print(f"[Prolog Query Error] {query_str}: {e}")
                return []
        else:
            return []

    def get_main_six(self) -> List[str]:
        if self.use_pyswip:
            res = self.query_prolog("main_six(P)")
            return [r["P"] for r in res]
        return ["twilight_sparkle", "rainbow_dash", "pinkie_pie", "rarity", "applejack", "fluttershy"]

    def get_traits(self, pony: str) -> List[str]:
        if self.use_pyswip:
            res = self.query_prolog(f"trait({pony}, T)")
            return [str(r["T"]) for r in res]
        fact_list = self.facts.get("trait", [])
        return [f[1] for f in fact_list if f[0] == pony]

    def get_loves(self, pony: str) -> List[str]:
        if self.use_pyswip:
            res = self.query_prolog(f"loves({pony}, A)")
            return [str(r["A"]) for r in res]
        fact_list = self.facts.get("loves", [])
        return [f[1] for f in fact_list if f[0] == pony]

    def get_type(self, pony: str) -> str:
        if self.use_pyswip:
            res = self.query_prolog(f"is_a({pony}, T)")
            return str(res[0]["T"]) if res else "unknown"
        fact_list = self.facts.get("is_a", [])
        for f in fact_list:
            if f[0] == pony:
                return f[1]
        return "unknown"

    def get_element(self, pony: str) -> str:
        if self.use_pyswip:
            res = self.query_prolog(f"bears_element({pony}, E)")
            return str(res[0]["E"]) if res else "нет"
        fact_list = self.facts.get("bears_element", [])
        for f in fact_list:
            if f[0] == pony:
                return f[1]
        return "нет"

    def check_rule(self, rule_name: str, pony: str) -> bool:
        if self.use_pyswip:
            res = self.query_prolog(f"{rule_name}({pony})")
            return len(res) > 0
        return False


TRAIT_SYNONYMS = {
    "умный": "studious",
    "ученый": "studious",
    "книжный": "studious",
    "организованный": "organized",
    "порядок": "organized",
    "спокойный": "gentle",
    "интроверт": "introverted",
    "скромный": "shy",
    "стеснительный": "shy",
    "заботливый": "caring",
    "добрый": "gentle",

    "смелый": "brave",
    "храбрый": "brave",
    "соревновательный": "competitive",
    "азартный": "competitive",
    "верный": "loyal",
    "преданный": "loyal",

    "веселый": "cheerful",
    "жизнерадостный": "cheerful",
    "спонтанный": "spontaneous",
    "общительный": "social",

    "творческий": "creative",
    "элегантный": "elegant",
    "стильный": "elegant",
    "драматичный": "dramatic",

    "трудолюбивый": "hardworking",
    "честный": "honest",
    "прямой": "honest",
    "упрямый": "stubborn",
}

LOVES_SYNONYMS = {
    "книги": "reading",
    "чтение": "reading",
    "магия": "magic_study",
    "учеба": "magic_study",

    "спорт": "sports",
    "полеты": "flying",
    "полет": "flying",

    "вечеринки": "parties",
    "праздники": "parties",
    "выпечка": "baking",
    "сладости": "baking",

    "мода": "fashion",
    "стиль": "fashion",
    "драгоценности": "gems",
    "кристаллы": "gems",

    "фермерство": "farming",
    "ферма": "farming",
    "яблоки": "farming",
    "родео": "rodeo",

    "животные": "animals",
    "звери": "animals",
    "природа": "nature",
}

PONY_NAMES_RU = {
    "twilight_sparkle": "Искорка (Twilight Sparkle)",
    "rainbow_dash": "Радуга Дэш (Rainbow Dash)",
    "pinkie_pie": "Пинки Пай (Pinkie Pie)",
    "rarity": "Рарити (Rarity)",
    "applejack": "Эпплджек (Applejack)",
    "fluttershy": "Флаттершай (Fluttershy)",
}

TYPE_RU = {
    "alicorn": "Аликорн",
    "pegasus": "Пегас",
    "unicorn": "Единорог",
    "earth_pony": "Земная пони",
}

ELEMENT_RU = {
    "magic": "Магия",
    "loyalty": "Верность",
    "laughter": "Смех",
    "generosity": "Щедрость",
    "honesty": "Честность",
    "kindness": "Доброта",
}


class PonyDSS:

    def __init__(self, pl_path: str):
        self.engine = PrologEngine(pl_path)

    def parse_input_line(self, line: str) -> Tuple[List[str], List[str]]:
        user_traits = []
        user_loves = []
        norm = line.lower()

        m_traits = re.search(r"мой характер:\s*([^;]+)", norm)
        if m_traits:
            raw_items = [x.strip() for x in m_traits.group(1).split(",")]
            for item in raw_items:
                if item in TRAIT_SYNONYMS:
                    user_traits.append(TRAIT_SYNONYMS[item])

        m_loves = re.search(r"мне нравятся:\s*(.+)", norm)
        if m_loves:
            raw_items = [x.strip() for x in m_loves.group(1).split(",")]
            for item in raw_items:
                if item in LOVES_SYNONYMS:
                    user_loves.append(LOVES_SYNONYMS[item])

        return list(set(user_traits)), list(set(user_loves))

    def conduct_short_dialogue(self, interactive: bool = True, answer: str = "") -> str:
        print("\nДиалог (уточняющий вопрос): Какой вид пони тебе ближе по духу?")
        print("  [1] Единорог (магия и интеллект)")
        print("  [2] Пегас (полеты и скорость)")
        print("  [3] Земная пони (трудолюбие и связь с землей)")
        print("  [4] Аликорн (гармония всех стихий)")
        print("  [5] Не имеет значения")

        if interactive:
            choice = input("\nТвой ответ (1-5): ").strip()
        else:
            choice = answer or "5"
            print(f"(Автовыбор диалога): {choice}")

        mapping = {
            "1": "unicorn",
            "2": "pegasus",
            "3": "earth_pony",
            "4": "alicorn",
            "5": "",
        }
        return mapping.get(choice, "")

    def solve(self, input_line: str, interactive: bool = True, dialogue_answer: str = ""):
        traits, loves = self.parse_input_line(input_line)
        preferred_type = self.conduct_short_dialogue(interactive=interactive, answer=dialogue_answer)
        main_six = self.engine.get_main_six()
        candidates = []

        for pony in main_six:
            p_traits = self.engine.get_traits(pony)
            p_loves = self.engine.get_loves(pony)
            p_type = self.engine.get_type(pony)
            p_element = self.engine.get_element(pony)

            matched_traits = set(traits).intersection(set(p_traits))
            matched_loves = set(loves).intersection(set(p_loves))

            score = len(matched_traits) * 2 + len(matched_loves)
            if preferred_type and p_type == preferred_type:
                score += 2

            active_rules = []
            for rule in ["can_use_magic", "can_fly", "studious_and_magical", "creative_pony", "outdoor_pony"]:
                if self.engine.check_rule(rule, pony):
                    active_rules.append(rule)

            candidates.append({
                "id": pony,
                "name": PONY_NAMES_RU.get(pony, pony),
                "type": TYPE_RU.get(p_type, p_type),
                "element": ELEMENT_RU.get(p_element, p_element),
                "score": score,
                "matched_traits": list(matched_traits),
                "matched_loves": list(matched_loves),
                "p_traits": p_traits,
                "p_loves": p_loves,
                "active_rules": active_rules,
            })

        candidates.sort(key=lambda x: x["score"], reverse=True)
        best = candidates[0]

        print(f"\n>>> Ты больше всего похож на: {best['name']} <<<")
        print(f"Стихия Гармонии: {best['element']} | Вид: {best['type']}")

        print("\nОбоснование вывода (Explainable AI на основе запросов к Prolog):")
        print(f"  Запрос фактов характера: ?- trait({best['id']}, T). -> {best['p_traits']}")
        print(f"  Запрос фактов интересов: ?- loves({best['id']}, A). -> {best['p_loves']}")
        print(f"  Сработавшие правила БЗ: {', '.join(best['active_rules'])}")
        print(f"  Совпавшие черты: {best['matched_traits']}")
        print(f"  Совпавшие увлечения: {best['matched_loves']}")

        print("\nРейтинг кандидатов:")
        for c in candidates:
            marker = " (выбор системы)" if c["id"] == best["id"] else ""
            print(f"  - {c['name']:<30}: {c['score']} очков{marker}")
        print()


def demo():
    kb_path = Path(__file__).parent / "knowledge_base.pl"
    dss = PonyDSS(str(kb_path))

    scenarios = [
        ("Мой характер: умный, спокойный; мне нравятся: книги, магия", "1"),
        ("Мой характер: смелый, верный; мне нравятся: спорт, полеты", "2"),
        ("Мой характер: веселый, общительный; мне нравятся: вечеринки, выпечка", "3"),
    ]

    for i, (text, diag_ans) in enumerate(scenarios, 1):
        print(f"\nТестовый пример {i}: {text}")
        dss.solve(text, interactive=False, dialogue_answer=diag_ans)


if __name__ == "__main__":
    kb_path = Path(__file__).parent / "knowledge_base.pl"
    dss = PonyDSS(str(kb_path))

    if len(sys.argv) > 1 and sys.argv[1] in ["--test", "-t", "--demo"]:
        demo()
    else:
        print("Введите строку фиксированного формата, например:")
        print("  Мой характер: умный, спокойный; мне нравятся: книги, магия")

        inp = input("\nВходная строка > ").strip()
        if inp.lower() in ["demo", "test"]:
            demo()
        else:
            if not inp:
                inp = "Мой характер: умный, спокойный; мне нравятся: книги, магия"
            dss.solve(inp, interactive=True)
