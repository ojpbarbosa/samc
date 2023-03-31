<samp>
  <h2>Summary</h2>
  <p>

  </p>
  <h2>Run</h2>

  ```bash
  # clone the repository
  $ git clone https://github.com/ojpbarbosa/samc.git

  # cd into the repository
  $ cd samc

  # create the virtual environment
  $ python -m venv venv

  # activate the virtual environment
  $ source ./venv/bin/activate
  # or
  $ ./venv/Scripts/activate.bat

  # install the required libraries
  $ pip install -r requirements.txt

  # run
  $ python ./level-i/question-ii/question-ii.py # headlessly outputs the movement sequence
  # or
  $ python ./level-i/question-ii/visualization # visually outputs the movement sequence
  ```

  <h2>References</h2>
  <ul>
    <li><a href="https://sigmageek.com/challenge/stone-automata-maze-challenge">Stone Maze Automata Challenge</a></li>
    <li><a href="https://www.python.org/">Python</a></li>
    <ul>
      <li><a href="https://www.pygame.org/">pygame</a></li>
      <li><a href="https://numpy.org/">NumPy</a></li>
      <li><a href="https://pypi.org/project/darkdetect/">Darkdetect</a></li>
    </ul>
  </ul>

  <h2>Todo</h2>
  - [ ] Improve visualization and interactivity
  - [ ] Improve "game" or validation
  - [ ] Use movement sequence as input
  - [ ] Remove garbage
  - [ ] Improve overall
</samp>
