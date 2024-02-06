# architectural style:

ADT-Architecture
- Information Hiding


# design pattern

- Data structure pattern
-- Singleton: 1 class only has 1 instance (for each window only 1 object, not opening multiple same ones at the same time)
--- using `def __new__()` to do sth before creating instance: like checking if there is already a instance there

- not using "stragegy pattern"

- facade pattern
-- use a simple interface/ as an entry point ([de] Schnittstelle 接口) to some subsystems
--- here: 
----    interface: open_component_window()
        subsystems: component classes (mlToolBox,PomodoroTimer...)


- factory method: wait and see if needed