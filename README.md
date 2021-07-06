# Kuro Bot #

[![kuroversion](https://img.shields.io/badge/version-1.0.0-fe9952)]()
[![python](https://img.shields.io/badge/python-3.7-376fa0)](https://www.python.org/)
[![karthuria](https://img.shields.io/badge/Karthuria-API-fb5457)](https://karth.top/home)
[![status](https://img.shields.io/badge/status-offline-red)](https://www.python.org/)
[![license](https://img.shields.io/badge/license-No%20license-blue)](https://www.python.org/)
[![coverage](coverage.svg)]()

**Discord Bot** - Share basic information about Shoujo☆Kageki Revue Starlight franchise.

All Information is collected from <span style="color:#fb5457;">Project Karthuria</span> API and website.

### Commands ###

This bot works either with `!` or `$` prefixes.

- **birthday**: Returns the birthday of any stage girl given a name.

```
!birthday claudine
```

- **birthday_announcements**: Allow you to set the channel where you want to receive birthdays notifications.

```
!birthday_announcements general
```
- **current_events**: Returns a list with the different current ongoing events in all Re-live servers.
These events are classified as _events_, _challenges_ and _score attack_ (bosses).

```
!current_events
```

### Tasks ###

This bot has the following automatic tasks that will be executed in any server.

- **birthday reminders**: In the birthday of one of the stage girls will send a notification to a preconfigured channel.
  if no channel was configured then it won't send them. _This task use @everyone._

## License ##

This project has no license, which means that default copyright laws apply, meaning that even if **Kuro Bot** code is
public, I retain all rights of the source code and no one may reproduce, distribute, or create derivative works from
this work.