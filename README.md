# Symulacja ruchu drogowego na I Obwodnicy Krakowa

Paweł Biłko, Karolina Filipiuk, Klaudia Kromołowska

Struktura repozytorium:

- XYZ_branch  --> branch do swobodnej pracy dla developera XYZ

- development --> branch na którym rozwiązujemy konflikty między wersjami i łączymy branche developerów

- master      --> główny branch zawierający ostatnią pełną wersję aplikacji wypuszczoną dla użytkowników

![GitFlow diagram](https://www.researchgate.net/profile/Stephan_Krusche/publication/262450959/figure/fig6/AS:668360731811856@1536361024747/Simplified-version-of-the-gitflow-branching-model-adapted-from-8.png)

# Opis rozwiązań technicznych
Silnik symulacji reprezentuje agentów symulacji za pomocą klas z modułu ns_sim.agents:  
- Vehicle - podstawowa klasa reprezentująca samochód w ruchu drogowym; zawiera informacje o:  
          --> aktualnej szybkości, self.vel, (nieujemna liczba całkowita)  
          --> szansie na zmniejszenie szybkości o 1 w danym kroku czasowym, self.behav, (ułamek między 0.00, a 1.00)  
          --> ilości zjazdów z obwodnicy, które agent ominie zanim wyjedzie najbliższym napotkanym zjazdem, self.dest, (nieujemna liczba całkowita)  
          
Silnik symulacji reprezentuje układ dróg na obwodnicy za pomocą klas z modułu ns_sim.roads:
- Road - reprezentuje odcinek drogi między dwoma skrzyżowaniami, zawiera: 
       --> listę komórek ruchu drogowego w znaczeniu komórek z modelu Nagela-Schreckenberga, każdy element listy jest obiektem klasy Vehicle albo None, self.cells, (lista obiektów None lub Vehicle)
       --> informację o ograniczeniu szybkości, self.speed_limit, (liczby całkowite, wartości ujemne oznaczają brak ograniczenia)
       --> referencje do skrzyżowania na początku i końcu tego odcinka drogi, należy je podać w konstruktorze drogi, self.start i self.end, (obiekty klasy Node)
- Node - reprezentuje skrzyżowanie, zawiera informacje o:
       --> typie skrzyżowania, self.type, (liczba całkowita, -1 oznacza zjazd z obwodnicy, 1 oznacza wjazd, a 0 funkcjonuje jako jedno i drugie)
       --> referencjach do dróg wychodzących i wchodzących na skrzyżowanie, self.output_road i self.input_road, (obiekty klasy  Road, po podaniu obiektu Node do konstruktora obiektu Road, ten automatycznie ustawi siebie jako input lub output w podanym obiekcie Node)
       --> (dla wjazdów) szansę na pojawienie się samochodu na skrzyżowaniu, self.chance_to_spawn, (ułamek od 0.00 do 1.00)
       --> (dla wjazdów) zakres ilości omijanych zjazdów, które zostaną nadane samochodom produkowanym przez ten wjazd, self.dest_range, (para liczba całkowitych nieujemnych)

Nadrzędnym elementem symulacji jest klasa Simulation, z modułu ns_sim.simulation:
- Simulation - klasa wysyła polecenia wykonania odpowiednich operacji klasą podrzędnym, w szczególności funkcji step(), obliczającej stan wszystkich obiektów po upłynięciu jednego kroku czasowego; w tym celu zawiera informacje o:
             --> referencjach do wszystkich obiektów układu dróg w symulacji, self.roads i self.nodes, (lista obiektów Road i Node)
             --> licznik pokazujący aktualną godzinę dnia w krokach czasowych, self.curr_time, (liczba całkowita nieujemna)
             --> informację o aktualnym natężeniu ruchu, self.phase, (para w postaci (int, float), pierwsza liczba oznacza o której godzinie (podanej w krokach czasowych) zaczyna się nowa faza ruchu drogowego, druga oznacza szansę w każdym kroku czasowym na pojawienie się samochodu na najmniej ruchliwym ze skrzyżowań)
- Config - zawiera stałe wartości w symulacji, takie jak długość komórki ruchu drogowego, kroku czasowego, punktów w czasie w których zmieni się natężenie ruchu (self.sim_daytime_phases), czasie symulacji (self.simulation_duration), godzinie rozpoczęcia symulacji (w krokach czasowych, self.sim_start_time); klasa ta powstała w celu spełnienia paradygmatu rozdzielenia problemów: Simulation kontroluje zmieniające się warunki symulacji, Config początkowe, niezmienne wartości, stałe

# Pomoce:

Tutorial PyGame:
https://youtu.be/VO8rTszcW4s
