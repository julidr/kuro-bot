# Kuro Bot #

[![kuroversion](https://img.shields.io/badge/version-1.2.1-fe9952)]()
[![python](https://img.shields.io/badge/python-3.7-376fa0)](https://www.python.org/)
[![karthuria](https://img.shields.io/badge/Karthuria-API-fb5457)](https://karth.top/home)
[![status](https://img.shields.io/badge/status-online-green)]()
[![license](https://img.shields.io/badge/license-No%20license-blue)]()
[![coverage](coverage.svg)]()

**Discord Bot** - Share basic information about Shoujo☆Kageki Revue Starlight franchise.

All Information is collected from <span style="color:#fb5457;">Project Karthuria</span> API and website.

### Commands ###

This bot works either with `!` or `$` prefixes.

- **birthday**: Returns the birthday of any stage girl given a name.

```
!birthday claudine
```

- **birthday_announcements**: Allow server admins to set the channel where they want to receive birthdays notifications
  and the role of these notifications. If no rol is specified then it will use `@everyone`. <br><br>
  First value is the channel name, second value the role name.

```
!birthday_announcements general
!birthday_announcements general admins
```

- **current_events**: Returns a list with the different current ongoing events in all Re-live servers. These events are
  classified as _events_, _challenges_ and _score attack_ (bosses).

```
!current_events
```

- **events_announcements**: Allow server admins to set the channel where they want to receive events notifications and
  the role of these notifications. If no rol is specified then it will use `@everyone`. <br><br>
  First value is the channel name, second value the role name.

```
!events_announcements general
!events_announcements general admins
```

- **remove_announcements**: Allow server admins to remove an event or birthday announcements configurations to avoid
  receiving notifications from Kuro Bot on the pre-configured channels. <br>
  Please use `event`, `birthday` or both to specify the announcement to remove.
  
```
!remove_announcements event
!remove_announcements birthday
!remove_announcements event birthday
```

### Tasks ###

This bot has the following automatic tasks that will be executed in any server.

- **birthday reminders**: In the birthday of one of the stage girls will send a notification to a preconfigured channel
  and rol. <br>
  If no channel was configured then it won't send them and if no role was configured it will use `@everyone`.

- **events reminders**: If an event is about to end or start in one day will send a notification to a preconfigured
  channel and rol. <br>
  If no channel was configured then it won't send them and if no role was configured it will use `@everyone`.

## License ##

This project has no license, which means that default copyright laws apply, meaning that even if **Kuro Bot** code is
public, I retain all rights of the source code and no one may reproduce, distribute, or create derivative works from
this work.