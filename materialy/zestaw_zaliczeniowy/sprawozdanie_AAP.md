# Sprawozdanie — Architektura Aplikacji w Pythonie

## Cel pracy
Celem zestawu było zbudowanie jednego pipeline’u analitycznego dla datasetu `stanfordnlp/imdb`, wykorzystując dekoratory, współbieżność, testowanie, SQLite, PySpark oraz walidację jakości danych.

## Lab 1 — Dekoratory
Zaimplementowano dekoratory `retry` oraz `cache_to_disk`. `retry` zwiększa odporność funkcji na losowe błędy przez ponawianie wywołań z exponential backoff. Przy prawdopodobieństwie pojedynczej awarii równym 0.5 i pięciu próbach teoretyczna szansa sukcesu wynosi `1 - 0.5^5 = 96.875%`, co powinno być zbliżone do wyniku eksperymentu na 100 wywołaniach.

## Lab 2 — Współbieżność
Porównano wykonanie sekwencyjne, `ThreadPoolExecutor` oraz `multiprocessing.Pool` dla prostego liczenia sentymentu na podstawie słownika pozytywnych i negatywnych słów. Dla zadań CPU-bound multiprocessing może być korzystny, ponieważ omija ograniczenie GIL. Przy małej liczbie danych lub bardzo lekkiej funkcji narzut tworzenia procesów może jednak sprawić, że wersja sekwencyjna będzie konkurencyjna.

## Lab 3 — Testowanie
Zaimplementowano klasę `Tokenizer` oraz testy w `pytest` z użyciem fixtures, parametryzacji i oznaczenia `xfail`. Testy sprawdzają przypadki brzegowe, między innymi pusty tekst, HTML, interpunkcję, wielkość liter oraz polskie znaki. Dodatkowo policzono rozmiar słownika dla 100 recenzji jako prostą heurystykę złożoności danych tekstowych.

## Lab 4 — Bazy danych
Porównano klasyczny schemat SQL z podejściem NoSQL-style w SQLite, gdzie cały dokument recenzji zapisano jako JSON w jednej kolumnie. JSON column daje elastyczność struktury i przypomina podejście schema-on-read. Dla tego problemu klasyczny SQL jest zwykle lepszy do agregacji i filtrowania po znanych polach, ponieważ jest prostszy, bardziej typowany i zwykle szybszy przy zapytaniach analitycznych.

## Lab 5 — PySpark
Użyto window functions do policzenia rankingu recenzji w obrębie klasy, różnicy od średniej klasowej oraz średniej kroczącej z okna 50 recenzji. Takie operacje są naturalnym przypadkiem użycia Spark SQL, ponieważ nie wymagają ręcznego grupowania danych po stronie Pythona. Window functions są szczególnie przydatne w analizie rankingów, szeregów czasowych i porównań względem grupy.

## Lab 6 — Data Quality
Zaimplementowano prosty framework walidacji danych składający się z `DataContract`, `Rule` oraz `DataValidator`. Kontrakt sprawdza kompletność danych, poprawność etykiet, minimalną i maksymalną długość recenzji, brak duplikatów oraz balans klas. Dodano też regułę ostrzegawczą `no_html_tags`, która pokazuje, że dataset zawiera pozostałości HTML, ale nie powoduje przerwania walidacji.

## Wnioski końcowe
Najważniejszy wniosek z zestawu jest taki, że architektura aplikacji analitycznej nie kończy się na samym kodzie obliczeniowym. Potrzebne są także mechanizmy odporności na błędy, cache, testy automatyczne, świadomy wybór modelu danych, skalowanie obliczeń oraz kontrola jakości danych. W praktyce dopiero połączenie tych elementów tworzy pipeline, który można utrzymywać i rozwijać.
