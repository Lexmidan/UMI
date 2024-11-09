# Ulohy

## Roboticky vysavac
Toto jsem implementoval ciste heuristicky. Zadefinoval jsem additivni potencial. Smeti generuje kolem sebe pole potencialu klesajici se vzdalenosti od smeti (vzdalenost je L1 nebo L2, zalezi zda povolime diagonalni pohyb). Roboticky vysavac pak hne smerem rostouciho potencialu, jakmile dosahne smeti, potencial generovany dosazenym smetim se odecte od celkoveho potencialu. Dale se pokracuje stejnym zpusobem, dokud vsechna smeti nebudou odstranena.

- reseni s vizualizaci je v jupyter notebooku `roomba.ipynb`

## NQueens
Implementoval jsem backtracking s filtraci (`nqueens.py`). Hranovou konzistenci jsem bohuzel po tydnu kodovani samostatne nezvladl, natoz zobecnenou hranovou konzistenci :C
Proto sahl jsem po cizim kodu s AC3, a pouzil ho ve sve funkci pro backtracking (`nqueens.ipynb`).
Co se tyce symetrie, zadefinoval jsem funkce pro symetricke usporadani, ale nevymyslel jsem jak je pouzit ve svem reseni. Jelikoz ve svem algoritmu prirazuji hodnoty striktne pocinaje prvnim radkem, nemuzu pouzit sve symmetricke zobrazeni na castecne prirazeni hodnot. Tedy i kdyz vim, ze prirazeni [1, 3, 5, 7, 0, ...] je nogood otocit ten nogood nedokazu.

## Hamiltonovska kruznice
Tady jsem implementoval obycejny BT. Pro testovani jsem pouzival knihovnu `networkx` kde testoval svuj kod na na nahodnem Erdosovem grafu. 