**TestScript Template:**

sequence:
- testcase 1
- testcase 2....

test:

- <testcase>:

    - <scenario>:

    - <step>:

         <name>

         <action>

         <target>

         <value>

         <screenshot_name>

         <sleep>

         <wait before action>

         <wait after action>

---------------------------------------------------------

- List of actions: input | click | import | sleep | wait | validate | function | hover | goto | screenshot | closebrowser

--------------


- **Test script for action - 'goto':**


.. code-block:: rst

    test:

    - testcase 1:
        - scenario: Open GitHub website

        - step 1:
            name: Go to WTRobot project repository

            action: goto

            target: https://github.com/vishalvijayraghavan/WTRobot-v2

-------

- **Test script for action - 'click':**


.. code-block:: rst

    test:

    - testcase 2:
        - scenario: See list of contributors involved in this project

        - step 1:
            name: Click on contributors

            action: click

            target: contributors

-------------


- **Test script for action - 'input':**


.. code-block:: rst


    test:

    - testcase 3:
        - scenario: Search other projects on GitHub

        - step 1:
            name: Searching GitHub projects

            action: input

            target: /html/body/div[1]/header/div[2]/div/div/form/label/input[1]

-----------


- **Test script for action - 'import':**


.. code-block:: bash


    test:

    - testcase 4:
        - scenario: Opening GitHub website and search projects

        - step 1:
            name: Opening GitHub website

            action: import

            target: testcase 1

        - step 2:
            name: Searching GitHub projects

            action: import

            target: testcase 3

-----------------


- **Test script for action - 'sleep':**



.. code-block:: rst


    test:

    - testcase 5:
        - scenario: Search other projects on GitHub and wait for sometime

        - step 1:
            name: Searching GitHub projects

            action: input

            target: /html/body/div[1]/header/div[2]/div/div/form/label/input[1]

        - step 2:
            name: Waiting for suggestion to appear while searching new project

            action: sleep
