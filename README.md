# f1_crawler
Crawls for F1 stats


# How to use this repo 

```
usage: main.py [-h] [-d DRIVERS [DRIVERS ...]] [-n] [-g GP_NAME [GP_NAME ...]] [-l]

optional arguments:
  -h, --help            show this help message and exit
  -d DRIVERS [DRIVERS ...], --drivers DRIVERS [DRIVERS ...]
                        Plot normalized times
  -n, --normalized      Plot normalized times
  -g GP_NAME [GP_NAME ...], --gp_name GP_NAME [GP_NAME ...]
                        GP to plot data for
  -l, --list            List all gps and drivers
```


## List Grand Prix and Drivers

```
python main.py -l 
```


## Plot lap times for specific Grand Prix

You can plot all Lap times, divided into plots per driver for a specific Grand Prix.
The command for this would be:

```
python main.py -g GRAND_PRIX
```

## Plot normalized lap times

The mean lap time is computed by taking the average of all drivers lap time.

```
python main.py -n -g GRAND_PRIX
```

## Plot normalized lap times accross season for a specific driver

```
python main.py -d DRIVER_NAME 
```
