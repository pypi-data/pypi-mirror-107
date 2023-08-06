# PomodoroPy

PomodoroPy is

* a simple command-line Pomodoro timer

PomodoroPy supports to

* quickly set up a series of repeatable Pomodoros
* log the historical Pomodoros including corresponding tag, task, time interval, self-rating and comment
* start session with interactive mode, customizing a Pomodoro each round
* automatically restart another Pomodoro until self-rating answered, where time interval is accumulatively counted



## Quickstart

```bash
$ pomodoro -h
```



### Requirements

#### Desktop Notification

* Install [`terminal-notifier`](https://github.com/julienXX/terminal-notifier) for macOS, e.g.,

  ```bash
  $ brew install terminal-notifier
  ```

#### Voice Notification

* Choose voice notification sound with macOS built-in `say`

  ```bash
  $ say -v ?
  ```



### Install PomodoroPy

`pip` can handle all other package dependencies.

```bash
$ pip install pomodoropy
```
