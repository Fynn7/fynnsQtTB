# architectural style:

ADT-Architecture
- Information Hiding


# design pattern
increment ([de] Inkrementät): add and grow more functionalities, since don't have a clear target how this software should look like or what kind of functions should it have

- Data structure pattern
-- Singleton: 1 class only has 1 instance (for each window only 1 object, not opening multiple same ones at the same time)
--- using `def __new__()` to do sth before creating instance: like checking if there is already a instance there

- not using "strategy pattern"

- facade pattern
-- use a simple interface/ as an entry point ([de] Schnittstelle 接口) to some subsystems
--- here: 
----    interface: open_component_window()
        subsystems: component classes (mlToolBox,PomodoroTimer...)


- factory method: wait and see if needed