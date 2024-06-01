Use Sprial Software Developing Model

Increment, since idk what more component to be developed











product backlog:

    -



sprint backlog:

Not yet started:
        write into errLog.txt if any UI layer errors occured

        connect sqlite Database (save all json file data)

        events log: eg. write this into file: 
        ```
            2024.2.23 10:17 
            [System] User starts to concentrate for 15 min long.

            2024.2.23 10:42 
            [System] User successfully concentrated for 15 min long, add 15€ into balance.

            2024.2.23 10:43
            [System] User bought {cheese burger} in the shop window, costs {5 €}, food bar +50%

            2024.2.24 0:00
            [System] Warning: low food bar, need to buy some food!
        ```



        get more test dataset for mlToolBox



        combine AI tools/chatbot

        + Data Analysis funcs inside MLtoolbox: ideas/inspirations see ChatGPT dialog before


Doing:



Done:
        inventory window + json data
        close ALL OTHER SUB- WINDOWS when main window is closed!

        install Qt Creator

        direct apply changes from settings, not after restart the software
            by using `self.load_settings()`
                NOTE: closeEvent() can be already "directly applied"

        change `update_balance()` more general: `update_data()`

        balance ($)
        shop window

Failed:
        Qt Creator cannot be used correctly, I prefer just using VScode
        build up qm translation files, know more about QTranslator, Qt Linguist