#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#<https://en.wikipedia.org/wiki/Pomodoro_Technique>

import argparse
import sys
import time
import subprocess


def parse_args():
    parser = argparse.ArgumentParser(
        prog='🍅',
        description='🍅 pomodoro timer'
    )
    parser.add_argument(
        '-w',
        '--work',
        default=25,
        type=int,
        help='time interval (in minutes) for work, default: 25 minutes'
    )
    parser.add_argument(
        '-r',
        '--rest',
        default=5,
        type=int,
        help='time interval (in minutes) for rest, default: 5 minutes'
    )
    parser.add_argument(
        '-v',
        '--voice',
        default='Alex',
        type=str,
        help='voice notification sound, default: Alex'
    )
    args = parser.parse_args()
    return args


def main(args):
    try:
        while True:
            # step 1. pick a task
            task = input("💡 what's your task for the pomodoro?\n  ")
            # step 2. set a timer for work, focus on work until time is up
            print('🍅 please focus on work for {} minutes, press Ctrl+C to abort'.format(args.work))
            timer('🍅', args.work, args.voice, "it's time to have a rest")
            # step 3. set a timer for rest, have a rest until time is up
            print('🥝 please have a rest for {} minutes, press Ctrl+C to abort'.format(args.rest))
            timer('🥝', args.rest, args.voice, "it's time to focus on work")
            # step 4. rate your focus
            rating = input('🎉 how was your focus (1-10)?\n  ')
            # step 5. log the pomodoro
            save(task, args.work, rating)
            # step 6. press Enter to repeat step 1-5
            input('🙈🙉🙊 press Enter to continue\n')
    except KeyboardInterrupt:
        print('\n💪 well done!')


def timer(prog, interval, voice, message):
    since = time.time()
    while True:
        secs_elapsed = time.time() - since
        secs_left = interval * 60 - secs_elapsed
        if secs_left <= 0:
            print('')
            break
        progressbar(prog, secs_elapsed, interval * 60, plus=countdown(secs_left))
        time.sleep(1)
    notify(prog, voice, message)


def countdown(secs_left):
    mins, secs = divmod(round(secs_left), 60)
    return '{:02d}:{:02d} ⏰'.format(mins, secs)


def progressbar(prog, secs_elapsed, secs, plus=''):
    if prog == '🍅':
        length = 25
    elif prog == '🥝':
        length = 5
    frac = secs_elapsed / secs
    loaded = round(frac * length)
    print('\r ', prog * loaded + '--' * (length - loaded), '[{:.0%}]'.format(frac), plus, end='')


def notify(prog, voice, message):
    try:
        # macOS voice notification
        if sys.platform == 'darwin':
            subprocess.run(['terminal-notifier', '-title', prog, '-message', message])
            subprocess.run(['say', '-v', voice, message])
        else:
            # TODO
            pass
    except:
        # TODO
        pass


def save(task, interval, rating, file='./pomodoro.log'):
    timestamp = time.strftime('%a %d %b %Y %H:%M:%S', time.localtime())
    entries = []
    print('😀 {} | ✅ task: {} | 🍅 pomodoro: {} minutes | 👉 self-rating: {}'.format(
        timestamp, task, str(interval), '⭐' * int(rating))
    )
    entries += [timestamp, task, str(interval), rating]
    with open(file, 'a') as f:
        f.write(' | '.join(entries))
        f.write('\n')


if __name__ == '__main__':
    args = parse_args()
    main(args)
